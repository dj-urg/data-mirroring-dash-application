import os
import logging
from app import app, server
from src.components.layout import create_layout
from src.components.callbacks import register_callbacks

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_app():
    """
    Set up the Dash app layout and register callbacks.
    """
    logging.info("Setting up app layout")
    try:
        app.layout = create_layout()
        logging.info("Layout setup complete")
    except Exception as e:
        logging.error("Error setting up layout: %s", e)

    logging.info("Registering callbacks")
    try:
        register_callbacks(app)
        logging.info("Callbacks registered")
    except Exception as e:
        logging.error("Error registering callbacks: %s", e)

def run_server():
    """
    Run the server with specified configurations.
    """
    logging.info("Starting server")
    try:
        port = int(os.environ.get('PORT', 8051))
        debug = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
        server.run(debug=debug, host='0.0.0.0', port=port)
        logging.info(f"Server running on port {port}")
    except Exception as e:
        logging.error("Error starting server: %s", e)
        raise

if __name__ == "__main__":
    setup_app()
    run_server()
