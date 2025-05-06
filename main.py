# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# import os
# import logging
# from langchain_groq import ChatGroq
# from langchain.schema import SystemMessage, HumanMessage
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# class PromptRequest(BaseModel):
#     prompt: str

# class CodeGenerator:
#     def react_code_generation(self, payload: PromptRequest):
#         try:
#             system_prompt = "You are an expert React developer. Generate complete React component code based on the user's prompt."
#             user_prompt = payload.prompt

#             messages = [
#                 SystemMessage(content=system_prompt),
#                 HumanMessage(content=user_prompt)
#             ]

#             llm = ChatGroq(
#                 model="meta-llama/llama-4-scout-17b-16e-instruct",
#                 temperature=0,
#                 api_key=os.getenv("GROQ_API_KEY")
#             )

#             response = llm.invoke(messages)

#             result = {
#                 "message": "UI code generation successful.",
#                 "code": response.content
#             }

#             return JSONResponse(content=result)

#         except Exception as e:
#             logging.error(f"Error generating UI code: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Error generating UI: {str(e)}")

# generator = CodeGenerator()

# @app.post("/generate-ui")
# def generate_ui(payload: PromptRequest):
#     return generator.react_code_generation(payload)

#################### VERSION-1 #####################################


##################### VERSION-2 #########################################


# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# import os
# import logging
# from langchain_groq import ChatGroq
# from langchain.schema import SystemMessage, HumanMessage
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# class PromptRequest(BaseModel):
#     prompt: str

# def load_system_prompt(file_path: str) -> str:
#     """
#     Reads the system prompt from a text file.

#     Args:
#         file_path (str): Path to the text file containing the system prompt.
    
#     Returns:
#         str: The content of the file.
#     """
#     try:
#         with open(file_path, "r", encoding="utf-8") as prompt_file:
#             content = prompt_file.read()
#             return content
#     except FileNotFoundError:
#         logging.error(f"System prompt file not found at {file_path}")
#         raise
#     except Exception as e:
#         logging.error(f"Error reading the system prompt file: {str(e)}")
#         raise

# class CodeGenerator:
#     def react_code_generation(self, payload: PromptRequest):
#         try:
#             # Load a more complex system prompt from an external text file.
#             system_prompt = load_system_prompt("system_prompt.txt")
#             user_prompt = payload.prompt

#             messages = [
#                 SystemMessage(content=system_prompt),
#                 HumanMessage(content=user_prompt)
#             ]

#             llm = ChatGroq(
#                 model="meta-llama/llama-4-scout-17b-16e-instruct",
#                 temperature=0,
#                 api_key=os.getenv("GROQ_API_KEY")
#             )

#             response = llm.invoke(messages)

#             result = {
#                 "message": "UI code generation successful.",
#                 "code": response.content
#             }

#             return JSONResponse(content=result)

#         except Exception as e:
#             logging.error(f"Error generating UI code: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Error generating UI: {str(e)}")

# generator = CodeGenerator()

# @app.post("/generate-ui")
# def generate_ui(payload: PromptRequest):
#     return generator.react_code_generation(payload)


##################### VERSION-2 #########################################

##################### VERSION-3 #########################################

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import logging
import re
import zipfile
import io
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

def load_system_prompt(file_path: str) -> str:
    """
    Load the system prompt from a text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error loading system prompt: {str(e)}")
        raise HTTPException(status_code=500, detail="System prompt not found.")

class CodeGenerator:
    def generate_project_scaffold(self, payload: PromptRequest):
        try:
            # Load the complex system prompt from an external file
            system_prompt = load_system_prompt("system_prompt.txt")
            user_prompt = payload.prompt

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            # Create the LLM instance and invoke it with the messages
            llm = ChatGroq(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                temperature=0,
                api_key=os.getenv("GROQ_API_KEY")
            )
            response = llm.invoke(messages)

            # Parse the generated output to extract individual file data.
            # The expected format is using custom tags:
            # <boltAction type="file" filePath="filename"> ... file contents ... </boltAction>
            pattern = r'<boltAction\s+type="file"\s+filePath="([^"]+)">(.*?)</boltAction>'
            matches = re.findall(pattern, response.content, re.DOTALL)
            
            if not matches:
                logging.error("No files found in the generated scaffold.")
                raise HTTPException(status_code=500, detail="No files found in the generated scaffold.")

            # Create an in-memory zip archive containing all the files
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for file_path, file_content in matches:
                    # Clean up file content if necessary
                    clean_content = file_content.strip()
                    zip_file.writestr(file_path, clean_content)
            
            zip_buffer.seek(0)

            # Return the zip file as a downloadable response
            headers = {"Content-Disposition": 'attachment; filename="project_scaffold.zip"'}
            return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)

        except Exception as e:
            logging.error(f"Error generating project scaffold: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating project scaffold: {str(e)}")

generator = CodeGenerator()

@app.post("/download-ui")
def download_ui(payload: PromptRequest):
    return generator.generate_project_scaffold(payload)


##################### VERSION-3 #########################################