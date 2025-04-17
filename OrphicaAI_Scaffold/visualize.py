#Visulaize
import json
import matplotlib.pyplot as plt
from datetime import datetime

MEMORY_PATH="data/user_journals/echovault_memory.json"

def load_memories():
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)
    
def get_primary_emotion(emotion_vector):
    if not emotion_vector:
        return "neutral"
    return max(emotion_vector.items(), key=lambda x: x[1])[0]

def plot_memory_timeline():
    memories=load_memories()
    timestamps=[]
    weights=[]
    emotions=[]

    for mem in memories:
        try:
            ts=datetime.fromisoformat(mem["timestamp"])
            weight=mem.get("depth_weight",0)
            emotion=get_primary_emotion(mem.get("emotion_vector", {}))

            timestamps.append(ts)
            weights.append(weight)
            emotions.append(emotion)        
        except Exception as e:
            print (f"skipping memory due to error: {e}")

    if not timestamps:
        print("No memories to plot.")
        return

    #plotting
    plt.figure(figsize=(10, 6))
    scatter=plt.scatter(timestamps, weights, c=range(len(emotions)), cmap='viridis', alpha=0.8) 

    #labeling of emotion per point
    for i, emotion in enumerate(emotions):
        plt.annotate(emotion, (timestamps[i], weights[i]), fontsize=8, alpha=0.7)

    
    #plot functionality
    plt.title("🧠 Orphica Memory Timeline (Salience vs. Time)")
    plt.xlabel("Timestamp")
    plt.ylabel("Depth (Salience Factor)")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_memory_timeline()
