import os
import logging
from dotenv import load_dotenv
from app import app, server
from src.components.layout import create_layout
from src.components.callbacks import register_callbacks

# Load environment variables from .env file
load_dotenv()

DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
PORT = int(os.getenv('PORT', 8051))

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def setup_app():
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
    logging.info("Starting server")
    try:
        server.run(debug=DEBUG, host='0.0.0.0', port=PORT)
        logging.info(f"Server running on port {PORT}")
    except Exception as e:
        logging.error("Error starting server: %s", e)
        raise

if __name__ == "__main__":
    setup_app()
    run_server()
