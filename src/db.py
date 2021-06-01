import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm.session import Session


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URI")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, index=True)
    link = Column(String)
    clicks = Column(Integer)


# CREATE
def add_url(db: Session, url, slug):
    db_url = Link(link=url, slug=slug, clicks=0)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


# READ
def get_url(db: Session, slug: Optional[str] = None, id: Optional[int] = None):
    if slug:
        return db.query(Link).filter(Link.slug == slug).first()
    return db.query(Link).filter(Link.id == id).first()


# READ ALL
def get_all(db: Session):
    return db.query(Link).all()


# UPDATE
def add_click(db: Session, slug: str):
    db.query(Link).filter(Link.slug == slug).first().clicks = +1
    db.commit()


# DELETE
def delete_url(db: Session, slug: Optional[str] = None, id: Optional[int] = None):
    if slug:
        res = db.query(Link).filter(Link.slug == slug).delete()
    if id:
        res = db.query(Link).filter(Link.id == id).delete()
    db.commit()
    return res
