import requests
import yaml
from os import environ


def auth(email, password):
    url = "http://138.68.73.173:81/api/tokens"

    payload = {"identity": email, "secret": password}
    headers = {
        "authorization": "Bearer null",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "content-type": "application/json; charset=UTF-8",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()["token"]


def add_host(api_key: str, domain_name: str, scheme: str, host: str, port: int):
    url = "http://138.68.73.173:81/api/nginx/proxy-hosts"

    payload = {
        "domain_names": [domain_name],
        "forward_scheme": scheme,
        "forward_host": host,
        "forward_port": port,
        "block_exploits": True,
        "allow_websocket_upgrade": True,
        "access_list_id": "0",
        "certificate_id": 1,
        "ssl_forced": True,
        "http2_support": True,
        "meta": {"letsencrypt_agree": False, "dns_challenge": False},
        "advanced_config": "",
        "locations": [],
        "caching_enabled": False,
        "hsts_enabled": False,
        "hsts_subdomains": False,
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "content-type": "application/json; charset=UTF-8",
        "Authorization": "Bearer " + api_key,
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return True


def delete_host(api_key: str, id: int):
    url = "http://138.68.73.173:81/api/nginx/proxy-hosts/" + str(id)

    headers = {
        "authorization": "Bearer " + api_key,
        "content-type": "application/json; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    response = requests.request("DELETE", url, headers=headers)


def get_hosts(api_key: str):
    url = "http://138.68.73.173:81/api/nginx/proxy-hosts"

    querystring = {"expand": "owner,access_list,certificate"}

    payload = ""
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "content-type": "application/json; charset=UTF-8",
        "Authorization": "Bearer " + api_key,
    }

    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
    )

    return response.json()


def _active_list(hosts):
    pairs = {}
    for host in hosts:
        pairs[host["id"]] = host["domain_names"][0]
    return pairs


def _config_list(hosts):
    pairs = []
    for host in hosts:
        pairs.append(host["domain_name"])
    return pairs


def _check(h, c, api_key):
    if h["scheme"] != c["forward_scheme"]:
        return True, c
    if h["host"] != c["forward_host"]:
        return True, c
    if h["port"] != c["forward_port"]:
        return True, c
    return False, None


def check_change(host, compare, api_key):
    for comp in compare:
        if host["domain_name"] == comp["domain_names"][0]:
            return _check(host, comp, api_key)


def main():
    user = environ["HL_NPM_USER"]
    password = environ["HL_NPM_PASSWORD"]
    api_key = auth(user, password)
    proxy_hosts = get_hosts(api_key)
    active = _active_list(proxy_hosts)
    config = yaml.load(open("./config.yml", "r"), Loader=yaml.Loader)
    configured = _config_list(config["reverse_proxy"])
    active_val = list(active.values())
    for host in config["reverse_proxy"]:
        if host["domain_name"] in active_val:
            print("Checking Existing: " + host["domain_name"])
            changed, comp = check_change(host, proxy_hosts, api_key)
            if changed:
                print("Host Changed: " + host["domain_name"])
                delete_host(api_key, comp["id"])
                add_host(
                    api_key=api_key,
                    domain_name=host["domain_name"],
                    scheme=host["scheme"],
                    host=host["host"],
                    port=host["port"],
                )
        else:
            add_host(
                api_key=api_key,
                domain_name=host["domain_name"],
                scheme=host["scheme"],
                host=host["host"],
                port=host["port"],
            )
            print("Added new: " + host["domain_name"])


if __name__ == "__main__":
    main()
