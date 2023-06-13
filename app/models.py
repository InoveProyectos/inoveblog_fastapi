from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TEXT, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }


class Posteo(Base):
    __tablename__ = "posteos"

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    texto = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "texto": self.texto,
            "user_id": self.user_id,
        }
