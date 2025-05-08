# import os
# import subprocess
# import re
# import json
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import re
# from langchain.schema import SystemMessage, HumanMessage, AIMessage
# from langchain_groq import ChatGroq

# app = FastAPI(title="Frontend UI Generator and Updater")

# ###############################################################################
# # HELPER FUNCTIONS
# ###############################################################################

# def setup_and_install_frontend(target_dir: str = ".") -> str:
#     """
#     Sets up a Vite frontend project, installs base dependencies,
#     and optionally updates any scaffolded dependencies.
#     """
#     project_name = "new_front"
#     framework = "react"
#     project_path = os.path.join(target_dir, project_name)

#     # Create the project if it doesn't exist.
#     if not os.path.exists(project_path):
#         print(f"🚀 Creating new Vite project '{project_name}' with {framework} in '{target_dir}'...")
#         cmd_create = f"npm create vite@latest {project_name} -- --template {framework}"
#         try:
#             subprocess.run(cmd_create, shell=True, check=True, cwd=target_dir)
#         except subprocess.CalledProcessError as e:
#             raise Exception(f"Project creation failed: {e}")
#     else:
#         print(f"⚡ Project '{project_name}' already exists. Skipping creation.")

#     # Install the base dependencies.
#     print("📦 Installing npm dependencies...")
#     try:
#         result = subprocess.run("npm install", shell=True, check=True, cwd=project_path, capture_output=True, text=True)
#         print(result.stdout)
#     except subprocess.CalledProcessError as e:
#         error_message = f"Installation of npm dependencies failed:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
#         raise Exception(error_message)

#     # Optionally: Extract and install additional dependencies from the scaffolded App.jsx.
#     app_file = os.path.join(project_path, "src", "App.jsx")
#     dependencies = extract_dependencies(app_file)
#     install_npm_packages(dependencies, project_path)

#     return project_path

# def extract_dependencies(file_path: str) -> set:
#     """
#     Extracts unique external package dependencies from a React file.
#     """
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             react_code = file.read()
#         pattern = r"import\s+(?:[\w*\s{},]+)\s+from\s+['\"]([^'\"]+)['\"]"
#         matches = re.findall(pattern, react_code)
#         return {match for match in matches if not match.startswith(('.', '/'))}
#     except FileNotFoundError:
#         print(f"❌ File not found: {file_path}")
#         return set()
#     except Exception as e:
#         print(f"⚠️ Error reading file: {e}")
#         return set()

# def install_npm_packages(dependencies: set, project_dir: str):
#     """
#     Checks package.json for installed dependencies and installs any missing ones.
#     """
#     package_json_path = os.path.join(project_dir, "package.json")
#     installed_deps = set()
#     if os.path.exists(package_json_path):
#         with open(package_json_path, "r", encoding="utf-8") as f:
#             package_data = json.load(f)
#         installed_deps = set(package_data.get("dependencies", {}).keys())

#     missing = dependencies - installed_deps
#     if missing:
#         print(f"🔍 Missing packages: {missing}")
#         for package in missing:
#             cmd = f"npm install {package}"
#             print(f"🚀 Running: {cmd}")
#             subprocess.run(cmd, shell=True, cwd=project_dir, check=True)
#     else:
#         print("✅ All dependencies are already installed.")

# def extract_dependencies_from_code(react_code: str) -> set:
#     """
#     Extracts unique external package dependencies from a provided string of React code.
#     """
#     pattern = r"import\s+(?:[\w*\s{},]+)\s+from\s+['\"]([^'\"]+)['\"]"
#     matches = re.findall(pattern, react_code)
#     return {match for match in matches if not match.startswith(('.', '/'))}

# def update_preview_app(react_code: str, project_dir: str):
#     """
#     Updates the preview project with the new React code:
#     - Installs any new dependencies from the code.
#     - Overwrites the main file (here, src/App.jsx) with the new code.
#     - Starts the Vite development server.
#     """
#     # Step 1: Extract dependencies from the provided code and install missing ones.
#     dependencies = extract_dependencies_from_code(react_code)
#     install_npm_packages(dependencies, project_dir)

#     # Step 2: Write the new React code into the preview file.
#     target_file = os.path.join(project_dir, "src", "App.jsx")
#     with open(target_file, "w", encoding="utf-8") as f:
#         f.write(react_code)
#     print(f"✅ Updated preview file: {target_file}")

#     # Step 3: Launch the Vite development server.
#     # Using subprocess.Popen so that the process is started and doesn't block.
#     print("🚀 Starting Vite development server...")
#     subprocess.Popen("npm run dev", shell=True, cwd=project_dir)

# ###############################################################################
# # CODE GENERATION LOGIC
# ###############################################################################

# import os
# from string import Template

