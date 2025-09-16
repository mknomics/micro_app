import os
import dash
from dash import dcc, html, Input, Output, State, ALL, callback_context
import plotly.graph_objects as go
import json

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # For deployment

# Define investment factors and their quiz questions
investment_factors = {
    'acquisition_costs': {
        'title': 'Acquisition, Maintenance, and Operating Costs',
        'description': 'These are the costs associated with purchasing, maintaining, and operating capital goods.',
        'question': 'If the cost of machinery and equipment increases significantly, what happens to the demand for investment?',
        'options': [
            {'label': 'Investment demand increases', 'value': 'increase'},
            {'label': 'Investment demand decreases', 'value': 'decrease'},
            {'label': 'Investment demand remains unchanged', 'value': 'unchanged'},
            {'label': 'Investment demand becomes unpredictable', 'value': 'unpredictable'}
        ],
        'correct': 'decrease',
        'explanation': 'When acquisition, maintenance, or operating costs increase, the expected net return on investment decreases. This makes fewer investment projects profitable at any given interest rate, shifting the investment demand curve to the left (decreasing investment demand).'
    },
    'business_taxes': {
        'title': 'Business Taxes',
        'description': 'Taxes on business profits and capital gains affect investment returns.',
        'question': 'If the government reduces corporate tax rates, what is the likely effect on investment demand?',
        'options': [
            {'label': 'Investment demand increases', 'value': 'increase'},
            {'label': 'Investment demand decreases', 'value': 'decrease'},
            {'label': 'Investment demand remains unchanged', 'value': 'unchanged'},
            {'label': 'Investment demand only changes for large corporations', 'value': 'partial'}
        ],
        'correct': 'increase',
        'explanation': 'Lower business taxes increase the after-tax returns on investment projects. This makes more investment projects profitable, shifting the investment demand curve to the right (increasing investment demand). Firms keep more of their profits, making investments more attractive.'
    },
    'technological_change': {
        'title': 'Technological Change',
        'description': 'Innovations and technological improvements affect productivity and investment opportunities.',
        'question': 'When a breakthrough technology emerges that significantly improves productivity, what happens to investment demand?',
        'options': [
            {'label': 'Investment demand increases', 'value': 'increase'},
            {'label': 'Investment demand decreases', 'value': 'decrease'},
            {'label': 'Investment demand remains unchanged', 'value': 'unchanged'},
            {'label': 'Investment demand initially decreases then increases', 'value': 'complex'}
        ],
        'correct': 'increase',
        'explanation': 'Technological advances increase the productivity of capital, raising the expected returns from investment projects. New technology often creates new investment opportunities and makes existing processes more efficient, shifting the investment demand curve to the right.'
    },
    'capital_stock': {
        'title': 'Stock of Capital Goods on Hand',
        'description': 'The existing amount of capital goods a firm already possesses.',
        'question': 'If a firm already has excess production capacity (unused machinery and equipment), what is the effect on its investment demand?',
        'options': [
            {'label': 'Investment demand increases', 'value': 'increase'},
            {'label': 'Investment demand decreases', 'value': 'decrease'},
            {'label': 'Investment demand remains unchanged', 'value': 'unchanged'},
            {'label': 'Investment demand fluctuates randomly', 'value': 'random'}
        ],
        'correct': 'decrease',
        'explanation': 'When firms have excess capacity (large stock of unused capital goods), they have less need for new investment. They can meet increased demand by utilizing existing equipment rather than purchasing new capital, reducing investment demand.'
    },
    'inventory_changes': {
        'title': 'Planned Inventory Changes',
        'description': 'Businesses adjust inventory levels based on expected future sales.',
        'question': 'If businesses expect future sales to increase and plan to build up inventories, what happens to investment demand?',
        'options': [
            {'label': 'Investment demand increases', 'value': 'increase'},
            {'label': 'Investment demand decreases', 'value': 'decrease'},
            {'label': 'Investment demand remains unchanged', 'value': 'unchanged'},
            {'label': 'Only affects retail investment demand', 'value': 'partial'}
        ],
        'correct': 'increase',
        'explanation': 'Inventory investment is a component of total investment. When firms expect higher future sales, they increase inventory levels to meet anticipated demand. This planned inventory accumulation increases investment demand.'
    },
    'expectations': {
        'title': 'Business Expectations',
        'description': 'Future profit expectations influence current investment decisions.',
        'question': 'If businesses become pessimistic about future economic conditions and profit opportunities, what happens to current investment demand?',
        'options': [
            {'label': 'Investment demand increases', 'value': 'increase'},
            {'label': 'Investment demand decreases', 'value': 'decrease'},
            {'label': 'Investment demand remains unchanged', 'value': 'unchanged'},
            {'label': 'Investment demand becomes more volatile', 'value': 'volatile'}
        ],
        'correct': 'decrease',
        'explanation': 'Investment decisions are forward-looking. Pessimistic expectations about future profits reduce the expected returns from current investments. Businesses postpone or cancel investment projects when they expect poor economic conditions, shifting investment demand to the left.'
    }
}

