"""
Kutsal Eşik Yerel Web Sunucusu
"""

from __future__ import annotations
import http.server
import socketserver
import webbrowser
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, format, *args):
        # Temiz terminal çıktısı
        print(f"  [Web] {self.address_string()} - {format % args}")


def run_server(port: int = 8000, open_browser: bool = True) -> None:
    """Yerel web sunucusunu başlatır."""
    url = f"http://localhost:{port}"
    print(f"\n=======================================================")
    print(f"  KUTSAL EŞİK - DİJİTAL BEŞERİ BİLİMLER PORTALI")
    print(f"  Yerel sunucu başlatıldı: {url}")
    print(f"  Web dizini: {WEB_DIR}")
    print(f"  Durdurmak için Ctrl+C tuşlarına basınız.")
    print(f"=======================================================\n")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    with socketserver.TCPServer(("", port), CustomHTTPHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu kapatıldı. İyi çalışmalar!")
