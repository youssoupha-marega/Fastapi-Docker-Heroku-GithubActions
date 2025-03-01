# Utilisation d'une image légère Python 3.12.2 slim
FROM python:3.12.2-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers dans le conteneur
COPY . /app

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port
#EXPOSE 8000

# Commande pour exécuter l'application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
