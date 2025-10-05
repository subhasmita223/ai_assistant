import pygame
import sys
import os
from datetime import datetime
from llm import TherapistCompanion
import dotenv
import threading
import pyttsx3
import queue

class TherapistGUI:
    def __init__(self, width=1000, height=618):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("1-25-1-1-14")
        self.phi = 1.618
        self.bg_color = (35, 35, 50)
        self.text_color = (230, 230, 230)
        self.input_bg_color = (45, 45, 60)
        self.accent_color = (10, 200, 255)  
        self.button_color = (70, 70, 90)
        self.button_hover_color = (100, 100, 130)
        self.font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.title_font2 = pygame.font.SysFont("Arial", 18) 
        self.messages = []
        self.input_text = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.input_active = False
        self.input_rect = pygame.Rect(20, height - 60, (width / self.phi) - 100, 40)
        self.send_button = pygame.Rect((width / self.phi) - 70, height - 60, 50, 40)
        self.speech_enabled = True
        self.speech_button = pygame.Rect((width / self.phi) - 130, height - 60, 50, 40)
        self.chat_rect = pygame.Rect(0, 0, width / self.phi, height)
        self.avatar_rect = pygame.Rect(width / self.phi, 0, width - (width / self.phi), height / self.phi)
        self.emotion_rect = pygame.Rect(width / self.phi, height / self.phi, 
                                       width - (width / self.phi), height - (height / self.phi))
        
        self.expressions = ["neutral", "smiling", "concerned", "listening", 
                           "thinking", "wink", "curious", "empathetic", 
                           "thoughtful", "reassuring"]
        
        self.therapist_images = {}
        self.load_therapist_images()
        
        self.current_emotion = "neutral"
        self.current_expression = "neutral"

        api_key = dotenv.dotenv_values(".env").get("API")
        if not api_key:
            print("Error: API key not found in .env file")
            sys.exit(1)
        self.therapist = TherapistCompanion(name="Ayane", api_key=api_key)
        self.setup_tts()
        self.speech_queue = queue.Queue()
        self.speech_thread = threading.Thread(target=self.speech_worker, daemon=True)
        self.speech_thread.start()
        self.add_message("Ayane", "Hello! I'm Ayane, your AI therapist companion. How are you feeling today?", "neutral", "smiling")
        
    def setup_tts(self):
        """Setup text-to-speech engine with female voice"""
        self.tts_engine = pyttsx3.init()
    

        self.tts_engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')

        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)  
    
    def speech_worker(self):
        """Background worker to process speech queue"""
        while True:
            text = self.speech_queue.get()
            if text == "STOP":
                self.tts_engine.stop()
                self.speech_queue.task_done()
                continue
                
            if text and self.speech_enabled:
                try:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                except Exception as e:
                    print(f"TTS Error: {e}")
            
            self.speech_queue.task_done()
    
    def speak(self, text):
        """Add text to speech queue"""
        if self.speech_enabled:
            self.speech_queue.put(text)
    
    def stop_speaking(self):
        """Stop current speech"""
        self.speech_queue.put("STOP")
        
    def toggle_speech(self):
        """Toggle speech on/off"""
        self.speech_enabled = not self.speech_enabled
        if not self.speech_enabled:
            self.stop_speaking()
    
    def load_therapist_images(self):
        """Load all therapist expression images"""
        for expression in self.expressions:
            try:
                img_path = f"assets/{expression}.jpeg"
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path)

                    scaled_img = pygame.transform.scale(img, 
                                                      (self.avatar_rect.width - 20, 
                                                       self.avatar_rect.height - 20))
                    self.therapist_images[expression] = scaled_img
                else:
                    print(f"Warning: Image for '{expression}' not found at {img_path}")
            except pygame.error as e:
                print(f"Error loading image for '{expression}': {e}")

                placeholder = pygame.Surface((300, 300))
                placeholder.fill((100, 100, 150))
                self.therapist_images[expression] = placeholder
    
    def add_message(self, sender, text, emotion, expression):
        """Add a new message to the chat history"""
        timestamp = datetime.now().strftime("%H:%M")
        self.messages.append({
            "sender": sender,
            "text": text,
            "timestamp": timestamp,
            "emotion": emotion,
            "expression": expression
        })
        
        if sender == "Ayane":
            self.current_emotion = emotion
            self.current_expression = expression
            #self.speak(text)
            print(f"-Therapist ({timestamp}): {text} \nEmotion: {emotion} \nExpression: {expression}", end="-\n", flush=True)
    
    def draw_chat(self):
        """Draw the chat section"""
        pygame.draw.rect(self.screen, self.bg_color, self.chat_rect)
        pygame.draw.rect(self.screen, self.accent_color, self.chat_rect, 2)

        title = self.title_font.render("Chat with Ayane", True, self.accent_color)
        self.screen.blit(title, (20, 15))

        y_offset = 50
        visible_height = self.height - 120  
        
        messages_to_display = []
        current_height = 0

        for msg in reversed(self.messages):
            text = msg["text"]
            sender = msg["sender"]
            timestamp = msg["timestamp"]
            
            header = f"{sender} ({timestamp}):"
            header_surface = self.font.render(header, True, self.accent_color)
            
            msg_width = self.chat_rect.width - 40
            wrapped_text = self.wrap_text(text, msg_width)
            text_height = len(wrapped_text) * self.font.get_height()
            
            message_height = header_surface.get_height() + text_height + 15 
            
            if current_height + message_height <= visible_height or not messages_to_display:
                messages_to_display.insert(0, {
                    "message": msg,
                    "height": message_height,
                    "wrapped_text": wrapped_text
                })
                current_height += message_height
            else:
                break
        
        for msg_data in messages_to_display:
            msg = msg_data["message"]
            wrapped_text = msg_data["wrapped_text"]
            message_height = msg_data["height"]
            
 
            header = f"{msg['sender']} ({msg['timestamp']}):"
            header_surface = self.font.render(header, True, self.accent_color)
            self.screen.blit(header_surface, (20, y_offset))

            line_offset = 0
            for line in wrapped_text:
                line_surface = self.font.render(line, True, self.text_color)
                self.screen.blit(line_surface, (20, y_offset + header_surface.get_height() + line_offset))
                line_offset += self.font.get_height()
            
            y_offset += message_height
        
        pygame.draw.rect(self.screen, self.input_bg_color, self.input_rect)
        pygame.draw.rect(self.screen, self.accent_color, self.input_rect, 1)

        if self.input_text:
            text_surface = self.font.render(self.input_text, True, self.text_color)

            clip_rect = pygame.Rect(0, 0, self.input_rect.width - 10, self.input_rect.height)
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 10), clip_rect)
        
        if self.input_active and self.cursor_visible:
            cursor_pos = self.font.render(self.input_text, True, self.text_color).get_width()
            cursor_pos = min(cursor_pos, self.input_rect.width - 15)
            pygame.draw.line(self.screen, self.text_color, 
                           (self.input_rect.x + 5 + cursor_pos, self.input_rect.y + 10),
                           (self.input_rect.x + 5 + cursor_pos, self.input_rect.y + 30), 2)

        speech_button_color = self.button_hover_color if self.is_mouse_over_speech_button() else self.button_color
        pygame.draw.rect(self.screen, speech_button_color, self.speech_button)
        pygame.draw.rect(self.screen, self.accent_color, self.speech_button, 2)
        
        if self.speech_enabled:
            pygame.draw.circle(self.screen, self.accent_color, 
                             (self.speech_button.x + 25, self.speech_button.y + 20), 10, 2)
            pygame.draw.line(self.screen, self.accent_color,
                           (self.speech_button.x + 25, self.speech_button.y + 10),
                           (self.speech_button.x + 25, self.speech_button.y + 30), 2)
        else:

            pygame.draw.circle(self.screen, self.accent_color, 
                             (self.speech_button.x + 25, self.speech_button.y + 20), 10, 2)
            pygame.draw.line(self.screen, self.accent_color,
                           (self.speech_button.x + 20, self.speech_button.y + 15),
                           (self.speech_button.x + 30, self.speech_button.y + 25), 2)
            pygame.draw.line(self.screen, self.accent_color,
                           (self.speech_button.x + 30, self.speech_button.y + 15),
                           (self.speech_button.x + 20, self.speech_button.y + 25), 2)
        
        button_color = self.button_hover_color if self.is_mouse_over_button() else self.button_color
        pygame.draw.rect(self.screen, button_color, self.send_button)
        pygame.draw.rect(self.screen, self.accent_color, self.send_button, 2)
        
        points = [
            (self.send_button.x + 15, self.send_button.y + 20),
            (self.send_button.x + 35, self.send_button.y + 20),
            (self.send_button.x + 25, self.send_button.y + 10)
        ]
        pygame.draw.polygon(self.screen, self.accent_color, points)
    
    def draw_avatar(self):
        """Draw the therapist avatar section"""
        pygame.draw.rect(self.screen, self.bg_color, self.avatar_rect)
        pygame.draw.rect(self.screen, self.accent_color, self.avatar_rect, 2)

        title = self.title_font.render("Therapist", True, self.accent_color)
        self.screen.blit(title, (self.avatar_rect.x + 10, self.avatar_rect.y + 10))

        expression = self.current_expression
        if expression in self.therapist_images:
            avatar_img = self.therapist_images[expression]
            img_x = self.avatar_rect.x + (self.avatar_rect.width - avatar_img.get_width()) // 2
            img_y = self.avatar_rect.y + (self.avatar_rect.height - avatar_img.get_height()) // 2
            self.screen.blit(avatar_img, (img_x, img_y))
        else:
            if "neutral" in self.therapist_images:
                avatar_img = self.therapist_images["neutral"]
                img_x = self.avatar_rect.x + (self.avatar_rect.width - avatar_img.get_width()) // 2
                img_y = self.avatar_rect.y + (self.avatar_rect.height - avatar_img.get_height()) // 2
                self.screen.blit(avatar_img, (img_x, img_y))
            else:
                msg = self.font.render(f"Expression: {expression}", True, self.text_color)
                self.screen.blit(msg, (self.avatar_rect.x + 20, self.avatar_rect.y + 50))
    
    def draw_emotion_meter(self):
        """Draw the emotion meter section"""

        pygame.draw.rect(self.screen, self.bg_color, self.emotion_rect)
        pygame.draw.rect(self.screen, self.accent_color, self.emotion_rect, 2)
        
        
        title = self.title_font2.render("Emotion Detected", True, self.accent_color)
        self.screen.blit(title, (self.emotion_rect.x + 10, self.emotion_rect.y + 4),)
        

        emotions = ["happy", "sad", "angry", "anxious", "fearful", "excited", "hopeful", "neutral"]

        spacing = self.emotion_rect.height / (len(emotions) + 1)
        bar_width = self.emotion_rect.width - 120
        
        for i, emotion in enumerate(emotions):
            y_pos = self.emotion_rect.y + 25 + (i * spacing)
            
            label = self.font.render(emotion.capitalize(), True, self.text_color)
            self.screen.blit(label, (self.emotion_rect.x + 20, y_pos))
            
            bar_bg_rect = pygame.Rect(self.emotion_rect.x + 100, y_pos, bar_width, 20)
            pygame.draw.rect(self.screen, self.input_bg_color, bar_bg_rect)
            
            if emotion == self.current_emotion:
                bar_fill_rect = pygame.Rect(self.emotion_rect.x + 100, y_pos, bar_width, 20)
                pygame.draw.rect(self.screen, self.accent_color, bar_fill_rect)
            else:
                pygame.draw.rect(self.screen, self.accent_color, bar_bg_rect, 1)
    
    def wrap_text(self, text, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def is_mouse_over_button(self):
        """Check if mouse is over the send button"""
        mouse_pos = pygame.mouse.get_pos()
        return self.send_button.collidepoint(mouse_pos)
    
    def is_mouse_over_speech_button(self):
        """Check if mouse is over the speech toggle button"""
        mouse_pos = pygame.mouse.get_pos()
        return self.speech_button.collidepoint(mouse_pos)
    
    def send_message(self):
        """Process user input and get therapist response"""
        if not self.input_text.strip():
            return
        
        user_message = self.input_text.strip()
        self.add_message("You", user_message, "neutral", "neutral")
        self.input_text = ""
        
        self.stop_speaking()

        result = self.therapist.respond(user_message)

        self.add_message(
            "Ayane", 
            result["response"], 
            result["emotion_detected"], 
            result["therapist_expression"]
        )
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_active = True
                elif self.send_button.collidepoint(event.pos):
                    self.send_message()
                elif self.speech_button.collidepoint(event.pos):
                    self.toggle_speech()
                else:
                    self.input_active = False
            
            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.send_message()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
        
        return True
    
    def update(self):
        """Update UI elements"""
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def run(self):
        """Main loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.screen.fill(self.bg_color)
            self.draw_chat()
            self.draw_avatar()
            self.draw_emotion_meter()

            pygame.display.flip()
            clock.tick(60)

        self.stop_speaking()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    if not os.path.exists("assets"):
        print("Warning: 'assets' directory not found. Creating directory.")
        os.makedirs("assets")
        print("Please place your therapist expression images in the 'assets' directory.")
        print("The files should be named: neutral.jpeg, smiling.jpeg, concerned.jpeg, etc.")
    
    try:
        import pyttsx3
    except ImportError:
        print("Error: pyttsx3 module is not installed.")
        print("Please install it using: pip install pyttsx3")
        sys.exit(1)
    
    app = TherapistGUI()
    app.run()