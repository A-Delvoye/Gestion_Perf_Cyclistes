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

```bash
gest_perf_cycl/
│── db/
│   ├── gest_perf_cycl.db  # Base de données SQLite
│── models/
│   ├── utilisateur_db.py  # Modèle SQL des utilisateurs
│   ├── cycliste_db.py  # Modèle SQL des cyclistes
│   ├── enregistrement_db.py  # Modèle SQL des enregistrements
│── routes/
│   ├── cycliste.py  # Endpoints pour la gestion des cyclistes
│   ├── enregistrement.py  # Endpoints pour la gestion des enregistrements
│── core/
│   ├── security.py  # Gestion des tokens et de l'authentification
│   ├── password_tools.py  # Hashage des mots de passe
│── main.py  # Point d'entrée de l'API
│── requirements.txt  # Dépendances du projet
│── README.md  # Documentation
```

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

### 📊 Enregistrements  

| Méthode | Endpoint                      | Description                         |
|---------|--------------------------------|-------------------------------------|
| POST    | `/enregistrement`             | Ajouter un enregistrement          |
| GET     | `/enregistrement?user_id=1`   | Récupérer les enregistrements d’un utilisateur |

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

---
📢 Contact & Support
- (https://github.com/A-Delvoye)
- (https://github.com/NicoCasso)
📧 Auteurs : wbensolt@example.com
🌐 Projet : (https://github.com/A-Delvoye/Gestion_Perf_Cyclistes)


N’hésitez pas à contribuer au projet et à ouvrir une issue en cas de problème ! 🚀
