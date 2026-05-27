import os
from fastapi import FastAPI
from datetime import datetime
import socket
import uuid

APP_VERSION = "0.2.4"
START_TIME = datetime.utcnow()
INSTANCE_ID = str(uuid.uuid4())[:8]

app = FastAPI(
    title="FastAPI TCC: GitOps Demo",
    description="Demo de la aplicación para pruebas de TCC: GitOps + ArgoCD",
    version=APP_VERSION,
)

@app.get("/")
def read_root():
    return {
        "message": "🚀 Hello from GKE Autopilot – NEW RELEASE!",
        "app_version": APP_VERSION,
        "instance_id": INSTANCE_ID,
        "pod_name": os.getenv("POD_NAME", "unknown"),
        "node_name": socket.gethostname(),
        "project_id": os.getenv("PROJECT_ID", "unknown"),
        "started_at_utc": START_TIME.isoformat() + "Z",
        "uptime_seconds": int((datetime.utcnow() - START_TIME).total_seconds()),
    }

@app.get("/version")
def version():
    return {
        "version": APP_VERSION,
        "instance_id": INSTANCE_ID,
        "started_at": START_TIME.isoformat() + "Z",
    }

@app.get("/whoami")
def whoami():
    return {
        "pod_name": os.getenv("POD_NAME"),
        "node": socket.gethostname(),
        "instance_id": INSTANCE_ID,
        "env": os.getenv("ENV", "production"),
    }

@app.get("/health/live")
def liveness():
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

@app.get("/health/ready")
def readiness():
    return {
        "status": "ready",
        "checks": {
            "config_loaded": True,
            "dependencies_ok": True,
        },
    }

@app.get("/config")
def config_preview():
    return {
        "env": {
            "POD_NAME": os.getenv("POD_NAME"),
            "PROJECT_ID": os.getenv("PROJECT_ID"),
            "ENV": os.getenv("ENV", "production"),
        }
    }

@app.get("/feature/experimental")
def experimental_feature():
    return {
        "feature": "experimental",
        "enabled": True,
        "changed_in": "0.1.6",
        "note": "This response is DIFFERENT than in 0.1.5",
    }

@app.get("/environment")
def environment_info():
    """Endpoint para verificar se está rodando localmente ou em GKE"""
    pod_name = os.getenv("POD_NAME")
    project_id = os.getenv("PROJECT_ID")
    
    # Se não tem POD_NAME ou PROJECT_ID, está rodando localmente
    is_local = not pod_name or not project_id
    
    return {
        "environment": "local" if is_local else "gke",
        "is_kubernetes": not is_local,
        "pod_name": pod_name or "localhost",
        "project_id": project_id or "not-set",
        "env_vars_set": {
            "POD_NAME": pod_name is not None,
            "PROJECT_ID": project_id is not None,
        },
        "app_version": APP_VERSION,
        "instance_id": INSTANCE_ID,
    }

from users import router as users_router

app.include_router(users_router)