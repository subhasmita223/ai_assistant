import pyttsx3

def list_available_voices():
    """Print all available voice options with their IDs"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}. ID: {voice.id}")
        print(f"   Name: {voice.name}")
        print(f"   Languages: {voice.languages}")
        print(f"   Gender: {voice.gender if hasattr(voice, 'gender') else 'Unknown'}")
        print("---")
    engine.stop()

list_available_voices()