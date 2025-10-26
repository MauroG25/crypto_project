from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from datetime import datetime


app = FastAPI(title="Crypto API")

# Dependencia de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET: listar todos los assets
@app.get("/assets", response_model=list[schemas.AssetSchema])
def get_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()

# POST: crear un nuevo asset
@app.post("/assets", response_model=schemas.AssetSchema)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe el símbolo
    db_asset = db.query(models.Asset).filter(models.Asset.symbol == asset.symbol).first()
    if db_asset:
        raise HTTPException(status_code=400, detail="El símbolo ya existe")

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