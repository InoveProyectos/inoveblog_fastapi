import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware

import settings
from database import Base, engine, get_db
from sqlalchemy.orm import Session
from crud import get_user, create_user, get_posteos, create_posteo, get_posteo, update_posteo, delete_posteos
from schemas import PosteoSchema
from auth.AuthHandler import auth_handler

# Create database
Base.metadata.create_all(bind=engine)

# Create server
app = FastAPI(
    title="InoveBlog",
    version="1.0.0",
    )

# CORS config
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# ------------ Views ----------------- #

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_item(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})

# ---------------- API ------------------------

@app.post("/api/v1.0/login", tags=["login"])
def login(usuario: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    if password != settings.LOGIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Password incorrecta")
    
    if get_user(db, usuario) is None:
        create_user(db, usuario)

    return {"usuario": usuario}


@app.post("/api/v1.0/posteos/{usuario}", tags=["posteos"])
def crear_posteo(usuario: str, posteo: PosteoSchema, db: Session = Depends(get_db)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    posteo = create_posteo(db, user, posteo.titulo, posteo.texto).serialize()
    posteo["usuario"] = usuario
    return posteo


@app.get("/api/v1.0/posteos/{usuario}", tags=["posteos"])
def leer_posteos(usuario: str, db: Session = Depends(get_db)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    posteos = []
    for posteo in get_posteos(db, user):
        data = posteo.serialize()
        data["usuario"] = usuario
        posteos.append(data)

    return posteos


@app.get("/api/v1.0/posteos/{usuario}/detail/{posteo_id}", tags=["posteos_extendido"])
def leer_posteo(usuario: str, posteo_id: int, db: Session = Depends(get_db)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    posteo = get_posteo(db, user, posteo_id)
    if posteo is None:
        raise HTTPException(status_code=404, detail="Posteo no encontrado")

    data = posteo.serialize()
    data["usuario"] = usuario
    return data


@app.put("/api/v1.0/posteos/{usuario}/update/{posteo_id}", tags=["posteos_extendido"])
def actualizar_posteo(usuario: str, posteo_id: int, posteo: PosteoSchema, db: Session = Depends(get_db)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    posteo = update_posteo(db, user, posteo_id, posteo.titulo, posteo.texto)
    if posteo is None:
        raise HTTPException(status_code=404, detail="Posteo no encontrado")
    
    data = posteo.serialize()
    data["usuario"] = usuario
    return data

@app.delete("/api/v1.0/posteos/{usuario}/delete/{posteo_id}", tags=["posteos_extendido"])
def eliminar_posteo(usuario: str, posteo_id: int, db: Session = Depends(get_db)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    delete_posteos(db, user, posteo_id)

    return {"posteo_eliminado": posteo_id}


# ---------------- AUTH API ------------------------

@app.post("/api/v1.0/auth/login", tags=["auth"])
def login(usuario: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    if password != settings.LOGIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Password incorrecta")
    
    user = get_user(db, usuario) 
    if user is None:
        user = create_user(db, usuario)

    token = auth_handler.encode_token(user.id)
    return {"usuario": usuario, "token": token, "token_type": "bearer"}


@app.post("/api/v1.0/auth/posteos/{usuario}", tags=["auth"])
def crear_posteo(usuario: str, posteo: PosteoSchema, db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    if user.id != user_id:
        raise HTTPException(status_code=401, detail="El token no pertenece al usuario")
    
    posteo = create_posteo(db, user, posteo.titulo, posteo.texto).serialize()
    posteo["usuario"] = usuario
    return posteo


@app.get("/api/v1.0/auth/posteos/{usuario}", tags=["auth"])
def leer_posteos(usuario: str, db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    if user.id != user_id:
        raise HTTPException(status_code=401, detail="El token no pertenece al usuario")
    
    posteos = []
    for posteo in get_posteos(db, user):
        data = posteo.serialize()
        data["usuario"] = usuario
        posteos.append(data)

    return posteos


@app.get("/api/v1.0/auth/posteos/{usuario}/detail/{posteo_id}", tags=["auth"])
def leer_posteo(usuario: str, posteo_id: int, db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    if user.id != user_id:
        raise HTTPException(status_code=401, detail="El token no pertenece al usuario")

    posteo = get_posteo(db, user, posteo_id)
    if posteo is None:
        raise HTTPException(status_code=404, detail="Posteo no encontrado")

    data = posteo.serialize()
    data["usuario"] = usuario
    return data


@app.put("/api/v1.0/auth/posteos/{usuario}/update/{posteo_id}", tags=["auth"])
def actualizar_posteo(usuario: str, posteo_id: int, posteo: PosteoSchema, db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    if user.id != user_id:
        raise HTTPException(status_code=401, detail="El token no pertenece al usuario")
    
    posteo = update_posteo(db, user, posteo_id, posteo.titulo, posteo.texto)
    if posteo is None:
        raise HTTPException(status_code=404, detail="Posteo no encontrado")
    
    data = posteo.serialize()
    data["usuario"] = usuario
    return data

@app.delete("/api/v1.0/auth/posteos/{usuario}/delete/{posteo_id}", tags=["auth"])
def eliminar_posteo(usuario: str, posteo_id: int, db: Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    user = get_user(db, usuario)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    if user.id != user_id:
        raise HTTPException(status_code=401, detail="El token no pertenece al usuario")
    
    delete_posteos(db, user, posteo_id)

    return {"posteo_eliminado": posteo_id}


if __name__ == "__main__":
    print('¡Inove@Server start!')
    # main --> es el nombre del archivo
    # app --> es el nombre de la variable creada como FastAPI()
    # uvicorn es el servidor web
    #uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)