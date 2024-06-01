import base64
import json
import pandas as pd
import plotly.express as px
from dash import html, dash_table, dcc

def parse_tiktok_contents(contents):
    """
    Parse the base64 encoded contents to JSON for TikTok data processing and return as DataFrame.
    
    :param contents: base64 encoded string from uploaded file
    :return: DataFrame containing the processed TikTok data
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    data = json.loads(decoded.decode('utf-8'))  # Decode to string before JSON parsing
    
    all_videos = []
    # Extract data sections from the uploaded file
    video_history = data.get('Activity', {}).get('Video Browsing History', {}).get('VideoList', [])
    for video in video_history:
        video['Source'] = 'Browsing'
    all_videos.extend(video_history)
    
    favorite_video_history = data.get('Activity', {}).get('Favorite Videos', {}).get('FavoriteVideoList', [])
    if not favorite_video_history:
        favorite_video_history = data.get('Activity', {}).get('Favorite', {}).get('FavoriteVideoList', [])
    for video in favorite_video_history:
        video['Source'] = 'Favorite'
    all_videos.extend(favorite_video_history)
    
    item_favorite_list = data.get('Activity', {}).get('Like List', {}).get('ItemFavoriteList', [])
    if not item_favorite_list:
        item_favorite_list = data.get('Activity', {}).get('Liked', {}).get('ItemFavoriteList', [])
    for video in item_favorite_list:
        video['Source'] = 'Liked'
    all_videos.extend(item_favorite_list)
    
    if all_videos:
        tiktok_df = pd.DataFrame(all_videos)
        return tiktok_df
    else:
        raise ValueError("No relevant data found in the selected sections.")

def extract_urls_for_4cat(df):
    """
    Extract URLs from the DataFrame for further analysis with 4CAT.
    
    :param df: DataFrame containing the TikTok data
    :return: String with URLs separated by commas
    """
    urls = df['Link'].tolist()
    return ','.join(urls)

def create_video_history_graph(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    
    monthly_counts = df.groupby('Month').size().reset_index(name='Counts')
    
    fig = px.bar(monthly_counts, x='Month', y='Counts', 
                 title='Videos Watched per Month',
                 labels={'Month': 'Month', 'Counts': 'Number of Videos Watched'})
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#2c3e50', family="Arial, Helvetica, sans-serif"),
        title=dict(x=0.5, xanchor='center')
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')
    
    return fig

def create_description():
    return html.P(
        "Upload successful! 🎉 The table below displays the first rows of your TikTok data. "
        "It includes the dates you watched videos, the video URLs, and your engagement (browsing, favoriting, or liking). "
        "You can download the complete dataset as a CSV file or extract the URLs for further analysis with 4CAT. "
        "Additionally, a visualization will show the number of videos watched per month, categorized by source. Enjoy exploring your data!",
        style={
            'textAlign': 'justify',
            'color': '#4B5563',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '1.1em',
            'lineHeight': '1.6',
            'marginTop': '20px',
            'marginBottom': '20px'
        }
    )

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

def create_download_buttons():
    return [
        html.Button("Download CSV", id="btn-download-csv", className="download-btn"),
        html.Button("Download URLs for 4CAT", id="btn-download-urls", className="download-btn")
    ]

def create_visualization(df):
    return dcc.Graph(figure=create_video_history_graph(df))
