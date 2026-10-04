"""Document OCR models ocrkit knows how to run with vLLM: prompt, output budget and engine settings.

Add a model by adding an entry. 'prompt' follows the model card; 'max_tokens' bounds one page's output;
'engine' are extra vllm.LLM(...) arguments; 'max_model_len' must hold the image tokens plus max_tokens.
Rankings change fast: as of October 2026, OvisOCR2 won a bake-off on old typewritten statistical tables
(NCRB), ahead of PaddleOCR-VL-1.6; TeleOCR (top of OmniDocBench v1.6) does not start in vLLM 0.30
(its head_dim breaks vLLM's Qwen2 rotary embedding) and is region-level, so it is not listed.
"""

from __future__ import annotations

import re

MODELS: dict[str, dict] = {
    "ATH-MaaS/OvisOCR2": {
        "prompt": "Extract all readable content from the image in natural human reading order and output as Markdown. "
                  "Use HTML image tags for charts/images, LaTeX for formulas, and HTML tables for tabular data.",
        "max_tokens": 16384, "max_model_len": 24576, "engine": {},
    },
    "PaddlePaddle/PaddleOCR-VL-1.6": {
        "prompt": "Table Recognition:", "max_tokens": 8192, "max_model_len": 16384,
        "engine": {"enable_prefix_caching": False, "mm_processor_cache_gb": 0, "max_num_batched_tokens": 16384},
    },
    "zai-org/GLM-OCR": {"prompt": "Table Recognition:", "max_tokens": 8192, "max_model_len": 16384, "engine": {}},
    "PaddlePaddle/PaddleOCR-VL-1.6:ocr": {   # plain text pages (no tables)
        "prompt": "OCR:", "max_tokens": 8192, "max_model_len": 16384, "hf": "PaddlePaddle/PaddleOCR-VL-1.6",
        "engine": {"enable_prefix_caching": False, "mm_processor_cache_gb": 0, "max_num_batched_tokens": 16384},
    },
}


def spec(model: str) -> dict:
    """Settings for a model id; an unknown id runs with a generic table prompt."""
    base = model.split("@")[0]
    s = dict(MODELS.get(base, {"prompt": "Convert this page to Markdown. Write tables as HTML tables.", "max_tokens": 8192,
                               "max_model_len": 16384, "engine": {}}))
    s.setdefault("hf", base.split(":")[0])
    return s


def slug(model: str, edge: int | None = None) -> str:
    """Cache folder name: 'ATH-MaaS/OvisOCR2' at 2048 px -> 'OvisOCR2-2048' (1600 px, the default, has no suffix)."""
    name = model.split("/")[-1] + (f"@{edge}" if edge and edge != 1600 else "")
    return re.sub(r"[^A-Za-z0-9.]+", "-", name).strip("-")
