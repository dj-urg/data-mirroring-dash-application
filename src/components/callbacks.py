import logging
import dash
from dash import Output, Input, State, html, dcc, dash_table
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
import pandas as pd
from src.components.data.insta_processing import parse_instagram_files, create_engagement_graph
from src.components.data.tiktok_processing import parse_tiktok_contents, create_video_history_graph, flatten_tiktok_data
from src.components.data.youtube_processing import parse_youtube_contents, create_watch_history_graph
from src.components.data.general_utils import create_data_table, create_download_buttons, extract_urls_for_4cat
from src.components.utils.security_utils import save_temp_file, cleanup_temp_file

# Global dataframe to store uploaded data
df = pd.DataFrame()

def create_description(platform):
    descriptions = {
        'tiktok': "Upload successful! 🎉 The table below displays the first rows of your TikTok data. "
                  "It includes the dates you watched videos, the video URLs, and your engagement (browsing, favoriting, or liking). "
                  "You can download the complete dataset as a CSV file or extract the URLs for further analysis with 4CAT. "
                  "Additionally, a visualization will show the number of videos watched per month, categorized by source. Enjoy exploring your data!",
        'instagram': "Upload successful! 🎉 The table below displays the first rows of your Instagram data. "
                     "You can download the complete dataset as a CSV file.",
        'youtube': "Upload successful! 🎉 The table below displays the first rows of your YouTube watch history data. "
                   "It includes the video titles, links, watch dates, channel names, and channel URLs. "
                   "You can download the complete dataset as a CSV file or extract the video URLs for further analysis with 4CAT. "
                   "Additionally, a visualization will show the number of videos watched per month. Enjoy exploring your data!"
    }
    return html.P(descriptions[platform], style={
        'textAlign': 'justify',
        'color': '#4B5563',
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '1.1em',
        'lineHeight': '1.6',
        'marginTop': '20px',
        'marginBottom': '20px'
    })

def create_visualization(platform, df):
    if platform == 'tiktok':
        fig = create_video_history_graph(df)
    elif platform == 'instagram':
        fig = create_engagement_graph(df)
    elif platform == 'youtube':
        fig = create_watch_history_graph(df)
    return dcc.Graph(figure=fig)

def parse_contents(platform, contents_list, selected_sections=None):
    logging.debug(f"Parsing contents for platform: {platform} with selected sections: {selected_sections}")
    
    temp_files = []
    try:
        for content in contents_list:
            filename = f"{platform}_data.json"
            temp_file_path = save_temp_file(content.encode('utf-8'), filename)
            temp_files.append(temp_file_path)
            
            if platform == 'tiktok':
                if not selected_sections:
                    selected_sections = ['video_history', 'favorite_video', 'item_favorite']
                parsed_data = parse_tiktok_contents(temp_file_path)
                return flatten_tiktok_data(parsed_data, selected_sections)
            elif platform == 'instagram':
                if selected_sections is None:
                    selected_sections = ['saved_posts.json', 'liked_posts.json', 'posts_viewed.json', 'suggested_accounts_viewed.json', 'videos_watched.json']
                return parse_instagram_files([temp_file_path], selected_sections)
            elif platform == 'youtube':
                return parse_youtube_contents(temp_file_path)
            else:
                raise ValueError("Unsupported platform")
    finally:
        for temp_file in temp_files:
            cleanup_temp_file(temp_file)

    return pd.DataFrame()

def register_callbacks(app):
    @app.callback(
        [Output('output-data-upload', 'children'),
         Output('download-container', 'children'),
         Output('visualization-container', 'children')],
        [Input({'type': 'upload-data', 'platform': ALL}, 'contents')],
        [State({'type': 'upload-data', 'platform': ALL}, 'filename'),
         State({'type': 'upload-data', 'platform': ALL}, 'id')]
    )
    def update_output(all_contents, all_filenames, all_ids):
        logging.info("update_output triggered")
        if not all_contents:
            raise PreventUpdate

        children = []
        download_buttons = []
        visualization = None

        global df  # Use global dataframe to store the uploaded data

        for contents, filename_list, id in zip(all_contents, all_filenames, all_ids):
            if contents and filename_list:
                platform = id['platform']  # Extract platform from the id

                try:
                    df = parse_contents(platform, [contents])
                    logging.debug(f"Parsed {platform.capitalize()} DataFrame: {df.head()}")
                    if not df.empty:
                        children.append(create_description(platform))
                        children.append(create_data_table(df))
                        download_buttons = create_download_buttons(platform)
                        visualization = create_visualization(platform, df)
                    else:
                        children.append(html.Div(f"No {platform.capitalize()} data found in the files.", className="error-message"))
                except Exception as e:
                    logging.error(f"Error processing files {filename_list}: {e}")
                    children.append(html.Div([
                        html.H5(', '.join(filename_list)),
                        html.Div(f"An error occurred: {e}", className="error-message")
                    ]))

        logging.info(f"Returning children: {children}, download_buttons: {download_buttons}, visualization: {visualization}")
        return children, download_buttons, visualization

    @app.callback(
        Output('download-dataframe-csv', 'data'),
        Input('btn-download-csv', 'n_clicks'),
        prevent_initial_call=True
    )
    def update_page_content(selected_platform):
        logging.info("update_page_content triggered")
        if selected_platform is None:
            return html.Div(" ", className="info-message")
        upload_component = html.Div([
            dcc.Upload(
                id={'type': 'upload-data', 'platform': selected_platform},
                children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'backgroundColor': '#F9FAFB',
                    'border': '2px dashed #CBD5E1'
                },
                multiple=True
            )
        ])

        descriptions = {
            'instagram': "You can upload the following files for Instagram: saved_posts.json, liked_posts.json, posts_viewed.json, suggested_accounts_viewed.json, videos_watched.json. You can upload one file or select multiple files at the same time.",
            'tiktok': "You can upload the user_data.json file for TikTok. The application will only extract engagement (browsing, liking, and/or favoriting) with TikTok videos (URLs) and discard any other information.",
            'youtube': "You can upload the watch-history.json file for YouTube. The application will extract your watch history data, including video titles, links, watch dates, channel names, and channel URLs."
        }

        description = html.P(descriptions[selected_platform], style={
            'textAlign': 'center',
            'color': '#4B5563',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '1.1em',
            'lineHeight': '1.6',
            'marginTop': '20px',
            'marginBottom': '20px'
        })

        return html.Div([
            upload_component,
            description
        ], className="upload-container")

    @app.callback(
        Output('download-dataframe-csv', 'data'),
        Input('btn-download-csv', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_csv(n_clicks):
        logging.info("download_csv triggered")
        global df  # Access the global dataframe
        if n_clicks:
            return dcc.send_data_frame(df.to_csv, "data.csv")

    @app.callback(
        Output('download-urls-txt', 'data'),
        Input('btn-download-urls', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_urls(n_clicks):
        logging.info("download_urls triggered")
        global df  # Access the global dataframe
        if n_clicks:
            urls = extract_urls_for_4cat(df)
            return dict(content=urls, filename="urls.txt")
