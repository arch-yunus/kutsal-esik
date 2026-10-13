"""
Kutsal Eşik Komut Satırı Arayüzü (CLI)
"""

from __future__ import annotations
import argparse
import sys
from .core import (
    get_quotes,
    get_concepts,
    get_timeline,
    get_traditions,
    get_bibliography,
    get_random_quote,
    search_all,
    get_stats,
    export_bibtex,
)
from .web_server import run_server


def format_quote(q: dict) -> str:
    lines = [
        "",
        "┌" + "─" * 68 + "┐",
        f"│  \"{q.get('text', '')}\"",
        "│",
        f"│  — {q.get('author', 'Anonim')} ({q.get('source', '')})",
        f"│  Dönem: {q.get('period', '')} | Kültür: {q.get('culture', '')}",
        f"│  Tema: {q.get('theme', '')}",
        "└" + "─" * 68 + "┘",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    # Ensure stdout handles UTF-8 cleanly
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        prog="kutsal-esik",
        description="Kutsal Eşik: İnsanlık Tarihinde Misafirperverlik ve Erdem Kütüphanesi",
    )
    subparsers = parser.add_subparsers(dest="command", help="Kullanılabilir komutlar")

    # quote
    quote_parser = subparsers.add_parser("quote", help="Felsefi veya edebi bir alıntı gösterir")
    quote_parser.add_argument("--theme", type=str, help="Tema filtresi")
    quote_parser.add_argument("--culture", type=str, help="Kültür/Medeniyet filtresi")

    # search
    search_parser = subparsers.add_parser("search", help="Tüm kütüphanede anahtar kelime arar")
    search_parser.add_argument("query", type=str, help="Aranacak kelime veya kavram")

    # concepts
    subparsers.add_parser("concepts", help="Temel felsefi ve antropolojik kavramları listeler")

    # timeline
    subparsers.add_parser("timeline", help="Misafirperverliğin tarihsel kronolojisini listeler")

    # traditions
    subparsers.add_parser("traditions", help="Dünya medeniyetlerinin konukseverlik geleneklerini listeler")

    # bib
    bib_parser = subparsers.add_parser("bib", help="Akademik kaynakçayı görüntüler")
    bib_parser.add_argument("--export", action="store_true", help="BibTeX formatında dışa aktar")

    # stats
    subparsers.add_parser("stats", help="Kütüphane istatistiklerini gösterir")

    # serve
    serve_parser = subparsers.add_parser("serve", help="İnteraktif web portalını başlatır")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port numarası (Varsayılan: 8000)")
    serve_parser.add_argument("--no-browser", action="store_true", help="Tarayıcıyı otomatik açma")

    args = parser.parse_args()

    if not args.command:
        # Default behavior: show random quote and brief welcome
        print("=" * 70)
        print("  KUTSAL EŞİK: Yabancıdan Dosta — Evrensel Ahlak Arkeolojisi")
        print("=" * 70)
        q = get_random_quote()
        print(format_quote(q))
        print("Yardım için: python -m kutsal_esik --help")
        print("Web arayüzü: python -m kutsal_esik serve")
        return

    if args.command == "quote":
        q = get_random_quote(theme=args.theme, culture=args.culture)
        print(format_quote(q))

    elif args.command == "search":
        results = search_all(args.query)
        print(f"\n🔍 '{args.query}' için arama sonuçları:\n")
        total_found = sum(len(v) for v in results.values())
        if total_found == 0:
            print("  Sonuç bulunamadı.")
            return

        if results["quotes"]:
            print(f"📖 Alıntılar ({len(results['quotes'])} adet):")
            for item in results["quotes"]:
                print(f"  • {item['author']}: \"{item['text'][:90]}...\" ({item['source']})")
            print()

        if results["concepts"]:
            print(f"🏛️ Kavramlar ({len(results['concepts'])} adet):")
            for item in results["concepts"]:
                print(f"  • {item['name']} ({item['civilization']}): {item['definition'][:100]}...")
            print()

        if results["timeline"]:
            print(f"⏳ Zaman Çizelgesi ({len(results['timeline'])} adet):")
            for item in results["timeline"]:
                print(f"  • [{item['year']}] {item['title']} - {item['region']}")
            print()

        if results["traditions"]:
            print(f"🌍 Medeniyet Gelenekleri ({len(results['traditions'])} adet):")
            for item in results["traditions"]:
                print(f"  • {item['name']}: {item['summary'][:100]}...")
            print()

        if results["bibliography"]:
            print(f"📚 Kaynakça ({len(results['bibliography'])} adet):")
            for item in results["bibliography"]:
                print(f"  • {item['author']} ({item['year']}) - {item['title']}")
            print()

    elif args.command == "concepts":
        concepts = get_concepts()
        print(f"\n🏛️ TEMEL KAVRAMLAR VE ANLAMLARI ({len(concepts)} Kavram):\n")
        for c in concepts:
            print(f"▶ {c['name']} [{c['civilization']}]")
            print(f"  Tanım: {c['definition']}")
            print("  İlkeler:")
            for p in c.get("core_principles", []):
                print(f"    - {p}")
            print()

    elif args.command == "timeline":
        timeline = get_timeline()
        print(f"\n⏳ MİSAFİRPERVERLİĞİN TARİHSEL KRONOLOJİSİ ({len(timeline)} Dönem):\n")
        for t in timeline:
            print(f"• [{t['year']}] {t['title']} ({t['region']})")
            print(f"  {t['description']}")
            print(f"  Kavram: {t['concept']} | Etki: {t['impact']}\n")

    elif args.command == "traditions":
        traditions = get_traditions()
        print(f"\n🌍 MEDENİYETLER VE KONUKSEVERLİK GELENEKLERİ ({len(traditions)} Bölge):\n")
        for trad in traditions:
            print(f"▶ {trad['name']} ({trad['region']})")
            print(f"  Semboller: {', '.join(trad.get('symbols', []))}")
            print(f"  Özet: {trad['summary']}")
            print(f"  Özlü Söz: \"{trad.get('famous_saying', '')}\"\n")

    elif args.command == "bib":
        if args.export:
            print(export_bibtex())
        else:
            bib = get_bibliography()
            print(f"\n📚 AKADEMİK KAYNAKÇA ({len(bib)} Eser):\n")
            for b in bib:
                print(f"• {b['author']} ({b['year']}). {b['title']}.")
                if b.get("original_title"):
                    print(f"  Orijinal: {b['original_title']}")
                print(f"  Yayım: {b.get('publisher', '')} | Kategori: {b.get('category', '')}")
                print(f"  Özet: {b.get('summary', '')}\n")

    elif args.command == "stats":
        stats = get_stats()
        print("\n📊 KUTSAL EŞİK VERİ TABANI İSTATİSTİKLERİ:")
        print(f"  • Toplam Alıntı Sayısı: {stats['total_quotes']}")
        print(f"  • Temel Kavram Sayısı: {stats['total_concepts']}")
        print(f"  • Kronolojik Dönüm Noktası: {stats['total_timeline_milestones']}")
        print(f"  • İncelenen Kültür/Gelenek Sayısı: {stats['total_traditions']}")
        print(f"  • Akademik Kaynakça: {stats['total_bibliography_sources']}")
        print(f"  • Kapsanan Kültürler: {', '.join(stats['cultures'])}")
        print()

    elif args.command == "serve":
        run_server(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
