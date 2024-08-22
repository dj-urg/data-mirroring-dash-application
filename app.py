from dash import Dash
import dash_bootstrap_components as dbc
from main import server  # Import the Flask server from main.py

app = Dash(__name__, 
           server=server,  # Use the Flask server from main.py
           external_stylesheets=[dbc.themes.BOOTSTRAP], 
           suppress_callback_exceptions=True)

app.title = "Data Mirroring App"
