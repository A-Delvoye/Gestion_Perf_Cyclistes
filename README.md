# 📊 Gestion des Performances Cyclistes  

Ce projet permet de gérer les performances des cyclistes via une API FastAPI avec une base de données SQLite.  

---

## 📌 Fonctionnalités  

- **Gestion des utilisateurs** : Création, authentification, gestion des rôles (admin/cycliste).  
- **Gestion des cyclistes** : Ajout, mise à jour, suppression et récupération des données des cyclistes.  
- **Suivi des performances** : Enregistrement des performances (puissance max, VO2 max, cadence, fréquence cardiaque et respiratoire).  
- **Gestion des jetons de connexion** : Authentification sécurisée via des jetons valides.  

---

## 🛠️ Technologies utilisées  

- **Python 3**  
- **FastAPI**  
- **SQLite**  
---

## 📂 Structure du projet  

# Structure du Projet - Gestion des Performances Cyclistes 🚴‍♂️

## 📁 app
Ce dossier contient le cœur de l'application, y compris l'API, la gestion de la base de données et les schémas de données.
- `api/` : Contient les endpoints de l'API.
- `db/` : Gestion de la base de données et scripts d'initialisation.
- `schemas/` : Définitions des structures de données utilisées dans l'application.
- `main.py` : Point d'entrée principal de l'application.

## 📁 core
Ce dossier contient les fonctionnalités de base et les outils nécessaires à l'application.
- `config.py` : Configuration globale de l'application.
- `password_tools.py` : Gestion des mots de passe et sécurité.
- `user_role_tools.py` : Gestion des rôles utilisateur.

## 📁 db
Dossier contenant les sessions de base de données et la gestion des connexions.
- `db_session.py` : Configuration des sessions de base de données.
- `token_white_list.py` : Gestion des jetons valides.

## 📁 endpoints
Dossier regroupant les différentes routes de l'API.
- `auth.py` : Gestion de l'authentification.
- `coach.py` : Endpoints pour les coachs.
- `cycliste.py` : Endpoints pour les cyclistes.
- `enregistrement.py` : Enregistrement des performances.
- `stats.py` : Calcul et affichage des statistiques.
- `user.py` : Gestion des utilisateurs.

## 📁 models
Dossier contenant les modèles de base de données.
- `cycliste_db.py` : Modèle pour les cyclistes.
- `enregistrement_db.py` : Modèle pour les enregistrements.
- `utilisateur_db.py` : Modèle pour les utilisateurs.

## 📁 schemas
Dossier définissant les schémas de validation des données pour l'API.
- `auth_data.py` : Schéma pour les données d'authentification.
- `cyclist_data.py` : Schéma pour les données des cyclistes.
- `record_data.py` : Schéma pour les enregistrements.
- `user_data.py` : Schéma pour les utilisateurs.

## 📁 utils
Dossier contenant des outils et utilitaires réutilisables.
- `db_utils.py` : Fonctions utilitaires pour la base de données.
- `jwt_handlers.py` : Gestion des jetons JWT.
- `lifespan_handler.py` : Gestion du cycle de vie de l'application.

## 📄 Fichiers racine
- `main.py` : Point d'entrée principal.
- `db_create_all_tables.py` : Script de création des tables.
- `README.md` : Documentation du projet.
- `requirements.txt` : Dépendances du projet.
- `test_api.py` : Tests de l'API.

---

## 🚀 Installation et exécution  

### 1️⃣ Cloner le projet  

```bash
git clone https://github.com/A-Delvoye/Gestion_Perf_Cyclistes
cd Gestion_Perf_Cyclistes
```

### 2️⃣ Installer les dépendances  

