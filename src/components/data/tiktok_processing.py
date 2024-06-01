import base64
import json
import pandas as pd
import plotly.express as px

def parse_tiktok_contents(contents, selected_sections):
    """
    Parse the base64 encoded contents to JSON for TikTok data processing and return as DataFrame.
    
    :param contents: base64 encoded string from uploaded file
    :param selected_sections: List of strings representing sections to process
    :return: DataFrame containing the processed TikTok data
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    data = json.loads(decoded.decode('utf-8'))  # Decode to string before JSON parsing
    
    all_videos = []
    # Extract selected data sections from the uploaded file
    if 'video_history' in selected_sections:
        video_history = data.get('Activity', {}).get('Video Browsing History', {}).get('VideoList', [])
        for video in video_history:
            video['Source'] = 'Browsing'
        all_videos.extend(video_history)
    
    if 'favorite_video' in selected_sections:
        favorite_video_history = data.get('Activity', {}).get('Favorite Videos', {}).get('FavoriteVideoList', [])
        # Fallback to 'Favorite' if 'Favorite Videos' does not exist
        if not favorite_video_history:
            favorite_video_history = data.get('Activity', {}).get('Favorite', {}).get('FavoriteVideoList', [])
        for video in favorite_video_history:
            video['Source'] = 'Favorite'
        all_videos.extend(favorite_video_history)
    
    if 'item_favorite' in selected_sections:
        item_favorite_list = data.get('Activity', {}).get('Like List', {}).get('ItemFavoriteList', [])
        # If not found, try the old key structure
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