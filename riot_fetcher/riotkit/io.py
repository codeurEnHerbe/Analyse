import os
import json
import re
import time

def _ts():
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

def _slug(x):
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", str(x)).strip("_")
    return s or "x"

def save_json(category, stem, payload, data_root="data"):
    d = os.path.join(data_root, category)
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f"{_ts()}_{_slug(stem)}.json")
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    return f
