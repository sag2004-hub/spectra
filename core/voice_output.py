from gtts import gTTS
import pygame
import pyttsx3
import threading
import tempfile
import os
from config.settings import Config

class VoiceOutput:
    def __init__(self):
        pygame.mixer.init()
        self.use_gtts = Config.USE_INTERNET_TTS
        
        # Initialize pyttsx3 as fallback
        self.engine = None
        try:
            self.engine = pyttsx3.init()
            # Configure pyttsx3
            self.engine.setProperty('rate', 180)
            self.engine.setProperty('volume', 0.9)
            
            # Try to find Indian voice
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'india' in voice.name.lower() or 'indian' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        except Exception as e:
            print(f"Failed to initialize pyttsx3: {e}")
    
    def speak(self, text):
        """Convert text to speech with Indian accent"""
        def _speak():
            if self.use_gtts:
                success = self._speak_gtts(text)
                if not success and self.engine:
                    self._speak_pyttsx3(text)
            elif self.engine:
                self._speak_pyttsx3(text)
            else:
                print(f"TTS not available: {text}")
        
        # Run in a thread to avoid blocking
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()
        thread.join(timeout=10)  # Wait for speech to complete with timeout
    
    def _speak_gtts(self, text):
        """Use gTTS for speech with Indian accent"""
        try:
            # Ensure temp directory exists
            temp_dir = tempfile.gettempdir()
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            temp_file = os.path.join(temp_dir, "spectra_tts.mp3")
            
            # Create gTTS with Indian English accent
            tts = gTTS(text=text, lang='en', tld='co.in')
            tts.save(temp_file)
            
            # Play audio with pygame
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.music.unload()
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            return True
        except Exception as e:
            print(f"gTTS failed: {e}, falling back to pyttsx3")
            self.use_gtts = False  # Disable gTTS for future requests
            return False
    
    def _speak_pyttsx3(self, text):
        """Use pyttsx3 as fallback"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"pyttsx3 also failed: {e}")