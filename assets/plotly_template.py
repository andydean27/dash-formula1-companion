import plotly.graph_objects as go

f1_graph_template = go.layout.Template(
    layout=go.Layout(
        plot_bgcolor='#646464',  # Background color of the plot area
        paper_bgcolor='#323232',  # Background color of the entire plot
        font=dict(color='#FFFFFF')  # Font color
    )
)