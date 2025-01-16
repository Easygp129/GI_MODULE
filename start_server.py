import os
import subprocess

# Set the default Streamlit port
port = os.getenv("PORT", 8501)

# Run Streamlit
subprocess.run(["streamlit", "run", "app.py", "--server.port", port, "--server.headless", "true"])