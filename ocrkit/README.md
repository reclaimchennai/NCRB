# ocrkit

Read scanned documents with current OCR models on a cloud GPU (Google Colab), fast and unattended, and
pick the best reading of every page by checks the documents carry themselves.

Built for NCRB's crime, accident and prison statistics (12,758 scanned pages from 1953–2000, read in about
2.5 hours on an A100 for about 13 Colab compute units), written to be reused for any project with scanned
PDFs, especially statistical tables.

## The whole loop

```
your computer                         Colab (A100)                          your computer
-------------                         ------------                          -------------
ocrkit manifest  ->  manifest.json -> notebook: bake-off, every page   ->  Drive folder download
(scanned pages)      (+ tars if        written to Drive page by page,       ocrkit fetch -> cache
                     not online)       GPU released at the last page        your extraction picks the
                                                                            best reading per file
```

### 1. Make a manifest

```bash
pip install "ocrkit @ git+https://github.com/reclaimchennai/NCRB#subdirectory=ocrkit"
ocrkit manifest raw/**/*.pdf --out work/                 # scanned pages only (no text layer)
ocrkit manifest --urls sources.csv --out work/           # url,path: Colab downloads these itself
ocrkit manifest ... --all-pages                          # every page, text layer or not
```

- **Prefer URLs.** When the sources are public, Colab downloads them itself. Nothing is uploaded from your
  computer, and each file is checked against its SHA-256.
- **Otherwise, a bundle.** Files that aren't online are cut down to their scanned pages and packed into tars
  of at most 1.9 GB. Host them anywhere Colab can reach, such as a GitHub release, and pass
  `--parts-base <URL>`.
- **Bake-off sample.** Up to 150 small files, spread over source folders (`--bench-files N`).

Host `manifest.json` next to the tars, or anywhere Colab can read it: a raw GitHub URL, or a path in your
Drive.

### 2. Run it on Colab

Open [notebooks/ocrkit_colab.ipynb](notebooks/ocrkit_colab.ipynb) in Colab
([direct link](https://colab.research.google.com/github/reclaimchennai/NCRB/blob/main/ocrkit/notebooks/ocrkit_colab.ipynb)).
Pick an A100 runtime, fill in the settings cell, then run the four cells.

| Setting | What it does |
|---|---|
| `BAKEOFF` | Models and page sizes to compare on the sample. The best two are tried again at `top_edges`. The winner reproduces the most sums (row and column totals); ties go to agreement with the other readings. |
| `RUNS` | `'winner'`, or explicit `[{'model', 'edge'}, ...]` for a second round on chosen `FILES`. |
| `scorer` | `'module:function'` taking `({page: text}, manifest entry)` and returning `(matched, checked)`. Use your documents' own checks, as NCRB uses its State/UT/all-India totals. |

### 3. Bring the readings back

On drive.google.com, right-click the project folder under `ocrkit/` and choose **Download**. Drive zips it on
its side; for many files it may make several zips. Then:

```bash
ocrkit fetch ~/Downloads/myproject-*.zip --cache data/ocr_cache
ocrkit score --cache data/ocr_cache --manifest work/manifest.json    # sums matched per reading
```

The cache layout is `<cache>/<model slug>/<file id>/<page:04d>.txt`, with one raw model output per page. A
page size other than 1600 px gets a suffix, e.g. `OvisOCR2-2048`. Parse the outputs with `ocrkit.tables`,
which handles HTML, OTSL and Markdown tables.

## Choosing between readings

Keep every reading of a page (Tesseract, model A, model A at a larger size, model B) and choose per file:

1. **Your documents' own checks.** For NCRB: State/UT/all-India total rows.
2. **Every other internal sum.** Total rows inside lists, and row totals (Male + Female = Total);
   `ocrkit.score.check_grid` does both.
3. **Agreement with the other independent readings.** Two models rarely misread the same digit the same
   way (`ocrkit.score.agreement`).

On NCRB this took the scanned years from 57% of printed totals matched (Tesseract) to 92% with one model,
then to 93.4% with two models and two page sizes. Each of the four readings was the best one for some files.

## Lessons this is built on

| What went wrong | What ocrkit does |
|---|---|
| Ctrl+C on the cell that started the job killed the job | The job starts detached (`start_new_session`), so no cell can stop it |
| An interrupted run left a vLLM engine holding 38 GB, so every restart "failed" | Leftover vLLM processes are killed and GPU memory freed before every start |
| A startup failure of a model that had worked was treated as the model failing | Models that have worked are retried; unknown ones get one try with the transformers backend, then are dropped |
| The GPU idled while pages rendered (51% use) | Pages are fetched and rendered in background threads, several batches ahead |
| Zipping 19,000 files on Drive with an A100 attached, then a deleted runtime left a half-written zip | No zip step: download the folder from Drive. The GPU is released as soon as the last page is read |
| A 4 GB bundle uploaded from a laptop | Colab downloads public sources itself |
| rclone with its shared Google client throttled to 174 B/s on many small files | Drive's own folder download; `ocrkit fetch` takes any zips or folders |
| One bad page crashed a batch | The batch is retried page by page; a page that fails alone gets `.err` and the run goes on |
| Several threads fetched the same file for different pages; the first renamed the download away from the others, and 226 page-readings failed (round 3) | One download per file behind a lock; pages that failed only for download reasons are tried again on the next run |
| The top benchmark model (TeleOCR) doesn't start in vLLM 0.30, and is region-level anyway | The bake-off decides on your own pages; a model that won't start is skipped within minutes |

## Models

[src/ocrkit/models.py](src/ocrkit/models.py) holds the prompt, output budget and vLLM settings per model.
Add a model by adding an entry. An unknown model id runs with a generic "Markdown with HTML tables" prompt.
