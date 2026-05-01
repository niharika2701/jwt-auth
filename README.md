# Module 13 - JWT Authentication with Playwright E2E Tests

**IS 601 | Python for Web API | NJIT**

Builds on Module 12 by adding JWT-based authentication, register and login
front-end pages, and Playwright E2E tests with a full CI/CD pipeline.

---

## Docker Hub

Image: `niharika2701/module13-jwt-auth:latest`

```bash
docker pull niharika2701/module13-jwt-auth:latest
```

Link: https://hub.docker.com/r/niharika2701/module13-jwt-auth

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /auth/register | Register and return user data |
| POST | /auth/login | Login and return JWT token |
| GET | /register | Register page |
| GET | /login | Login page |

---

## How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Run the app

```bash
DATABASE_URL="sqlite:///./local.db" python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/register and http://127.0.0.1:8000/login

### 3. Run E2E tests

```bash
python -m pytest tests/test_e2e.py -v
```

The server starts automatically during tests. No manual setup needed.

---

## CI/CD Pipeline

GitHub Actions runs on every push:

1. **Test job** - installs Playwright, starts server, runs all 9 E2E tests
2. **Deploy job** - builds and pushes Docker image to Docker Hub on success
