"""ocrkit: read scanned documents with current OCR models on a cloud GPU, fast and unattended.

    manifest  which pages to read (local PDFs or public URLs, scanned pages only by default)
    job       on the GPU: an optional bake-off between models, then every page, supervised,
              resumable, results written page by page to Google Drive
    fetch     bring the readings back (a Drive folder download, any zip, any folder)
    score     how far a reading's tables add up (row and column totals) and agree with others

The page cache layout is <out>/<model slug>/<file id>/<page:04d>.txt: one raw model output per page.
"""

__version__ = "0.1.0"
