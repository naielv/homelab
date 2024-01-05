import requests
import yaml
from os import environ

c = yaml.load(open("../config.yml", "r"), Loader=yaml.Loader)


def main():
    homer = {
        "title": c["homelab"]["name"],
        "subtitle": c["homelab"]["subtitle"],
        "documentTitle": c["homelab"]["name"],
        "icon": c["homelab"]["icon"],
        "header": true,
        "footer": false,
        "columns": 4,
        "connectivityCheck": true,
        "defaults": {"layout": "columns", "colorTheme": "auto"},
        "theme": "default",
        "services": c["dashboard"],
    }
    if c.get("warning") != None:
        if c["warning"].get("warninxg") != None:
            homer["message"] = (
                {
                    "style": "is-warning",
                    "title": c["warning"]["title"],
                    "icon": "fa fa-exclamation-triangle",
                    "content": c["warning"]["content"],
                },
            )
    yaml.dump(homer, open("../build/homer.yml", "w"), yaml.Dumper)


if __name__ == "__main__":
    main()
