import json
import sys
from pathlib import Path

import yaml


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


BASE_DIR = Path(__file__).parent
JSON_PATH = BASE_DIR / "config.json"
YAML_PATH = BASE_DIR / "config.yaml"


def show_config(title, config):
    print(title)
    print("  app_name:", config["app_name"])
    print("  debug:", config["debug"])
    print("  max_retries:", config["max_retries"])
    print("  provider:", config["provider"])


def update_config(config):
    config["debug"] = True
    config["max_retries"] = 5
    config["provider"] = "deepseek"
    return config


def main():
    json_config = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    show_config("JSON before:", json_config)
    json_config = update_config(json_config)
    JSON_PATH.write_text(
        json.dumps(json_config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    show_config("JSON after:", json_config)

    print()

    yaml_config = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    show_config("YAML before:", yaml_config)
    yaml_config = update_config(yaml_config)
    YAML_PATH.write_text(
        yaml.safe_dump(yaml_config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    show_config("YAML after:", yaml_config)


if __name__ == "__main__":
    main()
