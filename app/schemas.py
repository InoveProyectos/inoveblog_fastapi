from pydantic import BaseModel


class PosteoSchema(BaseModel):
    titulo: str
    texto: str
