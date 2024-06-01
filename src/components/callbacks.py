import logging
import dash
from dash import Output, Input, State, html, dcc, dash_table
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
from app import app
import pandas as pd

from src.components.data.insta_processing import (
    parse_json, create_engagement_graph,
    create_description as create_insta_description,
    create_data_table as create_insta_data_table,
    create_download_buttons as create_insta_download_buttons,
    create_visualization as create_insta_visualization
)
from src.components.data.tiktok_processing import (
    parse_tiktok_contents, extract_urls_for_4cat, create_video_history_graph,
    create_description as create_tiktok_description,
    create_data_table as create_tiktok_data_table,
    create_download_buttons as create_tiktok_download_buttons,
    create_visualization as create_tiktok_visualization
)
from src.components.data.youtube_processing import (
    parse_youtube_contents, create_watch_history_graph,
    create_description as create_youtube_description,
    create_data_table as create_youtube_data_table,
    create_download_buttons as create_youtube_download_buttons,
    create_visualization as create_youtube_visualization
)

# Global dataframe to store uploaded data
df = pd.DataFrame()

def process_data(contents, platform):
    if platform == 'tiktok':
        return parse_tiktok_contents(contents), 'tiktok'
    elif platform == 'instagram':
        return parse_json(contents, ['saved_posts.json', 'liked_posts.json', 'posts_viewed.json', 'suggested_accounts_viewed.json', 'videos_watched.json']), 'instagram'
    elif platform == 'youtube':
        return parse_youtube_contents(contents), 'youtube'
    else:
        raise ValueError("Unsupported platform")

def generate_ui_elements(df, platform):
    if df.empty:
        logging.error("DataFrame is empty.")
        return [html.Div(f"No data found.", className="error-message")], [], None

    if platform == 'tiktok':
        description = create_tiktok_description()
        data_table = create_tiktok_data_table(df)
        download_buttons = create_tiktok_download_buttons()
        visualization = create_tiktok_visualization(df)
    elif platform == 'instagram':
        description = create_insta_description()
        data_table = create_insta_data_table(df)
        download_buttons = create_insta_download_buttons()
        visualization = create_insta_visualization(df)
    elif platform == 'youtube':
        description = create_youtube_description()
        data_table = create_youtube_data_table(df)
        download_buttons = create_youtube_download_buttons()
        visualization = create_youtube_visualization(df)
    else:
        logging.error("Unsupported platform")
        return [html.Div(f"Unsupported platform.", className="error-message")], [], None

    logging.info(f"Generated UI elements for platform: {platform}")
    return [description, data_table], download_buttons, visualization

def register_callbacks(app):
    @app.callback(
        [Output('output-data-upload', 'children'),
         Output('download-container', 'children'),
         Output('visualization-container', 'children')],
        [Input({'type': 'upload-data', 'platform': ALL}, 'contents')],
        [State({'type': 'upload-data', 'platform': ALL}, 'filename'),
         State('platform-selection', 'value')]
    )
    def update_output(all_contents, all_filenames, selected_platform):
        logging.info("update_output triggered")
        if not all_contents:
            raise PreventUpdate

        children = []
        download_buttons = []
        visualization = None
        
        global df  # Use global dataframe to store the uploaded data

        for contents, filename_list in zip(all_contents, all_filenames):
            if contents and filename_list:
                filename = filename_list[0]  # Assuming one file per upload component
                content = contents[0] if isinstance(contents, list) else contents

                try:
                    df, platform = process_data(content, selected_platform)
                    ui_elements = generate_ui_elements(df, platform)
                    children.extend(ui_elements[0])
                    download_buttons.extend(ui_elements[1])
                    if ui_elements[2]:
                        visualization = ui_elements[2]
                except Exception as e:
                    logging.error(f"Error processing file {filename}: {e}")
                    children.append(html.Div([
                        html.H5(filename),
                        html.Div(f"An error occurred: {e}", className="error-message")
                    ]))

        logging.info(f"Returning children: {children}, download_buttons: {download_buttons}, visualization: {visualization}")
        return children, download_buttons, visualization

    @app.callback(
        Output('page-content', 'children'),
        Input('platform-selection', 'value')
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
            ),
        ])
        
        description = None
        if selected_platform == 'instagram':
            description = html.P(
                "You can upload the following files for Instagram: saved_posts.json, liked_posts.json, posts_viewed.json, suggested_accounts_viewed.json, videos_watched.json. You can upload one file or select multiple files at the same time.",
                style={
                    'textAlign': 'center',
                    'color': '#4B5563',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '1.1em',
                    'lineHeight': '1.6',
                    'marginTop': '20px',
                    'marginBottom': '20px'
                }
            )
        elif selected_platform is 'tiktok':
            description = html.P(
                "You can upload the user_data.json file for TikTok. The application will only extract engagement (browsing, liking, and/or favoriting) with TikTok videos (URLs) and discard any other information.",
                style={
                    'textAlign': 'center',
                    'color': '#4B5563',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '1.1em',
                    'lineHeight': '1.6',
                    'marginTop': '20px',
                    'marginBottom': '20px'
                }
            )
        elif selected_platform == 'youtube':
            description = html.P(
                "You can upload the watch-history.json file for YouTube. The application will extract your watch history data, including video titles, links, watch dates, channel names, and channel URLs.",
                style={
                    'textAlign': 'center',
                    'color': '#4B5563',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '1.1em',
                    'lineHeight': '1.6',
                    'marginTop': '20px',
                    'marginBottom': '20px'
                }
            )

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
