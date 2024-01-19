import os
import re, time
from os import environ

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]: return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]: return False
    else: return default
      
API_ID = int(os.environ.get("API_ID", "14688437"))
API_HASH = os.environ.get("API_HASH", "5310285db722d1dceb128b88772d53a6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6399781777:AAHQl6dNdsUKCeJYPqvCbDdhS6pp-qMDuj0")
FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "pvslogs")
SUPPORT = os.environ.get("SUPPORT", "blackcatnetwork")
UPDATES = os.environ.get("UPDATES", "blackcatserver")
BOT_NAME = os.environ.get("BOT_NAME", "Pvs")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "ZaidRoobot")
PHOTOS = [
    "https://media.macphun.com/img/uploads/macphun/blog/625/visiting-site-photo-frame.jpg?q=75&w=1710&h=906&resize=cover",
    "https://img.freepik.com/free-photo/spectral-light-illuminates-transparent-red-colored-red-roses-abstract-flower-art-generative-ai_157027-1729.jpg?w=826&t=st=1705682239~exp=1705682839~hmac=d5aa89d6d6104747af0f040a3defeec8ce34e51bc2cc248337e57ca5cdbb52e4",
]
