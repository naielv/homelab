import requests
import os
from yaml import safe_load
import json
def notify(msg: str):
    requests.get("http://192.168.0.3:1880/endpoint/notbk", params={
        "msg": msg
    })
def runAccountCreation(config):
  for account in config["Cuentas"]:
    if account["Servicios"].get("Annapurna") != None:
      annapurnaLicense = {
        "name": {
          "first": account["Nombre"]["Nombre"],
          "last": account["Nombre"]["Apellido"],
          "display": account["Nombre"]["Preferido"]
        },
        "fs_baseurl": account["Servicios"]["Annapurna"]["Identificador de FS"]
      }
      lid = str(account["Servicios"]["Annapurna"]["Licencia"]).upper()
      fid = account["Servicios"]["Annapurna"]["Identificador de FS"]
      try:
        os.mkdir(f"/mnt/storage/Annapurna/L1/{fid}/")
      except:
        pass
      json.dump(annapurnaLicense, open(f"/mnt/storage/Annapurna/License/{lid}.json", "w"))
  notify(f'He activado las cuentas del servidor.')
if __name__ == "__main__":
  config = safe_load(open("/mnt/storage/HomelabConfig.yml", "r").read())
  runAccountCreation(config)
