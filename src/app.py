from dash import Dash
import dash_bootstrap_components as dbc

# Only create the Dash application instance here
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Data Mirroring App"

server = app.server
