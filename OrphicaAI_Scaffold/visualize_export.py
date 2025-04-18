#visualize_export (exports memory from chart at users request)
import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px

#load/preprocess memories
with open("data/user_journals/echovault_memory.json", "r") as f:
    raw=json.load(f)

def get_primary_emotion(ev): 
    return max(ev.items(), key=lambda x: x[1]) [0] if ev else "neutral"

df=pd.DataFrame([{
    "Timestamp": datetime.fromisoformat(m["timestamp"]),
    "Salience": m.get("depth_weight", 0),
    "Emotion": get_primary_emotion(m.get("emotion_vector", {})),
    "Content":m.get("content","")

} for m in raw])


#plotly figure
fig=px.scatter(
    df,x="Timestamp", y="Salience", color="Emotion", 
    hover_data=["Content"], template="plotly_white"
)

#dash app
app=dash.Dash(__name__) #initialize dash app
app.layout=html.Div([
    html.H1("🧠 Memory Timeline"),

    #dropdown filter
    dcc.Dropdown(
        options=[{"label": e, "value": e} for e in sorted(df["Emotion"].unique())],
        placeholder="Filter by Emotion",
        id="emotion-filter"
    ),

    #salience filter
    dcc.Slider(
        0, 1, 0.05,
        value=0.0,
        marks={0: '0', 0.5: '0.5', 1: '1'},
        tooltip={"placement":"bottom", "always_visible":True},
        id="salience-filter"
    ),

    dcc.Dropdown(
        options=[
            {"label": "JSON", "value": "json"},
            {"label": "Text (.txt)", "value": "txt"},
            {"label": "Markdown (.md)", "value": "md"},
        ],
        value="json",
        id="export-format",
        placeholder="Choose export format"
    ),

    #memory chart
    dcc.Graph(id="memory-chart"),

    #exported memory block
    html.Button("Download Exported Memory", id="download-btn", n_clicks=0),
    dcc.Download(id="download-memory"),
    html.Div(id="exported-memory", style={"whiteSpace":"pre-wrap"}),
])

@app.callback(
    Output("download-memory", "data"),                 # triggers file download
    Output("exported-memory", "children"),             # updates memory preview
    Input("download-btn", "n_clicks"),                 # triggered by button
    State("memory-chart", "clickData"),                # uses click data
    State("export-format", "value"),                   # reads selected format
    prevent_initial_call=True
)

#new
def export_memory(n_clicks, clickData, fmt):
    if not clickData:
        return dash.no_update, "Please click a memory first to export it."
    
    point_index=clickData["points"][0]["pointIndex"]
    memory=df.iloc[point_index]

    export_data={
            "timestamp": memory["Timestamp"].isoformat(),
            "emotion": memory["Emotion"],
            "salience": memory["Salience"],
            "content": memory["Content"]
        }
    
    filename=f"memory_export.{fmt}"

    #formatting options
    if fmt=="json":
        content=json.dumps(export_data, indent=4)
    elif fmt=="txt":
        content=f"Timestamp: {export_data['timestamp']}\nEmotion: {export_data['emotion']}\nSalience: {export_data['salience']}\n\n{export_data['content']}"
    elif fmt=="md":
        content=f"# Memory Export\n- **Timestamp:** {export_data['timestamp']}\n- **Emotion:** {export_data['emotion']}\n- **Salience:** {export_data['salience']}\n\n---\n\n{export_data['content']}"
    else:
        content = "Invalid format"

    return dcc.send_string(content, filename), f"📤 Memory exported as `{filename}`."


#new





#subsequent callback function
@app.callback(
    Output("memory-chart", "figure"),
    Input("emotion-filter", "value"),
    Input("salience-filter","value")
)

def update_chart(emotion,salience):
    filtered=df.copy()
    if emotion:
        filtered=filtered[filtered["Emotion"]==emotion]
    filtered=filtered[filtered["Salience"]>=salience]

    fig=px.scatter(
        filtered,
        x="Timestamp",
        y="Salience",
        color="Emotion",
        hover_data=["Content", "Emotion", "Salience"],
        template="plotly_white"

    )

    fig.update_layout(title="🧠 Orphica Memory Timeline (Filtered)", title_font_size=20)
    return fig


if __name__=="__main__":
    app.run(debug=True)


