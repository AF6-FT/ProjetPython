Pipeline Log Analyser

1. Présentation du projet

Ce projet permet d’analyser des fichiers de logs qui contiennent les informations sur les connexions SSH à un serveur.

Le programme lit les fichiers, récupère les informations importantes et analyse les tentatives de connexion.

2. Les objectifs du projet

Le but est de connaître les activités de connexion sur un serveur.

Le programme permet de :

* Trouver les connexions réussies.
* Trouver les connexions échouées.
* Détecter les utilisateurs invalides.
* Trouver le pays lié à une adresse IP.
* Enregistrer les résultats dans une base de données PostgreSQL.

3. Organisation des fichiers

Le projet est divisé en plusieurs dossiers :

* ingestion : contient le code qui lit les fichiers de logs.
* processing : contient le code qui analyse les informations.
* storage : permet d’enregistrer les résultats dans CSV et PostgreSQL.
* serving : contient le code du dashboard.
* data : contient les fichiers de logs utilisés pour l’analyse.
* main.py : permet de lancer le programme.

4. Technologies utilisées

* Python : pour développer le programme.
* PostgreSQL : pour enregistrer les données.
* pgAdmin : pour gérer la base de données.
* Git : pour suivre les modifications du projet.

5. Installation

Pour utiliser le projet, il faut installer Python et PostgreSQL.

Il faut aussi installer la bibliothèque nécessaire pour connecter Python à PostgreSQL :

pip install psycopg2-binary

6. Création de la base de données

Ouvrir pgAdmin et créer une nouvelle base de données avec le nom :

log_analyser

La table auth_events sera créée automatiquement au lancement du programme.

7. Lancement du programme

Ouvrir le terminal dans le dossier du projet et exécuter :

python main.py

Après l’exécution, les résultats seront enregistrés dans :

* output/analysis.csv
* output/dashboard.html
* La base de données PostgreSQL.

8. Dashboard

Le dashboard affiche les informations demandées :

* Le nombre de tentatives échouées par pays.
* Le nombre de connexions réussies par utilisateur.
* Les tentatives effectuées avec un utilisateur invalide.

9. Gestion des erreurs

Les erreurs rencontrées pendant l’exécution sont enregistrées dans le fichier :

logs/app.log

Cela permet de retrouver les problèmes qui peuvent arriver pendant l’analyse.