# Books API on Kubernetes

A production-ready REST API for managing books, containerized with Docker and deployed on Kubernetes. Includes MySQL as a StatefulSet, Kustomize overlays for dev/prod, HPA autoscaling, and a full CI/CD pipeline with GitHub Actions.

---

## Project structure

```
books-api/
├── app.py                        # Flask app (health + ready endpoints added)
├── config/
│   ├── db.py                     # Config class from env vars
│   └── mysql.py                  # PyMySQL connection + schema init
├── routes/bookRoutes.py
├── service/bookService.py
├── requirements.txt
├── Dockerfile                    # Multi-stage, non-root, healthcheck
├── docker-compose.yml            # Local dev: Flask + MySQL together
├── k8s/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── secret.yaml           # MySQL credentials (base64)
│   │   ├── configmap.yaml        # Non-sensitive config
│   │   ├── mysql.yaml            # StatefulSet + headless Service
│   │   ├── deployment.yaml       # Flask API deployment + Service
│   │   ├── hpa.yaml              # Auto-scale 2 → 8 pods
│   │   ├── ingress.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── dev/                  # 1 replica, testdb_dev
│       └── prod/                 # 3 replicas
└── .github/workflows/ci-cd.yml   # Lint → Build → Dev → Prod (approval)
```

---

## Quick start

### Option 1 — Docker Compose (simplest)

```bash
cp .env.example .env          # fill in your values
docker compose up --build
```

Test it:
```bash
curl http://localhost:5000/books
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert C. Martin"}'
```

### Option 2 — Local Kubernetes with kind

```bash
# Requires: kind, kubectl, docker
chmod +x scripts/*.sh
./scripts/local-setup.sh

# In a separate terminal:
kubectl port-forward svc/books-api-service 5000:80 -n books-api

curl http://localhost:5000/books
```

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check message |
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe (pings MySQL) |
| GET | `/books` | List all books |
| GET | `/books/<id>` | Get book by ID |
| POST | `/books` | Create book `{"title": "...", "author": "..."}` |
| PUT | `/books/<id>` | Update book |
| DELETE | `/books/<id>` | Delete book |

---

## GitHub Secrets required

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `KUBECONFIG_DEV` | base64-encoded kubeconfig for dev cluster |
| `KUBECONFIG_PROD` | base64-encoded kubeconfig for prod cluster |

---

## Key design decisions

**Why StatefulSet for MySQL?** Databases are stateful — they need a stable network identity and persistent storage. A Deployment would lose all data on pod restart.

**Why a headless Service for MySQL?** StatefulSets use DNS-based discovery. A headless Service (`clusterIP: None`) lets pods resolve directly by name (`mysql-0.mysql-service`).

**Why does `/ready` ping MySQL?** The readiness probe uses your actual DB connection. This means Kubernetes only sends traffic to API pods that can actually reach the database. Without this, your app could be "running" but returning 500s on every request.

**Why separate ConfigMap and Secret?** Non-sensitive config (host, db name, user) goes in ConfigMap. Passwords go in Secret. Mixing them would force you to handle secrets more carefully than needed.
