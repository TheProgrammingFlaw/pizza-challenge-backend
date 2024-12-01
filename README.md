
# 🍕 Pizza Challenge Backend

This is the backend implementation for the **Pizza Eating Challenge** app, which manages users, virtual currency, pizza purchases, and a leaderboard system.

## 🚀 Features

- **User Management:** Create, update, delete, and manage players.
- **Virtual Currency System:** Users receive 500 coins upon registration to buy pizza slices.
- **Dedicated User Wallets.** User wallets created, updated and deleted with each update accordingly.
- **Pizza Logging:** Users can log pizzas only after purchasing them.
- **Leaderboard:** Displays players ranked by the number of pizzas eaten.
- **Real-Time Rank Updates:** Ensures the leaderboard reflects the latest data.

## 🛠️ Technology Stack

- **Backend:** Python (Flask)
- **Database:** Firebase NoSQL
- **Deployment:** Render

## 📋 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/TheProgrammingFlaw/pizza-challenge-backend.git
cd pizza-challenge-backend
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # For MacOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Firebase Setup
1. Create a Firebase project.
2. Download the service account JSON key and set it as an environment variable in `.env`:
   ```env
   FIREBASE_CREDENTIALS=/path/to/serviceAccountKey.json
   ```

### 5. Run the Application
```bash
python run.py
```

The backend will be available at `http://127.0.0.1:5000/`.

## 🔗 API Endpoints

| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| POST   | `/api/createUser`   | Creates a new user       |
| GET    | `/api/getUsers`     | Fetches all users        |
| POST   | `/api/buyPizza`     | Buys pizza for a user    |
| POST   | `/api/logPizza`     | Logs pizza consumption   |
etc...

## 🔄 Deployment

The backend can be deployed to **Render**

### Render Deployment
1. Create a new web service in Render.
2. Connect the GitHub repository.
3. Set the **Start Command** to:
   ```bash
   python run.py
   ```
4. Configure the environment variable `FIREBASE_CREDENTIALS` to point to the service account file.

## 🏗️ Contributors

- [**TheProgrammingFlaw**](https://github.com/TheProgrammingFlaw)
