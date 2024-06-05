from main import setup_app, server

setup_app()

app = server  # Gunicorn expects 'app' to be the WSGI callable