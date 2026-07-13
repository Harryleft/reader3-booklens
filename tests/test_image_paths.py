import unittest

from bs4 import BeautifulSoup

from reader3 import rewrite_content_image_paths


class RewriteContentImagePathsTests(unittest.TestCase):
    def setUp(self):
        self.image_map = {
            "OEBPS/Images/cover.jpeg": "images/cover.jpeg",
            "cover.jpeg": "images/cover.jpeg",
        }

    def test_rewrites_svg_xlink_cover(self):
        html = '<svg><image xlink:href="../Images/cover.jpeg"></image></svg>'

        result = rewrite_content_image_paths(
            html, "OEBPS/Text/cover.xhtml", self.image_map
        )
        image = BeautifulSoup(result, "html.parser").find("image")

        self.assertEqual(image["xlink:href"], "images/cover.jpeg")

    def test_rewrites_epub3_svg_href_cover(self):
        html = '<svg><image href="cover.jpeg"></image></svg>'

        result = rewrite_content_image_paths(
            html, "OEBPS/cover.xhtml", self.image_map
        )
        image = BeautifulSoup(result, "html.parser").find("image")

        self.assertEqual(image["href"], "images/cover.jpeg")

    def test_keeps_already_rewritten_image_path(self):
        html = '<img src="images/cover.jpeg">'

        result = rewrite_content_image_paths(
            html, "OEBPS/Text/cover.xhtml", self.image_map
        )
        image = BeautifulSoup(result, "html.parser").find("img")

        self.assertEqual(image["src"], "images/cover.jpeg")


if __name__ == "__main__":
    unittest.main()
