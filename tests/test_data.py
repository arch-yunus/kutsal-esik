"""
JSON Veri Bütünlüğü ve Şema Doğrulama Testleri
"""

import unittest
from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class TestDataIntegrity(unittest.TestCase):
    def test_data_files_exist(self):
        expected_files = [
            "quotes.json",
            "concepts.json",
            "timeline.json",
            "traditions.json",
            "bibliography.json",
        ]
        for filename in expected_files:
            file_path = DATA_DIR / filename
            self.assertTrue(file_path.exists(), f"{filename} bulunamadı!")

    def test_quotes_structure(self):
        path = DATA_DIR / "quotes.json"
        with open(path, "r", encoding="utf-8") as f:
            quotes = json.load(f)
        self.assertIsInstance(quotes, list)
        self.assertGreater(len(quotes), 0)
        required_keys = {"id", "author", "source", "period", "culture", "theme", "text"}
        for q in quotes:
            for key in required_keys:
                self.assertIn(key, q)
                self.assertTrue(bool(q[key]))

    def test_concepts_structure(self):
        path = DATA_DIR / "concepts.json"
        with open(path, "r", encoding="utf-8") as f:
            concepts = json.load(f)
        self.assertIsInstance(concepts, list)
        self.assertGreater(len(concepts), 0)
        required_keys = {"id", "name", "civilization", "definition", "core_principles"}
        for c in concepts:
            for key in required_keys:
                self.assertIn(key, c)
                self.assertTrue(bool(c[key]))

    def test_timeline_structure(self):
        path = DATA_DIR / "timeline.json"
        with open(path, "r", encoding="utf-8") as f:
            timeline = json.load(f)
        self.assertIsInstance(timeline, list)
        self.assertGreater(len(timeline), 0)
        required_keys = {"year", "period", "region", "title", "description", "concept"}
        for t in timeline:
            for key in required_keys:
                self.assertIn(key, t)
                self.assertTrue(bool(t[key]))

    def test_traditions_structure(self):
        path = DATA_DIR / "traditions.json"
        with open(path, "r", encoding="utf-8") as f:
            traditions = json.load(f)
        self.assertIsInstance(traditions, list)
        self.assertGreater(len(traditions), 0)
        required_keys = {"id", "name", "region", "symbols", "summary", "rituals"}
        for tr in traditions:
            for key in required_keys:
                self.assertIn(key, tr)
                self.assertTrue(bool(tr[key]))

    def test_bibliography_structure(self):
        path = DATA_DIR / "bibliography.json"
        with open(path, "r", encoding="utf-8") as f:
            bib = json.load(f)
        self.assertIsInstance(bib, list)
        self.assertGreater(len(bib), 0)
        required_keys = {"id", "author", "year", "title", "summary"}
        for b in bib:
            for key in required_keys:
                self.assertIn(key, b)
                self.assertTrue(bool(b[key]))


if __name__ == "__main__":
    unittest.main()
