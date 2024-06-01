import sys
import os
import pytest
from dash import Dash
from dash.testing.application_runners import import_app
from src.components.layout import create_layout
from src.components.callbacks import register_callbacks

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.usefixtures("dash_duo")
def test_update_output(dash_duo):
    app = Dash(__name__)
    app.layout = create_layout()
    register_callbacks(app)

    dash_duo.start_server(app)

    # Simulate user input and button click
    dash_duo.find_element('#input-box').send_keys('test input')
    dash_duo.find_element('#button').click()
    dash_duo.wait_for_text_to_equal('#output-container', 'You have entered: test input', timeout=10)
