import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/crypto/bitcoin")
def bitcoin_price():
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin&vs_currencies=usd",
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return response.json()
