from groq import Groq
from config.settings import Config
import requests

class CodeGenerator:
    def __init__(self):
        if not Config.GROQ_API_KEY or Config.GROQ_API_KEY == "your_groq_api_key_here":
            raise ValueError("❌ Missing or invalid GROQ_API_KEY in .env")
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.api_working = None  # Cache API status
        
    def generate_code(self, prompt, language="python"):
        """Generate code based on natural language prompt"""
        system_prompt = f"""You are Spectra, an expert AI coding assistant. Generate clean, well-commented, functional code based on the user's request.

Rules:
- Provide complete, runnable code
- Include necessary imports and dependencies  
- Add helpful comments for complex logic
- Follow best practices for {language}
- Make the code production-ready
- If creating a GUI or visual application, make it functional and attractive

Language: {language}
User Request: {prompt}"""

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",  # Using more capable model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more focused code generation
                max_tokens=8000,  # Increased token limit for complex code
                top_p=0.9
            )
            
            generated_code = completion.choices[0].message.content.strip()
            
            # Clean up the code (remove markdown formatting if present)
            if generated_code.startswith("```"):
                lines = generated_code.split('\n')
                # Remove first line with ```language
                if lines[0].startswith("```"):
                    lines = lines[1:]
                # Remove last line with ```
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                generated_code = '\n'.join(lines)
            
            self.api_working = True
            return generated_code
            
        except Exception as e:
            print(f"Groq API Error: {e}")
            self.api_working = False
            return self._get_fallback_code(prompt, language)
    
    def _get_fallback_code(self, prompt, language):
        """Provide more sophisticated fallback code when API is unavailable"""
        fallback_templates = {
            "python": {
                "web scraping": '''import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """Scrape website content"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    url = "https://example.com"
    content = scrape_website(url)
    print(content)''',
                
                "gui": '''import tkinter as tk
from tkinter import ttk

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spectra Application")
        self.root.geometry("400x300")
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Welcome to Spectra", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input field
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(main_frame, textvariable=self.input_var, width=30)
        input_entry.pack(pady=5)
        
        # Button
        action_button = ttk.Button(main_frame, text="Execute", 
                                  command=self.on_button_click)
        action_button.pack(pady=10)
        
        # Output area
        self.output_text = tk.Text(main_frame, height=10, width=50)
        self.output_text.pack(pady=5, fill=tk.BOTH, expand=True)
    
    def on_button_click(self):
        user_input = self.input_var.get()
        self.output_text.insert(tk.END, f"Processed: {user_input}\\n")
        self.input_var.set("")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()''',
                
                "api": '''import flask
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Sample data
data_store = []

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Spectra API", "status": "active"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data": data_store, "count": len(data_store)})

@app.route('/api/data', methods=['POST'])
def add_data():
    try:
        new_item = request.get_json()
        if new_item:
            data_store.append(new_item)
            return jsonify({"message": "Data added successfully", "item": new_item}), 201
        return jsonify({"error": "No data provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    try:
        if 0 <= item_id < len(data_store):
            deleted_item = data_store.pop(item_id)
            return jsonify({"message": "Data deleted", "item": deleted_item})
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)''',
                
                "default": '''# Python code generated by Spectra
import os
import sys
from datetime import datetime

def main():
    """Main function"""
    print("🌟 Code generated by Spectra")
    print(f"📅 Generated at: {datetime.now()}")
    print(f"💻 Python version: {sys.version}")
    
    # Your code logic here based on the prompt:
    # ''' + prompt + '''
    
    print("✅ Code execution completed!")

if __name__ == "__main__":
    main()'''
            },
            
            "javascript": {
                "web": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spectra Web App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; margin-bottom: 20px; }
        .input-section { margin: 20px 0; }
        .input-section input, .input-section button { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; }
        .input-section button { background: #007bff; color: white; cursor: pointer; }
        .input-section button:hover { background: #0056b3; }
        .output { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 Spectra JavaScript App</h1>
            <p>Interactive web application</p>
        </div>
        
        <div class="input-section">
            <input type="text" id="userInput" placeholder="Enter your input here...">
            <button onclick="processInput()">Process</button>
            <button onclick="clearOutput()">Clear</button>
        </div>
        
        <div class="output" id="output">
            <p>Welcome! Enter something above and click Process.</p>
        </div>
    </div>

    <script>
        function processInput() {
            const input = document.getElementById('userInput').value;
            const output = document.getElementById('output');
            
            if (input.trim()) {
                const timestamp = new Date().toLocaleTimeString();
                output.innerHTML += `<p><strong>${timestamp}:</strong> Processed "${input}"</p>`;
                document.getElementById('userInput').value = '';
            }
        }
        
        function clearOutput() {
            document.getElementById('output').innerHTML = '<p>Output cleared.</p>';
        }
        
        // Allow Enter key to process input
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                processInput();
            }
        });
        
        console.log("🌟 Spectra JavaScript App loaded successfully!");
    </script>
</body>
</html>''',
                
                "default": '''// JavaScript code generated by Spectra
console.log("🌟 Spectra JavaScript Generator");
console.log("📅 Generated at:", new Date().toISOString());

// Main application logic
class SpectraApp {
    constructor() {
        this.data = [];
        this.initialize();
    }
    
    initialize() {
        console.log("🚀 Initializing Spectra App...");
        // Your code logic here based on: ''' + prompt + '''
        this.run();
    }
    
    run() {
        console.log("▶️ Running application...");
        // Add your main application logic here
    }
    
    processData(input) {
        console.log("📊 Processing data:", input);
        this.data.push({
            timestamp: Date.now(),
            input: input,
            processed: true
        });
        return this.data;
    }
}

// Initialize the application
const app = new SpectraApp();
console.log("✅ Spectra App initialized successfully!");'''
            }
        }
        
        # Detect what type of code to generate based on keywords
        prompt_lower = prompt.lower()
        
        if language == "python":
            if any(keyword in prompt_lower for keyword in ["scrape", "web", "crawl", "beautifulsoup"]):
                return fallback_templates["python"]["web scraping"]
            elif any(keyword in prompt_lower for keyword in ["gui", "tkinter", "interface", "window"]):
                return fallback_templates["python"]["gui"]
            elif any(keyword in prompt_lower for keyword in ["api", "flask", "server", "endpoint"]):
                return fallback_templates["python"]["api"]
            else:
                return fallback_templates["python"]["default"]
        
        elif language == "javascript":
            if any(keyword in prompt_lower for keyword in ["web", "html", "browser", "frontend"]):
                return fallback_templates["javascript"]["web"]
            else:
                return fallback_templates["javascript"]["default"]
        
        elif language == "html":
            return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spectra Generated Page</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .container { max-width: 1000px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
        .header { text-align: center; margin-bottom: 30px; }
        .content { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 Generated by Spectra</h1>
            <p>Beautiful, modern web page</p>
        </div>
        <div class="content">
            <h2>Your Content Here</h2>
            <p>This page was generated based on: <em>''' + prompt + '''</em></p>
            <p>Customize this template to match your specific requirements.</p>
        </div>
    </div>
</body>
</html>'''
        
        else:
            return f"""# {language.upper()} code generated by Spectra
# Generated for: {prompt}
# 
# This is a basic template. The AI service is currently unavailable,
# but you can modify this code according to your requirements.

def main():
    print("Hello from Spectra!")
    # Add your {language} code here

if __name__ == "__main__":
    main()"""
    
    def detect_language(self, prompt):
        """Detect programming language from natural language request"""
        # Simple keyword-based detection as fallback
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["python", "django", "flask", "pandas", "numpy", "tkinter"]):
            return "python"
        elif any(word in prompt_lower for word in ["javascript", "js", "react", "node", "vue", "angular"]):
            return "javascript"  
        elif any(word in prompt_lower for word in ["java", "spring", "android"]):
            return "java"
        elif any(word in prompt_lower for word in ["c++", "cpp", "cplusplus"]):
            return "cpp"
        elif any(word in prompt_lower for word in ["html", "web page", "website"]):
            return "html"
        elif any(word in prompt_lower for word in ["css", "stylesheet", "styling"]):
            return "css"
        elif any(word in prompt_lower for word in ["sql", "database", "query"]):
            return "sql"
        elif any(word in prompt_lower for word in ["bash", "shell", "script"]):
            return "bash"
        else:
            return "python"  # Default fallback
        
        # If API is available, use AI detection
        if self.api_working:
            try:
                detection_prompt = f"""Based on this request, return ONLY the programming language name (one word):
                python, javascript, java, cpp, html, css, sql, bash
                
                Request: {prompt}"""
                
                completion = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": detection_prompt}],
                    temperature=0.1,
                    max_tokens=10
                )
                language = completion.choices[0].message.content.lower().strip()
                
                # Map variations to standard names
                mapping = {
                    "python": "python", "py": "python",
                    "javascript": "javascript", "js": "javascript", "node": "javascript",
                    "java": "java",
                    "c++": "cpp", "cpp": "cpp", "cplusplus": "cpp",
                    "html": "html", "web": "html",
                    "css": "css",
                    "sql": "sql",
                    "bash": "bash", "shell": "bash"
                }
                return mapping.get(language, "python")
            except:
                pass
        
        return "python"  # Ultimate fallback