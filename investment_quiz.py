import os
import dash
from dash import dcc, html, Input, Output, State, ALL
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

    # Quiz sections
    html.Div([
        html.Div([
            # Create a quiz card for each factor
            html.Div([
                html.Div([
                    html.H4(f'{i+1}. {factor_data["title"]}', style={'color': '#2c3e50', 'marginBottom': '10px'}),
                    html.P(factor_data['description'], style={'color': '#7f8c8d', 'fontSize': '14px', 'marginBottom': '15px'}),
                    html.P(factor_data['question'], style={'fontSize': '16px', 'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.RadioItems(
                        id={'type': 'quiz-radio', 'index': factor_key},
                        options=factor_data['options'],
                        style={'marginBottom': '15px'}
                    ),
                    html.Button('Submit Answer',
                               id={'type': 'submit-button', 'index': factor_key},
                               style={'padding': '8px 20px', 'backgroundColor': '#3498db', 'color': 'white',
                                     'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                                     'fontSize': '14px', 'marginRight': '10px'}),
                    html.Button('Show Hint',
                               id={'type': 'hint-button', 'index': factor_key},
                               style={'padding': '8px 20px', 'backgroundColor': '#95a5a6', 'color': 'white',
                                     'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                                     'fontSize': '14px'}),
                    html.Div(id={'type': 'feedback', 'index': factor_key}, style={'marginTop': '15px'}),
                    html.Div(id={'type': 'hint', 'index': factor_key}, style={'marginTop': '10px'})
                ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                         'marginBottom': '20px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ]) for i, (factor_key, factor_data) in enumerate(investment_factors.items())
        ])
    ], style={'padding': '20px'}),

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

    # Store for tracking answers
    dcc.Store(id='answer-store', data={})

], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ecf0f1'})

# Callback for quiz submissions
@app.callback(
    [Output({'type': 'feedback', 'index': ALL}, 'children'),
     Output('answer-store', 'data'),
     Output('progress-bar', 'children'),
     Output('summary-results', 'children')],
    [Input({'type': 'submit-button', 'index': ALL}, 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State({'type': 'quiz-radio', 'index': ALL}, 'value'),
     State('answer-store', 'data')]
)
def handle_quiz_submissions(submit_clicks, reset_click, answers, stored_answers):
    ctx = dash.callback_context

    if not ctx.triggered:
        return [[] for _ in investment_factors], {}, create_progress_bar({}), create_summary({})

    trigger_id = ctx.triggered[0]['prop_id']

    # Handle reset
    if 'reset-button' in trigger_id:
        return [[] for _ in investment_factors], {}, create_progress_bar({}), create_summary({})

    # Process answers
    feedback_outputs = []
    factor_keys = list(investment_factors.keys())

    for i, factor_key in enumerate(factor_keys):
        if answers[i] is not None and submit_clicks[i]:
            user_answer = answers[i]
            correct_answer = investment_factors[factor_key]['correct']

            if user_answer == correct_answer:
                stored_answers[factor_key] = 'correct'
                feedback = html.Div([
                    html.P('✓ Correct!', style={'color': 'green', 'fontWeight': 'bold', 'fontSize': '18px'}),
                    html.P('Well done! You understand this concept.', style={'color': 'green'})
                ])
            else:
                stored_answers[factor_key] = 'incorrect'
                feedback = html.Div([
                    html.P('✗ Incorrect', style={'color': 'red', 'fontWeight': 'bold', 'fontSize': '18px'}),
                    html.Div([
                        html.P('Explanation:', style={'fontWeight': 'bold', 'color': '#e74c3c'}),
                        html.P(investment_factors[factor_key]['explanation'],
                              style={'backgroundColor': '#ffe6e6', 'padding': '15px',
                                    'borderRadius': '5px', 'lineHeight': '1.6'})
                    ])
                ])
            feedback_outputs.append(feedback)
        else:
            if factor_key in stored_answers:
                # Maintain existing feedback
                if stored_answers[factor_key] == 'correct':
                    feedback = html.Div([
                        html.P('✓ Correct!', style={'color': 'green', 'fontWeight': 'bold', 'fontSize': '18px'}),
                        html.P('Well done! You understand this concept.', style={'color': 'green'})
                    ])
                else:
                    feedback = html.Div([
                        html.P('✗ Incorrect', style={'color': 'red', 'fontWeight': 'bold', 'fontSize': '18px'}),
                        html.Div([
                            html.P('Explanation:', style={'fontWeight': 'bold', 'color': '#e74c3c'}),
                            html.P(investment_factors[factor_key]['explanation'],
                                  style={'backgroundColor': '#ffe6e6', 'padding': '15px',
                                        'borderRadius': '5px', 'lineHeight': '1.6'})
                        ])
                    ])
                feedback_outputs.append(feedback)
            else:
                feedback_outputs.append([])

    progress_bar = create_progress_bar(stored_answers)
    summary = create_summary(stored_answers)

    return feedback_outputs, stored_answers, progress_bar, summary

# Callback for hints
@app.callback(
    Output({'type': 'hint', 'index': ALL}, 'children'),
    [Input({'type': 'hint-button', 'index': ALL}, 'n_clicks')]
)
def show_hints(hint_clicks):
    hints = []
    factor_keys = list(investment_factors.keys())

    hint_texts = {
        'acquisition_costs': 'Think about profitability: If costs go up, do profits go up or down?',
        'business_taxes': 'Consider after-tax returns: Lower taxes mean firms keep more of their profits.',
        'technological_change': 'New technology usually makes production more efficient and profitable.',
        'capital_stock': 'If you already have unused equipment, do you need to buy more?',
        'inventory_changes': 'Building inventory requires investment in goods to stock up.',
        'expectations': 'Investment is about the future - optimism or pessimism matters!'
    }

    for i, factor_key in enumerate(factor_keys):
        if hint_clicks[i] and hint_clicks[i] > 0:
            hints.append(html.Div([
                html.P('💡 Hint:', style={'fontWeight': 'bold', 'color': '#f39c12'}),
                html.P(hint_texts[factor_key], style={'color': '#f39c12', 'fontStyle': 'italic'})
            ], style={'backgroundColor': '#fff3cd', 'padding': '10px', 'borderRadius': '5px'}))
        else:
            hints.append([])

    return hints

def create_progress_bar(stored_answers):
    total = len(investment_factors)
    correct = sum(1 for v in stored_answers.values() if v == 'correct')
    incorrect = sum(1 for v in stored_answers.values() if v == 'incorrect')
    unanswered = total - correct - incorrect

    correct_pct = (correct / total) * 100
    incorrect_pct = (incorrect / total) * 100

    return html.Div([
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

def create_summary(stored_answers):
    if not stored_answers:
        return html.P('No answers submitted yet. Complete the quiz above to see your results!',
                     style={'color': '#7f8c8d', 'fontSize': '16px'})

    total = len(investment_factors)
    correct = sum(1 for v in stored_answers.values() if v == 'correct')
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

    return html.Div([
        html.H2(f'Your Score: {correct}/{total} ({score:.0f}%)',
                style={'color': color, 'textAlign': 'center'}),
        html.P(message, style={'fontSize': '18px', 'textAlign': 'center', 'marginTop': '10px'}),
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8051))
    app.run(host='0.0.0.0', port=port, debug=False)