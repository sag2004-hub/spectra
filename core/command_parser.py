import re

class CommandParser:
    @staticmethod
    def parse_command(command):
        """Extract intent and parameters from voice command"""
        if not command or "sorry" in command.lower() or "error" in command.lower():
            return {
                "language": "python",
                "project_name": None,
                "raw_command": command
            }
            
        command = command.lower()
        
        # Check for website commands first
        website_commands = ["open youtube", "open you tube", "open chatgpt", 
                           "open chat gpt", "open google", "open github", "open git hub"]
        
        if any(cmd in command for cmd in website_commands):
            return {
                "language": "website",
                "project_name": None,
                "raw_command": command
            }
        
        # Detect language
        language_keywords = {
            "python": ["python", "py"],
            "javascript": ["javascript", "js", "node"],
            "java": ["java"],
            "cpp": ["c++", "cpp", "c plus plus"],
            "html": ["html", "web page"],
            "css": ["css", "stylesheet"]
        }
        
        detected_language = "python"  # default
        for lang, keywords in language_keywords.items():
            if any(keyword in command for keyword in keywords):
                detected_language = lang
                break
        
        # Extract project name if specified
        project_name = None
        name_match = re.search(r'(?:named|called|as) (\w+)', command)
        if name_match:
            project_name = name_match.group(1)
        
        return {
            "language": detected_language,
            "project_name": project_name,
            "raw_command": command
        }