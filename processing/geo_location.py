import ipaddress
import json
import logging
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

URL_IPINFO = "https://ipinfo.io/"
logger = logging.getLogger(__name__)
_cache = {}

def get_location(ip):
    if not ip:
        return {"country": "Unknown"}
    if ip in _cache:
        return _cache[ip]
    try:
        address = ipaddress.ip_address(ip)
        if not address.is_global:
            result = {"country": "Local"}
        else:
            with urlopen(URL_IPINFO + ip + "/json", timeout=4) as response:
                result = json.loads(response.read().decode("utf-8"))
        _cache[ip] = result
        return result
    except (ValueError, URLError, HTTPError, TimeoutError, OSError, json.JSONDecodeError):
        logger.exception("Erreur de géolocalisation pour l'adresse IP %s", ip)
        result = {"country": "Unknown"}
        _cache[ip] = result
        return result
