import html
import logging
import os
from collections import Counter

logger = logging.getLogger(__name__)

def create_dashboard(rows, path):
    try:
        failed_country = Counter(row.get("country", "Unknown") for row in rows if row.get("status") in ("failed", "invalid_user"))
        success_user = Counter(row.get("user", "Unknown") for row in rows if row.get("status") == "success")
        invalid_rows = [row for row in rows if row.get("status") == "invalid_user"]
        def table(headers, data):
            output = "<table><tr>" + "".join("<th>" + html.escape(str(h)) + "</th>" for h in headers) + "</tr>"
            for item in data:
                output += "<tr>" + "".join("<td>" + html.escape(str(v)) + "</td>" for v in item) + "</tr>"
            return output + "</table>"
        failed_table = table(["Pays", "Tentatives échouées"], sorted(failed_country.items()))
        success_table = table(["Utilisateur", "Tentatives réussies"], sorted(success_user.items()))
        invalid_data = [(r.get("user") or "(vide)", r.get("ip") or "Unknown", r.get("month"), r.get("day"), r.get("time")) for r in invalid_rows]
        invalid_table = table(["Utilisateur invalide", "IP", "Mois", "Jour", "Heure"], invalid_data)
        page = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Pipeline Log Analyser</title>
<style>body{font-family:Arial,sans-serif;margin:35px;background:#f4f6f8;color:#222}h1{color:#17365d}section{background:white;padding:18px;margin:20px 0;border-radius:8px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:9px;text-align:left}th{background:#e8eef5}</style></head><body>
<h1>Dashboard - Pipeline Log Analyser</h1>
<section><h2>Nombre de tentatives échouées par pays</h2>""" + failed_table + """</section>
<section><h2>Nombre de tentatives réussies par utilisateur</h2>""" + success_table + """</section>
<section><h2>Tentatives avec utilisateur invalide</h2>""" + invalid_table + """</section>
</body></html>"""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as output:
            output.write(page)
        return True
    except (OSError, TypeError, ValueError):
        logger.exception("Erreur pendant la création du dashboard")
        return False
