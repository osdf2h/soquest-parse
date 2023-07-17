import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent.resolve()

load_dotenv(BASE_DIR / '.env')
ADDRESS = os.getenv('ADDRESS')
