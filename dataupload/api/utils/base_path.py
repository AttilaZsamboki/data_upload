import os
import platform
from dotenv import load_dotenv

load_dotenv()

base_path = (
    os.environ.get("BASE_PATH_LINUX")
    if platform.system() == "Linux"
    else os.environ.get("BASE_PATH_WINDOWS")
)