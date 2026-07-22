import logging
import os
import requests

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,   # DEBUG, INFO, WARNING
    format='[%(levelname)s] %(message)s'
)

AVATAR_DIR = os.path.expanduser("~/.config/steam-acolyte/avatars")
os.makedirs(AVATAR_DIR, exist_ok=True)

def get_avatar(steam_id):
    if not steam_id:
        logging.warning("get_avatar: steam_id is None")
        return None

    file_path = os.path.join(AVATAR_DIR, f"{steam_id}.jpg")  # <- DEFINIERE file_path VOR try
    if os.path.exists(file_path):
        logging.info(f"Avatar cached: {file_path}")
        return file_path


    try:
        logging.info(f"Downloading avatar for {steam_id} ...")
        r = requests.get(f"https://steamcommunity.com/profiles/{steam_id}?xml=1", timeout=5)
        if "<avatarFull>" not in r.text:
            logging.warning(f"Profile {steam_id} is private or no avatar found")
            return None

        start_tag = "<avatarFull>"
        end_tag = "</avatarFull>"
        start = r.text.find(start_tag)
        end = r.text.find(end_tag)

        avatar_url = r.text[start + len(start_tag):end].strip()
        if avatar_url.startswith("<![CDATA[") and avatar_url.endswith("]]>"):
            avatar_url = avatar_url[9:-3]

        logging.info(f"Avatar URL: {avatar_url}")

        img = requests.get(avatar_url, timeout=5).content
        with open(file_path, "wb") as f:
            f.write(img)

        logging.info(f"Avatar saved: {file_path}")
        return file_path

    except Exception as e:
        logging.error(f"Failed to download avatar for {steam_id}: {e}")
        if os.path.exists(file_path):
            return file_path
        return None
