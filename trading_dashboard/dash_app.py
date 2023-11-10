from dash import Dash, html, dcc, ctx
from dash import dash_table as dt
#import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template
from alpaca_calls import *
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


external_stylesheets = [dbc.themes.LUX]
template1 = load_figure_template('LUX')


app = Dash(__name__, external_stylesheets=external_stylesheets)

card_historical_bal = dbc.Card(
    dbc.CardBody(
        [   
            html.H3("Current Balance: "),
            dbc.Row([
                dbc.Col(
                    html.H3(id='live-bal',children=[],       
                            style={
                                "text-align": "right",
                                "width": "40.5rem",},
                ),
                ),
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                            id='indicator-graph',
                            figure={},
                            config={'displayModeBar':False},
                            style={"bottom": "80rem",}
                            ),
                            ]),
                )
            ]),
            html.Div(
                [
                dcc.Graph(
                id='balance-graph',
                figure={},
                config={'displayModeBar':False},
                style = template1
                    )
                ]
            ),
        ],
    ),
    className="text-center m-1",
    style={"border-radius": "5px",
    "padding": "1rem 1rem",
    },
    
)


card_tranx_history = dbc.Card(
    dbc.CardBody(
        [
            html.H1([html.I(className="bi bi-bank me-1"), "Transaction History"], className="text-nowrap"),
            html.Hr(),
            html.Div(id='tranx_tbl')
        ], #className="border-start border-primary border-5"
    ),
    className="text-center m-1",
    style={"border-radius": "5px",
    "padding": "1rem 1rem",}
    
)


card_portfolio_alloc = dbc.Card(
    dbc.CardBody(
        [
            html.H1([html.I(className="bi bi-cart me-1"), "Asset Allocation"], className="text-nowrap"),
            html.Hr(),
            html.Div(
                [
                dcc.Graph(
                id='aa_pie',
                figure={},
                config={'displayModeBar':False},
                style =  {'width': '275x', 'height': '272px'}
                    )
                ]
            ),
        ], # className="border-start border-primary border-5"
    ),
    className="text-center m-1",
    style={"border-radius": "5px",
    "padding": "1rem 1rem",}
)




# the styles for the main content position it to the right of the sidebar and
# add some padding.
sidebar = html.Div(
    [
        html.H4(["Order Entry",html.I(className="bi bi-bank me-1")]),
        html.Hr(),
        html.Div([
            html.H5(["Cash Available:",html.I(className="bi bi-bank me-1")]),
            html.H5(id='live-cash',children=[],       
                            style={
                                "text-align": "left","margin-bottom": "25px"
                                },)
            ]),
        html.Div([]),
        html.Div(
                children=[
                dcc.RadioItems(
                    id="order-type",
                    options=[
                        {'label':  html.Div('BUY', style={"display": "inline", "padding-left":"0.2rem", "padding-right":"0.5rem"}), 'value': 'BUY'},
                        {'label':  html.Div('SELL', style={"display": "inline", "padding-left":"0.2rem"}), 'value': 'SELL'},
                    ],
                    value='BUY',
                    labelStyle={'display': 'inline-block'},
                ),
                dcc.Input(id="order-symbol", type="text", placeholder="Symbol", className="form-control mb-2", style={'margin-top': "25px"}),
                dcc.Input(id="order-quantity", type="number", placeholder="Quantity", className="form-control mb-2"),
                html.Div(
                    [
                        html.H6(id='live-quote')
                    ], style = {'display': 'inline-block'}
                ),
                
                ],
        ),
        html.Div([
            html.Button("Submit", id="button", n_clicks = 0, className="btn btn-primary"),
            ],style={"margin-top": "25px", 'align': 'left'}),
        html.H6([],id='ord-status',style={"margin-top": "25px", 'align': 'left'})
    ],
    style= {
        "position": "fixed",
        "top": "9.5rem",
        "right": "1rem",
        "left": "1rem",
        "bottom": "1rem",
        "width": "18rem",
        "padding": "1rem 1rem",
        "border-radius": "5px",
        },
    
)

