import subprocess

subprocess.run(["uvicorn", "main:app", "--host", "localhost", "--port", "8000", "--reload"])
