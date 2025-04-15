
# Taxon Search Web App

This is a simple single-page application (SPA) built with FastAPI (backend) and Dash (frontend). It allows users to search taxon names using different search modes (contains, starts with, ends with) and displays paginated results.

---

## 🚀 Getting Started

### 1. Install Requirements

Install the required packages for both the frontend and backend:

```bash
pip3 install -r requirements.txt
```

---

### 2. Run the Backend

Start the FastAPI backend server:

```bash
cd backend
python3 main.py
```

This will run the API server at: `http://127.0.0.1:8000/`

---

### 3. Run the Frontend

In a new terminal, start the Dash frontend:

```bash
cd frontend
python3 app_v2.py
```

This will launch the app in your browser at: `http://127.0.0.1:8050/`

---

## 🧪 Features

- Search by keyword with different match types.
- Data fetched from FastAPI using query parameters.

---

## 🛠 Requirements

- Python 3.8+
- FastAPI
- Dash
- pandas
- SQLModel
- Uvicorn


---

## 💡 Tip

Make sure your database and models are correctly set up in `backend/main.py`. The app assumes an existing database with `Taxon` and `TaxonName` models.
