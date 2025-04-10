
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, desc, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from io import StringIO
import csv
import os
from datetime import datetime

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
