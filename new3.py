# def load_system_prompt(filepath: str = "backend/system_prompt.txt") -> str:
#     """
#     Reads the system prompt text from a local file.
#     """
#     try:
#         with open(filepath, "r", encoding="utf-8") as file:
#             return file.read()
#     except Exception as e:
#         raise Exception(f"Unable to load system prompt from {filepath}: {e}")
    
# if __name__ == "__main__":
#     prompt = load_system_prompt()
#     print("system prompt:",prompt)

# import re

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

# # Example usage with the provided artifact text:
# artifact_text = """
# <boltArtifact id="non-responsive-navbar" title="Non-Responsive Navigation Bar">
#   <boltAction type="file" filePath="index.html">
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#       <meta charset="UTF-8">
#       <meta name="viewport" content="width=device-width, initial-scale=1.0">
#       <title>Non-Responsive Navbar</title>
#       <link rel="stylesheet" href="style.css">
#     </head>
#     <body>
#       <nav class="navbar">
#         <ul>
#           <li><a href="#">Home</a></li>
#           <li><a href="#">About</a></li>
#           <li><a href="#">Contact</a></li>
#         </ul>
#       </nav>
#     </body>
#     </html>
#   </boltAction>

#   <boltAction type="file" filePath="style.css">
#     body {
#       margin: 0;
#       padding: 0;
#     }

#     .navbar {
#       background-color: #333;
#       color: #fff;
#       padding: 1em;
#       text-align: center;
#     }

#     .navbar ul {
#       list-style: none;
#       margin: 0;
#       padding: 0;
#       display: flex;
#       justify-content: space-between;
#     }

#     .navbar li {
#       margin-right: 20px;
#     }

#     .navbar a {
#       color: #fff;
#       text-decoration: none;
#     }

#     .navbar a:hover {
#       color: #ccc;
#     }
#   </boltAction>
# </boltArtifact>
# """

# actions = parse_actions(artifact_text)
# for action in actions:
#     print("Type:", action[0])
#     print("Path:", action[1])
#     print("Content:", action[2])
#     print("------")
    
import re

def parse_actions(artifact_text: str):
    """
    Returns a list of (type, path, content) tuples parsed from the artifact text.
    The function looks for <boltAction> tags with:
      - A required 'type' attribute ("file", "shell", or "start")
      - An optional 'filePath' or 'path' attribute
      - Some content inside the tag.
    """
    pattern = re.compile(
        r'<boltAction\s+type="(?P<type>file|shell|start)"'
        r'(?:\s+(?:filePath|path)="(?P<path>.*?)")?>'
        r'(?P<content>.*?)</boltAction>',
        re.DOTALL
    )
    
    actions = [
        (m.group('type'), m.group('path'), m.group('content').strip())
        for m in pattern.finditer(artifact_text)
    ]
    
    if not actions:
        print("DEBUG: No actions matched. Check the artifact text format.")
    return actions

# Example artifact text
artifact_text = """
<boltArtifact id="non-responsive-navbar" title="Non-Responsive Navigation Bar">
  <boltAction type="file" filePath="index.html">
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Non-Responsive Navbar</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <nav class="navbar">
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </nav>
    </body>
    </html>
  </boltAction>

  <boltAction type="file" filePath="style.css">
    body {
      margin: 0;
      padding: 0;
    }

    .navbar {
      background-color: #333;
      color: #fff;
      padding: 1em;
      text-align: center;
    }

    .navbar ul {
      list-style: none;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: space-between;
    }

    .navbar li {
      margin-right: 20px;
    }

    .navbar a {
      color: #fff;
      text-decoration: none;
    }

    .navbar a:hover {
      color: #ccc;
    }
  </boltAction>
</boltArtifact>
"""

if __name__ == "__main__":
    actions = parse_actions(artifact_text)
    if actions:
        for action in actions:
            print("Type:", action[0])
            print("Path:", action[1])
            print("Content:", action[2])
            print("------")
    else:
        print("No actions found.")
