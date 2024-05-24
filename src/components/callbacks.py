import logging
from dash import Output, Input, State, html, dcc, dash_table
from dash.dependencies import ALL
from dash.exceptions import PreventUpdate
from app import app
import pandas as pd
from src.components.data.insta_processing import parse_json, create_engagement_graph
from src.components.data.tiktok_processing import parse_tiktok_contents, extract_urls_for_4cat, create_video_history_graph

# Global dataframe to store uploaded data
df = pd.DataFrame()

def register_callbacks():
    @app.callback(
        [Output('output-data-upload', 'children'),
         Output('download-container', 'children'),
         Output('visualization-container', 'children')],
        [Input({'type': 'upload-data', 'platform': ALL}, 'contents')],
        [State({'type': 'upload-data', 'platform': ALL}, 'filename')]
    )
    def update_output(all_contents, all_filenames):
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
                    if 'tiktok' in filename.lower() or 'user_data.json' in filename.lower():
                        logging.info("Processing TikTok data")
                        df = parse_tiktok_contents(content, ['video_history', 'favorite_video', 'item_favorite'])
                        logging.debug(f"Parsed TikTok DataFrame: {df.head()}")
                        if not df.empty:
                            description = html.P(
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
                            children.append(description)
                            children.append(html.Div([
                                html.H5(filename),
                                dash_table.DataTable(
                                    data=df.head(10).to_dict('records'),  # Show only first 10 rows
                                    columns=[{'name': i, 'id': i} for i in df.columns],
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif', 'padding': '10px'},
                                    style_header={
                                        'backgroundColor': '#F3F4F6',
                                        'fontWeight': 'bold'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': '#F9FAFB'
                                        }
                                    ]
                                )
                            ], className='table-container'))
                            download_buttons = [
                                html.Button("Download CSV", id="btn-download-csv", className="download-btn"),
                                html.Button("Download URLs for 4CAT", id="btn-download-urls", className="download-btn")
                            ]
                            fig = create_video_history_graph(df)
                            logging.debug("Created TikTok visualization figure")
                            visualization = dcc.Graph(figure=fig)
                        else:
                            children.append(html.Div(f"No TikTok data found in the file {filename}.", className="error-message"))
                    elif any(keyword in filename.lower() for keyword in ['saved_posts', 'liked_posts', 'posts_viewed', 'suggested_accounts_viewed', 'videos_watched']):
                        logging.info("Processing Instagram data")
                        contents_list = contents if isinstance(contents, list) else [contents]
                        df = parse_json(contents_list, ['saved_posts.json', 'liked_posts.json', 'posts_viewed.json', 'suggested_accounts_viewed.json', 'videos_watched.json'])
                        logging.debug(f"Parsed Instagram DataFrame: {df.head()}")
                        if not df.empty:
                            description = html.P(
                                "Upload successful! 🎉 The table below displays the first rows of your Instagram data. "
                                "You can download the complete dataset as a CSV file.",
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
                            children.append(description)
                            children.append(html.Div([
                                html.H5(filename),
                                dash_table.DataTable(
                                    data=df.head(10).to_dict('records'),  # Show only first 10 rows
                                    columns=[{'name': i, 'id': i} for i in df.columns],
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'textAlign': 'left', 'fontFamily': 'Arial, sans-serif', 'padding': '10px'},
                                    style_header={
                                        'backgroundColor': '#F3F4F6',
                                        'fontWeight': 'bold'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': '#F9FAFB'
                                        }
                                    ]
                                )
                            ], className='table-container'))
                            download_buttons = [
                                html.Button("Download CSV", id="btn-download-csv", className="download-btn"),
                            ]
                            fig = create_engagement_graph(df)
                            logging.debug("Created Instagram visualization figure")
                            visualization = dcc.Graph(figure=fig)
                        else:
                            children.append(html.Div(f"No Instagram data found in the file {filename}.", className="error-message"))
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
            )
        ])
        
        description = None
        if selected_platform == 'instagram':
            description = html.P(
                "You can upload the following files for Instagram: saved_posts.json, liked_posts.json, posts_viewed.json, suggested_accounts_viewed.json, videos_watched.json.",
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
        elif selected_platform == 'tiktok':
            description = html.P(
                "You can upload the user_data.json file for TikTok.",
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