# -----------------------------------------------------
app.layout = html.Div([

    html.H1(
        children="Drum & Co Brokers",
        className="text-center m-4",
        style={
            "padding": "20px",
            "font-size": "50px",
            "text-align": "center"
        },
    ),
    html.Div([
        dbc.Container([
            
            dbc.Row(
                [dbc.Col(card_historical_bal)],
            ),
            dbc.Row(
                [dbc.Col(card_tranx_history,), dbc.Col(card_portfolio_alloc)],
            ),
        ]),
        dbc.Container([
            dbc.Row(
                [dbc.Col(sidebar)],
            ),
        ]),
    ]),
    dcc.Interval(id='update', n_intervals=0, interval=1000*5)
])

# -------------------------------------
@app.callback(
    Output('indicator-graph', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    bals_df = getHistoricalBalances()
    day_start = bals_df.iloc[len(bals_df)-2]['balance']
    day_end = bals_df.iloc[len(bals_df)-1]['balance']

    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':20})
    fig.update_layout(height=25, width=120)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')

    return fig

@app.callback(
    Output('balance-graph', 'figure'),
    Output('live-bal', 'children'),   
    Input('update', 'n_intervals')
)

def update_bals_chart(timer):
    bals_df = getHistoricalBalances()

    fig = px.line(bals_df, x='date', y='balance',
                   range_y=[bals_df['balance'].min(), bals_df['balance'].max()],
                   height=240).update_layout(margin=dict(t=10, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))

    day_start = bals_df.iloc[len(bals_df)-2]['balance']
    day_end = bals_df.iloc[len(bals_df)-1]['balance']

    live_bal = '${:,.2f}'.format(bals_df.iloc[len(bals_df)-1]['balance'])

    if day_end >= day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'}), live_bal
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',line={'color': 'red'}), live_bal
    
    
    return fig, live_bal

@app.callback(
    Output('tranx_tbl', 'children'),
    Input('update', 'n_intervals')
)
def update_tranx_tbl(timer):
    tx_df = getTransactionHistory()

    data = tx_df.to_dict('records')[:8]
    columns =  [{"name": i, "id": i,} for i in (tx_df.columns)]

    return dt.DataTable(
        data=data, columns=columns,style_cell={'textAlign': 'left'},style_as_list_view=True,
        style_header={'fontWeight': 'bold'},
        )

@app.callback(
    Output(component_id='aa_pie', component_property='figure'),
    Input('update', 'n_intervals')
)

def update_aa(timer):
    dff, assetvalue = getHoldings()
    fig = go.Figure()
    # Add a pie chart trace

    fig.add_trace(
    go.Pie(
        labels=dff['Ticker'],
        values=dff['Value']
    ))

    fig.update_layout(showlegend=False),
    fig.update_layout(margin=dict(t=0, r=0, l=0, b=0)),
    fig.update_traces(textinfo='label + percent')
    return fig

@app.callback(
    Output('live-cash', 'children'),
    Input('update', 'n_intervals')
)
def cash_avail(timer):
    cash_available = get_cash()
    
    return'${:,.2f}'.format(cash_available)

@app.callback(
    Output('live-quote', 'children'),
    Input('order-symbol', 'value'),
    Input('order-type', 'value'),
)
def getQuote(ticker,side):
    if ticker == None:
        return 'Current Price: '
    else:
        ticker = ticker.upper()
        live_price = get_live_price(ticker,side)
        if live_price == "Ticker Invalid":
            return live_price
        else:
            return 'Current Price: {:,.2f}'.format(live_price)
    
@app.callback(
    Output("ord-status", "children"),
    Input("button", "n_clicks"),
    State("order-type", "value"),
    State("order-symbol","value"),
    State("order-quantity","value"),
    )

def place_order(_, order_type, symbol, qty):
    if _ != 0:
        button_clicked = ctx.triggered_id
        if button_clicked == "button":
            
            if order_type == 'BUY':
                isBuySide = True
            else:
                isBuySide = False
            order(isBuySide, qty, symbol)

            return "Order Submitted ✓"
        

if __name__ == "__main__":
    app.run_server(debug=False)