import os
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


from db import (
    Base,
    SessionLocal,
    add_click,
    add_url,
    delete_url,
    engine,
    get_all,
    get_url,
)
from models import DataModel

Base.metadata.create_all(bind=engine)

PORT = os.getenv("PORT", 8000)
HOST = os.getenv("HOST", "0.0.0.0")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_all_short_urls(db: Session = Depends(get_db)):
    return get_all(db)


@app.post("/")
def create_short_url(data: DataModel, db: Session = Depends(get_db)):
    if get_url(db, data.slug):
        return {"msg": "Slug já existe, seu corno"}
    link = add_url(db, data.link, data.slug)
    return {"msg": "Link criado", "link": link.slug}


@app.get("/{slug}")
def redirect_to_link(slug: str, db: Session = Depends(get_db)):
    url = get_url(db, slug)
    if url:
        add_click(db, slug)
        return RedirectResponse(url.link)
    return {"msg": "Não encontrado"}


@app.delete("/")
def delete_link(
    slug: Optional[str] = None, id: Optional[int] = None, db: Session = Depends(get_db)
):
    if get_url(db, slug, id):
        if delete_url(db, slug, id):
            return {"msg": "Slug apagado!"}
    return {"msg": "Slug não existe, amigão"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=PORT)
