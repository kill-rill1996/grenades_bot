import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOMEN = os.getenv("DOMEN_DEV")

MAPS = ["Anubis", "Ancient", "Dust 2", "Inferno", "Mirage", "Nuke", "Overpass", "Vertigo"]
