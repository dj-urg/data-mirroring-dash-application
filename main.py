import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, session, render_template_string
from dash import Dash
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
from src.components.layout import create_layout
from src.components.callbacks import register_callbacks

# Load environment variables from .env file
load_dotenv()

DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
PORT = int(os.getenv('PORT', 8051))
ACCESS_CODE = os.getenv('ACCESS_CODE')

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

server = Flask(__name__)
server.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Apply Talisman for HTTPS enforcement and other security headers
csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\'',
    'style-src': '\'self\' \'unsafe-inline\'',
    'img-src': '\'self\''
}
Talisman(server, force_https=True, content_security_policy=csp)

# Configure session settings
server.config.update(
    SESSION_COOKIE_SECURE=True,  # Ensures cookies are sent over HTTPS only
    SESSION_COOKIE_HTTPONLY=True,  # Prevents client-side scripts from accessing the cookie
    SESSION_COOKIE_SAMESITE='Lax',  # Helps protect against CSRF
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)  # Session timeout for security
)

# Set up rate limiting to prevent brute force attacks
limiter = Limiter(
    get_remote_address,
    app=server,
    default_limits=["5 per minute"]  # Limit login attempts
)

app = Dash(__name__, server=server, url_base_pathname='/app/')
app.config.suppress_callback_exceptions = True

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

@server.route('/', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Apply rate limit to login route
def login():
    if request.method == 'POST':
        code = request.form['code']
        if code == ACCESS_CODE:
            session['authenticated'] = True
            session.permanent = True  # Make the session permanent to apply timeout
            return redirect('/app')
        else:
            return "Invalid Code", 403
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <form method="post">
            <label for="code">Access Code:</label>
            <input type="password" id="code" name="code">
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    '''

@server.route('/app')
def render_app():
    if not session.get('authenticated'):
        return redirect('/')
    return app.index()

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

setup_app()
application = server
