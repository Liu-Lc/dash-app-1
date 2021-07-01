import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import random
import plotly.graph_objs as go
from collections import deque

# Queue object
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

# Dash server
app = dash.Dash()

server = app.server

# Layout
app.layout = html.Div(children=[
    html.Div(
        html.H2('Live data visualization')
    ),
    html.Div(children=[
        # Live Graph
        dcc.Graph(id='live-graph', animate=True),
        # Update interval
        dcc.Interval(id='graph-update', interval=2000)
    ])
])

# Callback wrapper calback(output=, input=[], state=[])
@app.callback(
    # Output is the figure of the graph
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
# Callback function
def update_graph(interval):
    # Simulate live random values
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    # plotly scatter plot
    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )
    # Output is the figure with 'data' and 'layout'
    return {
        # data is a list
        'data':[data], 
        'layout': go.Layout(
            # axis update limits
            xaxis = dict(range=[min(X), max(X)]),
            yaxis = dict(range=[min(Y), max(Y)])
        )}

if __name__ == '__main__':
    app.run_server()