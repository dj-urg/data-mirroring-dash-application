import logging
from app import app
from src.components.layout import create_layout
from src.components.callbacks import register_callbacks

logging.basicConfig(level=logging.INFO)

def setup_app():
    app.layout = create_layout()
    register_callbacks()

def run():
    app.run_server(debug=True)

if __name__ == "__main__":
    setup_app()
    run()