# Gestion_Perf_Cyclistes
Conception d'une solution permettant d'enregistrer et d'analyser les performances des athlètes. Cette solution permet de stocker les données des tests effectués par les cyclistes dans une base de données, accessible via une API RESTful développée avec FastAPI et une base de données SQLite.


## Description
Ce projet est une application permettant de gérer les performances des cyclistes et les utilisateurs associés. Il utilise SQLite pour stocker les données des cyclistes, des coachs et des enregistrements de performance.

## Installation
### Prérequis
- Python 3.x installé sur votre machine
- SQLite3 intégré à Python

### Cloner le projet
```bash
git clone https://github.com/A-Delvoye/Gestion_Perf_Cyclistes
cd Gestion_Perf_Cyclistes
```

### Exécuter le script
```bash
python cyclists.py
```
Cela créera la base de données `cyclists.db` et insérera des données de test.

## Structure de la base de données
Le projet utilise une base de données SQLite avec les tables suivantes :

### `cyclists`
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identifiant unique du cycliste |
| nom | TEXT NOT NULL | Nom du cycliste |
| age | INTEGER NOT NULL | Âge du cycliste |
| poids | REAL NOT NULL | Poids du cycliste |

### `users`
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identifiant unique de l'utilisateur |
| username | TEXT NOT NULL UNIQUE | Nom d'utilisateur |
| password_hash | TEXT NOT NULL | Mot de passe (haché) |
| role | TEXT NOT NULL | Rôle de l'utilisateur (admin, coach, etc.) |
| is_active | BOOLEAN NOT NULL DEFAULT 1 | Statut actif |

### `valid_tokens`
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identifiant unique du token |
| expires | DATETIME NOT NULL | Date d'expiration |
| token | VARCHAR NOT NULL UNIQUE | Token d'authentification |

### `enregistrements`
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identifiant unique |
| time | DATETIME NOT NULL | Temps de l'enregistrement |
| power | REAL NOT NULL | Puissance développée |
| oxygen | REAL NOT NULL | Niveau d'oxygène |
| cadence | REAL NOT NULL | Cadence |
| HR | REAL NOT NULL | Fréquence cardiaque |
| RF | REAL NOT NULL | ??? (à préciser) |
| date | DATETIME NOT NULL | Date de l'enregistrement |

### `coachs`
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identifiant unique du coach |
| nom | TEXT NOT NULL | Nom du coach |
| user_id | INTEGER NOT NULL | Référence vers l'utilisateur associé |

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request sur GitHub.


