```markdown
# Airflow DAG avec Connexion SSH à PostgreSQL via Docker

Ce projet démontre comment exécuter une tâche Airflow qui se connecte à une base de données PostgreSQL distante (simulée avec Docker) en utilisant une clé RSA protégée par une passphrase.

## 📋 Table des Matières
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Dépannage](#dépannage)

## 🚀 Fonctionnalités
- Conteneur Docker avec **PostgreSQL + Serveur SSH**
- DAG Airflow automatisant une requête SQL via SSH
- Gestion sécurisée des clés RSA et paramètres dans `/opt/airflow/config`

## 📦 Prérequis
- **WSL** (Ubuntu recommandé)
- **Docker** et **Docker Compose**
- **Apache Airflow** (installé dans WSL)
- `sshpass` (pour l'automatisation SSH) :
  ```bash
  sudo apt-get install sshpass
  ```

## 🔧 Installation

### 1. Cloner le Projet
```bash
git clone https://github.com/votre-repo/airflow-ssh-postgres.git
cd airflow-ssh-postgres
```

### 2. Générer les Clés SSH
```bash
mkdir -p /opt/airflow/config
ssh-keygen -t rsa -b 4096 -f /opt/airflow/config/id_rsa -N "ma_passphrase"
```

### 3. Démarrer le Serveur PostgreSQL/SSH
```bash
docker build -t postgres-ssh ./docker
docker run -d -p 5432:5432 -p 2222:22 --name=postgres-ssh \
  -v /opt/airflow/config/id_rsa.pub:/root/.ssh/authorized_keys \
  postgres-ssh
```

## ⚙️ Configuration

### Fichier `params.json`
Créez `/opt/airflow/config/params.json` :
```json
{
  "host": "localhost",
  "port": 2222,
  "user": "root",
  "dbname": "postgres",
  "ssh_key": "/opt/airflow/config/id_rsa",
  "passphrase": "ma_passphrase"
}
```

### DAG Airflow
Placez le fichier `ssh_postgres_dag.py` dans `/opt/airflow/dags`.

## 🖥️ Utilisation

### 1. Démarrer Airflow
```bash
airflow webserver --port 8080 &
airflow scheduler
```

### 2. Déclencher le DAG
- Accédez à http://localhost:8080
- Activez et déclenchez manuellement le DAG `ssh_postgres_test`.

### 3. Vérifier la Base de Données
```bash
docker exec -it postgres-ssh psql -U postgres -c "SELECT * FROM test;"
```

## 📂 Structure du Projet
```
.
├── docker/
│   ├── Dockerfile          # Configuration PostgreSQL + SSH
│   └── start.sh           # Script de démarrage combiné
├── dags/
│   └── ssh_postgres_dag.py # DAG Airflow
└── README.md
```

## 🛠️ Dépannage

### Erreur "psql: connection to server failed"
- Vérifiez que le conteneur est actif :
  ```bash
  docker ps | grep postgres-ssh
  ```
- Consultez les logs PostgreSQL :
  ```bash
  docker logs postgres-ssh | grep 'PostgreSQL'
  ```

### Erreur SSH "Permission denied"
- Vérifiez que la clé publique est bien montée :
  ```bash
  docker exec -it postgres-ssh cat /root/.ssh/authorized_keys
  ```

### DAG Non Détecté
- Vérifiez le dossier des DAGs dans `airflow.cfg` :
  ```ini
  dags_folder = /opt/airflow/dags
  ```

## 🔒 Notes de Sécurité
- **Ne pas utiliser en production** : 
  - La passphrase est stockée en clair dans `params.json`.
  - L'accès SSH en tant que `root` est déconseillé.
- Pour un environnement réel :
  - Utilisez des secrets managés (ex: Airflow Variables chiffrées, Vault).
  - Remplacez `sshpass` par une méthode plus sécurisée.

---

**📌 Ce projet est une preuve de concept (POC) pour des tests locaux.**  
Auteur: [Votre Nom] | Date: 15 mars 2024
```
