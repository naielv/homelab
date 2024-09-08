import requests
import os
from yaml import safe_loads
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
def runAccountCreation(config):
    for account in config["Cuentas"]:
        if account["Servicios"].get("Annapurna") != None:
          annapurnaLicense = {
            "name": {
              "first": account["Nombre"]["Nombre"],
              "last": account["Nombre"]["Apellidos"],
              "display": account["Nombre"]["Preferido"]
            },
            "fs_baseurl": account["Servicios"]["Annapurna"]["Identificador de FS"]
          }
          lid = str(account["Servicios"]["Annapurna"]["Licencia"]).upper()
          fid =  account["Servicios"]["Annapurna"]["Identificador de FS"]
          os.mkdir(f"/mnt/storage/Annapurna/L1/{fid}/")
          json.dump(annapurnaLicense, open(f"/mnt/storage/Annapurna/License/{lid}.json", "w"))
    notify(f'He activado las cuentas del servidor.')
if __name__ == "__main__":
    config = safe_loads("HomelabConfig.yml")
    runBackups(config)
    runAccountCreation(config)
