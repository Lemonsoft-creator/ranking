import random
import requests
from faker import Faker

fake = Faker("de_DE")

URL = "http://localhost:8000/kunde"  

geschlechter = ["Maennlich", "Weiblich"]
schlaghaende = ["Rechts", "Links"]
schlagarten = ["Punch", "Hook", "Kick", "Elbow", "Knee"]
gewichte = [60, 65, 70, 75, 80, 85, 90, 100] 
gewicht_verteilung = [10, 15, 20, 20, 15, 10, 5, 5]

def gewicht_ziehen():
    return random.choices(gewichte, weights=gewicht_verteilung, k=1)[0]

def erstelle_kunde():
    vorname = fake.first_name()
    nachname = fake.last_name()
    geschlecht = random.choice(geschlechter)
    alter = random.randint(18, 60)
    gewicht = gewicht_ziehen()
    schlaghand = random.choice(schlaghaende)
    schlagart = random.choice(schlagarten)
    email = fake.email()
    plz_ort = f"{fake.postcode()} {fake.city()}"

    # Optional: Pseudonym basierend auf Name oder zufällig
    pseudonym = f"{vorname[:2]}_{nachname[:3]}_{random.randint(100, 999)}"

    return {
        "name": nachname,
        "vorname": vorname,
        "pseudonym": pseudonym,
        "alter": alter,
        "geschlecht": geschlecht,
        "gewicht": gewicht,
        "schlaghand": schlaghand,
        "schlagart": schlagart,
        "email": email,
        "plz_ort": plz_ort
    }

def registriere_kunden(n=100):
    erfolge = 0
    fehler = 0
    for _ in range(n):
        daten = erstelle_kunde()
        try:
            r = requests.post(URL, data=daten)
            if r.status_code == 200 or r.status_code == 303:
                erfolge += 1
            else:
                print(f"Fehler: {r.status_code} – {r.text}")
                fehler += 1
        except Exception as e:
            print(f"Exception: {e}")
            fehler += 1
    print(f"\nRegistrierung abgeschlossen: {erfolge} erfolgreich, {fehler} fehlgeschlagen.")

if __name__ == "__main__":
    registriere_kunden(100)
