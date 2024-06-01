from dash import html, dcc

def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),

        html.Div(style={'height': '50px'}),

        html.H1(
            'Data Mirroring: Reflective and Reflexive Agency through Data Donations',
            style={
                'textAlign': 'center', 
                'color': '#1F2937', 
                'fontFamily': 'Arial, sans-serif', 
                'marginBottom': '20px',
                'fontSize': '2.5em',
                'fontWeight': 'bold'
            }
        ),

        html.Div(
            id='platform-description',
            children=[
                html.P([
                    "Welcome to the Data Mirroring research project, developed by Daniel Jurg, Sarah Vis, and Ike Picone at the Vrije Universiteit Brussel as part of the ", html.A("NUSE-Unit", href="https://smit.research.vub.be/en/research-areas/news-uses-strategies-engagements", target='_blank'), ". This project aims to facilitate user reflection on social media usage through data conversion and visualization. "
                    "The application transforms Data Download Packages (DDPs) provided by social media platforms like TikTok, Instagram, and YouTube into a more human-readable format. By processing a subset of the DDP, the application offers users insights into their data while ensuring the removal of sensitive personal information. Data processing occurs in real-time, guaranteeing that personal information is never stored on any server. "
                    "Data extraction within the Data Mirroring application is designed to integrate with the 4CAT: Capture and Analysis Toolkit (Peeters & Hagen, 2022), enhancing the analysis of social media data. For more information about the project, please visit our ",
                    html.A("GitHub repository", href="https://github.com/dj-urg/data-mirroring-overview", target='_blank'),
                    ". Finally, for a detailed overview on how to use this application, please follow this instruction sheet."
                ], style={
                    'textAlign': 'justify', 
                    'color': '#4B5563', 
                    'fontFamily': 'Arial, sans-serif', 
                    'fontSize': '1.1em', 
                    'lineHeight': '1.6'
                }),
            ],
            style={
                'margin': 'auto', 
                'maxWidth': '800px', 
                'padding': '30px', 
                'backgroundColor': '#F9FAFB', 
                'borderRadius': '10px', 
                'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)'
            }
        ),

        html.Div(
            [
                html.H2(
                    'Select the social media platform',
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#1F2937',
                        'marginTop': '40px'
                    }
                ),
                dcc.RadioItems(
                    id='platform-selection',
                    options=[
                        {'label': ' TikTok', 'value': 'tiktok'},
                        {'label': ' Instagram', 'value': 'instagram'},
                        {'label': ' YouTube', 'value': 'youtube'},
                    ],
                    labelStyle={'display': 'inline-block', 'margin': '10px'},
                    style={
                        'textAlign': 'center', 
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#4B5563'
                    }
                )
            ],
            style={'textAlign': 'center', 'marginBottom': '40px'}
        ),

        html.Div(id='page-content'),

        dcc.Loading(
            id="loading-spinner",
            type="circle",
            children=html.Div(
                [
                    html.Div(
                        id='output-data-upload',
                        className='table-container',
                        style={
                            'marginTop': '40px',
                            'padding': '30px',
                            'backgroundColor': '#F9FAFB',
                            'borderRadius': '10px',
                            'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',
                            'maxWidth': '800px',
                            'margin': 'auto',
                            'color': '#1F2937'
                        }
                    ),
                    html.Div(id='download-container', style={'textAlign': 'center', 'marginTop': '20px'}),
                    dcc.Download(id="download-dataframe-csv"),
                    dcc.Download(id="download-urls-txt"),
                    html.Div(id='visualization-container', style={'marginTop': '40px'})
                ]
            )
        )
    ], style={'backgroundColor': '#FFFFFF', 'color': '#1F2937', 'padding': '30px'})
