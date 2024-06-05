import pandas as pd
from dash import html, dash_table, dcc

def create_data_table(df):
    return html.Div([
        dash_table.DataTable(
            data=df.head(10).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif', 'padding': '10px'},
            style_header={'backgroundColor': '#F3F4F6', 'fontWeight': 'bold'},
            style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#F9FAFB'}]
        )
    ], className='table-container')

def create_download_buttons(platform):
    buttons = [html.Button("Download CSV", id="btn-download-csv", className="download-btn")]
    if platform in ['tiktok', 'youtube']:
        buttons.append(html.Button("Download URLs for 4CAT processing", id="btn-download-urls", className="download-btn"))
    return buttons

def extract_urls_for_4cat(df):
    """
    Extract URLs from the DataFrame for further analysis with 4CAT.
    :param df: DataFrame containing the YouTube data
    :return: String with URLs separated by commas
    """
    urls = df['Link'].tolist()
    return ','.join(urls)