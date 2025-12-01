import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DB_ID = os.getenv('NOTION_DB_ID')
REMIND_CHANNEL_ID = os.getenv('REMIND_CHANNEL_ID')
HEATMAP_DAYS = int(os.getenv('HEATMAP_DAYS', 30))
DB_FILE = 'userdb.json'
