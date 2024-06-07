import base64
import json
import pandas as pd
import plotly.express as px
from dash import html, dash_table, dcc

def parse_youtube_contents(contents):
    # Ensure contents is a single string, if it's a list, get the first element
    if isinstance(contents, list):
        contents = contents[0]
        
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    data = json.loads(decoded.decode('utf-8'))  # Decode to string before JSON parsing

    all_videos = []

    # Extract watch history from the uploaded file
    watch_history = data if isinstance(data, list) else data.get('watch-history', [])
    for video in watch_history:
        video_details = {
            'Title': video.get('title', 'No Title'),
            'Link': video.get('titleUrl', 'No URL'),
            'Date': pd.to_datetime(video.get('time', 'No Date')),  # Convert timestamp to datetime
            'Channel Name': video.get('subtitles', [{}])[0].get('name', 'No Channel Name'),
            'Channel URL': video.get('subtitles', [{}])[0].get('url', 'No Channel URL')
        }
        all_videos.append(video_details)

    if all_videos:
        youtube_df = pd.DataFrame(all_videos)
        return youtube_df
    else:
        raise ValueError("No relevant data found in the selected sections.")

def create_watch_history_graph(df):
    """
    Create a visually appealing and insightful bar chart of the most watched channels per year.
    :param df: DataFrame containing the YouTube data
    :return: Plotly Figure
    """
    # Filter out rows with 'No Channel Name'
    df = df[df['Channel Name'] != 'No Channel Name']
    
    # Aggregate watch data by year and channel name
    df['Year'] = df['Date'].dt.year
    watch_summary = df.groupby(['Year', 'Channel Name']).size().reset_index(name='Watch Count')
    
    # Get top 10 channels per year
    top_channels_per_year = watch_summary.sort_values(['Year', 'Watch Count'], ascending=[True, False]) \
        .groupby('Year').head(10)

    # Create the bar chart
    fig = px.bar(top_channels_per_year, x='Year', y='Watch Count', color='Channel Name',
                 title='Top 10 Most Watched Channels Per Year',
                 labels={'Year': 'Year', 'Watch Count': 'Watch Count', 'Channel Name': 'Channel Name'},
                 color_discrete_sequence=px.colors.qualitative.Plotly)

    # Update layout for better appearance and insights
    fig.update_layout({
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {
            'color': '#2c3e50',
            'family': "Arial, Helvetica, sans-serif",
        },
        'title': {
            'text': 'Top 10 Most Watched Channels Per Year',
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 24,
                'color': '#2c3e50',
                'family': "Arial, Helvetica, sans-serif",
            }
        },
        'xaxis': {
            'title': 'Year',
            'showgrid': False,
            'linecolor': '#2c3e50',
            'tickfont': {'size': 12, 'family': "Arial, Helvetica, sans-serif"},
            'tickangle': 0,
            'dtick': 1,  # Set tick interval to 1 year
        },
        'yaxis': {
            'title': 'Watch Count',
            'showgrid': True,
            'gridcolor': '#e5e5e5',
            'linecolor': '#2c3e50',
            'tickfont': {'size': 12, 'family': "Arial, Helvetica, sans-serif"},
            'range': [0, 1.2 * top_channels_per_year['Watch Count'].max()],  # Set y-axis range
        },
        'legend': {
            'title': 'Channel Name',
            'font': {'size': 12, 'family': "Arial, Helvetica, sans-serif"},
            'orientation': 'v',
            'yanchor': 'top',
            'y': 1,
            'xanchor': 'left',
            'x': 1.05
        },
        'hoverlabel': {
            'font': {'size': 12, 'family': "Arial, Helvetica, sans-serif"},
        },
        'margin': {'l': 80, 'r': 80, 't': 60, 'b': 60},  # Adjust margins for better spacing
        'width': 1000,  # Set the width of the graph
        'height': 600,  # Set the height of the graph
    })

    return fig

def create_description():
    return html.P(
        "Upload successful! 🎉 The table below displays the first rows of your YouTube watch history data. "
        "It includes the video titles, links, watch dates, channel names, and channel URLs. "
        "You can download the complete dataset as a CSV file or extract the video URLs for further analysis with 4CAT. "
        "Additionally, a visualization will show the number of videos watched per month. Enjoy exploring your data!",
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

def create_visualization(df):
    return dcc.Graph(figure=create_watch_history_graph(df))
