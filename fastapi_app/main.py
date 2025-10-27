from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from .services.coingecko import fetch_ohlcv   # 👈 importamos el servicio nuevo

app = FastAPI(title="Crypto API")

# Dependencia de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints existentes ---
@app.get("/assets", response_model=list[schemas.AssetSchema])
def get_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()

@app.post("/assets", response_model=schemas.AssetSchema)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.symbol == asset.symbol).first()
    if db_asset:
        raise HTTPException(status_code=400, detail="El símbolo ya existe")

    from datetime import datetime
    new_asset = models.Asset(
        symbol=asset.symbol,
        name=asset.name,
        description=asset.description,
        created_at=datetime.utcnow()
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

# --- Nuevo endpoint para poblar OHLCV ---
@app.post("/assets/{symbol}/fetch_ohlcv")
def fetch_asset_ohlcv(symbol: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.symbol == symbol.upper()).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset no encontrado")

    # Ejecutamos en segundo plano para no bloquear la API
    background_tasks.add_task(fetch_ohlcv, db, asset, 30)
    return {"message": f"Descargando datos OHLCV para {asset.name}"}