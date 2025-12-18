import logging
import os
from config_loader import load_config

config = load_config()
LOG_DIR = config["logging"]["log_dir"]

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/controller.log"),
        logging.StreamHandler()
    ]
)

def log_alert(msg):
    logging.warning(msg)
    with open(f"{LOG_DIR}/alerts.log", "a") as f:
        f.write(msg + "\n")

def log_learning(msg):
    logging.info(msg)
    with open(f"{LOG_DIR}/learning.log", "a") as f:
        f.write(msg + "\n")
