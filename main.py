from fastapi import FastAPI, Form, Request
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
import csv
from io import StringIO
from sqlalchemy import DateTime, Column, Integer, String, Float, ForeignKey, create_engine, desc, func,select
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import load_dotenv
# Lädt .env Datei
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL is not set')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

"""
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


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
    max_joule = Column(Float)
    avg_joule = Column(Float)
    max_kgf = Column(Float)
    avg_kgf = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    #datum = Column(DateTime, default=datetime.now)
    kunde = relationship("Kunde", back_populates="messungen")

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Berechnet die Schlagkraft in kgf (Kilogramm-Kraft) aus der Energie (Joule).
def joule_to_kgf(joule: float, weg_in_m: float = 0.3) -> float:
    kraft_n = (2 * joule) / weg_in_m
    kgf = kraft_n / 9.81
    return round(kgf, 1)

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
    schlag_1: float = Form(...),
    schlag_2: float = Form(...),
    schlag_3: float = Form(...)
):
    avg_joule = round((schlag_1 + schlag_2 + schlag_3) / 3, 1)
    max_joule = round(max(schlag_1, schlag_2, schlag_3), 1)

    avg_kgf = joule_to_kgf(avg_joule)
    max_kgf = joule_to_kgf(max_joule)

    db: Session = SessionLocal()
    messung = Messung(
        kunde_id=kunde_id,
        avg_joule=avg_joule,
        max_joule=max_joule,
        avg_kgf=avg_kgf,
        max_kgf=max_kgf
    )
    db.add(messung)
    db.commit()
    db.close()
    return RedirectResponse("/messung", status_code=303)

@app.get("/kunden_json")
def kunden_json():
    db = SessionLocal()
    kunden = db.query(Kunde).all()
    db.close()
    return [{"id": k.id, "vorname": k.vorname, "name": k.name, "plz_ort": k.plz_ort} for k in kunden]

@app.get("/vergleich_daten")
def vergleich_daten():
    db = SessionLocal()
    messungen = db.query(Messung).options(joinedload(Messung.kunde)).all()
    db.close()

    # Referenzwerte
    tyson_max_kgf = 453
    tyson_gewicht = 113

    halmich_max_kgf = 240
    halmich_gewicht = 50

    daten = []

    for messung in messungen:
        kunde = messung.kunde
        if not kunde or not messung.max_kgf or not kunde.gewicht:
            continue

        geschlecht = kunde.geschlecht.strip().lower()

        if geschlecht == "maennlich":
            ref_max = tyson_max_kgf
            ref_gewicht = tyson_gewicht
            ref_name = "Mike Tyson"
        else:
            ref_max = halmich_max_kgf
            ref_gewicht = halmich_gewicht
            ref_name = "Regina Halmich"

        # Gewichtskorrigierte Schlagkraft
        gewicht_koeff = ref_gewicht / kunde.gewicht
        korrigierte_schlagkraft = messung.max_kgf * gewicht_koeff

        prozent = round((korrigierte_schlagkraft / ref_max) * 100, 1)

        daten.append({
            "pseudonym": kunde.pseudonym,
            "prozent_von_referenz": prozent,
            "referenz": ref_name,
            "gewicht": kunde.gewicht,
            "max_kgf": messung.max_kgf,
            "gewicht_koeffizient": round(gewicht_koeff, 4),
            "korrigierte_schlagkraft": round(korrigierte_schlagkraft, 2)
        })

    daten.sort(key=lambda x: x["prozent_von_referenz"], reverse=True)
    return daten

@app.get("/rangliste_daten")
def rangliste_daten():
    db = SessionLocal()

    gewichtsklassen = {
        "Maennlich": [91, 86, 81, 75, 71, 67, 63.5, 60, 57, 54, 48, 45],
        "Weiblich": [81, 75, 71, 67, 63.5, 60, 57, 54, 51, 48, 45]
    }

    def gewichtsklasse(geschlecht, gewicht):
        grenzen = gewichtsklassen.get(geschlecht, [])
        for g in sorted(grenzen):
            if gewicht <= g:
                return f"{g}kg"
        return f"+{grenzen[0]}kg"

    # Subquery: Nur letzte Messung je Kunde
    subquery = (
        db.query(
            Messung.kunde_id,
            func.max(Messung.timestamp).label("max_timestamp")
        )
        .group_by(Messung.kunde_id)
        .subquery()
    )

    # Nur die letzten Messungen pro Kunde abrufen
    messungen = (
        db.query(Messung)
        .join(
            subquery,
            (Messung.kunde_id == subquery.c.kunde_id) &
            (Messung.timestamp == subquery.c.max_timestamp)
        )
        .options(joinedload(Messung.kunde))
        .all()
    )

    rang_ungeordnet = {}

    for messung in messungen:
        kunde = messung.kunde
        if not kunde:
            continue
        geschlecht = kunde.geschlecht.strip().capitalize()
        klasse = gewichtsklasse(geschlecht, kunde.gewicht)
        key = f"{geschlecht} - {klasse}"
        if key not in rang_ungeordnet:
            rang_ungeordnet[key] = []

        rang_ungeordnet[key].append({
            "pseudonym": kunde.pseudonym,
            "max_kgf": messung.max_kgf
        })

    db.close()

    for teilnehmer in rang_ungeordnet.values():
        teilnehmer.sort(key=lambda x: x["max_kgf"], reverse=True)

    def sort_key(k):
        try:
            geschlecht, klasse = k.split(" - ")
            gkl = klasse.replace("kg", "")
            wert = float(gkl.replace("+", "").replace("-", ""))
        except Exception:
            return (9, 9999)

        return (
            0 if geschlecht == "Maennlich" else 1,
            -wert if "+" in gkl else wert
        )

    return dict(sorted(rang_ungeordnet.items(), key=sort_key))

@app.get("/admin")
def admin():
    return FileResponse(os.path.join("static", "admin.html"))

@app.get("/admin_daten")
def admin_daten():
    db = SessionLocal()
    anzahl = db.query(Kunde).count()
    maenner = db.query(Kunde).filter(Kunde.geschlecht.ilike("maennlich")).count()
    frauen = db.query(Kunde).filter(Kunde.geschlecht.ilike("weiblich")).count()
    max_mann = db.query(func.max(Messung.max_kgf)).join(Kunde).filter(Kunde.geschlecht.ilike("maennlich")).scalar() or 0
    max_frau = db.query(func.max(Messung.max_kgf)).join(Kunde).filter(Kunde.geschlecht.ilike("weiblich")).scalar() or 0
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

@app.get("/export_messung")
def export_messung():
    db = SessionLocal()
    kunden = db.query(Kunde).all()
    messungen = db.query(Messung).all()
    db.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Kunden-ID", "Pseudonym", "Vorname", "Nachname", "Geschlecht",
        "Max. Schlagkraft (kg)", "Ø Schlagkraft (kg)", "Datum"
    ])

    for kunde in kunden:
        for messung in messungen:
            if messung.kunde_id == kunde.id:
                writer.writerow([
                    kunde.id, kunde.pseudonym, kunde.vorname, kunde.name, kunde.geschlecht,
                    messung.max_kgf, messung.avg_kgf, messung.timestamp
                ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=messung_export.csv"
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
