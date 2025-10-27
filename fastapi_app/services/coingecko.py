import requests
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

def fetch_ohlcv(db: Session, asset: models.Asset, days: int = 30):
    url = COINGECKO_URL.format(id=asset.name.lower())
    params = {"vs_currency": "usd", "days": days}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Error al obtener datos: {response.text}")

    data = response.json()

    # CoinGecko devuelve precios como [timestamp, price]
    prices = data.get("prices", [])
    volumes = data.get("total_volumes", [])

    for i, (ts, price) in enumerate(prices):
        timestamp = datetime.utcfromtimestamp(ts / 1000)

        # Para simplificar: usamos el mismo precio como open/high/low/close
        # (CoinGecko no da OHLC exacto en este endpoint)
        volume = volumes[i][1] if i < len(volumes) else 0

        ohlcv = models.OHLCV(
            asset_id=asset.id,
            timestamp=timestamp,
            open=price,
            high=price,
            low=price,
            close=price,
            volume=volume
        )
        db.add(ohlcv)

    db.commit()