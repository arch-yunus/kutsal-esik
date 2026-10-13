"""
Kutsal Eşik Çekirdek Veri ve Arama Modülü
"""

from __future__ import annotations
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str) -> List[Dict[str, Any]]:
    """Belirtilen JSON veri dosyasını okur."""
    file_path = DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_quotes() -> List[Dict[str, Any]]:
    return load_json("quotes.json")


def get_concepts() -> List[Dict[str, Any]]:
    return load_json("concepts.json")


def get_timeline() -> List[Dict[str, Any]]:
    return load_json("timeline.json")


def get_traditions() -> List[Dict[str, Any]]:
    return load_json("traditions.json")


def get_bibliography() -> List[Dict[str, Any]]:
    return load_json("bibliography.json")


def get_random_quote(
    theme: Optional[str] = None, culture: Optional[str] = None
) -> Dict[str, Any]:
    """Filtrelenebilir rastgele bir alıntı döndürür."""
    quotes = get_quotes()
    if theme:
        theme_lower = theme.lower()
        quotes = [q for q in quotes if theme_lower in q.get("theme", "").lower()]
    if culture:
        culture_lower = culture.lower()
        quotes = [q for q in quotes if culture_lower in q.get("culture", "").lower()]
    if not quotes:
        quotes = get_quotes()
    return random.choice(quotes)


def search_all(query: str) -> Dict[str, List[Dict[str, Any]]]:
    """Tüm veri havuzlarında (alıntılar, kavramlar, kronoloji, gelenekler, kaynakça) arama yapar."""
    q = query.strip().lower()
    results: Dict[str, List[Dict[str, Any]]] = {
        "quotes": [],
        "concepts": [],
        "timeline": [],
        "traditions": [],
        "bibliography": [],
    }
    if not q:
        return results

    # Quotes
    for item in get_quotes():
        combined = f"{item.get('author', '')} {item.get('text', '')} {item.get('culture', '')} {item.get('theme', '')} {item.get('source', '')}".lower()
        if q in combined:
            results["quotes"].append(item)

    # Concepts
    for item in get_concepts():
        combined = f"{item.get('name', '')} {item.get('definition', '')} {item.get('civilization', '')} {' '.join(item.get('core_principles', []))}".lower()
        if q in combined:
            results["concepts"].append(item)

    # Timeline
    for item in get_timeline():
        combined = f"{item.get('title', '')} {item.get('description', '')} {item.get('region', '')} {item.get('concept', '')}".lower()
        if q in combined:
            results["timeline"].append(item)

    # Traditions
    for item in get_traditions():
        combined = f"{item.get('name', '')} {item.get('summary', '')} {item.get('region', '')} {' '.join(item.get('rituals', []))}".lower()
        if q in combined:
            results["traditions"].append(item)

    # Bibliography
    for item in get_bibliography():
        combined = f"{item.get('author', '')} {item.get('title', '')} {item.get('category', '')} {item.get('summary', '')} {' '.join(item.get('tags', []))}".lower()
        if q in combined:
            results["bibliography"].append(item)

    return results


def get_stats() -> Dict[str, Any]:
    """Kütüphane istatistiklerini hesaplar."""
    quotes = get_quotes()
    concepts = get_concepts()
    timeline = get_timeline()
    traditions = get_traditions()
    bib = get_bibliography()

    cultures = sorted({q.get("culture", "") for q in quotes if q.get("culture")})
    themes = sorted({q.get("theme", "") for q in quotes if q.get("theme")})

    return {
        "total_quotes": len(quotes),
        "total_concepts": len(concepts),
        "total_timeline_milestones": len(timeline),
        "total_traditions": len(traditions),
        "total_bibliography_sources": len(bib),
        "cultures": cultures,
        "themes": themes,
    }


def export_bibtex() -> str:
    """Kaynakça verilerini standart BibTeX formatında dışa aktarır."""
    bib = get_bibliography()
    lines = []
    for item in bib:
        item_id = item.get("id", "ref")
        author = item.get("author", "Anonim")
        title = item.get("title", "")
        year = item.get("year", "n.d.")
        publisher = item.get("publisher", "")
        lines.append(f"@book{{{item_id},")
        lines.append(f"  author = {{{author}}},")
        lines.append(f"  title = {{{title}}},")
        lines.append(f"  year = {{{year}}},")
        if publisher:
            lines.append(f"  publisher = {{{publisher}}},")
        lines.append("}\n")
    return "\n".join(lines)
