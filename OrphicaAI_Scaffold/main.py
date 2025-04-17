# Main
from vault.vault_core import create_entry
    
def main():
    print("Welcome to OrphicaAI - EchoVault Live Input")
    print("Please enter your text:")
    print("type 'exit' to quit program")

    while True:
        user_input = input("User Input: ").strip()
        #start of new
        #emotional recall command
        if user_input.lower().startswith("recall") and not user_input.lower().startswith("recall tag"):
            emotion=user_input.lower().split(" ", 1)[1]
            from vault.vault_core import recall_by_emotion
            memories=recall_by_emotion(emotion)
            print(f"\nRecalling memories with emoiton '{emotion}':")
            for m in memories:
                print(f"- [{m['timestamp']}] {m['content']})")
                print (f"{m['emotion_vector']}\n")
            continue

        #symbolic tagging recall command
        if user_input.lower().startswith("recall tag"):
            parts=user_input.lower().split(" ",2)
            if len(parts)<3 or not parts[2].strip():
                print("Please provide a symbolic tag to recall. (ex: 'recall tag 'joy')")
                continue
            symbol=parts[2].strip()

            from vault.vault_core import get_entry
            from vault.symbolic_index import get_entries_by_symbol

            entry_ids=get_entries_by_symbol(symbol)
            if not entry_ids:
                print(f"No memories found with tag {symbol}\n")
                continue

            print(f"\nRecalling memories with tag '{symbol}': ")
            for eid in entry_ids:
                entry=get_entry(eid)
                print(f"-[{entry['timestamp']}] {entry['content']}")
                print(f"  → {entry['emotion_vector']} | Tags: {entry['tags']}\n")
            continue

                                             

        #end of new
        if user_input.lower() == 'exit':
            print("Exiting program.")
            break
        if not user_input:
            continue

        entry = create_entry(user_input)

        print("\nMemory Stored:")
        print(f"Emotion Vector: {entry['emotion_vector']}")
        print(f"Depth (Salience) Factor: {round(entry['depth_weight'],2)}")
        print(f"Tags: {entry['tags']}\n") #placeholder if tagging not yet ready


if __name__ == "__main__":
    main()
            
