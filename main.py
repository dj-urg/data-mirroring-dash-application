import os
import logging
from app import app, server
from components.layout import create_layout
from components.callbacks import register_callbacks

logging.basicConfig(level=logging.INFO)

def setup_app():
    logging.info("Setting up app layout")
    app.layout = create_layout()
    logging.info("Registering callbacks")
    register_callbacks()
    logging.info("Setup complete")

setup_app()

if __name__ == "__main__":
    logging.info("Starting server")
    server.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8051)))
