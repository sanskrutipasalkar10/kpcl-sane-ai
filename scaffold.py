import os
from pathlib import Path

# Define the base directory
base_dir = "kpcl-ai-chatbot"

# Define all the folders we need to create
folders = [
    "frontend/public",
    "frontend/src/assets",
    "frontend/src/components/chat",
    "frontend/src/components/charts",
    "frontend/src/components/layout",
    "frontend/src/hooks",
    "frontend/src/services",
    "frontend/src/types",
    "backend/app/api",
    "backend/app/agents",
    "backend/app/core",
    "backend/app/models",
    "backend/app/services",
    "backend/data/raw",
    "backend/data/masked",
    "backend/logs/agent_decisions",
    "backend/tests"
]

# Define all the files we need to create
files = [
    "frontend/src/App.jsx",
    "frontend/src/main.jsx",
    "frontend/package.json",
    "frontend/vite.config.js",
    "backend/app/api/routes.py",
    "backend/app/agents/code_agent.py",
    "backend/app/agents/prompts.py",
    "backend/app/core/config.py",
    "backend/app/core/security.py",
    "backend/app/models/request.py",
    "backend/app/models/response.py",
    "backend/app/services/data_parser.py",
    "backend/app/services/chart_gen.py",
    "backend/logs/api_logs.json",
    "backend/tests/test_agent.py",
    "backend/tests/golden_dataset.json",
    "backend/requirements.txt",
    "backend/main.py",
    ".env",
    ".gitignore",
    "README.md"
]

print(f"🚀 Initializing S.A.N.E.-AI Project Structure for '{base_dir}'...")

# Create folders
for folder in folders:
    dir_path = Path(base_dir) / folder
    os.makedirs(dir_path, exist_ok=True)
    print(f"📁 Created folder: {dir_path}")

# Create empty files
for file in files:
    file_path = Path(base_dir) / file
    # Only create the file if it doesn't already exist
    if not file_path.exists():
        with open(file_path, 'w') as f:
            # Add a little boilerplate to the README
            if file == "README.md":
                f.write("# KPCL AI Chatbot\n\nBuilt with React, FastAPI, and Ollama.")
            else:
                pass
        print(f"📄 Created file: {file_path}")

print("\n✅ Scaffolding complete! You can now delete this script.")