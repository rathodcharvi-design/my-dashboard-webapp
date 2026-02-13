# My Dashboard Web App — Flask on DigitalOcean Kubernetes (DOKS)

This repository contains the **My Dashboard** Flask application containerized with Docker, pushed to **DigitalOcean Container Registry (DOCR)**, and deployed on **DigitalOcean Kubernetes (DOKS)** with a LoadBalancer Service and Horizontal Pod Autoscaling (HPA).

---

## Repository Contents
- `app/` – Flask application code
- `Dockerfile` – Container build definition
- `requirements.txt` – Python dependencies
- `k8s/` – Kubernetes manifests:
  - `deployment.yaml`
  - `service.yaml`

---

## Prerequisites
- DigitalOcean account
- `doctl` installed and authenticated
- `kubectl` installed
- Docker installed and running
- A DOKS cluster created
- A DOCR registry created

---

## Step 1 — Authenticate to DigitalOcean
```bash
doctl auth init
doctl account get

