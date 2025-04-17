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
        if user_input.lower().startswith('recall'):
            emotion=user_input.lower().split(" ", 1)[1]
            from vault.vault_core import recall_by_emotion
            memories=recall_by_emotion(emotion)
            print(f"\nrecalling memories with emotion '{emotion}':")
            for m in memories:
                print(f"- [{m['timestamp']}] {m['content']}")
                print(f"-> {m['emotion_vector']}\n")
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
            
