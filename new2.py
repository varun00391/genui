from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import logging 
from pydantic import BaseModel, Field
from fastapi import HTTPException
from fastapi.responses import JSONResponse


class PromptRequest(BaseModel):
     prompt: str

# def react_code_generation(self, payload: PromptRequest):
#         try:
#             session_id = payload.session_id

#             # Initialize or reset stored UI for the session if requested
#             if payload.reset_ui or session_id not in self.stored_ui:
#                 self._initialize_session_ui(session_id)

#             pages_response = {}

#             for page in payload.pages:
#                 existing_code = self.stored_ui[session_id].get(page.page_name, "")
                
#                 # Build prompts
#                 system_prompt = self._build_system_prompt(page.theme, page.font)
#                 user_prompt = self._build_user_prompt(page.page_name, page.prompt, existing_code,theme=page.theme,font=page.font)
                
#                 messages = [
#                     SystemMessage(content=system_prompt),
#                     HumanMessage(content=user_prompt)
#                 ]

#                 # Invoke the LLM
#                 llm = ChatGroq(
#                     model="meta-llama/llama-4-scout-17b-16e-instruct",    # llama3-8b-8192, meta-llama/llama-4-scout-17b-16e-instruct
#                     temperature=0, 
#                     api_key=os.getenv("GROQ_API_KEY")
#                 )
                
#                 response = llm.invoke(messages)
#                 extracted_code = self._process_llm_response(response)
                
#                 # Store the code and update response
#                 logging.info("storing the UI code to mongo db")

#                 encoded_code = self._store_code_in_database(
#                     session_id, 
#                     page.page_name, 
#                     page.prompt, 
#                     page.theme, 
#                     page.font, 
#                     extracted_code
#                 )
#                 self.stored_ui[session_id][page.page_name] = encoded_code
#                 logging.info("storing the UI code to mongo db completed")
#                 pages_response[page.page_name] = encoded_code
#                 logging.info(f"Updated UI for session: {session_id}, page: {page.page_name}")

#             result = {
#                 "message": "UI update successful.",
#                 "session_id": session_id,
#                 "pages": pages_response
#             }
            
#             return JSONResponse(content=result, media_type="application/json")

#         except Exception as e:
#             logging.error(f"Error updating code: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Error updating UI: {str(e)}")


################################################################### CORRECTED CODE ##############################################################
# def react_code_generation(self, payload: PromptRequest):
#     try:
#         # Build prompt messages using only the user input
#         system_prompt = "You are an expert React developer. Generate complete React component code based on the user's prompt."
#         user_prompt = payload.prompt

#         messages = [
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=user_prompt)
#         ]

#         # Call the LLM
#         llm = ChatGroq(
#             model="meta-llama/llama-4-scout-17b-16e-instruct",
#             temperature=0,
#             api_key=os.getenv("GROQ_API_KEY")
#         )

#         response = llm.invoke(messages)

#         result = {
#             "message": "UI code generation successful.",
#             "code": response
#         }

#         return JSONResponse(content=result, media_type="application/json")

#     except Exception as e:
#         logging.error(f"Error generating UI code: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error generating UI: {str(e)}")

################################################################### CORRECTED CODE ##############################################################


################################################################### FASTAPI CODE ##############################################################

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import logging
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

class CodeGenerator:
    def react_code_generation(self, payload: PromptRequest):
        try:
            system_prompt = "You are an expert React developer. Generate complete React component code based on the user's prompt."
            user_prompt = payload.prompt

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            llm = ChatGroq(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                temperature=0,
                api_key=os.getenv("GROQ_API_KEY")
            )

            response = llm.invoke(messages)

            result = {
                "message": "UI code generation successful.",
                "code": response.content
            }

            return JSONResponse(content=result)

        except Exception as e:
            logging.error(f"Error generating UI code: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating UI: {str(e)}")

generator = CodeGenerator()

@app.post("/generate-ui")
def generate_ui(payload: PromptRequest):
    return generator.react_code_generation(payload)



################################################################### FASTAPI CODE ##############################################################