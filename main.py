import os
import logging
from app import app, server
from src.components.layout import create_layout
from src.components.callbacks import register_callbacks

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_app():
    logging.info("Setting up app layout")
    try:
        app.layout = create_layout()
        logging.info("Layout setup complete")
    except Exception as e:
        logging.error("Error setting up layout: %s", e)

    logging.info("Registering callbacks")
    try:
        register_callbacks()
        logging.info("Callbacks registered")
    except Exception as e:
        logging.error("Error registering callbacks: %s", e)

setup_app()

if __name__ == "__main__":
    logging.info("Starting server")
    port = int(os.environ.get('PORT', 8051))
    server.run(debug=bool(os.environ.get('DEBUG', False)), host='0.0.0.0', port=port)
