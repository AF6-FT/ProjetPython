import logging
import re

logger = logging.getLogger(__name__)

pattern = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<server>\S+)\s+"
    r"(?P<service>\w+)\[(?P<pid>\d+)\]:\s*(?P<message>.*)$"
)

def extract_from_row(row):
    try:
        match = pattern.search(row.strip())
        if not match:
            return None
        result = match.groupdict()
        message = result["message"]
        result.update({
            "ip": None,
            "user": None,
            "status": "other",
            "event": message
        })
        ip_match = re.search(r"\b(?:from|rhost=)\s*(\d{1,3}(?:\.\d{1,3}){3})", message)
        if ip_match:
            result["ip"] = ip_match.group(1)
        invalid = re.search(r"Invalid user\s+(\S*)\s+from\s+(\d{1,3}(?:\.\d{1,3}){3})", message)
        if invalid:
            result["status"] = "invalid_user"
            result["user"] = invalid.group(1)
            result["ip"] = invalid.group(2)
        else:
            failed = re.search(r"Failed password for (?:invalid user )?(\S+) from", message)
            accepted = re.search(r"Accepted (?:password|publickey) for (\S+) from", message)
            if failed:
                result["status"] = "failed"
                result["user"] = failed.group(1)
            elif accepted:
                result["status"] = "success"
                result["user"] = accepted.group(1)
            elif "authentication failure" in message:
                result["status"] = "failed"
                user_match = re.search(r"user=(\S+)", message)
                if user_match:
                    result["user"] = user_match.group(1)
        return result
    except (AttributeError, TypeError, re.error):
        logger.exception("Erreur pendant l'extraction d'une ligne")
        return None
