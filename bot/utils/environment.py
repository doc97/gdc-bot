import os
import dotenv


dotenv.load_dotenv()

def get_discord_token():
    return os.getenv('DISCORD_TOKEN')
