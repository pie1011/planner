from venv import create
from dotenv import load_dotenv

from root.factory import create_app

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run()