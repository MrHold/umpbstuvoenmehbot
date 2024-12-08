import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "BOT_TOKEN": os.getenv("BOT_TOKEN"),
    "ADMINS": [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x],
    "DATABASE_URL": os.getenv("DATABASE_URL"),
}
