import logging
from pathlib import Path

from ingestion import raw
from processing import extract_transforme
from processing import geo_location
from storage import results
from storage import database
from serving import dashboard

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    try:
        lines = raw.to_rows(BASE_DIR / "data")
        records = []
        for line in lines:
            record = extract_transforme.extract_from_row(line)
            if record and record["status"] in ("failed", "success", "invalid_user"):
                location = geo_location.get_location(record.get("ip"))
                record["country"] = location.get("country", "Unknown")
                records.append(record)
        results.save_results(records, BASE_DIR / "output" / "analysis.csv")
        database.save_to_database(records)
        dashboard.create_dashboard(records, BASE_DIR / "output" / "dashboard.html")
        print("Analyse terminée.")
        print("Événements analysés :", len(records))
        print("CSV :", BASE_DIR / "output" / "analysis.csv")
        print("Dashboard :", BASE_DIR / "output" / "dashboard.html")
        print("Base de données : PostgreSQL (voir logs/app.log en cas d'erreur)")
    except Exception:
        logger.exception("Erreur générale pendant l'exécution du pipeline")
        print("Une erreur est survenue. Consultez logs/app.log.")

if __name__ == "__main__":
    main()
