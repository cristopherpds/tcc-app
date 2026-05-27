import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/predict/age/{name}")
def predict_age(name: str):
    try:
        response = requests.get(
            f"https://api.agify.io?name={name}",
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return response.json()