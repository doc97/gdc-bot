import os
import dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
dotenv.load_dotenv(dotenv_path=os.path.join(BASE_DIR, "../", ".env"))

# dotenv.load_dotenv()

def get_discord_token():
    return os.getenv('DISCORD_TOKEN')
