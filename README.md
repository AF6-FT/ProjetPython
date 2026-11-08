# Pipeline Log Analyser

## Présentation
Ce projet lit les fichiers de logs SSH, extrait les événements d'authentification, associe un pays aux adresses IP publiques et produit un fichier CSV ainsi qu'un dashboard HTML.

Le projet utilise uniquement la bibliothèque standard de Python. La géolocalisation utilise le service IPinfo via `urllib` (connexion Internet nécessaire). Si une adresse ne peut pas être localisée, le pays indiqué est `Unknown`. Les adresses locales sont classées `Local`.

## Fonctionnalités
- Lecture des fichiers `auth.log` normaux et compressés en `.gz`.
- Détection des connexions réussies, des tentatives échouées et des utilisateurs invalides.
- Géolocalisation des adresses IP.
- Enregistrement des erreurs dans `logs/app.log`.
- Export des événements dans `output/analysis.csv`.
- Dashboard avec :
  - nombre de tentatives échouées par pays ;
  - nombre de tentatives réussies par utilisateur ;
  - liste des tentatives avec utilisateur invalide.

## Structure
- `ingestion/raw.py` : lecture des fichiers de logs.
- `processing/extract_transforme.py` : extraction et classification des événements.
- `processing/geo_location.py` : recherche du pays à partir de l'adresse IP.
- `storage/results.py` : sauvegarde des résultats CSV.
- `serving/dashboard.py` : création du dashboard HTML.
- `main.py` : exécution du pipeline.
- `data/` : fichiers de logs d'entrée.
- `logs/` : fichiers d'erreurs.
- `output/` : résultats générés.

## Prérequis
Python 3.10 ou une version plus récente. Aucun package externe n'est nécessaire.

## Exécution
Depuis le dossier `log_analysis` :

```bash
python main.py
```

Puis ouvrir `output/dashboard.html` dans un navigateur. Les données détaillées sont disponibles dans `output/analysis.csv`.

## Remarque
Les pays dépendent de la disponibilité du service IPinfo et d'une connexion Internet. Les événements qui ne correspondent pas aux formats d'authentification pris en charge ne sont pas comptabilisés dans les trois indicateurs.
