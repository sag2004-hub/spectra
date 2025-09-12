import speech_recognition as sr
from config.settings import Config

class VoiceInput:
    def __init__(self, device_index=None):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        try:
            # List available microphones
            print("Available microphones:")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"{index}: {name}")
            
            # Try to use the default microphone
            self.microphone = sr.Microphone(device_index=device_index)
            self.adjust_for_ambient_noise()
        except Exception as e:
            print(f"[Microphone Error] {e}")
            # Try to use any available microphone
            try:
                self.microphone = sr.Microphone()
                self.adjust_for_ambient_noise()
            except Exception as e2:
                print(f"[Fallback Microphone Error] {e2}")

    def adjust_for_ambient_noise(self):
        if not self.microphone:
            return
        try:
            with self.microphone as source:
                print("[Init] Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
        except Exception as e:
            print(f"[Ambient Noise Error] {e}")

    def listen_for_wake_word(self):
        """Listen once for wake word, return True if detected"""
        if not self.microphone:
            print("[Wake Word] No microphone available.")
            return False

        try:
            with self.microphone as source:
                print(f"[Wake Word] Listening for '{Config.WAKE_WORD}'...")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"[Heard] {text}")

                # Accept variants
                wake_variants = [Config.WAKE_WORD.lower(), "spectra", "specter", "spektra", "spectro"]
                if any(word in text for word in wake_variants):
                    print("[Wake Word Detected ✅]")
                    return True
        except sr.WaitTimeoutError:
            print("[Wake Word] Timeout")
        except sr.UnknownValueError:
            print("[Wake Word] Could not understand")
        except Exception as e:
            print(f"[Wake Word Error] {e}")

        return False

    def get_audio_input(self):
        """Capture full command after wake word"""
        if not self.microphone:
            return "Error: No microphone available."

        try:
            with self.microphone as source:
                print("[Command] Listening...")
                audio = self.recognizer.listen(source, phrase_time_limit=8)
                text = self.recognizer.recognize_google(audio)
                print(f"[Command Heard] {text}")
                return text
        except sr.UnknownValueError:
            print("[Command] Could not understand")
            return "Sorry, I didn't catch that."
        except Exception as e:
            print(f"[Command Error] {e}")
            return f"Error: {str(e)}"