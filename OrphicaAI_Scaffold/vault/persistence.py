#persistence.py
import json
from pathlib import Path

#set memory archive path
MEMORY_PATH=Path("data/user_journals/echovault_memory.json")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True) #creates parent directory if it does not exist

#ensures existence of file
if not MEMORY_PATH.exists():
    MEMORY_PATH.write_text("[]") #creates empty file if one does not exist
    
def save_memory_to_archive(entry:dict):
    with open(MEMORY_PATH, 'r') as f:
        memories=json.load(f)
    memories.append(entry)

    with open(MEMORY_PATH, "w") as f:
        json.dump(memories, f, indent=2)
    print(f"Memory archived! Total entries: {len(memories)}") #confirms successful save