import subprocess

# pip install PyInstaller

subprocess.call(r"python -m PyInstaller --onefile --name CUBIC_CB-HCHO cubic_CB-HCHO.py")
