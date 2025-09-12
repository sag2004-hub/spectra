import sys
import os
import threading
import webbrowser
from PyQt5.QtWidgets import QApplication, QMessageBox

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from core.voice_input import VoiceInput
from core.voice_output import VoiceOutput
from core.code_generator import CodeGenerator
from core.file_manager import FileManager
from core.ide_controller import IDEController
from core.command_parser import CommandParser
from ui.orb_ui import AnimatedOrb

def check_pyaudio():
    try:
        import pyaudio
        return True
    except ImportError:
        return False

class Spectra:
    def __init__(self):
        # Check for PyAudio before initializing VoiceInput
        if not check_pyaudio():
            # Show error dialog and exit
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "Missing Dependency",
                "PyAudio is not installed.\nPlease install it with:\n\npip install pyaudio")
            sys.exit(1)
        
        self.voice_input = VoiceInput()
        self.voice_output = VoiceOutput()
        self.code_gen = CodeGenerator()
        self.file_mgr = FileManager()
        self.ide_ctrl = IDEController()
        self.parser = CommandParser()
        
        # Create UI
        self.app = QApplication(sys.argv)
        self.orb = AnimatedOrb()
        self.orb.show()
        
    def run(self):
        """Main execution loop"""
        print("Spectra activated. Waiting for wake word...")
        self.voice_output.speak("Spectra activated. Waiting for your command.")
        
        # Start listening for wake word in a separate thread
        wake_word_thread = threading.Thread(target=self._wake_word_listener)
        wake_word_thread.daemon = True
        wake_word_thread.start()
        
        sys.exit(self.app.exec_())
    
    def _wake_word_listener(self):
        """Listen for wake word in background thread"""
        while True:
            if self.voice_input.listen_for_wake_word():
                # Wake word detected
                self.orb.set_listening_state(True)
                self._process_command()
                self.orb.set_listening_state(False)
    
    def _process_command(self):
        """Process user command after wake word"""
        self.voice_output.speak("Yes, Tony?")
        command = self.voice_input.get_audio_input()
        
        if not command or "sorry" in command.lower() or "error" in command.lower():
            self.voice_output.speak("Let's try that again.")
            return
        
        print(f"Command received: {command}")
        
        # Check for website opening commands
        if self._handle_website_commands(command):
            return
            
        # Parse command
        parsed = self.parser.parse_command(command)
        
        # Generate code
        self.voice_output.speak("Generating code now.")
        code = self.code_gen.generate_code(command, parsed["language"])
        
        if code.startswith("⚠️") or code.startswith("Error") or "groq" in code.lower():
            self.voice_output.speak("I encountered an error generating the code. Please check your API key.")
            print(f"Code generation error: {code}")
            return
        
        # Create file
        filepath, project_path = self.file_mgr.create_file(
            code, parsed["language"], parsed["project_name"]
        )
        
        # Open VS Code
        self.voice_output.speak("Opening Visual Studio Code.")
        self.ide_ctrl.open_vscode(project_path)
        
        # Run code if it's executable
        if parsed["language"] in ["python", "javascript"]:
            self.voice_output.speak("Running the program now.")
            stdout, stderr = self.ide_ctrl.run_code(filepath, parsed["language"])
            
            if stderr:
                self.voice_output.speak("There was an error running the program.")
                print(f"Error: {stderr}")
            else:
                output_msg = stdout if stdout else "Program executed successfully."
                # Limit output length for speech
                if len(output_msg) > 100:
                    output_msg = output_msg[:100] + "..."
                self.voice_output.speak(f"Program output: {output_msg}")
        else:
            self.voice_output.speak("Code generated successfully.")
    
    def _handle_website_commands(self, command):
        """Handle website opening commands"""
        command_lower = command.lower()
        
        if "open youtube" in command_lower or "open you tube" in command_lower:
            self.voice_output.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            return True
            
        elif "open chatgpt" in command_lower or "open chat gpt" in command_lower:
            self.voice_output.speak("Opening ChatGPT")
            webbrowser.open("https://chat.openai.com")
            return True
            
        elif "open google" in command_lower:
            self.voice_output.speak("Opening Google")
            webbrowser.open("https://www.google.com")
            return True
            
        elif "open github" in command_lower or "open git hub" in command_lower:
            self.voice_output.speak("Opening GitHub")
            webbrowser.open("https://www.github.com")
            return True
            
        return False

if __name__ == "__main__":
    spectra = Spectra()
    spectra.run()