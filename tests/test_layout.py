import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Dash
from src.components.layout import create_layout

class TestLayout(unittest.TestCase):
    def setUp(self):
        self.app = Dash(__name__)

    def test_layout(self):
        layout = create_layout()
        self.assertIsNotNone(layout, "Layout should not be None")
        
        # Print layout children for debugging
        print(f"Layout children: {layout.children}")
        
        # Adjust this to the correct number of children after inspecting the print output
        self.assertEqual(len(layout.children), 7, "Layout should have the correct number of children")

if __name__ == '__main__':
    unittest.main()
