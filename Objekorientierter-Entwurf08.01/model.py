
from pydantic import BaseModel, Field

class Spieler(BaseModel):
    name: str = Field(default="Felix")
    jahrgang: int = Field( ge=16, le=5000)
    staerke: int = Field( ge=0, le=10)
    torschuss: int = Field( ge=1, le=10)
    

