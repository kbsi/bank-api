---

# 🏦 **API Bancaire NoSQL**

Flask
MongoDB
Python
Docker

## 🌟 **Présentation du Projet**
Bienvenue dans notre projet d'API bancaire avancée utilisant une base de données NoSQL (MongoDB Atlas). Ce projet a été développé dans le cadre d'un TP et a pour objectif de démontrer la conception d'une architecture backend robuste, sécurisée et évolutive.

### **Fonctionnalités principales :**
- **Opérations CRUD** : Gestion des utilisateurs, comptes bancaires et transactions.
- **Gestion des rôles et droits d'accès** : Différents niveaux d'accès (Admin, Client, Analyste...).
- **Système de logging** : Traçabilité complète des actions effectuées.
- **Analyse comportementale** : Extraction de données anonymisées pour les besoins marketing.

---

## 🔧 **Stack Technique**

| Technologie         | Description                                                            |
| ------------------- | ---------------------------------------------------------------------- |
| **Python**          | Langage principal utilisé pour développer l'API.                       |
| **Flask**           | Framework web léger pour créer l'API RESTful.                          |
| **MongoDB Atlas**   | Base de données NoSQL hébergée dans le cloud pour stocker les données. |
| **Redis**           | Cache utilisé pour la gestion des sessions.                            |
| **Docker**          | Conteneurisation de l'application pour un déploiement simplifié.       |
| **Swagger/OpenAPI** | Documentation interactive des endpoints exposés par l'API.             |

---

## 📂 **Structure du Projet**

```
bank-api/
├── app/
│   ├── __init__.py          # Initialisation de l'application Flask
│   ├── config.py            # Configuration globale (MongoDB URI, JWT secret)
│   ├── models/              # Modèles représentant les entités principales
│   │   ├── user.py          # Modèle utilisateur
│   │   ├── account.py       # Modèle compte bancaire
│   │   └── transaction.py   # Modèle transaction
│   ├── routes/              # Endpoints exposés par l'API
│   │   ├── auth.py          # Authentification et gestion des utilisateurs
│   │   ├── accounts.py      # Gestion des comptes bancaires
│   │   ├── admin.py         # Fonctionnalités administratives
│   ├── services/            # Logique métier et interactions avec MongoDB
│   │   ├── auth.py          # Gestion des tokens JWT
│   │   ├── mongo.py         # Fonctions utilitaires pour MongoDB
│   │   └── logger.py        # Système de logging centralisé
│   ├── utils/               # Fonctions utilitaires réutilisables
│       ├── decorators.py    # Décorateurs pour sécuriser les endpoints
│       └── validators.py    # Validation des données entrantes
├── scripts/                 # Scripts auxiliaires
│   └── generate_data.py     # Génération de données factices (100+ entrées)
├── tests/                   # Tests unitaires et fonctionnels
├── .env                     # Variables d'environnement sensibles (MongoDB URI, JWT secret)
├── Pipfile                  # Gestionnaire de dépendances (pipenv)
├── docker-compose.yml       # Déploiement conteneurisé avec Docker Compose
├── Dockerfile               # Image Docker pour l'application Flask
└── README.md                # Documentation du projet
```

---

## 🗂️ **Schéma de la Base de Données**

### Collections principales :

1. **`users`**

   ```json
   {
     "_id": "ObjectId",
     "email": "client@example.com",
     "password_hash": "hashed_password",
     "roles": ["client"],
     "accounts": ["account_id"],
     "created_at": "2025-02-04T09:00:00Z"
   }
   ```

2. **`accounts`**

   ```json
   {
     "_id": "ObjectId",
     "user_id": "user_id",
     "account_number": "FR761111222233334444",
     "balance": 1500.5,
     "currency": "EUR",
     "transactions": ["transaction_id"],
     "status": "active"
   }
   ```

3. **`transactions`**

   ```json
   {
     "_id": "ObjectId",
     "from_account": "account_id",
     "to_account": "account_id",
     "amount": 200.0,
     "type": "transfer",
     "timestamp": "2025-02-04T09:10:00Z",
     "status": "completed"
   }
   ```

4. **`logs`**
   ```json
   {
     "_id": "ObjectId",
     "user_id": "user_id",
     "action_type": "transfer",
     "details": { ... },
     "timestamp": "2025-02-04T09:10:00Z"
   }
   ```

---

## 🚀 **Exemples d'Endpoints API**

### Authentification :

1. **Enregistrement d'un utilisateur**

   ```http
   POST /api/auth/register
   Body: { "email": "...", "password": "...", ... }
   Response: { "message": "Utilisateur enregistré avec succès" }
   ```

2. **Connexion et génération de token JWT**
   ```http
   POST /api/auth/login
   Body: { "email": "...", "password": "...", ... }
   Response: { "access_token": "<JWT_TOKEN>" }
   ```

### Gestion des Comptes :

1. **Création d'un compte bancaire**

   ```http
   POST /api/accounts/create
   Headers: { Authorization: Bearer <JWT_TOKEN> }
   Body: {
       "balance": 5000,
       "currency": "EUR"
    }
   Response: { ... }
   ```

2. **Transfert entre comptes**
   ```http
   POST /api/accounts/transfer
   Headers: { Authorization: Bearer <JWT_TOKEN> }
   Body: {
       "from_account": "<account_id>",
       "to_account": "<account_id>",
       "amount": 200
    }
   Response: { ... }
   ```

---

## 🛠️ **Installation et Lancement**

### Prérequis :

1. Python 3.9+
2. Pipenv installé (`pip install pipenv`)
3. Docker et Docker Compose

### Étapes :

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-repo/bank-api.git && cd bank-api
   ```
2. Installez les dépendances :
   ```bash
   pipenv install --dev && pipenv shell
   ```
3. Configurez les variables d'environnement dans `.env`.

4. Lancez via Docker Compose :
   ```bash
   docker-compose up --build
   ```

---

## 📖 **Documentation API**

La documentation interactive est disponible via Swagger à l'adresse suivante après démarrage de l'application :

```
http://localhost:5050/apidocs/
```

---

## 🎯 **User Stories**

### Exemple : Consultation du solde d'un compte en tant que client.

1. Le client se connecte via `/api/auth/login`.
2. Il utilise le token JWT généré pour accéder à `/api/accounts`.

---

### Ajouter le jeton JWT dans Swagger UI

1. Accédez à Swagger UI : Ouvrez votre navigateur et accédez à l'URL de Swagger UI, par exemple http://localhost:5050/apidocs/.

2. Utiliser /api/auth/login pour récupérer un jeton
   se connecter avec cmurray@example.net et password123 par exemple (user support / analyst / admin)

3. Ajouter le jeton JWT :

- Cliquez sur le bouton Authorize en haut à droite de Swagger UI.
- Une fenêtre modale s'ouvrira. Dans le champ Value, entrez votre jeton JWT avec le préfixe Bearer. Par exemple :

```
Bearer your_jwt_token
```

- Cliquez sur le bouton Authorize pour enregistrer le jeton.

4. Tester les endpoints : Vous pouvez maintenant tester les endpoints protégés par JWT dans Swagger UI. Le jeton JWT sera automatiquement inclus dans les en-têtes Authorization des requêtes.
