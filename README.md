# Airflow DAG avec Connexion SSH à base de données via Docker

Pour réaliser le test et vérifier le résultat, j'ai défini server de base données postgresql avec une image docker.
##  Fonctionnalités
- Conteneur Docker avec **PostgreSQL + Serveur SSH**
- DAG Airflow automatisant une requête SQL via SSH
- Gestion sécurisée des clés RSA et paramètres dans `/opt/airflow/config`

## Outils utilisés
- **WSL** 
- **Docker** et **Docker Compose** pour configurer un serveur de base données en local
- **Apache Airflow** (installé dans WSL)
- `sshpass` (pour l'automatisation SSH) :
  ```bash
  sudo apt-get install sshpass
  ```

##  Installation

### 1. Cloner le Projet
```bash
git clone https://github.com/thibaut7/Test_technique.git
cd airflow-ssh-postgres
```


### DAG Airflow
Placez le fichier `dag.py` dans `/opt/airflow/dags`.

## Utilisation

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
## Problème rencontré
J'ai plutot rencontré de problème au niveau de la configuration de l'authentification ssh au niveau du wsl. C'est à dire j'ai une erreur 'Permission denied(publickey)'. Alors que si je n'ai pas ce problème en accédant au server par windows.


Auteur: [thibaut7] | Date: 15 mars 2024
```
