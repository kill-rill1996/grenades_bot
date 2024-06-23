import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMEN = os.getenv("DOMEN_PROD")
VERSION = os.getenv("VERSION")

ADMINS = [int(user_id) for user_id in os.getenv("ADMINS").split(",")]

MAPS = ["Anubis", "Ancient", "Dust 2", "Inferno", "Mirage", "Nuke", "Overpass", "Vertigo"]
