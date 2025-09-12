import subprocess
import os
import sys

class IDEController:
    @staticmethod
    def open_vscode(project_path):
        """Open VS Code with the specified project"""
        try:
            if sys.platform == "win32":
                subprocess.Popen(["code", project_path], shell=True)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", "-a", "Visual Studio Code", project_path])
            else:  # Linux
                subprocess.Popen(["code", project_path])
            return True
        except Exception as e:
            print(f"Error opening VS Code: {e}")
            return False
    
    @staticmethod
    def run_code(filepath, language):
        """Run the generated code based on language"""
        try:
            if language == "python":
                result = subprocess.run([sys.executable, filepath], 
                                      capture_output=True, text=True, cwd=os.path.dirname(filepath))
                return result.stdout, result.stderr
            elif language == "javascript":
                result = subprocess.run(["node", filepath], 
                                      capture_output=True, text=True, cwd=os.path.dirname(filepath))
                return result.stdout, result.stderr
            # Add other languages as needed
            else:
                return f"Code generated successfully for {language}", ""
        except Exception as e:
            return "", f"Error running code: {str(e)}"