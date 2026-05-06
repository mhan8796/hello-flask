# Split React + Flask

A small full-stack app split into separate frontend and backend folders.

```text
backend/    Flask API
frontend/   React frontend
```

## Run Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --port 5002
```

## Run Frontend

From another terminal:

```bash
cd frontend
python3 -m http.server 5173
```

Then open http://127.0.0.1:5173.

The frontend calls the backend at http://127.0.0.1:5002.

## Run With Docker

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:5174
```

The containerized frontend is served by nginx on port `5174`, and the Flask API
is served by gunicorn on port `5002`.

## Deploy To Local Kubernetes With Helm

This project includes separate Helm charts for the backend and frontend:

```text
charts/hello-flask-backend/
charts/hello-flask-frontend/
```

Build the images and load them into the local kind cluster:

```bash
docker compose build
../kubernetes-lab/bin/kind load docker-image hello-flask-backend:0.1.0 --name terraform-k8s
../kubernetes-lab/bin/kind load docker-image hello-flask-frontend:0.1.0 --name terraform-k8s
```

Install NGINX ingress with Helm:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --kube-context kind-terraform-k8s \
  --wait
```

Deploy the backend chart:

```bash
helm upgrade --install hello-flask-backend charts/hello-flask-backend \
  --namespace hello-flask \
  --create-namespace \
  --kube-context kind-terraform-k8s \
  --wait
```

Deploy the frontend chart:

```bash
helm upgrade --install hello-flask-frontend charts/hello-flask-frontend \
  --namespace hello-flask \
  --create-namespace \
  --kube-context kind-terraform-k8s \
  --wait
```

Expose it locally:

```bash
kubectl --context kind-terraform-k8s -n ingress-nginx port-forward service/ingress-nginx-controller 8080:80
```

Then open:

```text
http://127.0.0.1:8080
```

The Ingress routes `/` to the frontend service and `/api` to the backend service.
