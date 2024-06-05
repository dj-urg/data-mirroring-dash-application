import logging
import base64
import json
import pandas as pd
import plotly.express as px
from dash import html, dash_table, dcc

def parse_tiktok_contents(contents):
    # Ensure contents is a single string, if it's a list, get the first element
    if isinstance(contents, list):
        contents = contents[0]
    
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    parsed_data = json.loads(decoded.decode('utf-8'))
    logging.debug(f"Parsed TikTok Data Keys: {parsed_data.keys()}")
    return parsed_data

def flatten_tiktok_data(data, selected_sections):
    logging.debug(f"Flattening TikTok data for sections: {selected_sections}")
    flat_tiktok_data = []

    if 'video_history' in selected_sections:
        video_history = data.get('Activity', {}).get('Video Browsing History', {}).get('VideoList', [])
        for video in video_history:
            video['Source'] = 'Browsing'
        flat_tiktok_data.extend(video_history)

    if 'favorite_video' in selected_sections:
        favorite_video_history = data.get('Activity', {}).get('Favorite Videos', {}).get('FavoriteVideoList', [])
        if not favorite_video_history:
            favorite_video_history = data.get('Activity', {}).get('Favorite', {}).get('FavoriteVideoList', [])
        for video in favorite_video_history:
            video['Source'] = 'Favorite'
        flat_tiktok_data.extend(favorite_video_history)

    if 'item_favorite' in selected_sections:
        item_favorite_list = data.get('Activity', {}).get('Like List', {}).get('ItemFavoriteList', [])
        if not item_favorite_list:
            item_favorite_list = data.get('Activity', {}).get('Liked', {}).get('ItemFavoriteList', [])
        for video in item_favorite_list:
            video['Source'] = 'Liked'
        flat_tiktok_data.extend(item_favorite_list)

    if flat_tiktok_data:
        return pd.DataFrame(flat_tiktok_data)
    else:
        raise ValueError("No relevant data found in the selected sections.")
    
def create_video_history_graph(df):
    df['Date'] = pd.to_datetime(df['Date'])
    category_counts_per_date = df.groupby([df['Date'].dt.to_period('M'), 'Source']).size().unstack(fill_value=0)
    category_counts_per_date = category_counts_per_date.reset_index()
    category_counts_per_date['Date'] = category_counts_per_date['Date'].astype(str)
    fig = px.bar(category_counts_per_date, x='Date', y=['Browsing', 'Favorite', 'Liked'], 
                 title="Watched Videos per Month", labels={'value': 'Number of Videos', 'variable': 'Source'}, barmode='stack')
    fig.update_layout({
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {'color': '#2c3e50', 'family': "Arial, Helvetica, sans-serif"},
        'title': {'x': 0.5, 'xanchor': 'center'}
    })
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')
    return fig

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

def create_visualization(df):
    return dcc.Graph(figure=create_video_history_graph(df))
