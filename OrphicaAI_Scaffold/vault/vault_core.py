# Vault Core
from datetime import datetime  #for timestamping new memories
from uuid import uuid4 #generation of unique IDs for each memory entry in question
from .emotion_vectorizer import classify_emotions, estimate_intensity #Analyzes the emotional tone associated with eahc piece of contetn
from .symbolic_index import tag_entry, find_symbolic_associations, SYMBOLIC_INDEX #symbolic tagging/index linking fucntionality
from .decay import decay_weights, reinforce_entry #weighting and decay of memory entries
from vault.persistence import save_memory_to_archive
from .persistence import load_memory_archive, save_memory_to_archive 
#from utils.symbolic_index import find_symbolic_associations, tag_entry

#TEMPORARY: in-built memory store for prototyping purposes
VAULT=load_memory_archive() #MAIN MEMORY VAULT (OR "SUBCONSCIOUS" MEMORY BANK EFFECGTIVELY)


##Core Entry Structure
def create_entry(content: str, metadata:dict={}) -> dict:
    """
    Creates and returns fully formulated memory entry from user input.

    METADATA, CONTENT VARIABLES OT BE DEFINED. HIGHLIGHTED IN THE GOOGLE DOC!
    """

    entry_id=str(uuid4()) #generation of a unique user ID for given memory entry
    timestamp=metadata.get('timestamp', datetime.utcnow().isoformat()) #use of currently existtent timestamp, or generation of a new one is deemed necessary

    #emotional tagging
    emotion_vector=classify_emotions(content) #deals with assessment of emotional makeup and associated undertimes, context of content in question
    intensity_score = estimate_intensity(content) #estimation of emotional intensity associated with user input (TBD: to be used for salience factor)
    
    #symbolic tagging
    symbols=find_symbolic_associations(content) #deals with extraction of symbolic tags, as per the user input. could take form in the shape of recurring themes, images, archetypes, etc.

    #creation of full memory entry object
    entry = { #TBD: define entry structure
        'id': entry_id, #unique ID for memory in question
        'timestamp': timestamp, #time of memory creation
        'content': content, #raw user input (be that thought, journal, audio file, etc etc etc.)
        'tags': symbols, #symobic tags associated with associated user content 
        'emotion_vector': emotion_vector, #emotional mapping (ex: {'distress': 0.7})
        'depth_weight': intensity_score, #how 'deep' a given memory is to the user, effectively a scale of emotinal relevance/importance: now directly wired up to "emotional charge"
        'retrieval_decay': 0.01, #rate at which memory faces if memory not reinforced
        'associations': [], #linking to other related memories or user entries/inputs (can be filled out later)
    }  

    VAULT[entry_id]=entry #save memory into larger subconscious repository
    tag_entry(entry_id, symbols) #adds tags to symbolic index for retrieval purposes
    save_memory_to_archive(entry) #saves memory to archive for long-term storage (TBD)

    return entry #returns full memory entry object in question. basically, end of the function that concocts all computations together, as 'return' statements generally intend to do X)


#memeory retrieval functions
def get_entry(entry_id:str):
    """
    retrieves user entry by ID
    """
    return VAULT.get(entry_id) #pulls memory from subnconscious utilizing assigned unique ID

def recall_by_symbol(symbol:str, max_results: int=5) -> list:
    """
    retrieves user entries with use of symbolic tagging
    """
    associated_ids=SYMBOLIC_INDEX.get(symbol, [])[:max_results] #links memory IDs to relevant symbols
    return [VAULT[entry_id] for entry_id in associated_ids if entry_id in VAULT] #RETURNS FULL MEMORY OBJECTS 

def resurface_candidates(context_vector:dict) -> list:
    """
    returns a list of letent memories that are likely to become relevant to user down the road.
    -would compare embeddings/emotinal vectors within full release
    """
    candidates=[] #empty list to store potential candidates
    for entry in VAULT.values(): #checks every stored memory from cumulative inputs set
        for k in context_vector: #parse each key words/associated 'emotional tag' within current context
            if k in entry['emotion_vector']: #checks if there is emptional overlap within memory
                candidates.append(entry) #add memory to candiate list
                break #stops after first match, as we only need one to add to the list. prevents 'double coutning' 
        return sorted(candidates, key=lambda x: -x['depth_weight'])[:5] #sort by importance, returns top matches

##Memory Maintenance:
def reinforce(entry_id:str, boost: float=0.01):
    """
    fortifies salience of a given user entry, as if it were being consciously recalled.
    """
    if entry_id in VAULT:
        VAULT[entry_id]['depth_weight']+=boost #increases the 'depth weight' of each memory entry (i.e: 'importance' factor)
        reinforce_entry(entry_id, boost) #calls external function to handle symbolic/index boost as well

def decay_all():
    """
    global dacay tick: lowers the weighting factor associated with all user entires over time.
    """
    decay_weights(VAULT) #CALLS DECAY FUNCTION TO AGE ALL ASSOCIATED MEMORY ENTRIES

def recall_by_emotion(emotion: str, max_results:int=5) -> list:
    #retreval of user 'emotions' by category
    filtered=[
        entry for entry in VAULT.values()
        if emotion in entry["emotion_vector"] 
    ]

    return sorted(filtered, key=lambda e: -e["emotion_vector"][emotion])[:max_results] #sorts by emotional weight, returns top matches

