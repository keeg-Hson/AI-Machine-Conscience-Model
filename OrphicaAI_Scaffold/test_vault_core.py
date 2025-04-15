# test_vault_core.py

from vault.vault_core import (
    create_entry,
    get_entry,
    recall_by_symbol,
    resurface_candidates,
    reinforce,
    decay_all,
)

# Sample test entry
test_text = "I saw a mirror and it made me reflect on who I used to be."

# Create an entry
print("Creating entry...")
entry = create_entry(test_text)
entry_id = entry['id']
print("Entry created:", entry)

# Retrieve entry by ID
print("\nRetrieving entry...")
retrieved = get_entry(entry_id)
print("Entry retrieved:", retrieved)

# Recall by symbolic tag (assumes symbolic extractor tags 'mirror')
print("\nRecalling by symbol 'mirror'...")
symbol_recall = recall_by_symbol('mirror')
print("Symbol recall result:", symbol_recall)

# Simulate context for resurfacing
print("\nTesting resurfacing candidates (context: 'reflect')...")
context_vector = {'reflect': 1.0}
resurfaced = resurface_candidates(context_vector)
print("Resurfaced entries:", resurfaced)

# Reinforce the entry
print("\nReinforcing entry...")
reinforce(entry_id, boost=0.2)
print("Reinforced entry:", get_entry(entry_id))

# Apply decay to all entries
print("\nApplying decay to all entries...")
decay_all()
print("Entry after decay:", get_entry(entry_id))