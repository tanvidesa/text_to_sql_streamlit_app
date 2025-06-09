import plotly.express as px

def generate_graph_if_needed(user_query, df, columns):
    if len(columns) < 2:
        return None
    x = df[columns[0]]
    y = df[columns[1]]

    if "trend" in user_query.lower() or "over time" in user_query.lower():
        return "line", x, y
    elif "distribution" in user_query.lower() or "breakdown" in user_query.lower():
        return "pie", x, y
    elif "compare" in user_query.lower() or "comparison" in user_query.lower():
        return "bar", x, y
    return None

def generate_pie_chart(labels, values):
    return px.pie(names=labels, values=values, title="Pie Chart")
