import plotly.express as px
import pandas as pd

def create_video_history_graph(tiktok_df):
    # Assuming tiktok_df has a 'Date' column in datetime format and a 'Source' column
    
    # Group data by month and source, count entries
    links_per_month = tiktok_df.groupby(tiktok_df['Date'].dt.to_period('M')).size().reset_index(name='counts')
    links_per_month['year_month'] = links_per_month['Date'].astype(str)

    category_counts_per_date = tiktok_df.groupby([tiktok_df['Date'].dt.to_period('M'), 'Source']).size().unstack(fill_value=0)
    category_counts_per_date = category_counts_per_date.reset_index()
    category_counts_per_date['Date'] = category_counts_per_date['Date'].astype(str)

    # Create a stacked bar chart
    fig = px.bar(category_counts_per_date, x='Date', y=['Browsing', 'Favorite', 'Liked'],
                 title="Watched Videos per Month",
                 labels={'value': 'Number of Videos', 'variable': 'Source'},
                 barmode='stack')
    
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

    # Customize axes
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')

    return fig