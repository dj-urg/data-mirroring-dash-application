from dash import html, dcc

def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),

        html.Div(style={'height': '50px'}),

        html.H1(
            'Data Mirroring',
            style={
                'textAlign': 'center', 
                'color': '#007BFF', 
                'fontFamily': 'Arial, sans-serif', 
                'marginBottom': '20px',
                'fontSize': '3em',
                'fontWeight': 'bold'
            }
        ),

        html.Div(
            id='platform-description',
            children=[
                html.P([
                    "Welcome to the Data Mirroring website! Developed by Daniel Jurg, Sarah Vis, and Ike Picone at the University of Brussels, Data Mirroring seeks to help users reflect on their social media usage through data visualization. "
                    "This application serves as a preliminary step to transform Data Download Packages (DDPs), as provided by social media platforms like TikTok and Instagram, into a more readable form. Rather than donating entire DDPs, this application provides the user insight into what they are donating and strips any sensitive personal information out of the DDP. Your data is processed in real-time, ensuring that personal information is never stored on any server. "
                    "This platform is designed to work with the 4CAT: Capture and Analysis Toolkit, enhancing the analysis of social media data. For more information, visit our ",
                    html.A("GitHub repository", href="https://github.com/dj-urg/data-mirroring-overview", target='_blank'),
                    "."
                ], style={
                    'textAlign': 'center', 
                    'color': 'black', 
                    'fontFamily': 'Arial, sans-serif', 
                    'fontSize': '1.2em', 
                    'lineHeight': '1.6'
                }),
            ],
            style={
                'margin': 'auto', 
                'maxWidth': '800px', 
                'padding': '20px', 
                'backgroundColor': '#f9f9f9', 
                'borderRadius': '10px', 
                'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)'
            }
        ),

        html.Div(
            [
                html.H2(
                    'Select from which platform you requested your data',
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#333',
                        'marginTop': '40px'
                    }
                ),
                dcc.RadioItems(
                    id='platform-selection',
                    options=[
                        {'label': 'TikTok', 'value': 'tiktok'},
                        {'label': 'Instagram', 'value': 'instagram'},
                    ],
                    labelStyle={'display': 'inline-block', 'margin': '10px'},
                    style={
                        'textAlign': 'center', 
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#333'
                    }
                )
            ],
            style={'textAlign': 'center', 'marginBottom': '40px'}
        ),

        html.Div(id='page-content'),

        html.Div(
            id='output-data-upload',
            className='table-container',  # Apply the CSS class here
            style={
                'marginTop': '40px',
                'padding': '20px',
                'backgroundColor': '#f9f9f9',
                'borderRadius': '10px',
                'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',
                'maxWidth': '800px',
                'margin': 'auto',
                'color': 'black'
            }
        ),

        html.Div(id='download-container', style={'textAlign': 'center', 'marginTop': '20px'}),
        dcc.Download(id="download-dataframe-csv"),
        dcc.Download(id="download-urls-txt"),

        html.Div(id='visualization-container', style={'marginTop': '40px'})
    ], style={'backgroundColor': 'white', 'color': 'black', 'padding': '20px'})
