import json
from pathlib import Path
from typing import Dict, List

# DB = Path("reports.json")
DB = Path(__file__).resolve().parent / "reports.json"


def _loadAll() -> List[Dict]:

    if not DB.exists():
        return []

    try:
        return json.loads(DB.read_text(encoding="utf-8"))
    except Exception:
        return []

def _saveAll(items: List[Dict]) -> None:

    jsonString = json.dumps(items, indent=2, ensure_ascii=False)
    DB.write_text(jsonString, encoding="utf-8")

def saveReport(report: Dict) -> None:
    all_items = _loadAll()
    all_items.append(report)
    _saveAll(all_items)

# def listReports() -> List[Dict]:
#      return _loadAll()