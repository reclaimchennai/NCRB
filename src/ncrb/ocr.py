"""OCR for scanned pages (Tesseract, with Apple Vision as a fallback).

Older NCRB volumes (roughly pre-2000) were scanned as images with no text
layer. The page is rendered and recognised, and the output is converted to the
same ``Word`` objects the text-layer path produces, in PDF point coordinates,
so the table logic in ``pdftable`` is shared.

Every OCR word carries the engine's confidence; nothing read this way should
be treated as exact without checking it against the source scan.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile

import numpy as np
import pymupdf as fitz

from .pdftable import Word

try:  # pyobjc is only available on macOS
    import Quartz
    import Vision
    from Foundation import NSData

    AVAILABLE = True
except Exception:  # pragma: no cover
    AVAILABLE = False

TARGET_PX = 3000  # long edge of the rendered page handed to Vision
VISION_FAILURES = 0  # pages on which Vision could not be run and Tesseract was used alone


def _recognise(png: bytes) -> list[tuple[str, float, float, float, float, float]]:
    """(text, confidence, x0, y0, x1, y1) per word, in unit coordinates with origin top-left."""
    data = NSData.dataWithBytes_length_(png, len(png))
    src = Quartz.CGImageSourceCreateWithData(data, None)
    image = Quartz.CGImageSourceCreateImageAtIndex(src, 0, None)
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    req.setUsesLanguageCorrection_(False)  # language models "correct" numbers and codes into words
    req.setRecognitionLanguages_(["en-US"])
    req.setMinimumTextHeight_(0.0)
    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(image, None)
    ok, err = handler.performRequests_error_([req], None)
    if not ok:
        raise RuntimeError(f"Vision OCR failed: {err}")
    out = []
    for obs in req.results() or []:
        cand = obs.topCandidates_(1)
        if not cand:
            continue
        cand = cand[0]
        text = str(cand.string())
        conf = float(cand.confidence())
        for m in re.finditer(r"\S+", text):
            box, _ = cand.boundingBoxForRange_error_((m.start(), m.end() - m.start()), None)
            if box is None:
                continue
            bb = box.boundingBox()
            x0, y0 = bb.origin.x, 1 - (bb.origin.y + bb.size.height)
            out.append((m.group(), conf, x0, y0, x0 + bb.size.width, y0 + bb.size.height))
    return out


def _tesseract(png: bytes, psm: int = 6) -> list[tuple[str, float, float, float, float, float, tuple]]:
    """(text, confidence 0..1, x0, y0, x1, y1 in pixels, line key) per word, via the tesseract CLI."""
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        f.write(png)
        f.flush()
        res = subprocess.run(
            ["tesseract", f.name, "stdout", "--psm", str(psm), "-l", "eng", "-c", "preserve_interword_spaces=1", "tsv"],
            capture_output=True, text=True, timeout=300,
        )
    if res.returncode != 0:
        raise RuntimeError(f"tesseract failed: {res.stderr[:200]}")
    out = []
    for line in res.stdout.splitlines()[1:]:
        f = line.split("\t")
        if len(f) < 12 or f[0] != "5" or not f[11].strip():
            continue
        x, y, w, h, conf = int(f[6]), int(f[7]), int(f[8]), int(f[9]), float(f[10])
        out.append((f[11].strip(), max(conf, 0) / 100, x, y, x + w, y + h, (f[2], f[3], f[4])))
    return out


def remove_rules(pix: fitz.Pixmap, min_len_frac: float = 0.04) -> bytes:
    """PNG of the page with long straight rules whitened.

    Table grids are the main cause of digits being dropped or misread: a figure
    touching a cell border is segmented together with the line. Runs of dark
    pixels much longer than any character are lines, so they are erased.
    """
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).copy()
    dark = img < 200  # scanned rules are often grey and broken
    for axis in (1, 0):
        n = dark.shape[axis]
        # horizontal runs must be longer and denser than vertical ones: a line of bold text is
        # itself a fairly dense horizontal band, but nothing in text makes a tall vertical run
        k = max(40, int((1.5 if axis == 1 else 1.0) * min_len_frac * n))
        need = 0.88 if axis == 1 else 0.8
        c = np.cumsum(dark, axis=axis, dtype=np.int32)
        pad = [(0, 0), (0, 0)]
        pad[axis] = (1, 0)
        c = np.pad(c, pad)
        # window sums of length k: positions where a full run of k dark pixels starts
        if axis == 1:
            full = (c[:, k:] - c[:, :-k]) >= need * k
            starts = np.zeros_like(dark)
            starts[:, : full.shape[1]] = full
            d = np.cumsum(starts, axis=1, dtype=np.int32)
            d = np.pad(d, ((0, 0), (k, 0)))
            line = (d[:, k:] - d[:, :-k]) > 0  # dilate the run starts back to full runs
        else:
            full = (c[k:, :] - c[:-k, :]) >= need * k
            starts = np.zeros_like(dark)
            starts[: full.shape[0], :] = full
            d = np.cumsum(starts, axis=0, dtype=np.int32)
            d = np.pad(d, ((k, 0), (0, 0)))
            line = (d[k:, :] - d[:-k, :]) > 0
        # thicken by a pixel each side so the anti-aliased edge of the rule goes too
        grow = line.copy()
        if axis == 1:
            grow[1:, :] |= line[:-1, :]
            grow[:-1, :] |= line[1:, :]
        else:
            grow[:, 1:] |= line[:, :-1]
            grow[:, :-1] |= line[:, 1:]
        img[grow] = 255
    out = fitz.Pixmap(fitz.csGRAY, pix.width, pix.height, img.tobytes(), False)
    return out.tobytes("png")


def _skew(words: list[tuple]) -> float:
    """Slope (dy/dx) of the text lines, from tesseract's own line grouping."""
    lines: dict[tuple, list[tuple]] = {}
    for w in words:
        lines.setdefault(w[6], []).append(w)
    if not words:
        return 0.0
    width = max(w[4] for w in words) - min(w[2] for w in words)
    slopes = []
    for ws in lines.values():
        ws = [w for w in ws if re.search(r"[A-Za-z0-9]", w[0]) and w[5] - w[3] > 0]
        if len(ws) < 4:
            continue
        xs = [(w[2] + w[4]) / 2 for w in ws]
        ys = [w[5] for w in ws]  # bottoms sit on the baseline
        if max(xs) - min(xs) < 0.4 * width:
            continue
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        den = sum((x - mx) ** 2 for x in xs)
        if den:
            slopes.append(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den)
    if len(slopes) < 3:
        return 0.0
    slopes.sort()
    return slopes[len(slopes) // 2]


def _overlap(a, b) -> float:
    """Share of box a (x0, y0, x1, y1) covered by box b."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    area = (a[2] - a[0]) * (a[3] - a[1])
    return (w * h) / area if w > 0 and h > 0 and area > 0 else 0.0


def ocr_page_words(page: fitz.Page, engine: str | None = None) -> tuple[list[Word], float]:
    """Words of a scanned page in PDF points (deskewed), and the mean recognition confidence.

    Tesseract is the base engine: on these dense number tables it finds isolated
    digits and dashes that Vision's detector skips. Where both are available
    (``engine="both"``, the default on macOS) Vision fills in what tesseract
    read with low confidence or missed, notably the row of column numbers.
    """
    has_t = bool(shutil.which("tesseract"))
    engine = engine or ("both" if has_t and AVAILABLE else "tesseract" if has_t else "vision")
    if engine == "vision" and not AVAILABLE or engine != "vision" and not has_t:
        raise RuntimeError("no OCR engine: install tesseract, or use macOS with pyobjc-framework-Vision")
    w, h = page.rect.width, page.rect.height
    boxes: list[tuple[str, float, float, float, float, float]] = []  # unit coordinates
    slope = 0.0
    if engine in ("tesseract", "both"):
        zoom = min(300 / 72, 5000 / max(w, h))
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), colorspace=fitz.csGRAY, alpha=False)
        raw = _tesseract(remove_rules(pix))
        slope = _skew(raw) * pix.width / pix.height  # to unit coordinates
        boxes = [(t, c, x0 / pix.width, y0 / pix.height, x1 / pix.width, y1 / pix.height) for t, c, x0, y0, x1, y1, _ in raw]
    if engine in ("vision", "both"):
        zoom = TARGET_PX / max(w, h)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), colorspace=fitz.csGRAY, alpha=False)
        try:
            vis = _recognise(pix.tobytes("png"))
        except RuntimeError:
            if engine == "vision":
                raise
            vis = []  # Vision is only a supplement here; it is unavailable e.g. while the screen is locked
            global VISION_FAILURES
            VISION_FAILURES += 1
        if engine == "vision":
            boxes = vis
        else:
            keep = list(boxes)
            for v in vis:
                hits = [b for b in keep if _overlap(v[2:], b[2:]) > 0.3 or _overlap(b[2:], v[2:]) > 0.3]
                if not hits:
                    boxes.append(v)  # tesseract saw nothing here
                elif all(b[1] < 0.5 for b in hits) and len(hits) == 1 and re.fullmatch(r"[\d,.()\-]+", v[0]):
                    boxes.remove(hits[0])  # a doubtful tesseract token that Vision reads as a clean number
                    keep.remove(hits[0])
                    boxes.append(v)
    words = []
    heights = sorted((b[5] - b[3]) * h for b in boxes if re.search(r"[A-Za-z0-9]{2}", b[0]))
    # one nominal font size for the page: box heights of dashes and dots say nothing about the line they sit on
    size = 1.6 * heights[len(heights) // 2] if heights else 8.0
    for text, conf, x0, y0, x1, y1 in boxes:
        dy = slope * (((x0 + x1) / 2) - 0.5)
        wd = Word(x0 * w, (y0 - dy) * h, x1 * w, (y1 - dy) * h, text)
        wd.size = size
        wd.conf = conf
        words.append(wd)
    mean = sum(b[1] for b in boxes) / len(boxes) if boxes else 0.0
    return words, mean
