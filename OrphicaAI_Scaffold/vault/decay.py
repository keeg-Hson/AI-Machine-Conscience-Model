# Decay
def decay_weights(vault):
    #placeholder for global decay
    for entry in vault.values():
        entry['depth_weight']*=0.99 #decay factor: 1% decay per tick

def reinforce_entry(entry_id,boost):
    #placeholder logic to be furthe r expanded upon later on
    pass