# Spectra 🪐

**Spectra** is an AI-powered voice coding assistant that listens for your commands, generates code, and opens your project in VS Code—all hands-free!

## 🚀 Features

- 🎤 Voice-activated coding (wake word: configurable)
- 🤖 AI code generation (Groq API, Llama-3)
- 🗂️ Automatic file/project creation
- 🖥️ VS Code integration
- 🟢 Animated floating orb UI
- 🗣️ Voice feedback (gTTS/pyttsx3 fallback)
- 🧠 Multi-language support (Python, JavaScript, Java, C++, HTML, CSS)

## 🛠️ Setup

1. **Clone the repo**
   ```sh
   git clone https://github.com/yourusername/spectra.git
   cd spectra
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file**
   ```
   GROQ_API_KEY=your_groq_api_key_here
   WAKE_WORD=spectra
   ```

5. **Run Spectra**
   ```sh
   python main.py
   ```

## 📝 Usage

- Say the wake word (default: "spectra") to activate.
- Give your coding command (e.g., "Create a Python script named hello_world that prints Hello World").
- Spectra will generate code, create the file, and open it in VS Code.
- Supported languages: Python, JavaScript, Java, C++, HTML, CSS.

## ⚡ Troubleshooting

- Make sure your microphone is working and selected.
- Install [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) if you get audio errors:
  ```sh
  pip install pyaudio
  ```
- If gTTS fails, pyttsx3 will be used for voice output.
- Check your Groq API key in `.env`.

## 💡 Credits

- Built with [PyQt5](https://riverbankcomputing.com/software/pyqt/), [SpeechRecognition](https://pypi.org/project/SpeechRecognition/), [gTTS](https://pypi.org/project/gTTS/), [Groq API](https://groq.com/), and [Llama-3](https://llama.meta.com/).

---

Made with ❤️ by yourusername
