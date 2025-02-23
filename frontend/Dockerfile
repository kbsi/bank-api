# Utiliser une image de base Node.js
FROM node:14

# Définir le répertoire de travail
WORKDIR /frontend

# Copier le fichier package.json et installer les dépendances
COPY package.json ./
RUN npm install

# Copier le reste du code source
COPY . .

# Exposer le port 3000
EXPOSE 3000

# Commande pour démarrer l'application React
CMD ["npm", "start"]