# My Dashboard Web App on DigitalOcean Kubernetes (DOKS)

This repository contains the My Dashboard Flask application containerized with Docker, pushed to DigitalOcean Container Registry (DOCR), and deployed on DigitalOcean Kubernetes (DOKS) using:

- Kubernetes Deployment
- Kubernetes Service (Type: LoadBalancer)
- Health Probes (/healthz, /readyz)
- Horizontal Pod Autoscaling (HPA)

---

## Repository Structure

app/                → Flask application code  
Dockerfile          → Container build definition  
requirements.txt    → Python dependencies  
k8s/deployment.yaml → Kubernetes Deployment  
k8s/service.yaml    → Kubernetes Service  

---

## Prerequisites

- DigitalOcean account
- Docker installed
- doctl installed and authenticated
- kubectl installed
- DOKS cluster created
- DOCR registry created

---

## 1. Authenticate to DigitalOcean

Generate Personal Access Token from DO Console → API → Tokens.

Initialize doctl:

    doctl auth init
    doctl account get

---

## 2. Configure kubectl for DOKS

    doctl kubernetes cluster kubeconfig save my-dashboard-cluster
    kubectl get nodes

---

## 3. Build and Push Docker Image

Login to registry:

    doctl registry login

Build image:

    docker build -t registry.digitalocean.com/my-dashboard-registry/my-dashboard:1.1 .

Push image:

    docker push registry.digitalocean.com/my-dashboard-registry/my-dashboard:1.1

---

## 4. Create Namespace and Configure Registry Pull Secret

Create namespace:

    kubectl create namespace my-dashboard

Create image pull secret:

    doctl registry kubernetes-manifest --namespace my-dashboard | kubectl apply -f -

Attach secret to default service account:

    kubectl patch serviceaccount default -n my-dashboard \
      -p '{"imagePullSecrets":[{"name":"registry-my-dashboard-registry"}]}'

---

## 5. Deploy Application

Deploy Kubernetes resources:

    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml

Verify deployment:

    kubectl rollout status deployment my-dashboard -n my-dashboard
    kubectl get pods -n my-dashboard -o wide
    kubectl get svc -n my-dashboard

---

## 6. Access Application

Retrieve external IP:

    kubectl get svc -n my-dashboard

Test endpoints:

    curl http://<EXTERNAL-IP>/status
    curl http://<EXTERNAL-IP>/healthz
    curl http://<EXTERNAL-IP>/readyz

---

## 7. Enable Horizontal Pod Autoscaling (HPA)

Install Metrics Server:

    kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

Create HPA (70% CPU target, min=2, max=6):

    kubectl autoscale deployment my-dashboard \
      -n my-dashboard \
      --cpu=70% \
      --min=2 \
      --max=6

Verify:

    kubectl get hpa -n my-dashboard
    kubectl top pods -n my-dashboard

---

## Troubleshooting

ImagePullBackOff / 401 Unauthorized

    kubectl get secret -n my-dashboard | grep registry
    doctl registry kubernetes-manifest --namespace my-dashboard | kubectl apply -f -

CrashLoopBackOff (exec format error)

    docker build --platform=linux/amd64 \
      -t registry.digitalocean.com/my-dashboard-registry/my-dashboard:1.1 .
    docker push registry.digitalocean.com/my-dashboard-registry/my-dashboard:1.1
    kubectl rollout restart deployment my-dashboard -n my-dashboard

HPA shows cpu: <unknown>/70%

    kubectl top pods -n my-dashboard

---

## Cleanup

    kubectl delete namespace my-dashboard

---

## References

- DigitalOcean Kubernetes (DOKS): https://docs.digitalocean.com/products/kubernetes/
- DigitalOcean Container Registry (DOCR): https://docs.digitalocean.com/products/container-registry/
- doctl CLI Installation: https://docs.digitalocean.com/reference/doctl/how-to/install/
- Kubernetes Documentation: https://kubernetes.io/docs/home/
- Kubernetes Metrics Server: https://github.com/kubernetes-sigs/metrics-server
- Docker Documentation: https://docs.docker.com/