# def generate_react_code(prompt: str) -> str:
#     """
#     Generates production-quality React code based on a user prompt.
#     The LLM is instructed to output UI code using JSX with Tailwind CSS,
#     React hooks, and Lucide React icons. The design should be beautiful
#     and fully featured.

#     Args:
#         prompt (str): A description of the UI or modifications to be implemented.

#     Returns:
#         str: The generated React code.

#     Raises:
#         Exception: If the LLM response is invalid or empty.
#     """
#     # Base system prompt with design guidelines.
#     system_prompt = (
#         "For all designs I ask you to make, have them be beautiful, not cookie cutter. "
#         "Make webpages that are fully featured and production-worthy. "
#         "By default, this template supports JSX syntax with Tailwind CSS classes, React hooks, "
#         "and Lucide React for icons. Do not install other UI libraries unless absolutely necessary. "
#         "Use icons from lucide-react for logos and link to stock photos from Unsplash where appropriate. "
#         "Do not remove existing code unless it is specifically asked by user. "
#         "When modifying existing code, please preserve all existing UI components and only add or remove elements as specified. "
#         "Please return only the React code wrapped inside triple backticks if possible."
#     )

#     # Build the conversation messages.
#     messages = [
#         SystemMessage(content=system_prompt),
#         HumanMessage(content=prompt)
#     ]

#     # Initialize the LLM (you might also try another model if necessary).
#     llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)
#     response = llm.invoke(messages)

#     if not isinstance(response, AIMessage) or not response.content:
#         raise Exception("Invalid response from LLM.")

#     # Print the raw response for debugging purposes.
#     raw_response = response.content.strip()
#     print("LLM Raw Response:\n", raw_response)

#     # Try to extract code wrapped in triple backticks, if present.
#     match = re.search(r"```(?:jsx|js)?\n(.*?)\n```", raw_response, re.DOTALL)
#     code = match.group(1) if match else raw_response

#     # If no code is detected, raise an error.
#     if not code.strip():
#         raise Exception("No code extracted from LLM response.")

#     return code

# ###############################################################################
# # FASTAPI REQUEST MODELS & ENDPOINTS
# ###############################################################################

# class PromptInput(BaseModel):
#     prompt: str

# @app.post("/generate-and-update")
# def generate_and_update_ui(prompt_input: PromptInput):
#     """
#     Receives a user prompt, sets up the frontend (if not already set up),
#     generates React code from the prompt, updates the preview, and starts the dev server.
#     """
#     # Ensure the project is set up.
#     project_dir = os.path.join(".", "new_front")
#     if not os.path.exists(project_dir):
#         try:
#             project_dir = setup_and_install_frontend()
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Frontend setup failed: {e}")

#     # Generate React code based on the prompt.
#     react_code = generate_react_code(prompt_input.prompt)

#     # Update the preview app with the generated code.
#     try:
#         update_preview_app(react_code, project_dir)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to update preview: {e}")

#     return {"message": "UI generated and updated successfully.", "react_code": react_code}

# # (Optional) Include your existing /setup or /update-preview endpoints if needed.

# ###############################################################################
# # MAIN
# ###############################################################################

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


import os
import subprocess
import re
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import LangChain messaging classes and ChatGroq from your LLM setup.
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq

app = FastAPI(title="Dynamic Frontend UI Generator and Updater")

