import os
import re
from datetime import datetime
from config.settings import Config

class FileManager:
    def __init__(self):
        self.base_dir = Config.CODE_DIRECTORY
        os.makedirs(self.base_dir, exist_ok=True)
    
    def create_file(self, code, language, project_name=None):
        """Create a file with the generated code"""
        if not project_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"project_{timestamp}"
        
        project_path = os.path.join(self.base_dir, project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # Determine file extension
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "cpp": "cpp",
            "html": "html",
            "css": "css"
        }
        
        extension = extensions.get(language, "txt")
        filename = f"main.{extension}" if language not in ["html", "css"] else f"index.{extension}"
        filepath = os.path.join(project_path, filename)
        
        # Clean up code (remove markdown code blocks if present)
        clean_code = re.sub(r"```(?:\w+)?\s*(.*?)\s*```", r"\1", code, flags=re.DOTALL)
        clean_code = clean_code.strip()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean_code)
        
        print(f"File created at: {filepath}")
        return filepath, project_path