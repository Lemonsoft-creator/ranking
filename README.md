# Rangliste

## Beschreibung der App
Über die Registrierung werden neue User der Datenbank hinzugefügt. Die neuen User werden auf der Datenbank gespeichert und können via das Dropdown auf der Seite [Messung Eintragen](/frontend/templates/messung_eintragen.html) abgerufen werden. Sobald der User aus dem Dropdown ausgewählt wurde, können die Messwerte von dem Boxkissen, eingetragen und gespeichert werden. Auf der Seite [Rangliste](/frontend/templates/rangliste.html) werden die User, sortiert nach Geschlecht und Platzierung, angezeigt.

## Technische Dokumentation
Dieses Kapitel soll einen Überblick darüber geben, mit welchen APIs und Technologien das Projekt Rangliste umgesetzt worden ist.


### FastAPI
__Links:__

- [Build a REST API](https://www.youtube.com/watch?v=iWS9ogMPOI0)

Damit FastAPI weiss wo es die HTML-Files findet, wird dem FasAPI-Objekt der Pfad übergeben:

````Python
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
````
Sobald, zum Beispiel auf der lokalen Umgebung, der Endpoint:

````Python
@app.get("/admin")
def admin():
    return FileResponse(os.path.join("static", "admin.html"))
````
mit:

````Python
http://127.0.0.1:8000/admin
````
aufgerufen wird, weiss FastAPI wo es die HTML-Seiten findet, unter `/static/...`


- JS ruft das Backend FastAPI auf und FastAPI gibt eine Response(Result) zurück(hier nach Möglichkeit noch ein Bild zur illustration ergänzen.)


- venv environment anlegen im Backend-Folder für eine isolierte Python Umgebung, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html).

````bash
cd backend
````
anschliessend die virtuelle Umgebung einrichten:

````bash
python3 -m venv venv
````
Sobald die virtuelle Umgebung eingerichtet ist, muss diese noch aktiviert werden:

````bash
# for mac
source venv/bin/activate
````
Danach ist die virtuelle Umgebung aktiviert. Im Terminal ist am linken Rand die (venv) zu sehen, was eine erfolgreiche Aktivierung bedeutet:

````bash
# local terminal prompt
(venv) bitwielder >
````
Sobald die virtuelle Umgebung aktiv ist, kann mit Hilfe des `requirements.txt` und `pip` alle APIs installiert werden:

````bash
# local terminal prompt
pip3 install -r requirements.txt
````

Das `venv/`Verzeichnis ist ein lokales Set-Up. Dieses Set-Up sollte nicht mit ins git eingecheckt werden. Das Verzeichnis im `.gitignore` hinterlegen. Im `equirements.txt` werden alle Verwendeten APIs dokumentiert. Mit:

````bash
pip freeze > requirements.txt
````
wird das `requirements.txt` geupdatete mit der dazugehörigen Version der verwendeten APIs.


__SQLAlchemy ORM__
- Links:
    - [SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html)

Beschreibung:
- SQLAlchemy wird als ORM Mapper verwendet.

Hier zu müssen alle Entity Klassen von `Base`erben. In SQLAlchemy dient `declarative_base()` dazu, eine Basisklasse zu erzeugen, von der alle ORM-Modelle erben sollen. Diese Basisklasse enthält Metadaten über die Modelle, z. B. deren Tabellennamen, Spalten und Beziehungen.

````Python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
````
Ab dann erstellt man eigene Modelle so:

````Python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
````
Alle Modellklassen, die von derselben Base-Instanz erben, werden zentral registriert. Diese Registrierung ist notwendig, damit SQLAlchemy weiß, welche Tabellen es anlegen oder verwalten soll.

### JAVA Script
#### fetch API
Mit der `fetch` API können HTTP Requests über das Netzwerk verschickt und eine Response empfangen werden. Für den Request in [Rangliste](/frontend/scripte/rangliste.js):
````JavaScript
const data = await fetchRankingData("/rangliste_daten");
````
wird eine HTTP-GET-Anfrage an den Server-Endpunkt `/rangliste_daten` gesendet. Der Server sollte als Antwort JSON-Daten zurückgeben. Dabei wird ein relativer URL verwendet, die sich auf den aktuellen Speicherort der HTML-Datei bezieht.Das heisst relativ zur Basis-URL der aktuellen Seite. Beispiel:

> Wenn sich die Seite beispielsweise unter https://example.com/rangliste.html befindet, wird die Anfrage an https://example.com/rangliste_daten gesendet.

