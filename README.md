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
./bin/kind load docker-image hello-flask-backend:0.1.0 --name terraform-k8s
./bin/kind load docker-image hello-flask-frontend:0.1.0 --name terraform-k8s
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

## GitOps Deploy With GitHub Actions And Argo CD

The workflow at `.github/workflows/deploy.yml` builds both Docker images and
pushes them to GitHub Container Registry. It does not talk to Kubernetes
directly.

After pushing images, the workflow updates these Helm values files with the new
image tags and commits the change back to `main`:

```text
charts/hello-flask-backend/values.yaml
charts/hello-flask-frontend/values.yaml
```

Argo CD then watches this repo, sees the changed chart values, and syncs the
Helm charts into Kubernetes.

The Argo CD Application manifests are:

```text
argocd/ingress-nginx.yaml
argocd/hello-flask-backend.yaml
argocd/hello-flask-frontend.yaml
```

After Argo CD is installed in a cluster, apply them once:

```bash
kubectl apply -f argocd/ingress-nginx.yaml
kubectl apply -f argocd/hello-flask-backend.yaml
kubectl apply -f argocd/hello-flask-frontend.yaml
```

From then on, the flow is:

```text
Git push
  -> GitHub Actions builds and pushes images
  -> GitHub Actions updates Helm values in Git
  -> Argo CD syncs Kubernetes from Git
```
