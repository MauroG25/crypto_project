from pydantic import BaseModel
from datetime import datetime

class AssetSchema(BaseModel):
    id: int
    symbol: str
    name: str
    description: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
        
class AssetCreate(BaseModel):
    symbol: str
    name: str
    description: str | None = None
