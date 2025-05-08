import os
import re
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq  # Adjust this import based on your actual library

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="React Code Generator API")

# ----------------------------
# Request and System Prompt
# ----------------------------
class GenerateRequest(BaseModel):
    user_input: str

def load_system_prompt(filepath: str = "backend/system_prompt.txt") -> str:
    """
    Reads the system prompt text from a local file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Unable to load system prompt from {filepath}: {e}")

# Load the system prompt (from file)
SYSTEM_PROMPT = load_system_prompt()  # file "system_prompt.txt" must exist

# ----------------------------
# LLM Code Generation
# ----------------------------
def generate_react_code(user_input: str, system_prompt: str) -> str:
    """
    Calls the ChatGroq LLM with a system prompt (loaded from file)
    and user input to generate React code.
    """
    try:
        # Build the conversation messages.
        # user_input = "create a non resonsive navigation bar with 1. agent dashboard 2. agent analysis 3. agent final conclusion"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input} # user_input
        ]
        
        # Initialize the ChatGroq model.
        llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            temperature=0, 
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Invoke the LLM with the messages.
        response = llm.invoke(messages)
    
        # Access the content attribute if response is an AIMessage object.
        generated_code = response.content
        return generated_code.strip()
    except Exception as e:
        raise Exception(f"LLM generation error: {e}")

# ----------------------------
# Parsing Actions from Code
# ----------------------------
def parse_actions(artifact_text: str):
    """
    Extracts and returns a list of (action_type, path, content) tuples 
    from artifact_text by matching <boltAction> tags.
    
    The regex captures:
      - The required 'type' attribute (file, shell, or start)
      - An optional 'filePath' or 'path' attribute
      - The content inside the <boltAction> ... </boltAction> tag.
    """
    pattern = re.compile(
        r'<boltAction\s+type="(?P<type>file|shell|start)"(?:\s+(?:filePath|path)="(?P<path>.*?)")?>'
        r'(?P<content>.*?)</boltAction>',
        re.DOTALL
    )
    return [
        (m.group('type'), m.group('path'), m.group('content').strip())
        for m in pattern.finditer(artifact_text)
    ]

# ----------------------------
# Execution of Parsed Actions
# ----------------------------
_started = False  # Global flag for "start" actions

def execute_actions(actions):
    """
    Iterates over the parsed actions and executes each based on its type.
    
    - For "file" actions: writes the content to the specified file path.
    - For "shell" actions: runs the given shell command.
    - For "start" actions: starts a process if not already started.
    """
    global _started
    for action_type, path, content in actions:
        if action_type == 'file':
            full_path = os.path.join('.', path.lstrip('/'))
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[FILE WRITTEN]: {full_path}")
        elif action_type == 'shell':
            print(f"[RUN SHELL]: {content}")
            result = subprocess.run(content, shell=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"[ERROR]: {result.stderr}")
        elif action_type == 'start':
            if _started:
                print("[SERVER ALREADY STARTED]")
                continue
            print(f"[START SERVER]: {content}")
            subprocess.Popen(content, shell=True)
            _started = True
        else:
            print(f"[UNKNOWN ACTION]: {action_type}")

# ----------------------------
# FastAPI Endpoint
# ----------------------------
@app.post("/generate-react-code")
async def generate_code(request_data: GenerateRequest):
    """
    Endpoint that:
      - Loads the system prompt from a file.
      - Generates React code using the ChatGroq LLM and the provided user input.
      - Parses the generated code for <boltAction> tags.
      - Executes the parsed actions (writing files, executing shell commands, etc.).
    Returns:
      - A JSON response containing the generated code and the count of executed actions.
    """
    try:
        # Use the loaded system prompt.
        system_prompt = SYSTEM_PROMPT  
        
        # Generate React code (expected to be a "boltArtifact")
        react_code = generate_react_code(request_data.user_input, system_prompt)
        
        # For debugging: print the generated code in the console.
        print("[Generated React Code]:")
        print(react_code)
        
        # Parse the generated artifact for individual actions.
        actions = parse_actions(react_code)
        
        # Execute each of the parsed actions.
        execute_actions(actions)
        
        return {
            "status": "success",
            "generated_code": react_code,
            "actions_executed": len(actions)
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
