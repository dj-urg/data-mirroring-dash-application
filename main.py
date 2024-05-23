import os
import logging
from app import app, server
from src.components.layout import create_layout
from src.components.callbacks import register_callbacks

logging.basicConfig(level=logging.INFO)

def setup_app():
    app.layout = create_layout()
    register_callbacks()

if __name__ == "__main__":
    setup_app()
    server.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8051)))
