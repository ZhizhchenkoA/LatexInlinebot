import os
from dotenv import load_dotenv

load_dotenv()

def get_proxy():
    """Читает настройки прокси из .env. Возвращает None, если хост не указан."""
    hostname = os.getenv("PROXY_HOSTNAME")
    if not hostname:
        return None
    
    proxy = {
        "scheme": os.getenv("PROXY_SCHEME", "socks5"),
        "hostname": hostname,
        "port": int(os.getenv("PROXY_PORT", 1080)),
    }
    
    username = os.getenv("PROXY_USERNAME")
    password = os.getenv("PROXY_PASSWORD")
    if username: proxy["username"] = username
    if password: proxy["password"] = password
        
    return proxy

class Settings:
    API_ID: int = int(os.getenv("API_ID", 0))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    PROXY: dict = get_proxy()

config = Settings()