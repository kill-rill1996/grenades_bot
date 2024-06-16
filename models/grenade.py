from pydantic import BaseModel


class StatusError(BaseModel):
    error: str


class StatusOK(BaseModel):
    message: str


class Image(BaseModel):
    id: int
    name: str
    grenade_id: int = None
    image_url: str


class CreateGrenadeModel(BaseModel):
    map: str
    title: str
    description: str
    type: str
    side: str


class Grenade(CreateGrenadeModel):
    id: int
    version: int
    images: list[Image] = None


class Grenades(BaseModel):
    grenades: list[Grenade]
