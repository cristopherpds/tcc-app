import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/pokemon/{name}")
def pokemon(name: str):
    try:
        response = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{name.lower()}",
            timeout=10
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Pokemon not found"
            )

        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    data = response.json()

    return {
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "base_experience": data["base_experience"]
    }