###############################################################################
# HELPER FUNCTIONS: PROJECT SETUP & DEPENDENCY MANAGEMENT
###############################################################################
def setup_and_install_frontend(target_dir: str = ".") -> str:
    """
    Sets up a Vite React project using the official template,
    installs base npm dependencies, and installs any additional dependencies
    parsed from the scaffolded code.
    """
    project_name = "new_front"
    framework = "react"
    project_path = os.path.join(target_dir, project_name)

    # Create the project if it doesn't already exist.
    if not os.path.exists(project_path):
        print(f"🚀 Creating new Vite project '{project_name}' with {framework} in '{target_dir}'...")
        cmd_create = f"npm create vite@latest {project_name} -- --template {framework}"
        try:
            subprocess.run(cmd_create, shell=True, check=True, cwd=target_dir)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Project creation failed: {e}")
    else:
        print(f"⚡ Project '{project_name}' already exists. Skipping creation.")

    # Install base npm dependencies.
    print("📦 Installing npm dependencies...")
    try:
        result = subprocess.run("npm install", shell=True, check=True, cwd=project_path, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        err_msg = f"Installation of npm dependencies failed:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
        raise Exception(err_msg)

    # Optionally, extract and install any additional dependencies from the preexisting App.jsx.
    app_file = os.path.join(project_path, "src", "App.jsx")
    dependencies = extract_dependencies(app_file)
    install_npm_packages(dependencies, project_path)

    return project_path

def extract_dependencies(file_path: str) -> set:
    """
    Extracts unique external package dependencies from a React file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            react_code = file.read()
            pattern = r"import\s+(?:[\w*\s{},]+)\s+from\s+['\"]([^'\"]+)['\"]"
            matches = re.findall(pattern, react_code)
            # Exclude relative imports.
            return {match for match in matches if not match.startswith(('.', '/'))}
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return set()
    except Exception as e:
        print(f"⚠️ Error reading file: {e}")
        return set()

def install_npm_packages(dependencies: set, project_dir: str):
    """
    Reads package.json from the project directory and installs any missing dependencies.
    """
    package_json_path = os.path.join(project_dir, "package.json")
    installed_deps = set()
    if os.path.exists(package_json_path):
        with open(package_json_path, "r", encoding="utf-8") as f:
            package_data = json.load(f)
        installed_deps = set(package_data.get("dependencies", {}).keys())
    
    missing = dependencies - installed_deps
    if missing:
        print(f"🔍 Missing packages: {missing}")
        for package in missing:
            cmd = f"npm install {package}"
            print(f"🚀 Running: {cmd}")
            subprocess.run(cmd, shell=True, cwd=project_dir, check=True)
    else:
        print("✅ All dependencies are already installed.")

def extract_dependencies_from_code(react_code: str) -> set:
    """
    Extracts unique external package dependencies from provided React code.
    """
    pattern = r"import\s+(?:[\w*\s{},]+)\s+from\s+['\"]([^'\"]+)['\"]"
    matches = re.findall(pattern, react_code)
    return {match for match in matches if not match.startswith(('.', '/'))}

def update_preview_app(react_code: str, project_dir: str):
    """
    Updates the preview application:
      - Installs any new dependencies from the generated code.
      - Overwrites src/App.jsx with the generated component code.
      - Starts the Vite development server.
    """
    # Install any new dependencies discovered from the code.
    dependencies = extract_dependencies_from_code(react_code)
    install_npm_packages(dependencies, project_dir)
    
    # Write the generated code to src/App.jsx.
    target_file = os.path.join(project_dir, "src", "App.jsx")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(react_code)
    print(f"✅ Updated preview file: {target_file}")
    
    # Launch the Vite development server.
    print("🚀 Starting Vite development server...")
    subprocess.Popen("npm run dev", shell=True, cwd=project_dir)

###############################################################################
# DYNAMIC CODE GENERATION USING LLM (NO HARD-CODED UI)
###############################################################################
def generate_react_code(prompt: str) -> str:
    """
    Dynamically generates production-quality React component code based on a user prompt.
    
    The LLM is instructed to output only the React component code (without any rendering instructions)
    so that it fits into the standard Vite project. The generated code must export a default component
    named App.
    
    Returns:
      str: The generated React code.
    
    Raises:
      Exception: If the LLM response is invalid or no usable code is extracted.
    """
    system_prompt = (
        "You are an expert UI designer and React developer. "
        "Generate a production-quality React component in JSX that exports a default component named App. "
        "Do not include any rendering commands (such as ReactDOM.render or createRoot) because "
        "the project already has a src/main.jsx which handles mounting. "
        "Wrap your code in triple backticks and ensure it is complete and syntactically correct."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]
    
    # Initialize the LLM (adjust the model parameters as needed).
    llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)
    response = llm.invoke(messages)
    
    if not isinstance(response, AIMessage) or not response.content:
        raise Exception("Invalid response from LLM.")
    
    raw_response = response.content.strip()
    print("LLM Raw Response:\n", raw_response)
    
    # Attempt to extract code wrapped in triple backticks.
    match = re.search(r"```(?:jsx|js)?\n(.*?)\n```", raw_response, re.DOTALL)
    code = match.group(1) if match else raw_response
    
    if not code.strip():
        raise Exception("No code extracted from LLM response.")
    
    return code

###############################################################################
# FASTAPI REQUEST MODELS & ENDPOINTS
###############################################################################
class PromptInput(BaseModel):
    prompt: str

@app.post("/generate-and-update")
def generate_and_update_ui(prompt_input: PromptInput):
    """
    Receives a user prompt, sets up the frontend if needed, dynamically generates React component code
    using the LLM, updates the preview (src/App.jsx), and starts the Vite dev server.
    """
    # Ensure the Vite project is set up.
    project_dir = os.path.join(".", "new_front")
    if not os.path.exists(project_dir):
        try:
            project_dir = setup_and_install_frontend()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Frontend setup failed: {e}")
    
    # Generate React code based on the prompt.
    try:
        react_code = generate_react_code(prompt_input.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code generation failed: {e}")
    
    # Update the preview application with the new code.
    try:
        update_preview_app(react_code, project_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update preview: {e}")
    
    return {"message": "UI generated and updated successfully.", "react_code": react_code}

###############################################################################
# MAIN ENTRY POINT
###############################################################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

