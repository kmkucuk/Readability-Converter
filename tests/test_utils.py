import unittest
import os
import tempfile
from readability_converter.utils.file_loader import getFilesInDir
from readability_converter.utils.image_properties import round_for_image, get_dimensions
from readability_converter.utils.text_format_manager import getTextProperties

class TestGetFilesInDir(unittest.TestCase):
    def test_get_files_in_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test")
            files = getFilesInDir(temp_dir)
            self.assertTrue(any("test.txt" in f for f in files))

class TestImageDimensions(unittest.TestCase):
    def test_round_for_image(self):
        self.assertEqual(round_for_image(3.6), 4)
        self.assertEqual(round_for_image(2.1), 2)

    def test_get_dimensions(self):
        dims = get_dimensions(100.4, 200.6)
        self.assertEqual(dims["width"], 100)
        self.assertEqual(dims["height"], 201)
        self.assertIn("center_x", dims)
        self.assertIn("center_y", dims)

class TestTextProperties(unittest.TestCase):
    def setUp(self):
        # Use a common system font (requires fontTools to parse)
        import matplotlib.font_manager as fm
        self.font_path = fm.findSystemFonts(fontpaths=None, fontext='ttf')[0]

    def test_get_font_name(self):
        obj = getTextProperties([self.font_path], [12], [1], [1])
        name = obj.get_font_name(0)
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)

    def test_get_glyph_height(self):
        obj = getTextProperties([self.font_path], [12], [1], [1])
        height = obj.get_glyph_height(0)
        self.assertIsInstance(height, int)
        self.assertGreater(height, 0)

if __name__ == "__main__":
    unittest.main()
