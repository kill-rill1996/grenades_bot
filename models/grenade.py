from pydantic import BaseModel


class Image(BaseModel):
    id: int
    name: str
    grenade_id: int = None
    image_url: str


class Grenade(BaseModel):
    id: int
    map: str
    title: str
    description: str
    type: str
    side: str
    version: int
    images: list[Image] = None


class Grenades(BaseModel):
    grenades: list[Grenade]