# App layout
app.layout = html.Div([
    # Header section matching app.py styling
    html.Div([
        html.H1('Newberry College', style={'textAlign': 'center', 'color': 'crimson', 'fontSize': '48px', 'fontWeight': 'bold', 'marginBottom': '10px'}),
        html.H1('Investment Demand Self-Test', style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.P('Test Your Understanding of Factors Affecting Investment Demand', style={'textAlign': 'center', 'fontSize': '18px', 'color': '#7f8c8d'}),
        html.Hr()
    ]),

    # Introduction section
    html.Div([
        html.Div([
            html.H3('Understanding Investment Demand', style={'color': '#3498db'}),
            html.P([
                'Investment demand represents the relationship between the real interest rate and the quantity of investment goods demanded. ',
                'The key principle is that firms compare the ', html.B('expected rate of return'),
                ' from an investment project with the ', html.B('interest rate (cost of borrowing)'), '.'
            ], style={'fontSize': '16px', 'lineHeight': '1.6'}),
            html.P([
                'If Expected Return > Interest Rate → ', html.Span('Invest', style={'color': 'green', 'fontWeight': 'bold'}),
                html.Br(),
                'If Expected Return < Interest Rate → ', html.Span('Don\'t Invest', style={'color': 'red', 'fontWeight': 'bold'})
            ], style={'fontSize': '16px', 'backgroundColor': '#f0f8ff', 'padding': '15px', 'borderRadius': '5px', 'marginTop': '10px'}),
            html.P('Test your knowledge of how various factors shift the investment demand curve:',
                   style={'fontSize': '16px', 'marginTop': '15px'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'})
    ]),

    # Progress tracker
    html.Div([
        html.H4('Your Progress:', style={'marginBottom': '10px'}),
        html.Div(id='progress-bar', style={'marginBottom': '20px'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'marginBottom': '20px'}),

    # Single question display
    html.Div([
        html.Div(id='question-display', children=[]),

        # Navigation buttons
        html.Div([
            html.Button('← Previous',
                       id='prev-button',
                       style={'padding': '10px 25px', 'backgroundColor': '#95a5a6', 'color': 'white',
                             'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                             'fontSize': '16px', 'marginRight': '15px'}),
            html.Button('Next →',
                       id='next-button',
                       style={'padding': '10px 25px', 'backgroundColor': '#3498db', 'color': 'white',
                             'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                             'fontSize': '16px', 'marginRight': '15px'}),
            html.Button('Submit Answer',
                       id='submit-current-button',
                       style={'padding': '10px 25px', 'backgroundColor': '#2ecc71', 'color': 'white',
                             'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                             'fontSize': '16px', 'marginRight': '15px'}),
            html.Button('Show Hint',
                       id='hint-current-button',
                       style={'padding': '10px 25px', 'backgroundColor': '#f39c12', 'color': 'white',
                             'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                             'fontSize': '16px'})
        ], style={'textAlign': 'center', 'marginTop': '30px'}),

        # Feedback and hint areas
        html.Div(id='current-feedback', style={'marginTop': '20px'}),
        html.Div(id='current-hint', style={'marginTop': '10px'})

    ], style={'padding': '20px', 'minHeight': '400px'}),

    # Summary section
    html.Div([
        html.H3('Summary of Results', style={'color': '#2c3e50', 'marginBottom': '20px'}),
        html.Div(id='summary-results'),
        html.Button('Reset All Answers', id='reset-button',
                   style={'marginTop': '20px', 'padding': '10px 30px', 'backgroundColor': '#e74c3c',
                         'color': 'white', 'border': 'none', 'borderRadius': '5px',
                         'cursor': 'pointer', 'fontSize': '16px'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px',
              'marginTop': '20px', 'marginBottom': '40px'}),

    # Store for tracking answers and current question
    dcc.Store(id='answer-store', data={}),
    dcc.Store(id='current-question', data=0)

], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ecf0f1'})

# Callback to display current question
@app.callback(
    [Output('question-display', 'children'),
     Output('prev-button', 'disabled'),
     Output('next-button', 'disabled'),
     Output('current-question', 'data')],
    [Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('current-question', 'data'),
     State('answer-store', 'data')]
)
def update_question_display(prev_clicks, next_clicks, reset_clicks, current_q, stored_answers):
    ctx = callback_context

    # Handle reset
    if ctx.triggered and 'reset-button' in ctx.triggered[0]['prop_id']:
        current_q = 0
    elif ctx.triggered:
        # Handle navigation
        if 'prev-button' in ctx.triggered[0]['prop_id'] and current_q > 0:
            current_q -= 1
        elif 'next-button' in ctx.triggered[0]['prop_id'] and current_q < len(investment_factors) - 1:
            current_q += 1

    # Ensure current_q is valid
    current_q = max(0, min(current_q, len(investment_factors) - 1))

    # Get current question data
    factor_keys = list(investment_factors.keys())
    factor_key = factor_keys[current_q]
    factor_data = investment_factors[factor_key]

    # Create question display
    question_content = html.Div([
        html.Div([
            html.H3(f'Question {current_q + 1} of {len(investment_factors)}',
                   style={'color': '#3498db', 'textAlign': 'center', 'marginBottom': '20px'}),
            html.H4(factor_data["title"], style={'color': '#2c3e50', 'marginBottom': '15px'}),
            html.P(factor_data['description'], style={'color': '#7f8c8d', 'fontSize': '16px', 'marginBottom': '20px', 'lineHeight': '1.6'}),
            html.P(factor_data['question'], style={'fontSize': '18px', 'fontWeight': 'bold', 'marginBottom': '20px', 'color': '#2c3e50'}),
            dcc.RadioItems(
                id='current-quiz-radio',
                options=factor_data['options'],
                value=stored_answers.get(factor_key) if stored_answers and factor_key in stored_answers and stored_answers[factor_key] not in ['correct', 'incorrect'] else None,
                style={'fontSize': '16px', 'marginBottom': '20px'},
                labelStyle={'display': 'block', 'marginBottom': '10px', 'cursor': 'pointer'}
            )
        ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '15px',
                 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)', 'maxWidth': '800px', 'margin': '0 auto'})
    ])

    # Button states
    prev_disabled = current_q == 0
    next_disabled = current_q == len(investment_factors) - 1

    return question_content, prev_disabled, next_disabled, current_q

# Callback for answer submission
@app.callback(
    [Output('current-feedback', 'children'),
     Output('answer-store', 'data'),
     Output('progress-bar', 'children'),
     Output('summary-results', 'children')],
    [Input('submit-current-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('current-quiz-radio', 'value'),
     State('current-question', 'data'),
     State('answer-store', 'data')]
)
def handle_current_answer(submit_clicks, reset_clicks, answer, current_q, stored_answers):
    ctx = callback_context

    if stored_answers is None:
        stored_answers = {}

    # Handle reset
    if ctx.triggered and 'reset-button' in ctx.triggered[0]['prop_id']:
        return [], {}, create_progress_bar({}), create_summary({})

    feedback = []

    # Handle answer submission
    if ctx.triggered and 'submit-current-button' in ctx.triggered[0]['prop_id'] and answer is not None:
        factor_keys = list(investment_factors.keys())
        factor_key = factor_keys[current_q]
        correct_answer = investment_factors[factor_key]['correct']

        if answer == correct_answer:
            stored_answers[factor_key] = 'correct'
            feedback = html.Div([
                html.P('✓ Correct!', style={'color': '#2ecc71', 'fontWeight': 'bold', 'fontSize': '24px', 'textAlign': 'center'}),
                html.P('Excellent! You understand this concept.', style={'color': '#2ecc71', 'fontSize': '18px', 'textAlign': 'center'})
            ], style={'backgroundColor': '#d5f4e6', 'padding': '20px', 'borderRadius': '10px', 'margin': '20px 0'})
        else:
            stored_answers[factor_key] = 'incorrect'
            feedback = html.Div([
                html.P('✗ Incorrect', style={'color': '#e74c3c', 'fontWeight': 'bold', 'fontSize': '24px', 'textAlign': 'center'}),
                html.Div([
                    html.P('Explanation:', style={'fontWeight': 'bold', 'color': '#e74c3c', 'marginBottom': '10px'}),
                    html.P(investment_factors[factor_key]['explanation'],
                          style={'lineHeight': '1.6', 'fontSize': '16px'})
                ])
            ], style={'backgroundColor': '#fdeaea', 'padding': '20px', 'borderRadius': '10px', 'margin': '20px 0'})

    progress_bar = create_progress_bar(stored_answers)
    summary = create_summary(stored_answers)

    return feedback, stored_answers, progress_bar, summary

# Callback for hints
@app.callback(
    Output('current-hint', 'children'),
    [Input('hint-current-button', 'n_clicks')],
    [State('current-question', 'data')]
)
def show_current_hint(hint_clicks, current_q):
    if not hint_clicks or hint_clicks == 0:
        return []

    factor_keys = list(investment_factors.keys())
    factor_key = factor_keys[current_q]

    hint_texts = {
        'acquisition_costs': 'Think about profitability: If costs go up, do profits go up or down?',
        'business_taxes': 'Consider after-tax returns: Lower taxes mean firms keep more of their profits.',
        'technological_change': 'New technology usually makes production more efficient and profitable.',
        'capital_stock': 'If you already have unused equipment, do you need to buy more?',
        'inventory_changes': 'Building inventory requires investment in goods to stock up.',
        'expectations': 'Investment is about the future - optimism or pessimism matters!'
    }

    return html.Div([
        html.P('💡 Hint:', style={'fontWeight': 'bold', 'color': '#f39c12', 'fontSize': '18px'}),
        html.P(hint_texts[factor_key], style={'color': '#f39c12', 'fontStyle': 'italic', 'fontSize': '16px'})
    ], style={'backgroundColor': '#fff3cd', 'padding': '15px', 'borderRadius': '10px', 'textAlign': 'center'})

def create_progress_bar(stored_answers):
    total = len(investment_factors)
    # Filter out click counters from stored_answers
    answer_values = {k: v for k, v in stored_answers.items() if not k.endswith('_clicks')}
    correct = sum(1 for v in answer_values.values() if v == 'correct')
    incorrect = sum(1 for v in answer_values.values() if v == 'incorrect')
    unanswered = total - correct - incorrect

    correct_pct = (correct / total) * 100
    incorrect_pct = (incorrect / total) * 100

    # Create money visualization
    money_visual = create_money_pile(correct)

    return html.Div([
        # Money pile visualization
        html.Div([
            html.H5('Your Investment Returns:', style={'color': '#2c3e50', 'marginBottom': '10px'}),
            money_visual,
            html.H3(f'Total Earned: ${correct * 100}',
                   style={'textAlign': 'center', 'color': '#27ae60', 'marginTop': '10px'})
        ], style={'marginBottom': '20px'}),

        # Original progress stats
        html.Div([
            html.Span(f'Correct: {correct}', style={'color': 'green', 'marginRight': '20px'}),
            html.Span(f'Incorrect: {incorrect}', style={'color': 'red', 'marginRight': '20px'}),
            html.Span(f'Unanswered: {unanswered}', style={'color': 'gray'})
        ]),
        html.Div([
            html.Div(style={'width': f'{correct_pct}%', 'backgroundColor': '#2ecc71',
                           'height': '20px', 'display': 'inline-block'}),
            html.Div(style={'width': f'{incorrect_pct}%', 'backgroundColor': '#e74c3c',
                           'height': '20px', 'display': 'inline-block'}),
            html.Div(style={'width': f'{(unanswered/total)*100}%', 'backgroundColor': '#95a5a6',
                           'height': '20px', 'display': 'inline-block'})
        ], style={'width': '100%', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px',
                  'overflow': 'hidden', 'marginTop': '10px'})
    ])

def create_money_pile(correct_answers):
    """Create visual stack of money that grows with correct answers"""
    if correct_answers == 0:
        return html.Div([
            html.P('💸 Start answering correctly to earn money!',
                  style={'textAlign': 'center', 'fontSize': '18px', 'color': '#95a5a6'})
        ], style={'height': '150px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})

    # Create stacked money bills
    bills = []
    for i in range(correct_answers):
        # Calculate position and styling for each bill
        bottom_position = i * 15
        left_offset = 50 + (i % 3 - 1) * 3  # Slight horizontal variation
        rotation = -3 + (i % 5) * 1.5  # Slight rotation variation

        bills.append(
            html.Div([
                html.Div('$100', style={
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': '16px'
                })
            ], style={
                'position': 'absolute',
                'bottom': f'{bottom_position}px',
                'left': f'{left_offset}%',
                'transform': f'translateX(-50%) rotate({rotation}deg)',
                'backgroundColor': '#85bb65',
                'border': '2px solid #5a7c4e',
                'borderRadius': '3px',
                'padding': '8px 20px',
                'boxShadow': '2px 2px 4px rgba(0,0,0,0.3)',
                'zIndex': i
            })
        )

    # Make the top bill slightly brighter (no animation for now)
    if correct_answers > 0:
        bills[-1] = html.Div([
            html.Div('$100', style={
                'color': 'white',
                'fontWeight': 'bold',
                'fontSize': '16px'
            })
        ], style={
            'position': 'absolute',
            'bottom': f'{(correct_answers-1) * 15}px',
            'left': f'{50 + ((correct_answers-1) % 3 - 1) * 3}%',
            'transform': f'translateX(-50%) rotate({-3 + ((correct_answers-1) % 5) * 1.5}deg)',
            'backgroundColor': '#2ecc71',  # Brighter green for the top bill
            'border': '2px solid #27ae60',
            'borderRadius': '3px',
            'padding': '8px 20px',
            'boxShadow': '3px 3px 6px rgba(0,0,0,0.4)',  # Slightly stronger shadow
            'zIndex': correct_answers-1
        })

    # Add CSS animation as inline style for the floating bill
    return html.Div([
        html.Div(bills, style={
            'position': 'relative',
            'height': f'{max(150, correct_answers * 15 + 50)}px',
            'width': '100%'
        })
    ], style={
        'position': 'relative'
    })

def create_summary(stored_answers):
    # Filter out click counters
    answer_values = {k: v for k, v in stored_answers.items() if not k.endswith('_clicks')}

    if not answer_values:
        return html.P('No answers submitted yet. Complete the quiz above to see your results!',
                     style={'color': '#7f8c8d', 'fontSize': '16px'})

    total = len(investment_factors)
    correct = sum(1 for v in answer_values.values() if v == 'correct')
    score = (correct / total) * 100

    if score == 100:
        message = 'Perfect score! You have mastered the factors affecting investment demand!'
        color = '#2ecc71'
    elif score >= 80:
        message = 'Great job! You have a strong understanding of investment demand factors.'
        color = '#3498db'
    elif score >= 60:
        message = 'Good effort! Review the explanations for incorrect answers to strengthen your understanding.'
        color = '#f39c12'
    else:
        message = 'Keep studying! Review the explanations carefully and try again.'
        color = '#e74c3c'

    # Create portfolio growth visualization
    portfolio_graph = create_portfolio_growth_chart(correct)

    return html.Div([
        html.H2(f'Your Score: {correct}/{total} ({score:.0f}%)',
                style={'color': color, 'textAlign': 'center'}),
        html.P(message, style={'fontSize': '18px', 'textAlign': 'center', 'marginTop': '10px'}),

        # Portfolio growth visualization
        html.Div([
            html.H4('Knowledge Pays: Your Investment Portfolio Growth',
                   style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '30px'}),
            dcc.Graph(figure=portfolio_graph, config={'displayModeBar': False})
        ]),

        html.Div([
            html.H5('Key Takeaways:', style={'marginTop': '20px', 'marginBottom': '10px'}),
            html.Ul([
                html.Li('Investment demand is based on comparing expected returns with interest rates'),
                html.Li('Factors that increase expected returns shift investment demand right (increase)'),
                html.Li('Factors that decrease expected returns shift investment demand left (decrease)'),
                html.Li('Investment decisions are forward-looking and depend heavily on expectations')
            ], style={'lineHeight': '1.8'})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginTop': '20px'})
    ])

def create_portfolio_growth_chart(correct_answers):
    """Create a chart showing portfolio growth based on knowledge"""
    import plotly.graph_objects as go

    # Create data for visualization
    years = list(range(11))  # 0 to 10 years
    initial_investment = 10000

    # Calculate returns based on correct answers
    # More correct answers = better investment decisions = higher returns
    knowledge_return_rate = 1 + (0.05 + (correct_answers * 0.02))  # 5% base + 2% per correct answer
    no_knowledge_return = 1.03  # 3% return without knowledge

    # Calculate portfolio values
    educated_portfolio = [initial_investment * (knowledge_return_rate ** year) for year in years]
    uneducated_portfolio = [initial_investment * (no_knowledge_return ** year) for year in years]

    # Create the figure
    fig = go.Figure()

    # Add educated investor line
    fig.add_trace(go.Scatter(
        x=years,
        y=educated_portfolio,
        name=f'Your Portfolio ({correct_answers}/6 correct)',
        line=dict(color='#27ae60', width=3),
        fill='tonexty',
        fillcolor='rgba(39, 174, 96, 0.2)',
        hovertemplate='Year %{x}<br>Value: $%{y:,.0f}<extra></extra>'
    ))

    # Add baseline (no knowledge)
    fig.add_trace(go.Scatter(
        x=years,
        y=uneducated_portfolio,
        name='Without Knowledge',
        line=dict(color='#95a5a6', width=2, dash='dash'),
        hovertemplate='Year %{x}<br>Value: $%{y:,.0f}<extra></extra>'
    ))

    # Calculate profit difference
    profit_10_years = educated_portfolio[-1] - uneducated_portfolio[-1]

    fig.update_layout(
        title=dict(
            text=f'10-Year Profit from Knowledge: ${profit_10_years:,.0f}',
            font=dict(size=16)
        ),
        xaxis=dict(title='Years', gridcolor='#ecf0f1'),
        yaxis=dict(title='Portfolio Value ($)', gridcolor='#ecf0f1', tickformat='$,.0f'),
        hovermode='x unified',
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        plot_bgcolor='white',
        height=400,
        margin=dict(l=60, r=20, t=60, b=40)
    )

    return fig

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8051))
    app.run(host='0.0.0.0', port=port, debug=False)