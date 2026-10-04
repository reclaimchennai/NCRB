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

Open the notebook, pick an A100 (or L4) runtime and run its two cells. Cell 1
mounts Drive and starts [run_all.py](run_all.py) in the background; cell 2
([monitor.py](monitor.py)) shows progress, says where the result folder is at the end
and releases the GPU so no compute units are used after that.

| Step | What |
|---|---|
| Pages | the scanned pages only, one PDF per source file, with `manifest.json` (source SHA-256 and page numbers): release [`ocr-pages`](https://github.com/reclaimchennai/NCRB/releases/tag/ocr-pages), 4.1 GB, built by `scripts/build_ocr_bundle.py` |
| Bake-off | every candidate reads 280 pages (149 small files, up to 8 per report and decade); the best two read them again at 2048 px instead of 1600; the reading that reproduces most of NCRB's printed row and column totals wins |
| Full run | the winner reads all 12,945 pages; a crash or 25 minutes without a page restarts it (6 times at most); everything stops at 14 hours |
| Result | the folder `<root>/ocr_cache/<model>/` (or `<root>/<plan name>/`) on Drive. Download it from drive.google.com (right-click, Download; Drive zips it), then `python -m ncrb.vlm_import <zip>` copies it into `data/ocr_cache/<model>/` |

Everything is written to Drive (`MyDrive/ncrb_ocr/`) as it goes, so a reset
VM resumes where it stopped: run the cells again.

Extraction weighs every reading of a file it has (Tesseract, GLM-OCR on the
laptop, the Colab model) by the totals check, a missed total costing twice a
matched one, and keeps the best. No file whose totals can be checked gets worse.

## Candidates (October 2026)

Benchmarks are on modern documents (OmniDocBench v1.6); old typewritten
statistical tables can rank differently, hence the bake-off.

| Model | Size | Licence | OmniDocBench v1.6 overall | Table TEDS |
|---|---|---|---|---|
| [ATH-MaaS/OvisOCR2](https://huggingface.co/ATH-MaaS/OvisOCR2) | 0.8B | Apache-2.0 | 96.58 | 94.76 |
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

## Why not TeleOCR

TeleOCR (Aug 2026) tops OmniDocBench v1.6 (96.87, table TEDS 97.05) but is not in
the bake-off:

- its score comes from a two-stage pipeline (a layout pass at 1036 px, then each
  region cropped and read with its own prompt: "This is the image of a table...");
  the model card points to a separate project, NaviDC-OCR, for whole documents.
  Our job reads whole pages, and the page title and surrounding text are what join
  a table across years;
- its text model has `head_dim: 128` with a hidden size of 1024. vLLM's
  `Qwen2Attention` computes `head_dim = hidden_size // heads` (64), so the
  rotary embedding asserts (`sum(mrope_section) == rotary_dim // 2`) at start-up,
  in vLLM 0.30.0 on Colab. The transformers backend would take about a day.

If the bake-off winner leaves many files below the Tesseract reading, the
two-stage TeleOCR pipeline with a patched `Qwen2Attention` is the next thing to try.

## ocrkit: the reusable version

The scripts here are NCRB's own. [ocrkit/](../ocrkit/README.md) is the same machinery made general for any
scanned-document project: a manifest from local PDFs or public URLs (Colab downloads them itself), a
detached, supervised job with a bake-off and a pluggable scorer, page rendering ahead of the GPU, results
written page by page to Drive with no zip step, and `ocrkit fetch` for whatever Drive's folder download gives.
