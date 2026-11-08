import logging
import os

logger = logging.getLogger(__name__)


def save_to_database(rows):
    connection = None
    try:
        import psycopg2

        connection = psycopg2.connect(
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
            dbname=os.getenv("PGDATABASE", "log_analyser"),
            user=os.getenv("PGUSER", "postgres"),
            password=os.getenv("PGPASSWORD", ""),
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_events (
                id SERIAL PRIMARY KEY,
                month VARCHAR(10),
                day INTEGER,
                event_time TIME,
                server VARCHAR(255),
                service VARCHAR(100),
                pid INTEGER,
                ip VARCHAR(45),
                country VARCHAR(100),
                username VARCHAR(255),
                status VARCHAR(30),
                event TEXT
            )
        """)
        values = []
        for row in rows:
            values.append((
                row.get("month"), row.get("day"), row.get("time"),
                row.get("server"), row.get("service"), row.get("pid"),
                row.get("ip"), row.get("country", "Unknown"),
                row.get("user"), row.get("status"), row.get("event")
            ))
        if values:
            cursor.executemany("""
                INSERT INTO auth_events
                (month, day, event_time, server, service, pid, ip, country, username, status, event)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, values)
        connection.commit()
        cursor.close()
        return True
    except Exception:
        logger.exception("Erreur pendant l'enregistrement dans PostgreSQL")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()
