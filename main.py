 from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, desc, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
import os
from datetime import datetime
from datetime import datetime
from fastapi.responses import StreamingResponse
import csv
from io import StringIO

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

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
    messungen = relationship("Messung", back_populates="kunde", cascade="all, delete")

class Messung(Base):
    __tablename__ = "messungen"
    id = Column(Integer, primary_key=True, index=True)
    kunde_id = Column(Integer, ForeignKey("kunden.id"))
    max_schlagkraft = Column(Float)
    avg_schlagkraft = Column(Float)
    datum = Column(String, default=str(datetime.now()))
    kunde = relationship("Kunde", back_populates="messungen")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        name=name, vorname=vorname, pseudonym=pseudonym, alter=alter,
        geschlecht=geschlecht, gewicht=gewicht, schlaghand=schlaghand,
        schlagart=schlagart, email=email, plz_ort=plz_ort
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
        avg_schlagkraft=avg_schlagkraft
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

    # Gewichtsklassen Definition
    gewichtsklassen = {
        "Maennlich": [45, 48, 54, 57, 60, 63.5, 67, 71, 75, 81, 86, 91],
        "Weiblich": [45, 48, 51, 54, 57, 60, 63.5, 67, 71, 75, 81]
    }

    # Hilfsfunktion zur Klassenzuweisung
    def gewichtsklasse(geschlecht, gewicht):
        grenzen = gewichtsklassen.get(geschlecht, [])
        for grenze in grenzen:
            if gewicht <= grenze:
                return f"-{grenze}kg"
        return f"+{grenzen[-1]}kg" if grenzen else "Unbekannt"

    # Rangliste vorbereiten
    rangliste = {}

    # Messungen mit Kunden laden
    messungen = db.query(Messung).options(joinedload(Messung.kunde)).all()

    for messung in messungen:
        kunde = messung.kunde
        if not kunde:
            continue

        geschlecht = kunde.geschlecht.capitalize()
        klasse = gewichtsklasse(geschlecht, kunde.gewicht)
        key = f"{geschlecht} - {klasse}"

        if key not in rangliste:
            rangliste[key] = []

        rangliste[key].append({
            "pseudonym": kunde.pseudonym,
            "max_schlagkraft": messung.max_schlagkraft
        })

    db.close()

    # Alle Gruppen sortieren (nach Schlagkraft)
    for gruppe in rangliste:
        rangliste[gruppe].sort(key=lambda x: x["max_schlagkraft"], reverse=True)

    return rangliste

@app.get("/admin")
def admin():
    return FileResponse(os.path.join("static", "admin.html"))

@app.get("/admin_daten")
def admin_daten():
    db = SessionLocal()
    anzahl = db.query(Kunde).count()
    maenner = db.query(Kunde).filter(Kunde.geschlecht.ilike("mann")).count()
    frauen = db.query(Kunde).filter(Kunde.geschlecht.ilike("frau")).count()
    max_mann = db.query(func.max(Messung.max_schlagkraft)).join(Kunde).filter(Kunde.geschlecht.ilike("mann")).scalar() or 0
    max_frau = db.query(func.max(Messung.max_schlagkraft)).join(Kunde).filter(Kunde.geschlecht.ilike("frau")).scalar() or 0
    kunden = db.query(Kunde).all()
    db.close()
    return {
        "anzahl": anzahl,
        "maenner": maenner,
        "frauen": frauen,
        "max_mann": round(max_mann, 1),
        "max_frau": round(max_frau, 1),
        "kunden": [{"id": k.id, "pseudonym": k.pseudonym, "vorname": k.vorname, "name": k.name, "geschlecht": k.geschlecht} for k in kunden]
    }

@app.get("/export_csv")
def export_csv():
    db = SessionLocal()
    kunden = db.query(Kunde).all()
    db.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Name", "Vorname", "Pseudonym", "Alter", "Geschlecht",
        "Gewicht", "Schlaghand", "Schlagart", "Email", "PLZ/Ort"
    ])

    for k in kunden:
        writer.writerow([
            k.id, k.name, k.vorname, k.pseudonym, k.alter, k.geschlecht,
            k.gewicht, k.schlaghand, k.schlagart, k.email, k.plz_ort
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=kunden_export.csv"
    })

@app.get("/admin_loeschen")
def admin_loeschen(id: int):
    db = SessionLocal()
    kunde = db.query(Kunde).filter(Kunde.id == id).first()
    if kunde:
        db.delete(kunde)
        db.commit()
    db.close()
    return RedirectResponse(url="/admin", status_code=302)

