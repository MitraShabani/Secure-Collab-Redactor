import json
from pathlib import Path
from typing import Dict, List
import re

# DB = Base Path
DB = Path(__file__).resolve().parent / "data"


def safe_filename(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9_\- ]", "", name)
    name = name.replace(" ", "_")
    return name or "results"

def _loadAll(path: Path) -> List[Dict]:

    if not path.exists():
        return []

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

def _saveAll(path: Path, items: List[Dict]) -> None:

    jsonString = json.dumps(items, indent=2, ensure_ascii=False)
    path.write_text(jsonString, encoding="utf-8")

def saveReport(results: Dict) -> None:
    title = results.get("title", "results")
    filename = safe_filename(title) + ".json"
    file_path = DB / filename

    all_items = _loadAll(file_path)
    all_items.append(results)
    _saveAll(file_path, all_items)

# def listReports() -> List[Dict]:
#      return _loadAll()