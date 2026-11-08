import csv
import logging
import os

logger = logging.getLogger(__name__)

def save_results(rows, path):
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fields = ["month", "day", "time", "server", "service", "pid", "ip", "country", "user", "status", "event"]
        with open(path, "w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        return True
    except (OSError, csv.Error):
        logger.exception("Erreur lors de l'enregistrement de %s", path)
        return False
