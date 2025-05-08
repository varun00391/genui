# import re
# import os
# import subprocess

# # Track server start
# _started = False

# def parse_actions(artifact_text: str):
#     """
#     Returns a list of (type, path, content) tuples.
#     """
#     pattern = re.compile(
#         r'<boltAction type="(?P<type>file|shell|start)"(?: path="(?P<path>.*?)")?>(?P<content>.*?)</boltAction>',
#         re.DOTALL
#     )
#     return [
#         (m.group('type'), m.group('path'), m.group('content').strip())
#         for m in pattern.finditer(artifact_text)
#     ]


# def execute_actions(actions):
#     global _started
#     for action_type, path, content in actions:
#         if action_type == 'file':
#             full_path = os.path.join('.', path.lstrip('/'))
#             os.makedirs(os.path.dirname(full_path), exist_ok=True)
#             with open(full_path, 'w', encoding='utf-8') as f:
#                 f.write(content)
#             print(f"[FILE WRITTEN]: {full_path}")

#         elif action_type == 'shell':
#             print(f"[RUN SHELL]: {content}")
#             result = subprocess.run(
#                 content, shell=True, capture_output=True, text=True
#             )
#             print(result.stdout)
#             if result.stderr:
#                 print(f"[ERROR]: {result.stderr}")

#         elif action_type == 'start':
#             if _started:
#                 print("[SERVER ALREADY STARTED]")
#                 continue
#             print(f"[START SERVER]: {content}")
#             subprocess.Popen(content, shell=True)
#             _started = True

#         else:
#             print(f"[UNKNOWN ACTION]: {action_type}")


import re
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Track server start
_started = False

def parse_actions(artifact_text: str):
    """
    Returns a list of (type, path, content) tuples.
    """
    pattern = re.compile(
        r'<boltAction type="(?P<type>file|shell|start)"(?: path="(?P<path>.*?)")?>(?P<content>.*?)</boltAction>',
        re.DOTALL
    )
    return [
        (m.group('type'), m.group('path'), m.group('content').strip())
        for m in pattern.finditer(artifact_text)
    ]


def execute_actions(actions):
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
            result = subprocess.run(
                content, shell=True, capture_output=True, text=True
            )
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
