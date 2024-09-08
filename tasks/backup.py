import requests
import os
from yaml import safe_load
import json
def copy(src: str, dest: str):
  os.system(f'rsync -Lau --partial --no-perms --info=progress2 "{src}" "{dest}"')
  return "Ok"

def notify(msg: str):
  requests.get("http://192.168.0.3:1880/endpoint/notbk", params={
      "msg": msg
  })

def backup_db(dest: str):
  os.system(f'mysqldump --all-databases > "{dest}"')

def runBackups(config):
  for target in config["Copias de seguridad"]["Bases de datos"]:
    print(f"::Backups:: Haciendo copia de seguridad de las bases de datos")
    print(f"::Backups::   Destino: " + target["Destino"])
    backup_db(target["Destino"])
  for target in config["Copias de seguridad"]["Carpetas"]:
    print(f"::Backups:: Haciendo copia de seguridad de las carpetas")
    print(f"::Backups::   Origen: " + target["Origen"])
    print(f"::Backups::   Destino: " + target["Destino"])
    copy(target["Origen"], target["Destino"])
  notify(f'He hecho la copia de seguridad semanal.')
if __name__ == "__main__":
  config = safe_load("/mnt/storage/HomelabConfig.yml")
  runBackups(config)
