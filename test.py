from llm import TherapistCompanion
import dotenv

def run_therapist_console():
    """Run an interactive console with the therapist companion"""
    print(f"=== Therapist Companion Console ===")
    print(f"Type 'exit' or 'quit' to end the conversation")
    print(f"Type 'sessions' to list previous conversations")
    print(f"Type 'debug on' or 'debug off' to toggle debugging")
    print(f"====================================")
    
    api_key = dotenv.dotenv_values(".env").get("API")
    if not api_key:
        print("Error: API key not found in .env file")
        return
    
    therapist = TherapistCompanion(name="Asha" , api_key=api_key)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Take care of yourself.")
            break
        
        if user_input.lower() == "sessions":
            sessions = therapist.list_sessions()
            print("\nPrevious conversation sessions:")
            for session in sessions:
                print(f"ID: {session['session_id'][:8]}... | Started: {session['start_time']} | Messages: {session['message_count']}")
            continue
        
        if user_input.lower() == "debug on":
            therapist.debug = True
            print("Debug mode enabled.")
            continue
        
        if user_input.lower() == "debug off":
            therapist.debug = False
            print("Debug mode disabled.")
            continue
        
        result = therapist.respond(user_input)
        
        print(f"\n{therapist.name}: {result['response']}")
        print(f"[Emotion detected: {result['emotion_detected']}]")
        print(f"[{therapist.name}'s expression: {result['therapist_expression']}]")

if __name__ == "__main__":
    run_therapist_console()