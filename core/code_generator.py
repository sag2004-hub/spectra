from groq import Groq
from config.settings import Config
import requests

class CodeGenerator:
    def __init__(self):
        if not Config.GROQ_API_KEY or Config.GROQ_API_KEY == "your_groq_api_key_here":
            raise ValueError("❌ Missing or invalid GROQ_API_KEY in .env")
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        
    def generate_code(self, prompt, language="python"):
        """Generate code based on natural language prompt"""
        # If API key is invalid, provide a simple code template
        if not self._check_api_key():
            return self._get_fallback_code(prompt, language)
            
        system_prompt = f"""
        You are Spectra, an AI coding assistant. Generate clean, functional code based on the user's request.
        Always provide only the code without explanations unless asked. 
        The code should be complete and ready to run.
        Language: {language}
        """
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq API Error: {e}")
            return self._get_fallback_code(prompt, language)
    
    def _check_api_key(self):
        """Check if the API key is valid"""
        try:
            # Simple test request to check API key
            self.client.models.list()
            return True
        except:
            return False
    
    def _get_fallback_code(self, prompt, language):
        """Provide fallback code when API is unavailable"""
        if "python" in language:
            return '''# Simple Python program
print("Hello, World!")

# Add your code here based on: ''' + prompt
        
        elif "javascript" in language:
            return '''// Simple JavaScript program
console.log("Hello, World!");

// Add your code here based on: ''' + prompt
        
        elif "html" in language:
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Generated Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <!-- Add your content here based on: ''' + prompt + ''' -->
</body>
</html>'''
        
        else:
            return f"# Code for {language}\n# Based on: {prompt}"
    
    def detect_language(self, prompt):
        """Detect programming language from natural language request"""
        detection_prompt = f"""
        Based on the following request, determine the primary programming language needed.
        Return only the language name (python, javascript, java, cpp, html, css).
        
        Request: {prompt}
        """
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": detection_prompt}],
                temperature=0.1,
                max_tokens=10
            )
            language = completion.choices[0].message.content.lower().strip()
            mapping = {
                "python": "python", "py": "python",
                "javascript": "javascript", "js": "javascript",
                "java": "java",
                "c++": "cpp", "cpp": "cpp", "cplusplus": "cpp",
                "html": "html",
                "css": "css"
            }
            return mapping.get(language, "python")
        except Exception:
            return "python"  # fallback