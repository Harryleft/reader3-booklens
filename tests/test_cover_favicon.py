import unittest

from reader3 import Book, BookMetadata
from server import book_cover_image_name


class CoverFaviconTests(unittest.TestCase):
    def make_book(self, images):
        return Book(
            metadata=BookMetadata(title="Test", language="zh"),
            spine=[],
            toc=[],
            images=images,
            source_file="test.epub",
            processed_at="2026-07-13T00:00:00",
        )

    def test_selects_cover_image_filename(self):
        book = self.make_book({
            "OEBPS/Images/cover.jpeg": "images/cover.jpeg",
            "cover.jpeg": "images/cover.jpeg",
        })

        self.assertEqual(book_cover_image_name(book), "cover.jpeg")

    def test_returns_none_when_no_cover_candidate_exists(self):
        book = self.make_book({"Images/chapter-1.jpg": "images/chapter-1.jpg"})

        self.assertIsNone(book_cover_image_name(book))


if __name__ == "__main__":
    unittest.main()
