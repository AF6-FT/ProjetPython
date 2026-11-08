import gzip
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def to_rows(path):
    data_dir = Path(path)
    rows = []
    try:
        files = sorted(os.listdir(data_dir))
    except OSError:
        logger.exception("Impossible de lire le dossier des logs : %s", path)
        return rows

    for file in files:
        file_path = data_dir / file
        if not file_path.is_file():
            continue
        try:
            if file.endswith(".gz"):
                with gzip.open(file_path, mode="rt", encoding="utf-8", errors="replace") as f:
                    rows.extend(f.readlines())
            else:
                with open(file_path, mode="r", encoding="utf-8", errors="replace") as f:
                    rows.extend(f.readlines())
        except (OSError, EOFError, gzip.BadGzipFile, UnicodeError):
            logger.exception("Erreur de lecture du fichier %s", file_path)
    return rows

if __name__ == "__main__":
    data = to_rows("../data")
    print(data[:10])
