#Visulaize
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
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


#filter memories
def filter_memories(memories, emotion_filter=None, salience_min=0.0, days_back=None):
    now=datetime.utcnow()
    rows=[]

    for mem in memories:
        try:
            ts = datetime.fromisoformat(mem["timestamp"])
            if days_back and ts < now - timedelta(days=days_back):
                continue

            weight=mem.get("depth_weight", 0)
            if weight<salience_min:
                continue

            emotion=get_primary_emotion(mem.get("emotion_vector", {}))
            if emotion_filter and emotion != emotion_filter:
                continue



            content=mem.get("content", "")

            rows.append({
                "Timestamp":ts,
                "Salience": weight,
                "Emotion":emotion,
                "Content":content
            })
        except Exception as e:
            print(f"skipping memory due to error: {e}")
            continue
    return pd.DataFrame(rows)



def plot_memory_timeline(): #new
    memories=load_memories()

    print(f"Loaded {len(memories)} total memories")
    for m in memories:
        print(m["timestamp"], m.get("emotion_vector"), m.get("depth_weight"))
    df=filter_memories(memories, emotion_filter=None, salience_min=0.0, days_back=None) #tweak filtering as seen fit
    


    if df.empty:
        print("No memories to plot")
        return


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

    fig.write_html("memory_timeline_interactive.html", include_plotlyjs='cdn') #save results for web viewing
    fig.show()



if __name__ == "__main__":
    plot_memory_timeline()
