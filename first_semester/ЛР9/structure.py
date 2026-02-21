import os

exclude = {"venv", "__pycache__", ".git"}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in exclude]
    level = root.replace(".", "").count(os.sep)
    indent = " " * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")