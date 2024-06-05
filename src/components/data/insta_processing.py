import base64
import json
import pandas as pd
import plotly.express as px
from dash import html, dash_table, dcc

def parse_instagram_contents(contents):
    """
    Parse base64 encoded contents to JSON.
    
    :param contents: base64 encoded string from uploaded file
    :return: Parsed JSON content
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return json.loads(decoded.decode('utf-8'))

def parse_instagram_contents(contents):
    # Ensure contents is a single string, if it's a list, get the first element
    if isinstance(contents, list):
        contents = contents[0]
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return json.loads(decoded.decode('utf-8'))

def flatten_instagram_data(data):
    flat_instagram_data = []

    # Process various Instagram data structures
    for key in ['saved_saved_media', 'likes_media_likes', 'impressions_history_posts_seen', 
                'impressions_history_chaining_seen', 'impressions_history_videos_watched']:
        if key in data:
            for item in data[key]:
                if key == 'saved_saved_media':
                    flat_instagram_data.append({
                        'title': item.get('title', 'No Title'),
                        'href': item['string_map_data'].get('Saved on', {}).get('href', ''),
                        'timestamp': pd.to_datetime(item['string_map_data'].get('Saved on', {}).get('timestamp', 0), unit='s'),
                        'category': key,
                        'file_name': 'saved_posts.json'
                    })
                elif key == 'likes_media_likes':
                    for like_data in item.get('string_list_data', []):
                        flat_instagram_data.append({
                            'title': item.get('title', 'No Title'),
                            'href': like_data.get('href', ''),
                            'timestamp': pd.to_datetime(like_data.get('timestamp', 0), unit='s'),
                            'category': key,
                            'file_name': 'liked_posts.json'
                        })
                elif key == 'impressions_history_posts_seen':
                    flat_instagram_data.append({
                        'title': item['string_map_data'].get('Author', {}).get('value', 'Unknown'),
                        'href': 'N/A',
                        'timestamp': pd.to_datetime(item['string_map_data'].get('Time', {}).get('timestamp', 0), unit='s'),
                        'category': key,
                        'file_name': 'posts_viewed.json'
                    })
                elif key == 'impressions_history_chaining_seen':
                    flat_instagram_data.append({
                        'title': item['string_map_data'].get('Username', {}).get('value', 'Unknown'),
                        'href': 'N/A',
                        'timestamp': pd.to_datetime(item['string_map_data'].get('Time', {}).get('timestamp', 0), unit='s'),
                        'category': key,
                        'file_name': 'suggested_accounts_viewed.json'
                    })
                elif key == 'impressions_history_videos_watched':
                    flat_instagram_data.append({
                        'title': item['string_map_data'].get('Author', {}).get('value', 'Unknown'),
                        'href': 'N/A',
                        'timestamp': pd.to_datetime(item['string_map_data'].get('Time', {}).get('timestamp', 0), unit='s'),
                        'category': key,
                        'file_name': 'videos_watched.json'
                    })

    return pd.DataFrame(flat_instagram_data)

def parse_instagram_files(contents_list, selected_sections):
    """
    Main function to parse the uploaded JSON files and return a merged DataFrame.
    
    :param contents_list: List of base64 encoded strings from uploaded files
    :param selected_sections: List of strings representing sections to process
    :return: DataFrame with processed data
    """
    all_data = pd.DataFrame()
    for contents in contents_list:
        data = parse_instagram_contents(contents)
        flat_instagram_data = flatten_instagram_data(data)
        if not flat_instagram_data.empty:
            filtered_data = flat_instagram_data[flat_instagram_data['file_name'].isin(selected_sections)]
            all_data = pd.concat([all_data, filtered_data], ignore_index=True)
    if not all_data.empty:
        return all_data
    else:
        raise ValueError("No relevant data found in the selected sections.")
    
def create_engagement_graph(df):
    """
    Create a bar chart of the most engaged titles per year.
    
    :param df: DataFrame containing the Instagram data
    :return: Plotly Figure
    """
    # Ensure the timestamp column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Aggregate engagement data by year and title
    engagement_summary = df.groupby([df['timestamp'].dt.year, 'title']).size().reset_index(name='engagement_count')
    
    # Get top 10 titles per year
    top_titles_per_year = engagement_summary.sort_values(['timestamp', 'engagement_count'], ascending=[True, False]) \
                                            .groupby('timestamp').head(10)

    fig = px.bar(top_titles_per_year, x='timestamp', y='engagement_count', color='title', 
                 title='Most Engaged Titles Per Year',
                 labels={'timestamp': 'Year', 'engagement_count': 'Engagement Count', 'title': 'Title'})
    
    # Update layout for better appearance
    fig.update_layout({
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {
            'color': '#2c3e50',
            'family': "Arial, Helvetica, sans-serif",
        },
        'title': {
            'x': 0.5,
            'xanchor': 'center'
        }
    })
    
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

def create_download_buttons():
    return [html.Button("Download CSV", id="btn-download-csv", className="download-btn")]

def create_visualization(df):
    return dcc.Graph(figure=create_engagement_graph(df))
