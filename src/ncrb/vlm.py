"""Read scanned table pages with an OCR vision-language model (MLX, Apple Silicon).

Classical OCR (Tesseract) recognises characters and leaves the table structure
to be rebuilt from word positions, which is where most errors on the old
scans come from. Document VLMs read the page image and write the table out
directly as HTML, structure included. This module runs such a model locally
through ``mlx-vlm`` and turns its output into the same grids the Excel reader
consumes, so the rest of the pipeline (title, header levels, row labels,
totals check) is shared.

Install the extra first: ``uv sync --extra vlm``.
"""

from __future__ import annotations

import html as htmllib
import re
from dataclasses import dataclass
from functools import lru_cache
from html.parser import HTMLParser

import pymupdf as fitz

# model id -> (prompt, max tokens). Prompts follow each model card.
MODELS = {
    "mlx-community/GLM-OCR-bf16": ("Table Recognition:", 8192),
    "mlx-community/PaddleOCR-VL-1.5-bf16": ("Table Recognition:", 8192),
    "mlx-community/dots.ocr-8bit": (
        "Extract the table on this page as HTML. Reproduce every row and every column exactly as printed, "
        "including the column numbers row, using rowspan and colspan for merged header cells.",
        8192,
    ),
    "mlx-community/DeepSeek-OCR-2-8bit": ("<|grounding|>Convert the document to markdown.", 8192),
    "mlx-community/Qwen3-VL-8B-Instruct-4bit": (
        "This is a scanned page of a statistical table from an Indian government report. Transcribe the "
        "table title and the complete table as HTML. Copy every number exactly as printed, digit by digit, "
        "keeping commas and decimal points. Use rowspan/colspan for merged header cells. Write a dash for "
        "cells printed as a dash. Output only the title line and the HTML table.",
        8192,
    ),
}
DEFAULT_MODEL = "mlx-community/GLM-OCR-bf16"

# Models run on a cloud GPU with vLLM (colab/ocr_pages.py); their output lands in the same page cache.
# Same prompts as the model cards; the table comes back as OTSL or HTML, both parsed below.
MODELS |= {
    "XingChen-AGI/TeleOCR": ("output the table in OTSL format.", 8192),
    "PaddlePaddle/PaddleOCR-VL-1.6": ("Table Recognition:", 8192),
    "zai-org/GLM-OCR": ("Table Recognition:", 8192),
}
# every model whose cached reading of a file is weighed against the others by the totals check
VLM_MODELS = [DEFAULT_MODEL, "XingChen-AGI/TeleOCR", "PaddlePaddle/PaddleOCR-VL-1.6", "zai-org/GLM-OCR"]


@lru_cache(maxsize=2)
def _load(model_id: str):
    from mlx_vlm import load
    from mlx_vlm.utils import load_config

    model, processor = load(model_id)
    return model, processor, load_config(model_id)


def page_image(page: fitz.Page, long_edge: int = 1600):
    """The page as an RGB PIL image with its long edge at ``long_edge`` pixels."""
    from PIL import Image

    zoom = long_edge / max(page.rect.width, page.rect.height)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def read_image(image, model_id: str = DEFAULT_MODEL, prompt: str | None = None) -> str:
    """Raw text the model writes for one page image."""
    from mlx_vlm import generate
    from mlx_vlm.prompt_utils import apply_chat_template

    model, processor, config = _load(model_id)
    default_prompt, max_tokens = MODELS.get(model_id, ("Table Recognition:", 8192))
    text = apply_chat_template(processor, config, prompt or default_prompt, num_images=1)
    out = generate(model, processor, text, [image], max_tokens=max_tokens, temperature=0.0, verbose=False)
    return out.text if hasattr(out, "text") else str(out)


# --------------------------------------------------------------------------- parsing


@dataclass
class Grid:
    rows: list[list[str]]
    merged: list[tuple[int, int, int, int]]  # r0, r1, c0, c1, half-open, as xlstable expects


