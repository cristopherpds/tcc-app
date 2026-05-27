import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/users/random")
def random_user():
    try:
        response = requests.get("https://randomuser.me/api/", timeout=10)
        response.raise_for_status()
        user = response.json()["results"][0]
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return {
        "name": f"{user['name']['first']} {user['name']['last']}",
        "email": user["email"],
        "country": user["location"]["country"],
    }

@router.get("/users/nationality/{nat}")
def users_by_nationality(nat: str):
    try:
        response = requests.get(
            f"https://randomuser.me/api/?nat={nat}&results=5",
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    users = response.json()["results"]

    return [
        {
            "name": f"{u['name']['first']} {u['name']['last']}",
            "email": u["email"]
        }
        for u in users
    ]

