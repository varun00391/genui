# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import os
# import httpx
# from executor import parse_actions, execute_actions
# from dotenv import load_dotenv

# load_dotenv()

# # Load environment
# # GROQ_API_URL = os.getenv("GROQ_API_URL")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# # SYSTEM_PROMPT = "<bolt system prompt goes here>"

# # Load system prompt from file
# with open(os.path.join(os.path.dirname(__file__), "system_prompt.txt"), "r", encoding="utf-8") as f:
#     SYSTEM_PROMPT = f.read()

# app = FastAPI()

# class ChatRequest(BaseModel):
#     prompt: str

# class ChatResponse(BaseModel):
#     artifact: str

# @app.post("/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest):
#     # if not GROQ_API_URL or not GROQ_API_KEY:
#     #     raise HTTPException(status_code=500, detail="API credentials not set")

#     if not GROQ_API_KEY :
#         raise HTTPException(status_code=500, detail="API credentials not set")

#     # Prepare payload
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": req.prompt}
#     ]

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     async with httpx.AsyncClient() as client:
#         resp = await client.post(
#             GROQ_API_URL,
#             headers=headers,
#             json={"model": "llama4", "messages": messages}
#         )
#         resp.raise_for_status()
#         data = resp.json()
#         artifact = data.get("choices", [])[0].get("message", {}).get("content", "")

#     # Optionally: parse and execute
#     actions = parse_actions(artifact)
#     execute_actions(actions)

#     return ChatResponse(artifact=artifact)


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import os
# import httpx
# from dotenv import load_dotenv
# from executor import parse_actions, execute_actions

# # Load environment variables from .env
# load_dotenv()

# # Access API credentials from environment
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Load system prompt from file
# SYSTEM_PROMPT_PATH = "backend/system_prompt.txt"
# if os.path.exists(SYSTEM_PROMPT_PATH):
#     with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
#         SYSTEM_PROMPT = f.read()
# else:
#     SYSTEM_PROMPT = "no system prompt provided"

# app = FastAPI()

# class ChatRequest(BaseModel):
#     prompt: str

# class ChatResponse(BaseModel):
#     artifact: str

# @app.post("/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest):
#     if not GROQ_API_KEY:
#         raise HTTPException(status_code=500, detail="API credentials not set")

#     # Prepare payload
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": req.prompt}
#     ]

#     # headers = {
#     #     "Authorization": f"Bearer {GROQ_API_KEY}",
#     #     "Content-Type": "application/json"
#     # }
#     # GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

#     async with httpx.AsyncClient() as client:
#         resp = await client.post(
#             json={"model": "meta-llama/llama-4-maverick-17b-128e-instruct", "messages": messages}
#         )
#         resp.raise_for_status()
#         data = resp.json()
#         artifact = data.get("choices", [])[0].get("message", {}).get("content", "")

#     # Optionally: parse and execute
#     actions = parse_actions(artifact)
#     execute_actions(actions)

#     return ChatResponse(artifact=artifact)


# import os
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# # Hypothetical Chatgroq LLM library. Replace this with the actual import if different.
# from langchain_groq import ChatGroq
# import os

# # Set your Chatgroq API key from an environment variable.
# os.environ['GROQ_API_KEY']= ""   #os.getenv("CHATGROQ_API_KEY")

# app = FastAPI(title="React Code Generator API")


# class GenerateRequest(BaseModel):
#     user_input: str


# def load_system_prompt(filepath: str = "system_prompt.txt") -> str:
#     """
#     Reads the system prompt text from a local file.
#     """
#     try:
#         with open(filepath, "r", encoding="utf-8") as file:
#             return file.read()
#     except Exception as e:
#         raise Exception(f"Unable to load system prompt from {filepath}: {e}")


# def generate_react_code(user_input: str, system_prompt: str) -> str:
#     """
#     Calls the Chatgroq LLM with a system prompt (loaded from file)
#     and user input to generate React code.
#     """
#     try:
#         # Invoke the LLM
#         llm = ChatGroq(
#             model="meta-llama/llama-4-scout-17b-16e-instruct", 
#             temperature=0, 
#             api_key=os.getenv("GROQ_API_KEY")
#         )
        
#         response = llm.invoke(messages)
    
#         # Parse and return the generated code.
#         generated_code = response["choices"][0]["message"]["content"]
#         return generated_code.strip()
#     except Exception as e:
#         raise Exception(f"LLM generation error: {e}")


# @app.post("/generate-react-code")
# async def generate_code(request_data: GenerateRequest):
#     """
#     Endpoint that reads the system prompt from a file, calls the Chatgroq-based LLM
#     with the user input, and returns the generated React code.
#     """
#     try:
#         system_prompt = load_system_prompt()
#         react_code = generate_react_code(request_data.user_input, system_prompt)
#         return {"react_code": react_code}
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=str(exc))


import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Hypothetical Chatgroq LLM library. Replace this with the actual import if different.
from langchain_groq import ChatGroq

# Load API keys and settings from .env
load_dotenv()

# Ensure that the GROQ API key is set in the environment before running the app.
# For example, your .env file should contain:
# GROQ_API_KEY=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

app = FastAPI(title="React Code Generator API")


class GenerateRequest(BaseModel):
    user_input: str


def load_system_prompt(filepath: str = "system_prompt.txt") -> str:
    """
    Reads the system prompt text from a local file.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Unable to load system prompt from {filepath}: {e}")

# # Define the system prompt as a constant.
# SYSTEM_PROMPT = (
#     "You are a skilled React developer. Provide clean, modular, and well-commented React code."
# )
SYSTEM_PROMPT = load_system_prompt()

def generate_react_code(user_input: str, system_prompt: str) -> str:
    """
    Calls the Chatgroq LLM with a system prompt (loaded from file)
    and user input to generate React code.
    """
    try:
        # Build the conversation messages.
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
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


@app.post("/generate-react-code")
async def generate_code(request_data: GenerateRequest):
    """
    Endpoint that reads the system prompt from a file, calls the Chatgroq-based LLM
    with the user input, and returns the generated React code.
    """
    try:
        system_prompt = SYSTEM_PROMPT
        react_code = generate_react_code(request_data.user_input, system_prompt)
        return {"react_code": react_code}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))



