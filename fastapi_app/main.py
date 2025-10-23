from fastapi import FastAPI

app = FastAPI(title="Crypto API")

@app.get("/")
def root():
    return {"message": "FastAPI funcionando junto a Django 🚀"}

