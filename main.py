from sqlalchemy import desc
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os
from datetime import datetime

# --- PostgreSQL Verbindung (über Umgebungsvariable) ---
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

# --- FastAPI Setup ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=engine)

# --- Routen ---
@app.get("/")
def root():
    return FileResponse(os.path.join("static", "rangliste.html"))

@app.get("/registrieren")
def registrieren():
    return FileResponse(os.path.join("static", "kunde_registrieren.html"))

@app.get("/registrierung_erfolgreich")
def registrierung_erfolgreich():
    return FileResponse(os.path.join("static", "registrierung_erfolgreich.html"))

@app.get("/messung")
def messung():
    return FileResponse(os.path.join("static", "messung_eintragen.html"))

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
    return RedirectResponse(url="/registrierung_erfolgreich", status_code=302)

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

@app.get("/kunden_json")
def kunden_json():
    db = SessionLocal()
    kunden = db.query(Kunde).all()
    db.close()
    return [{"id": k.id, "vorname": k.vorname, "name": k.name, "plz_ort": k.plz_ort} for k in kunden]

@app.get("/rangliste_daten")
def rangliste_daten():
    db = SessionLocal()
    messungen = db.query(Messung).join(Kunde).order_by(desc(Messung.max_schlagkraft)).all()
    db.close()

    def gewichtsklasse(geschlecht, gewicht):
        grenzen_mann = [45, 48, 54, 57, 60, 63.5, 67, 71, 75, 81, 86, 91]
        grenzen_frau = [45, 48, 51, 54, 57, 60, 63.5, 67, 71, 75, 81]
        grenzen = grenzen_mann if geschlecht.lower() == "mann" else grenzen_frau
        for g in grenzen:
            if gewicht <= g:
                return f"-{g}kg"
        return "+91kg" if geschlecht.lower() == "mann" else "+81kg"

    rangliste = {}

    for messung in messungen:
        kunde = messung.kunde
        klasse = gewichtsklasse(kunde.geschlecht, kunde.gewicht)
        geschlecht = kunde.geschlecht.capitalize()
        key = f"{geschlecht} - {klasse}"

        if key not in rangliste:
            rangliste[key] = []
        rangliste[key].append({
            "pseudonym": kunde.pseudonym,
            "max_schlagkraft": messung.max_schlagkraft
        })

    return rangliste
