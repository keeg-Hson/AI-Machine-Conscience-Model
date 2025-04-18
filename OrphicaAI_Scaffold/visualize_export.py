#visualize_export (exports memory from chart at users request)
import dash
from dash import dcc, html, Input, Output
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

    #memory chart
    dcc.Graph(id="memory-chart"),

    #exported memory block
    html.Div(id="exported-memory", style={"whiteSpace":"pre-wrap"}),
])

@app.callback(
    Output("exported-memory", "children"),
    Input("memory-chart", "clickData")
)

def export_memory(clickData):
    if clickData:
        point=clickData['points'][0]['pointIndex']
        memory=df.iloc[point['pointIndex']]
        export_data={
            "timestamp": memory["Timestamp"].isoformat(),
            "emotion": memory["Emotion"],
            "salience": memory["Salience"],
            "content": memory["Content"]
        }

        with open("data/user_journals/exported_memory.json", "w") as f:
            json.dump(export_data, f, indent=4)
        return f"📤 Memory exported:\n{json.dumps(export_data, indent=2)}"
    return "🖱 Click a memory to export it" 




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


