from dash import Dash, html, dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import requests
import json


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.title = "My Crypto App"
app.description = "This is my crypto app"

app.layout = html.Div(children=[
    html.Link(rel='shortcut icon', type='favicon.ico', href="assets/btc.png"),
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('btc.png'), id="ads-img", style={
                'height': '60px',
                'width': 'auto',
                'margin-bottom': '25px'
            })
        ], className='one-third column'),
        html.Div([
            html.Div([
                html.H1("Crypto App", style={'margin-bottom': '0px', 'color': 'orange',
                                             'text-align': 'center', 'font-weight': 'bold'}),
                html.H5("CryptoCurrency Prices", style={'margin-bottom': '0px', 'color': 'orange',
                                                        'text-align': 'center', 'font-weight': 'bold'})
            ])
        ], className="one-third column", id='title')
    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),

    # ------------------ START DROPDOWN SECTION ---------------------------#

    html.Div([
        # ------ Crypto Selection Start-------- #
        html.Div([
            html.Label('Crypto Asset', style={'color': 'Orange', 'margin-bottom': '5px'}),
            dcc.Dropdown(
                id='coin',
                options=[
                    {'label': 'Bitcoin', 'value': 'BTC'},
                    {'label': 'Ethereum', 'value': 'ETH'},
                    {'label': 'Bitcoin Cash', 'value': 'BCH'},
                    {'label': 'Litecoin', 'value': 'LTC'}
                ],
                value='BTC'
            )
        ], className='card_container three columns'),
        # ------ Crypto Selection End -------- #
        # ------ Time Period Selection Start-------- #
        html.Div([
            html.Label('Time', style={'color': 'Orange', 'margin-bottom': '5px'}),
            dcc.Dropdown(
                id='time',
                options=[
                    {'label': 'Minute', 'value': '1MIN'},
                    {'label': 'Day', 'value': '10DAY'},
                    {'label': 'Month', 'value': '3MTH'},
                    {'label': 'Year', 'value': '1YRS'}
                ],
                value='10DAY'
            )
        ], className='card_container three columns')
        # ------ Time Period Selection End-------- #
    ], className="row flex display"),

    # ------------------ END DROPDOWN SECTION -----------------------------#

    # ----------------- PRICES START --------------------------------------#
    html.Div([
        # ------- Opening ------#
        html.Div([
            html.H6(
                children='Price Open',
                style={'textAlign': 'center',
                       'color': '#ffffff',
                       }
            ),
            html.P(
                id='price_open',
                style={'textAlign': 'center',
                       'color': 'Orange',
                       'fontSize': 40
                       }
            )
        ], className='card_container three columns'),

        # ------- Closing ------#
        html.Div([
            html.H6(
                children='Price Close',
                style={'textAlign': 'center',
                       'color': '#ffffff',
                       }
            ),
            html.P(
                id='price_close',
                style={'textAlign': 'center',
                       'color': 'Orange',
                       'fontSize': 40
                       }
            )
        ], className='card_container three columns'),

        # ------- Price High ------#

        html.Div([
            html.H6(
                children='Price High',
                style={'textAlign': 'center',
                       'color': '#ffffff',
                       }
            ),
            html.P(
                id='price_high',
                style={'textAlign': 'center',
                       'color': 'Orange',
                       'fontSize': 40
                       }
            )
        ], className='card_container three columns'),

        # ------- Volume ------#

        html.Div([
            html.H6(
                children='Volume Traded',
                style={'textAlign': 'center',
                       'color': '#ffffff',
                       }
            ),
            html.P(
                id='volume_traded',
                style={'textAlign': 'center',
                       'color': 'Orange',
                       'fontSize': 40
                       }
            )
        ], className='card_container three columns')
    ], className='row flex display'),
    # ----------------- PRICES END ----------------------------------------#

    # ----------------- GRAPH START ---------------------------------------#
    html.Div([
        html.Div([
            dcc.Graph(
                id='graph', config={'displayModeBar': False}
            ),
        ], className='card_container twelve columns')
    ], className='row flex display')
    # ----------------- GRAPH END -----------------------------------------#
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'}
)


# Callbacks
@app.callback(
    [
        Output(component_id='price_open', component_property='children'),
        Output(component_id='price_close', component_property='children'),
        Output(component_id='price_high', component_property='children'),
        Output(component_id='volume_traded', component_property='children'),
        Output(component_id='graph', component_property='figure')
    ],
    [
        Input(component_id='coin', component_property='value'),
        Input(component_id='time', component_property='value')
    ]
)
def update_content(currency, time_change):
    """This function fetches the data from the coin API and returns the prices, volumes and the graph"""
    with open('./coin_api_key.json') as file:
        apikey = json.load(file).get('key')
    url = f"https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}"
    header = {'X-CoinAPI-KEY': apikey}
    response = requests.get(url, headers=header)
    data = response.json()
    df = pd.DataFrame(data)
    # Price Open
    price_open = df['price_open'][0]
    # Price Close
    price_close = df['price_close'][0]
    # Price High
    price_high = df['price_high'][0]
    # Volume
    volume_traded = round(df['volume_traded'][0], 2)

    # GRAPH
    fig = go.Figure(data=[go.Candlestick(x=df.time_period_start,
                                         open=df.price_open,
                                         high=df.price_high,
                                         low=df.price_low,
                                         close=df.price_close,
                                         text=currency)],
                    )

    fig.update_layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                      template='plotly_dark',
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      margin={'b': 15},
                      hovermode='x',
                      autosize=True,
                      title={'text': 'Cryptocurrency Prices', 'font': {'color': 'white'}, 'x': 0.5}, )
    return price_open, price_close, price_high, volume_traded, fig


if __name__ == "__main__":
    app.run_server()
