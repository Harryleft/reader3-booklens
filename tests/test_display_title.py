import unittest

from server import display_title


class DisplayTitleTests(unittest.TestCase):
    def test_removes_promotional_parenthetical_copy(self):
        title = (
            "理解媒介：论人的延伸"
            "（互联网思维奠基之作，认知突围必读经典。启发多位作者的预言书！）"
        )

        self.assertEqual(display_title(title), "理解媒介：论人的延伸")

    def test_removes_ascii_promotional_parenthetical_copy(self):
        self.assertEqual(display_title("书名 (畅销经典推荐)"), "书名")

    def test_preserves_non_promotional_edition_information(self):
        self.assertEqual(display_title("Python（第2版）"), "Python（第2版）")


if __name__ == "__main__":
    unittest.main()
