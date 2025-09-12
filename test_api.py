from groq import Groq
from config.settings import Config

def test_api():
    try:
        client = Groq(api_key=Config.GROQ_API_KEY)
        models = client.models.list()
        print("✅ API key is valid!")
        print("Available models:")
        for model in models.data:
            print(f"  - {model.id}")
        return True
    except Exception as e:
        print(f"❌ API key error: {e}")
        return False

if __name__ == "__main__":
    test_api()