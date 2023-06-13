from models import User, Posteo

def get_user(db, nombre):
    user = db.query(User).filter(User.nombre == nombre).first()
    return user


def create_user(db, nombre: str):
    user = User(nombre=nombre)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_posteo(db, user: User, posteo_id: int) -> Posteo:
    posteo = db.query(Posteo).filter(
        Posteo.user_id==user.id,
        Posteo.id==posteo_id
    ).first()
    return posteo


def get_posteos(db, user: User):
    posteos = db.query(Posteo).filter(
        Posteo.user_id==user.id
    ).all()
    return posteos


def create_posteo(db, user: User, titulo: str, texto: str) -> Posteo:
    posteo = Posteo(user=user, titulo=titulo, texto=texto)
    db.add(posteo)
    db.commit()
    db.refresh(posteo)
    return posteo


def update_posteo(db, user: User, posteo_id: int, titulo: str, texto: str) -> Posteo:
    posteo = get_posteo(db, user, posteo_id)
    if posteo is None:
        return None
    
    posteo.titulo = titulo
    posteo.texto = texto
    db.commit()
    return posteo


def delete_posteos(db, user: User, posteo_id: int) -> None:
    db.query(Posteo).filter(
        Posteo.user_id==user.id,
        Posteo.id==posteo_id
    ).delete()
    db.commit()