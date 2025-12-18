import yaml

CONFIG_PATH = "controller/config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)
