# TaskFlow

A minimal Python/Flask task manager.

## Stack

| Layer | Tech |
|---|---|
| App | Python 3.11 + Flask |
| Tests | pytest + pytest-cov |
| Container | Docker + Gunicorn |
| CI/CD | Jenkins Declarative Pipeline |

---

## Project Structure

```
taskflow/
├── app/
│   ├── __init__.py
│   └── routes.py          # Flask API (GET/POST/PATCH/DELETE)
├── tests/
│   └── test_api.py        # 20 pytest tests across 5 classes
├── templates/
│   └── index.html         # Single-page UI
├── Dockerfile
├── Jenkinsfile            # 4-stage pipeline
├── requirements.txt
├── pytest.ini
└── wsgi.py
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | UI |
| GET | `/health` | Health check |
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create task `{"title":"..."}` |
| PATCH | `/api/tasks/<id>` | Toggle done/pending |
| DELETE | `/api/tasks/<id>` | Delete task |

---

## Run Locally

```bash
pip install -r requirements.txt
python wsgi.py
# → http://localhost:5000
```

## Run Tests

```bash
pytest
```

---

## Jenkins Pipeline Stages

```
Checkout → Build → Test → Deploy
```
