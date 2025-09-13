import os
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # For deployment

# Load and prepare data
data_url = 'https://raw.githubusercontent.com/mknomics/teaching_intro_price_optimization/refs/heads/main/soda.csv'
df = pd.read_csv(data_url)
df['date'] = pd.to_datetime(df['date'])

# Process data
df_mean_Q = df.groupby(['brand','container','city','date'])['quantity'].mean().reset_index()
df_mean_P = df.groupby(['brand','container','city','date'])['price'].mean().reset_index()
df_city = pd.merge(df_mean_Q, df_mean_P)
df_city.rename(columns={'quantity': 'mean_q', 'price': 'mean_p'}, inplace=True)
df_city = df_city.pivot(index='date', columns=['city','brand','container'], values=['mean_q','mean_p'])

# Available options
brands = ['adult-cola', 'gazoza', 'kinder-cola', 'lemon-boost', 'orange-power']
containers = ['plastic', 'can', 'glass']

# App layout
app.layout = html.Div([
    html.Div([
        html.H1('Elasticity Analysis Tool', style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.P('Athens Soda Market Data Analysis', style={'textAlign': 'center', 'fontSize': '18px', 'color': '#7f8c8d'}),
        html.Hr()
    ]),

    # Main content with two columns
    html.Div([
        # Left column - Own Price Elasticity
        html.Div([
            html.H3('Own-Price Elasticity Analysis', style={'color': '#3498db'}),
            html.Div([
                html.Label('Select Brand:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='own-brand-dropdown',
                    options=[{'label': b, 'value': b} for b in brands],
                    value='adult-cola',
                    style={'marginBottom': '10px'}
                ),

                html.Label('Select Container:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='own-container-dropdown',
                    options=[{'label': c, 'value': c} for c in containers],
                    value='plastic',
                    style={'marginBottom': '10px'}
                ),

                html.Label('Price Point:', style={'fontWeight': 'bold'}),
                dcc.Slider(
                    id='own-price-slider',
                    min=0.5,
                    max=5.0,
                    value=2.0,
                    step=0.1,
                    marks={i: f'${i}' for i in range(1, 6)},
                    tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                html.Br(),
                html.Button('Calculate Own-Price Elasticity',
                           id='own-elasticity-button',
                           style={'width': '100%', 'padding': '10px',
                                 'backgroundColor': '#3498db', 'color': 'white',
                                 'border': 'none', 'borderRadius': '5px',
                                 'fontSize': '16px', 'cursor': 'pointer'}),

                html.Div(id='own-elasticity-output', style={'marginTop': '20px'}),
                dcc.Graph(id='own-price-graph', style={'marginTop': '20px'})
            ])
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top',
                  'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),

        # Right column - Cross Price Elasticity
        html.Div([
            html.H3('Cross-Price Elasticity Analysis', style={'color': '#e74c3c'}),
            html.Div([
                html.Label('Product 1 (Demand):', style={'fontWeight': 'bold', 'color': '#2c3e50'}),
                dcc.Dropdown(
                    id='cross-brand1-dropdown',
                    options=[{'label': b, 'value': b} for b in brands],
                    value='adult-cola',
                    style={'marginBottom': '5px'}
                ),
                dcc.Dropdown(
                    id='cross-container1-dropdown',
                    options=[{'label': c, 'value': c} for c in containers],
                    value='plastic',
                    style={'marginBottom': '15px'}
                ),

                html.Label('Product 2 (Price Change):', style={'fontWeight': 'bold', 'color': '#2c3e50'}),
                dcc.Dropdown(
                    id='cross-brand2-dropdown',
                    options=[{'label': b, 'value': b} for b in brands],
                    value='gazoza',
                    style={'marginBottom': '5px'}
                ),
                dcc.Dropdown(
                    id='cross-container2-dropdown',
                    options=[{'label': c, 'value': c} for c in containers],
                    value='plastic',
                    style={'marginBottom': '10px'}
                ),

                html.Label('Price Point for Product 2:', style={'fontWeight': 'bold'}),
                dcc.Slider(
                    id='cross-price-slider',
                    min=0.5,
                    max=5.0,
                    value=2.0,
                    step=0.1,
                    marks={i: f'${i}' for i in range(1, 6)},
                    tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                html.Br(),
                html.Button('Calculate Cross-Price Elasticity',
                           id='cross-elasticity-button',
                           style={'width': '100%', 'padding': '10px',
                                 'backgroundColor': '#e74c3c', 'color': 'white',
                                 'border': 'none', 'borderRadius': '5px',
                                 'fontSize': '16px', 'cursor': 'pointer'}),

                html.Div(id='cross-elasticity-output', style={'marginTop': '20px'}),
                dcc.Graph(id='cross-price-graph', style={'marginTop': '20px'})
            ])
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top',
                  'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px',
                  'marginLeft': '2%'})
    ]),

    # Data preview section
    html.Div([
        html.H3('Data Preview', style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.Div(id='data-preview', style={'overflowX': 'auto'})
    ], style={'marginTop': '40px', 'padding': '20px', 'backgroundColor': '#f8f9fa',
              'borderRadius': '10px'})
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ecf0f1'})

# Callback for own-price elasticity
@app.callback(
    [Output('own-elasticity-output', 'children'),
     Output('own-price-graph', 'figure')],
    [Input('own-elasticity-button', 'n_clicks')],
    [State('own-brand-dropdown', 'value'),
     State('own-container-dropdown', 'value'),
     State('own-price-slider', 'value')]
)
def calculate_own_price_elasticity(n_clicks, brand, container, price_point):
    if n_clicks is None:
        return '', go.Figure()

    try:
        Qx = df_city['mean_q']['Athens'][brand][container].values.reshape(-1,1)
        Px = df_city['mean_p']['Athens'][brand][container].values.reshape(-1,1)

        # Calculate regression
        reg = LinearRegression().fit(Px, Qx)
        Px_plot = np.linspace(Px.min(), Px.max(), 100).reshape(-1,1)
        Qx_pred = reg.predict(Px_plot)

        # Calculate elasticity
        Q_hat = reg.predict(np.array(price_point).reshape(-1, 1))
        elasticity = reg.coef_[0][0] * (price_point / Q_hat[0][0])

        # Create plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Qx.flatten(), y=Px.flatten(),
                                 mode='markers', name='Data',
                                 marker=dict(size=10, color='blue', opacity=0.7)))
        fig.add_trace(go.Scatter(x=Qx_pred.flatten(), y=Px_plot.flatten(),
                                 mode='lines', name='Regression Line',
                                 line=dict(color='red', width=2)))
        fig.add_trace(go.Scatter(x=[Q_hat[0][0]], y=[price_point],
                                 mode='markers', name='Analysis Point',
                                 marker=dict(size=15, color='green', symbol='star')))

        fig.update_layout(
            title=f'Price vs Quantity: {brand} {container}',
            xaxis_title=f'Quantity',
            yaxis_title=f'Price ($)',
            showlegend=True,
            hovermode='closest'
        )

        # Interpretation
        if elasticity < -1:
            interpretation = 'Demand is ELASTIC (responsive to price changes)'
            color = 'green'
        elif elasticity > -1 and elasticity < 0:
            interpretation = 'Demand is INELASTIC (less responsive to price changes)'
            color = 'orange'
        else:
            interpretation = 'Unusual elasticity value - check data'
            color = 'red'

        result = html.Div([
            html.H4(f'Own-Price Elasticity: {elasticity:.3f}'),
            html.P(interpretation, style={'color': color, 'fontWeight': 'bold'}),
            html.P(f'At price ${price_point:.2f}, estimated quantity: {Q_hat[0][0]:.0f}')
        ])

        return result, fig

    except Exception as e:
        error_msg = html.Div([
            html.P(f'Error: {str(e)}', style={'color': 'red'})
        ])
        return error_msg, go.Figure()

# Callback for cross-price elasticity
@app.callback(
    [Output('cross-elasticity-output', 'children'),
     Output('cross-price-graph', 'figure')],
    [Input('cross-elasticity-button', 'n_clicks')],
    [State('cross-brand1-dropdown', 'value'),
     State('cross-container1-dropdown', 'value'),
     State('cross-brand2-dropdown', 'value'),
     State('cross-container2-dropdown', 'value'),
     State('cross-price-slider', 'value')]
)
def calculate_cross_price_elasticity(n_clicks, brand1, container1, brand2, container2, price_point):
    if n_clicks is None:
        return '', go.Figure()

    try:
        Qx = df_city['mean_q']['Athens'][brand1][container1].values.reshape(-1,1)
        Px1 = df_city['mean_p']['Athens'][brand1][container1].values.reshape(-1,1)
        Px2 = df_city['mean_p']['Athens'][brand2][container2].values.reshape(-1,1)
        Px = np.concatenate((Px1, Px2), axis=1)

        reg = LinearRegression().fit(Px, Qx)
        mPx1 = np.mean(Px1)
        P = np.array([[mPx1, price_point]])
        Q_hat = reg.predict(P)
        cross_elasticity = reg.coef_[0][1] * (price_point / Q_hat[0][0])

        # Create visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Px2.flatten(), y=Qx.flatten(),
                                 mode='markers', name=f'{brand1} Quantity vs {brand2} Price',
                                 marker=dict(size=10, color='purple', opacity=0.7)))

        # Add regression line
        Px2_plot = np.linspace(Px2.min(), Px2.max(), 100).reshape(-1,1)
        Px_pred = np.column_stack([np.full(100, mPx1), Px2_plot])
        Qx_pred = reg.predict(Px_pred)

        fig.add_trace(go.Scatter(x=Px2_plot.flatten(), y=Qx_pred.flatten(),
                                 mode='lines', name='Regression Line',
                                 line=dict(color='orange', width=2)))

        fig.update_layout(
            title=f'Cross-Price Relationship: {brand2} Price Effect on {brand1} Demand',
            xaxis_title=f'{brand2} Price ($)',
            yaxis_title=f'{brand1} Quantity',
            showlegend=True,
            hovermode='closest'
        )

        # Interpretation
        if cross_elasticity > 0.1:
            interpretation = 'Products are SUBSTITUTES (price increase of one increases demand for other)'
            color = 'blue'
        elif cross_elasticity < -0.1:
            interpretation = 'Products are COMPLEMENTS (price increase of one decreases demand for other)'
            color = 'green'
        else:
            interpretation = 'Products are relatively INDEPENDENT (minimal cross-price effect)'
            color = 'gray'

        result = html.Div([
            html.H4(f'Cross-Price Elasticity: {cross_elasticity:.3f}'),
            html.P(interpretation, style={'color': color, 'fontWeight': 'bold'}),
            html.P(f'{brand2} price effect on {brand1} demand at ${price_point:.2f}')
        ])

        return result, fig

    except Exception as e:
        error_msg = html.Div([
            html.P(f'Error: {str(e)}', style={'color': 'red'})
        ])
        return error_msg, go.Figure()

# Callback for data preview
@app.callback(
    Output('data-preview', 'children'),
    [Input('own-brand-dropdown', 'value')]  # Triggers on page load
)
def update_data_preview(brand):
    sample_data = df[['date', 'brand', 'container', 'price', 'quantity']].head(10)

    return html.Table([
        html.Thead([
            html.Tr([html.Th(col) for col in sample_data.columns])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(sample_data.iloc[i][col]) for col in sample_data.columns
            ]) for i in range(len(sample_data))
        ])
    ], style={'width': '100%', 'textAlign': 'center'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False)