```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer l'application  

```bash
uvicorn main:app --reload
```

L'API sera accessible à l'adresse : [http://127.0.0.1:8000](http://127.0.0.1:8000)  

---

## 🗃️ Base de données  

La base de données SQLite est initialisée avec les tables suivantes : 

Le Modele Physique des Données (MPD) est consultable sur le fichier MPD_Cycling_Team.png ou en suivant le lien suivant : 

[https://lucid.app/lucidchart/21bf50b1-b15a-42b3-870d-3f10ded8d95c/edit?invitationId=inv_d7385ee4-ab3e-4eee-8638-13195f57a0be] (https://lucid.app/lucidchart/21bf50b1-b15a-42b3-870d-3f10ded8d95c/edit?invitationId=inv_d7385ee4-ab3e-4eee-8638-13195f57a0be)

### 🔹 Utilisateurs (`utilisateurs`)  

| Champ         | Type     | Description                              |
|--------------|---------|------------------------------------------|
| id          | INTEGER | Clé primaire (auto-incrément)          |
| username    | TEXT    | Nom d'utilisateur                        |
| email       | TEXT    | Adresse e-mail                           |
| password_hash | TEXT  | Mot de passe hashé                      |
| role        | TEXT    | Rôle de l'utilisateur (admin/cycliste) |

### 🔹 Cyclistes (`cyclistes`)  

| Champ          | Type     | Description                                |
|---------------|---------|--------------------------------------------|
| id           | INTEGER | Clé primaire (auto-incrément)            |
| nom          | TEXT    | Nom du cycliste                            |
| age          | INTEGER | Âge du cycliste                          |
| poids       | REAL    | Poids en kg                                |
| taille      | REAL    | Taille en mètres                          |
| sexe        | TEXT    | Sexe (M/F)                                 |
| utilisateur_id | INTEGER | Clé étrangère vers `utilisateurs(id)` |

### 🔹 Enregistrements (`enregistrements`)  

| Champ               | Type     | Description                                      |
|---------------------|---------|--------------------------------------------------|
| id                | INTEGER | Clé primaire (auto-incrément)                  |
| id_utilisateur    | INTEGER | Clé étrangère vers `utilisateurs(id)`        |
| date              | DATETIME | Date de l'enregistrement                         |
| puissance_max     | REAL    | Puissance maximale (W)                          |
| vO2_max          | REAL    | VO2 max (ml/kg/min)                             |
| cadence_max      | REAL    | Cadence maximale (rpm)                          |
| f_cardiaque_max  | REAL    | Fréquence cardiaque max (bpm)                   |
| f_respiratoire_max | REAL  | Fréquence respiratoire max                     |

---

## 🔗 Endpoints disponibles  

### 🏁 Cyclistes  

| Méthode | Endpoint                      | Description                         |
|---------|--------------------------------|-------------------------------------|
| GET     | `/get_cycliste?cycliste_id=1`  | Récupérer un cycliste par ID       |
| POST    | `/create_cycliste`            | Ajouter un nouveau cycliste        |
| PUT     | `/update_cycliste/{id}`       | Modifier les informations d’un cycliste |
| DELETE  | `/delete_cycliste/{id}`       | Supprimer un cycliste              |

### 🏁 Enregistrements  

| Méthode | Endpoint                      | Description                         |
|---------|--------------------------------|-------------------------------------|
| POST    | `/enregistrement`             | Ajouter un enregistrement          |
| GET     | `/enregistrement?user_id=1`   | Récupérer les enregistrements d’un utilisateur |

### 📊 Statistiques

| Méthode | Endpoint                      | Description                         |
|---------|--------------------------------|-------------------------------------|
| POST    | `/stats/puissance_max_globale`             | Afficher la puissance max sur l'ensemble des cyclistes          |
| GET     | `/puissance_max_cycliste/id`   | Affiche la puissance max d'un cycliste donnée (id) |

---

## 🔒 Gestion des jetons  

L’authentification se fait via des jetons JWT. Un utilisateur doit inclure un token valide dans l’en-tête de ses requêtes.  

**Exemple d’en-tête d’authentification :**  

```http
Authorization: Bearer <token>
```

---

## 🏗️ Améliorations futures  

- 🔄 Implémentation d’un système de pagination pour les enregistrements.  
- 📈 Ajout de statistiques détaillées et visualisation des performances.  
- ☁️ Hébergement de l’API sur Azure avec Docker.  
- 🚀 Ajout d'un outil de visualisation Streamlit pour l'application et PowerBI pour les statistiques.

---
📢 Contact & Support

📧 Auteurs : 

- [Antoine Delvoye](https://github.com/A-Delvoye)
- [Nicolas Cassonnet](https://github.com/NicoCasso)

🌐 Projet : 
Gestion_Perf_Cyclistes :
(https://github.com/A-Delvoye/Gestion_Perf_Cyclistes)


N’hésitez pas à contribuer au projet et à ouvrir une issue en cas de problème ! 🚀
