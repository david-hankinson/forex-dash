# app.py
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import requests

# Fetch data
def fetch_exchange_rate():
    url = 'https://api.exchangerate-api.com/v4/latest/GBP'
    response = requests.get(url)
    data = response.json()
    exchange_rate = data['rates']['CAD']
    return exchange_rate

# Create Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("GBP to CAD Exchange Rate"),
    dcc.Graph(id='exchange-rate-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # Update every minute
        n_intervals=0
    )
])

# Initialize data
exchange_rate_data = {'time': [], 'rate': []}

# Update graph with exchange rate data
@app.callback(
    Output('exchange-rate-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    exchange_rate = fetch_exchange_rate()
    exchange_rate_data['time'].append(pd.Timestamp.now())
    exchange_rate_data['rate'].append(exchange_rate)
    
    # Keep only the 10 most recent minutes
    recent_data = exchange_rate_data.copy()
    recent_data['time'] = recent_data['time'][-10:]
    recent_data['rate'] = recent_data['rate'][-10:]
    
    return {
        'data': [go.Scatter(x=recent_data['time'], y=recent_data['rate'], mode='lines+markers')],
        'layout': go.Layout(
            title='GBP to CAD Exchange Rate',
            xaxis=dict(title='Time (minutes)', tickformat='%H:%M', tickangle=45),
            yaxis=dict(title='Exchange Rate (CAD per GBP)'),
            showlegend=False,
            font=dict(family="Arial, sans-serif", size=14, color="#7f7f7f")
        )
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
