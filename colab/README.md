# Cloud OCR for the scanned years

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/reclaimchennai/NCRB/blob/main/colab/NCRB_OCR.ipynb)

Almost every NCRB table before 2000 is a scanned page: 12,945 pages across
Crime in India (1953–1999), ADSI (1967–2000) and Prison Statistics (1995–2000).
Tesseract reads them with errors (misread digits, garbled headings), so many
of those tables fail NCRB's own row and column totals and are left out of the
Explore page and the long series. Running a document-OCR model on a laptop
takes about a minute a page (over a week for all of them). A cloud GPU running
the model with vLLM does them in hours.

## What runs

| Step | What | Where |
|---|---|---|
| Pages | `scripts/build_ocr_bundle.py` packs only the scanned pages (one PDF per source file) with `manifest.json` (source file SHA-256 and page numbers) | release [`ocr-pages`](https://github.com/reclaimchennai/NCRB/releases/tag/ocr-pages), 4.1 GB in 3 tars |
| Bake-off | `colab/ocr_pages.py --bench` runs each candidate model on 48 files whose totals can be checked; `colab/score.py` ranks them by the share of NCRB's printed totals their tables reproduce | Colab |
| Full run | the winner reads every page; output goes to your Google Drive, resumable | Colab |
| Import | `python -m ncrb.vlm_import <zip>` copies the pages into `data/ocr_cache/<model>/`; `python -m ncrb.extract --scanned --vlm-ready --force` re-reads the scanned files | laptop |

Extraction weighs every reading of a file it has (Tesseract, GLM-OCR on the
laptop, the Colab model) by the totals check, a missed total costing twice a
matched one, and keeps the best. No file whose totals can be checked gets worse.

## Candidates (October 2026)

Benchmarks are on modern documents (OmniDocBench v1.6); old typewritten
statistical tables can rank differently, hence the bake-off.

| Model | Size | Licence | OmniDocBench v1.6 overall | Table TEDS |
|---|---|---|---|---|
| [XingChen-AGI/TeleOCR](https://huggingface.co/XingChen-AGI/TeleOCR) (Aug 2026) | 1.2B | Apache-2.0 | 96.87 | 97.05 |
| [PaddlePaddle/PaddleOCR-VL-1.6](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6) (Jun 2026) | 0.9B | Apache-2.0 | 96.33 | 94.76 |
| [zai-org/GLM-OCR](https://huggingface.co/zai-org/GLM-OCR) (the laptop model, full precision) | 0.9B | MIT | 95.22 | 92.83 |

## After the run

```bash
uv run python -m ncrb.vlm_import ~/Downloads/TeleOCR.zip
uv run python -m ncrb.extract --scanned --vlm-ready --force
uv run python -m ncrb.build && uv run python -m ncrb.webdata
uv run --extra vlm --extra analysis python -m analysis.families
uv run --extra vlm --extra analysis python -m analysis.longseries
./deploy.sh
```
