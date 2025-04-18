#Visulaize
import json
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.patches as mpatches
import pandas as pd
import plotly.express as px



MEMORY_PATH="data/user_journals/echovault_memory.json"

#colour mapping
color_map={
    'joy': 'green',
    'grief': 'purple',
    'fear': 'red',
    'anger': 'orange',
    'surprise': 'blue',
    'neutral': 'gray'

}


def load_memories():
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)
    
def get_primary_emotion(emotion_vector):
    if not emotion_vector:
        return "neutral"
    return max(emotion_vector.items(), key=lambda x: x[1])[0]

def plot_memory_timeline(): #new
    memories=load_memories()
    rows=[]

    for mem in memories:
        try:
            ts=datetime.fromisoformat(mem["timestamp"])
            weight=mem.get("depth_weight",0)
            emotion=get_primary_emotion(mem.get("emotion_vector", {}))
            content=mem.get("content", "")

            rows.append({
                "Timestamp":ts,
                "Salience":weight,
                "Emotion":emotion,
                "Content":content
            })
        except Exception as e:
            print (f"skipping memory due to error: {e}")

    if not rows:
        print("No memories to plot.")
        return
    
    df=pd.DataFrame(rows)

    fig=px.scatter(
        df,
        x="Timestamp",
        y="Salience",
        color="Emotion",
        hover_data=["Content", "Emotion", "Salience"],
        title="🧠 Orphica Memory Timeline (Salience vs. Time)",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Depth (Salience Factor)",
        title_font_size=20,
        legend_title="Emotion"
    )

    fig.write_html("memory_timeline_interactive.html") #save results for web viewing
    fig.show()





if __name__ == "__main__":
    plot_memory_timeline()
