from venv import create
from dotenv import load_dotenv

from root.factory import create_app

load_dotenv()
app = create_app()
