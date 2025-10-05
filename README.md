# Therapist Companion

A GUI-based AI therapist companion application built with Pygame and powered by Google's Gemini AI.

## 🎯 Demo

### Live Application Screenshots

**Initial Conversation - Emotion Detection:**
![Happy Emotion Detection](screenshots/Screenshot%20(1077).png)

*User expresses happiness, AI detects emotion and responds with smiling expression*



**Complex Emotion Handling - Interview Anxiety:**
![Anxiety Detection](screenshots/Screenshot%20(1079).png)

*AI processes mixed emotions and provides empathetic response*



### Key Visual Features Shown:
- **Dynamic facial expressions** that change based on conversation context
- **Real-time emotion detection bars** showing confidence levels for each emotion
- **Professional therapist avatar** with multiple expressions
- **Clean chat interface** with timestamp and speaker identification
- **Emotion visualization panel** displaying current emotional state

## 🛠️ Technologies Used

- **Python 3.8+** - Core programming language
- **Pygame** - GUI framework and graphics rendering
- **Google Gemini AI** - Conversational AI and natural language processing
- **pyttsx3** - Text-to-speech functionality
- **python-dotenv** - Environment variable management
- **Threading** - Non-blocking audio processing
- **PyInstaller** - Executable creation for distribution

## 🎨 Features

- 🤖 AI-powered therapeutic conversations
- 🎭 Dynamic facial expressions (10+ emotions)
- 📊 Real-time emotion detection and visualization
- 🗣️ Text-to-speech functionality
- 💬 Conversation history management
- 🎨 Responsive GUI with golden ratio design

## 🚀 Quick Start

### Windows
```bash
# Run the setup script
setup.bat

# After setup, run the application
venv\Scripts\python.exe main.py
```

### Linux/macOS
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# After setup, run the application
source venv/bin/activate
python main.py
```

## 📋 Requirements

- Python 3.8+
- Google Gemini API key
- Internet connection (for AI features)

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment options including:

- **Standalone Executable**: For easy distribution to end users
- **Docker**: For containerized deployment
- **Cloud**: AWS, GCP, Azure deployment guides

### Quick Executable Build
```bash
# Build executable
python build_executable.py
```

## 📁 Project Structure
```
therapist-companion/
├── main.py              # Main GUI application
├── llm.py               # AI therapist logic
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys)
├── assets/              # Therapist expression images
├── build_executable.py  # Build script for standalone exe
├── Dockerfile          # Container deployment
├── docker-compose.yml  # Container orchestration
└── DEPLOYMENT.md       # Deployment guide
```

## 🔒 Environment Variables
```env
API=your_google_gemini_api_key
```

## 📄 License

This project is provided as-is for educational and personal use.