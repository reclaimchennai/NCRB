"""OCR for scanned pages using Apple's Vision framework (macOS only).

Older NCRB volumes (roughly pre-2000) were scanned as images with no text
layer. Vision's text recogniser is run on a rendering of the page and its
output is converted to the same ``Word`` objects the text-layer path produces,
in PDF point coordinates, so the table logic in ``pdftable`` is shared.

Every OCR word carries Vision's confidence; nothing read this way should be
treated as exact without checking it against the source scan.
"""

from __future__ import annotations

import re

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


def ocr_page_words(page: fitz.Page) -> tuple[list[Word], float]:
    """Words of a scanned page in PDF points, and the mean recognition confidence."""
    if not AVAILABLE:
        raise RuntimeError("Apple Vision is not available; OCR needs macOS with pyobjc-framework-Vision")
    w, h = page.rect.width, page.rect.height
    zoom = TARGET_PX / max(w, h)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), colorspace=fitz.csGRAY, alpha=False)
    raw = _recognise(pix.tobytes("png"))
    words = []
    for text, conf, x0, y0, x1, y1 in raw:
        wd = Word(x0 * w, y0 * h, x1 * w, y1 * h, text)
        wd.size = (y1 - y0) * h
        wd.conf = conf
        words.append(wd)
    mean = sum(c for _, c, *_ in raw) / len(raw) if raw else 0.0
    return words, mean
