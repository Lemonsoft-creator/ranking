from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join("static", "rangliste.html"))

@app.get("/registrieren")
def registrieren():
    return FileResponse(os.path.join("static", "kunde_registrieren.html"))

@app.get("/messung")
def messung():
    return FileResponse(os.path.join("static", "messung_eintragen.html"))

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, desc
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os
from datetime import datetime