class _TableParser(HTMLParser):
    """HTML tables to grids, expanding rowspan/colspan into merged ranges."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables: list[Grid] = []
        self._cells: list[list[tuple[str, int, int]]] | None = None
        self._row: list | None = None
        self._cell: list[str] | None = None
        self._span = (1, 1)
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self._depth += 1
            if self._depth == 1:
                self._cells = []
        elif self._cells is None:
            return
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._cell = []
            self._span = (_int(a.get("rowspan")), _int(a.get("colspan")))
        elif tag == "br" and self._cell is not None:
            self._cell.append(" ")

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None and self._row is not None:
            text = re.sub(r"\s+", " ", "".join(self._cell)).strip()
            self._row.append((text, *self._span))
            self._cell = None
        elif tag == "tr" and self._row is not None and self._cells is not None:
            self._cells.append(self._row)
            self._row = None
        elif tag == "table":
            self._depth -= 1
            if self._depth == 0 and self._cells is not None:
                self.tables.append(_expand(self._cells))
                self._cells = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _int(v) -> int:
    try:
        return max(1, int(v))
    except (TypeError, ValueError):
        return 1


def _expand(rows: list[list[tuple[str, int, int]]]) -> Grid:
    occupied: dict[tuple[int, int], str] = {}
    merged = []
    for r, row in enumerate(rows):
        c = 0
        for text, rs, cs in row:
            while (r, c) in occupied:
                c += 1
            for i in range(r, r + rs):
                for j in range(c, c + cs):
                    occupied[(i, j)] = text if (i, j) == (r, c) else ""
            if rs > 1 or cs > 1:
                merged.append((r, r + rs, c, c + cs))
            c += cs
    if not occupied:
        return Grid([], [])
    h = max(i for i, _ in occupied) + 1
    w = max(j for _, j in occupied) + 1
    grid = [[occupied.get((i, j), "") for j in range(w)] for i in range(h)]
    return Grid(grid, merged)


def _markdown_tables(text: str) -> list[Grid]:
    out, block = [], []
    for line in text.splitlines() + [""]:
        if line.strip().startswith("|"):
            block.append(line)
            continue
        if len(block) >= 2:
            rows = []
            for b in block:
                cells = [c.strip() for c in b.strip().strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    continue  # the |---|---| separator
                rows.append(cells)
            w = max(len(r) for r in rows)
            out.append(Grid([r + [""] * (w - len(r)) for r in rows], []))
        block = []
    return out


OTSL = re.compile(r"<(fcel|ecel|lcel|ucel|xcel|nl|ched|rhed|srow)>")
OTSL_SPAN = re.compile(r"<otsl>.*?(</otsl>|$)|<(?:fcel|ecel|ched|rhed|srow)>.*(?:<nl>|</otsl>)", re.S)


def _otsl_tables(text: str) -> list[Grid]:
    """OTSL (the token table format some document models emit) to grids.

    Header tokens (<ched> column header, <rhed> row header, <srow> section row), which TeleOCR and
    Docling-style models write, are filled cells like <fcel>."""
    if not re.search(r"<(fcel|ecel|ched)>", text):
        return []
    text = re.sub(r"</?otsl>|<loc_\d+>", "", text)
    rows: list[list[str]] = [[]]
    merged = []
    pos = 0
    tokens = list(OTSL.finditer(text))
    for k, m in enumerate(tokens):
        kind = m.group(1)
        content = text[m.end() : tokens[k + 1].start()] if k + 1 < len(tokens) else ""
        if kind == "nl":
            rows.append([])
            continue
        rows[-1].append(content.strip() if kind in ("fcel", "ched", "rhed", "srow") else "")
        if kind in ("lcel", "xcel"):
            merged.append((len(rows) - 1, len(rows), len(rows[-1]) - 2, len(rows[-1])))
        elif kind == "ucel" and len(rows) > 1:
            j = len(rows[-1]) - 1
            merged.append((len(rows) - 2, len(rows), j, j + 1))
    rows = [r for r in rows if r]
    if not rows:
        return []
    w = max(len(r) for r in rows)
    return [Grid([r + [""] * (w - len(r)) for r in rows], merged)]


NUMTOK = re.compile(r"^[-–—]?[\d,]+(\.\d+)?$|^[-–—]+$")


def _text_table(text: str) -> list[Grid]:
    """The model sometimes writes a table as plain lines; rebuild rows of label + figures.

    Only lines with the full number of figures are kept, aligned by position:
    with a cell missing there is no way to tell which one, so the row is
    dropped rather than shifted.
    """
    lines = [ln.split() for ln in text.splitlines() if ln.strip()]
    anchor = next((ln for ln in lines if len(ln) >= 3 and all(re.fullmatch(r"\(\d{1,3}\)", t) for t in ln)), None)
    if anchor is None:
        return []
    n_label = 2 if anchor[:2] == ["(1)", "(2)"] else 1
    n_fig = len(anchor) - n_label
    rows = [anchor]
    for ln in lines:
        if ln is anchor:
            continue
        k = len(ln)
        while k > 0 and NUMTOK.match(ln[k - 1]):
            k -= 1
        figs = ln[k:]
        label = ln[:k]
        if not figs and label and len(" ".join(label)) < 40:
            rows.append([" ".join(label)] + [""] * (len(anchor) - 1))  # section heading
        elif len(figs) == n_fig:
            serial = label[0] if label and re.fullmatch(r"\d{1,3}\.?", label[0]) else ""
            name = " ".join(label[1:] if serial else label)
            rows.append(([serial, name] if n_label == 2 else [f"{serial} {name}".strip()]) + figs)
    return [Grid(rows, [])] if len(rows) > 3 else []


def parse_output(text: str) -> tuple[list[str], list[Grid]]:
    """Text lines outside tables (titles, notes) and the tables, from a model's output."""
    text = re.sub(r"<\|(ref|det)\|>.*?<\|/\1\|>", "", text, flags=re.S)  # DeepSeek grounding boxes
    text = re.sub(r"```(?:html|markdown)?", "", text)
    p = _TableParser()
    p.feed(text)
    grids = [g for g in p.tables if g.rows]
    if not grids:
        grids = _otsl_tables(text) or _markdown_tables(text) or _text_table(text)
    outside = re.sub(r"<table.*?</table>", "\n", text, flags=re.S | re.I)
    outside = OTSL_SPAN.sub("\n", outside)
    outside = re.sub(r"<[^>]+>", " ", outside)
    lines = [htmllib.unescape(re.sub(r"\s+", " ", ln)).strip() for ln in outside.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("|")]
    return lines, grids
