"""
Kutsal Eşik Modül ve Fonksiyonel Birim Testleri
"""

import unittest
from kutsal_esik.core import (
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


class TestKutsalEsikCore(unittest.TestCase):
    def test_get_collections(self):
        quotes = get_quotes()
        self.assertGreaterEqual(len(quotes), 10)

        concepts = get_concepts()
        self.assertGreaterEqual(len(concepts), 5)

        timeline = get_timeline()
        self.assertGreaterEqual(len(timeline), 5)

        traditions = get_traditions()
        self.assertGreaterEqual(len(traditions), 4)

        bib = get_bibliography()
        self.assertGreaterEqual(len(bib), 5)

    def test_get_random_quote(self):
        q = get_random_quote()
        self.assertIn("author", q)
        self.assertIn("text", q)

        # Filtered by theme or culture
        q_filtered = get_random_quote(culture="Yunan")
        self.assertIn("Yunan", q_filtered.get("culture", ""))

    def test_search_all(self):
        # Search for known term
        res = search_all("Zeus")
        self.assertTrue(len(res["quotes"]) > 0 or len(res["concepts"]) > 0)

        # Search for non-existent term
        res_empty = search_all("xyz_non_existent_term_123")
        self.assertEqual(sum(len(v) for v in res_empty.values()), 0)

    def test_get_stats(self):
        stats = get_stats()
        self.assertIn("total_quotes", stats)
        self.assertIn("total_concepts", stats)
        self.assertIn("cultures", stats)
        self.assertGreater(stats["total_quotes"], 0)

    def test_export_bibtex(self):
        bibtex = export_bibtex()
        self.assertIn("@book{", bibtex)
        self.assertIn("author =", bibtex)
        self.assertIn("title =", bibtex)


if __name__ == "__main__":
    unittest.main()
