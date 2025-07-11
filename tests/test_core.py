import unittest
from readability_converter.core.converter import wrap_text
from readability_converter.core.text_loader import getStimulusSheet
from PIL import ImageFont
import pandas as pd
import tempfile
import os

class TestConverterFunctions(unittest.TestCase):
    def test_wrap_text_simple(self):
        font = ImageFont.load_default()
        text = "This is a sample sentence for testing"
        image_dimensions = {"wrap_width": 100, "page_borders": 5}
        lines = wrap_text(text, font, kerning=0, imageDimensions=image_dimensions)
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)

class TestGetStimulusSheet(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file
        self.test_data = pd.DataFrame({
            "Passage": ["Intro", "Body"],
            "Text": ["This is the intro.", "This is the body."]
        })
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w')
        self.test_data.to_csv(self.temp_file.name, index=False)
        self.temp_file.close()
        self.sheet = getStimulusSheet(self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_item_count_single_digit(self):
        result = self.sheet.item_count("passage3")
        self.assertEqual(result, 3)

    def test_item_count_double_digit(self):
        result = self.sheet.item_count("passage12")
        self.assertEqual(result, 12)

    def test_get_text(self):
        text = self.sheet.get_text(0)
        self.assertIn("intro", text.lower())

if __name__ == "__main__":
    unittest.main()
