from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os
from datetime import datetime

# --- PostgreSQL Datenbank-Verbindung ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- Datenbank-Modelle ---
class Kunde(Base):
    __tablename__ = "kunden"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    vorname = Column(String)
    pseudonym = Column(String)
    alter = Column(Integer)
    geschlecht = Column(String)
    gewicht = Column(Float)
    schlaghand = Column(String)
    schlagart = Column(String)
    email = Column(String)
    plz_ort = Column(String)
    messungen = relationship("Messung", back_populates="kunde")

class Messung(Base):
    __tablename__ = "messungen"
    id = Column(Integer, primary_key=True, index=True)
    kunde_id = Column(Integer, ForeignKey("kunden.id"))
    max_schlagkraft = Column(Float)
    avg_schlagkraft = Column(Float)
    datum = Column(String, default=str(datetime.now()))
    kunde = relationship("Kunde", back_populates="messungen")

# --- Datenbank-Tabellen anlegen ---
Base.metadata.create_all(bind=engine)

# --- FastAPI App ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Routen für Seiten ---
@app.get("/")
def root():
    return FileResponse(os.path.join("static", "rangliste.html"))

@app.get("/registrieren")
def registrieren():
    return FileResponse(os.path.join("static", "kunde_registrieren.html"))

@app.get("/messung")
def messung():
    return FileResponse(os.path.join("static", "messung_eintragen.html"))

# --- POST: Kunde registrieren ---
@app.post("/kunde")
async def registriere_kunde(
    name: str = Form(...),
    vorname: str = Form(...),
    pseudonym: str = Form(...),
    alter: int = Form(...),
    geschlecht: str = Form(...),
    gewicht: float = Form(...),
    schlaghand: str = Form(...),
    schlagart: str = Form(...),
    email: str = Form(...),
    plz_ort: str = Form(...)
):
    db = SessionLocal()
    neuer_kunde = Kunde(
        name=name,
        vorname=vorname,
        pseudonym=pseudonym,
        alter=alter,
        geschlecht=geschlecht,
        gewicht=gewicht,
        schlaghand=schlaghand,
        schlagart=schlagart,
        email=email,
        plz_ort=plz_ort
    )
    db.add(neuer_kunde)
    db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=302)

# --- POST: Messung speichern ---
@app.post("/messung")
async def messung_eintragen(
    kunde_id: int = Form(...),
    max_schlagkraft: float = Form(...),
    avg_schlagkraft: float = Form(...)
):
    db = SessionLocal()
    messung = Messung(
        kunde_id=kunde_id,
        max_schlagkraft=max_schlagkraft,
        avg_schlagkraft=avg_schlagkraft,
    )
    db.add(messung)
    db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=302)
from fastapi.responses import HTMLResponse

@app.get("/kunden", response_class=HTMLResponse)
def kundenliste():
    db = SessionLocal()
    kunden = db.query(Kunde).all()
    db.close()

    html = "<h2>🆔 Kundenübersicht</h2><table border='1' cellpadding='8' style='font-family:sans-serif;'>"
    html += "<tr><th>ID</th><th>Pseudonym</th><th>Vorname</th><th>Name</th></tr>"
    for k in kunden:
        html += f"<tr><td>{k.id}</td><td>{k.pseudonym}</td><td>{k.vorname}</td><td>{k.name}</td></tr>"
    html += "</table>"

    return html
