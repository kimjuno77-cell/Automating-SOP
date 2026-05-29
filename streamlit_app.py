import sys
import os

# Add 'frontend' and root directories to path to ensure all imports resolve correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, 'frontend')

if frontend_dir not in sys.path:
    sys.path.insert(0, frontend_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Load the streamlit_app.py from the frontend directory
import importlib.util
spec = importlib.util.spec_from_file_location("frontend_streamlit_app", os.path.join(frontend_dir, "streamlit_app.py"))
frontend_app = importlib.util.module_from_spec(spec)
sys.modules["frontend_streamlit_app"] = frontend_app
spec.loader.exec_module(frontend_app)
