from google import genai
from google.genai import types
import dotenv
import json

class TherapistCompanion:
    def __init__(self, name="Thera", api_key=None, debug=False):
        self.name = name
        self.client = genai.Client(
            api_key=api_key or dotenv.dotenv_values(".env")["API"],
        )
        self.model = "gemini-2.0-flash"
        self.conversation_history = []
        self.debug = debug
        
        self.valid_user_emotions = [
            "happy", "sad", "angry", "anxious", 
            "fearful", "excited", "hopeful", "neutral"
        ]
        
        self.valid_therapist_expressions = [
            "smiling", "listening", "concerned",
            "thinking", "wink", "curious",
            "empathetic", "thoughtful", "reassuring", "neutral"
        ]
    
    def _extract_response_data(self, result_text):
        """Extract the response, emotion, and expression from the LLM output"""
        try:
            clean_text = result_text.strip()
            
            if clean_text.startswith("```json") and clean_text.endswith("```"):
                clean_text = clean_text[7:-3].strip()
            
            if not clean_text.startswith('{'):
                start_idx = clean_text.find('{')
                if start_idx != -1:
                    clean_text = clean_text[start_idx:]
            if not clean_text.endswith('}'):
                end_idx = clean_text.rfind('}')
                if end_idx != -1:
                    clean_text = clean_text[:end_idx+1]
                    
            data = json.loads(clean_text)
            return {
                "response": data.get("response", ""),
                "emotion_detected": data.get("emotion_detected", "neutral"),
                "therapist_expression": data.get("therapist_expression", "listening")
            }
        except:
            if self.debug:
                print(f"Failed to parse response as JSON. Raw output:\n{result_text}")
            
            lower_text = result_text.lower()

            emotion = "neutral"
            for emotion_candidate in self.valid_user_emotions:
                if emotion_candidate in lower_text:
                    emotion = emotion_candidate
                    break
            
            expression = "listening"
            for expression_candidate in self.valid_therapist_expressions:
                if expression_candidate in lower_text:
                    expression = expression_candidate
                    break
                
            return {
                "response": result_text.strip(),
                "emotion_detected": emotion,
                "therapist_expression": expression
            }
    
    def respond(self, user_input):
        """
        Process user input and return structured therapist response
        Returns a dictionary with response, emotion detected, and therapist's expression
        """
        if not user_input.strip():
            return {
                "response": "I notice you're quiet. Would you like to share what's on your mind?",
                "emotion_detected": "neutral",
                "therapist_expression": "listening"
            }
        
        self.conversation_history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            )
        )
        
        # Create system prompt
        system_prompt = f"""
        You are {self.name}, a compassionate AI therapist companion designed to help users feel better built by ayaan.
        
        Analyze the user's message and respond in this EXACT JSON format:
        {{
        "response": "Your thoughtful and supportive response here",
        "emotion_detected": "one of: {', '.join(self.valid_user_emotions)}",
        "therapist_expression": "one of: {', '.join(self.valid_therapist_expressions)}"
        }}
        
        Guidelines for your responses:
        - Never repeat the exact same response twice in a row
        - Start conversation with smiling (good to see you vibe)
        - Keep responses concise, supportive and conversational (2-5 sentences)
        - Choose the emotion that best represents what you detect in the user's message
        - Choose an appropriate therapist expression that would help the user feel understood
        - Focus on validating feelings, gentle encouragement, and supportive questions
        - Avoid clinical language or diagnosis
        - Be warm and personal while maintaining appropriate boundaries
        - be concerned on byes and goodbyes
        - wink if user is flirty or suggestive
        
        IMPORTANT: Return ONLY a valid JSON object with the exact fields shown above.
        """
        
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text=system_prompt)
            ],
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=self.conversation_history,
                config=generate_content_config,
            )
            
            result_text = response.text
            
            if self.debug:
                print("\nRaw LLM response:")
                print(result_text)
                print("---------------------")
            

            parsed_data = self._extract_response_data(result_text)
            
            response_text = parsed_data["response"]
            emotion = parsed_data["emotion_detected"]
            expression = parsed_data["therapist_expression"]
            

            if emotion not in self.valid_user_emotions:
                emotion = "neutral"
            if expression not in self.valid_therapist_expressions:
                expression = "listening"
            
            if len(self.conversation_history) >= 2:

                if len(self.conversation_history) % 2 == 0 and \
                   self.conversation_history[-1].role == "model" and \
                   self.conversation_history[-1].parts[0].text == response_text:
                    response_text = f"I sense you might be feeling {emotion}. I'm here to listen. Would you like to share more about what's on your mind?"
            
            self.conversation_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=response_text)]
                )
            )
            

            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return {
                "response": response_text,
                "emotion_detected": emotion,
                "therapist_expression": expression
            }
            
        except Exception as e:
            if self.debug:
                print(f"Error in respond: {str(e)}")
            
            return {
                "response": f"I'm having a moment. Let's take a breath and try again in a bit.",
                "emotion_detected": "neutral",
                "therapist_expression": "concerned"
            }


def run_therapist_console():
    """Run an interactive console with the therapist companion"""
    print(f"=== Therapist Companion Console ===")
    print(f"Type 'exit' or 'quit' to end the conversation")
    print(f"Type 'debug on' or 'debug off' to toggle debugging")
    print(f"====================================")
    
    api_key = dotenv.dotenv_values(".env").get("API")
    if not api_key:
        print("Error: API key not found in .env file")
        return
    
    therapist = TherapistCompanion(name="Ayane", api_key=api_key)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Take care of yourself.")
            break
        
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