
from pydantic import BaseModel, Field

class Spieler(BaseModel):
    name: str = Field(default="Felix")
    age: int = Field(default=18, ge=16, le=50)
    staerke: int = Field(default=5, ge=1, le=10)
    torschuss: int = Field(default=5, ge=1, le=10)
    motivation: int = Field(default=5, ge=1, le=10)

  

s = Spieler(name="Alice", age=30)
print(s.model_dump())

