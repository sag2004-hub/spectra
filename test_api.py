import requests
from config.settings import Config

def test_api():
    try:
        # Debug: check if key is loaded from .env
        if not Config.GROK_API_KEY:
            print("❌ No API key found in .env (GROK_API_KEY missing).")
            return False
        else:
            print(f"🔑 Loaded API key (masked): {Config.GROK_API_KEY[:6]}...")

        # Gemini endpoint (v1beta generateContent)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={Config.GROK_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {"parts": [{"text": "Hello, can you hear me?"}]}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        print(f"HTTP {response.status_code}")
        try:
            print(response.json())
        except Exception:
            print("⚠️ Could not parse JSON response.")

        if response.status_code == 200:
            print("✅ API key is valid and Gemini responded!")
            return True
        else:
            print("❌ Something went wrong with the request.")
            return False

    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    test_api()
