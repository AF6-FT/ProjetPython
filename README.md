# Pipeline Log Analyser

## Présentation
Ce projet lit les fichiers de logs SSH, extrait les événements d'authentification, associe un pays aux adresses IP publiques et enregistre les résultats dans un fichier CSV et dans une base PostgreSQL. Il produit également un dashboard HTML.

## Fonctionnalités
- Lecture des fichiers `auth.log` normaux et compressés en `.gz`.
- Détection des connexions réussies, des tentatives échouées et des utilisateurs invalides.
- Géolocalisation des adresses IP publiques avec IPinfo (Internet nécessaire).
- Enregistrement des erreurs dans `logs/app.log`.
- Export des événements dans `output/analysis.csv`.
- Enregistrement des événements dans PostgreSQL, table `auth_events`.
- Dashboard avec le nombre de tentatives échouées par pays, le nombre de tentatives réussies par utilisateur et la liste des utilisateurs invalides.

## Structure
- `ingestion/raw.py` : lecture des fichiers de logs.
- `processing/extract_transforme.py` : extraction et classification des événements.
- `processing/geo_location.py` : recherche du pays à partir de l'adresse IP.
- `storage/results.py` : sauvegarde CSV.
- `storage/database.py` : sauvegarde PostgreSQL.
- `serving/dashboard.py` : création du dashboard HTML.
- `main.py` : exécution du pipeline.
- `data/` : fichiers de logs d'entrée.
- `logs/` : fichiers d'erreurs.
- `output/` : résultats générés.
- `database.sql` : commande de création de la base.

## Installation
Python 3.10 ou plus récent et PostgreSQL doivent être installés. Le seul package Python externe nécessaire est le pilote PostgreSQL `psycopg2-binary`.

Dans le terminal, depuis le dossier du projet :

```bash
python -m pip install psycopg2-binary
```

## Création de la base avec pgAdmin
1. Ouvrir pgAdmin et se connecter au serveur PostgreSQL.
2. Faire un clic droit sur `Databases` puis `Create` > `Database`.
3. Donner le nom `log_analyser` puis cliquer sur `Save`.
4. La table `auth_events` sera créée automatiquement au premier lancement du programme.

On peut aussi ouvrir `database.sql` dans Query Tool et exécuter la commande `CREATE DATABASE log_analyser;` (ne pas l'exécuter si la base existe déjà).

## Configuration de la connexion
Les valeurs par défaut sont : hôte `localhost`, port `5432`, base `log_analyser`, utilisateur `postgres`. Définir les variables d'environnement si les paramètres sont différents :

- `PGHOST` : serveur PostgreSQL.
- `PGPORT` : port PostgreSQL.
- `PGDATABASE` : nom de la base.
- `PGUSER` : utilisateur PostgreSQL.
- `PGPASSWORD` : mot de passe PostgreSQL.

Exemple macOS/Linux avant de lancer le programme :

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=log_analyser
export PGUSER=postgres
export PGPASSWORD='votre_mot_de_passe'
```

## Exécution
Depuis le dossier du projet :

```bash
python main.py
```

Ouvrir ensuite `output/dashboard.html`. Les données détaillées sont aussi disponibles dans `output/analysis.csv` et dans la table `auth_events` de PostgreSQL.

## Requêtes SQL utiles pour vérifier les indicateurs

```sql
-- Tentatives échouées par pays
SELECT country, COUNT(*)
FROM auth_events
WHERE status IN ('failed', 'invalid_user')
GROUP BY country
ORDER BY COUNT(*) DESC;

-- Tentatives réussies par utilisateur
SELECT username, COUNT(*)
FROM auth_events
WHERE status = 'success'
GROUP BY username
ORDER BY COUNT(*) DESC;

-- Tentatives avec utilisateur invalide
SELECT username, ip, month, day, event_time
FROM auth_events
WHERE status = 'invalid_user';
```

## Gestion des erreurs
Les erreurs de lecture, d'extraction, de géolocalisation, de sauvegarde et de connexion PostgreSQL sont enregistrées dans `logs/app.log`. Si PostgreSQL n'est pas disponible, les résultats CSV et le dashboard sont quand même produits.

## Git : les six commits progressifs
L'historique Git fourni contient déjà les six étapes. Pour les refaire manuellement dans un nouveau dépôt, ajouter les fichiers par étape puis exécuter le commit correspondant :

```bash
git init
git add ingestion processing pyproject.toml
git commit -m "Etape 1 - ingestion et traitement des logs"

git add storage/results.py
git commit -m "Etape 2 - sauvegarde des resultats"

git add serving/dashboard.py
git commit -m "Etape 3 - dashboard HTML"

git add main.py
git commit -m "Etape 4 - integration du pipeline"

git add README.md .gitignore .python-version
 git commit -m "Etape 5 - documentation et configuration"

git add data/
git commit -m "Etape 6 - ajout des fichiers de logs de test"
```

Pour enregistrer ensuite l'ajout PostgreSQL dans le dépôt existant :

```bash
git add storage/database.py database.sql main.py pyproject.toml README.md
git commit -m "Ajout du stockage PostgreSQL"
```

Pour vérifier les commits :

```bash
git log --oneline
```
