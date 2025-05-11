# Rangliste

## Beschreibung der App
Über die Registrierung werden neue User der Datenbank hinzugefügt. Die neuen User werden auf der Datenbank gespeichert und können via das Dropdown auf der Seite [Messung Eintragen](/frontend/templates/messung_eintragen.html) abgerufen werden. Sobald der User aus dem Dropdown ausgewählt wurde, können die Messwerte von dem Boxkissen, eingetragen und gespeichert werden. Auf der Seite [Rangliste](/frontend/templates/rangliste.html) werden die User, sortiert nach Geschlecht und Platzierung, angezeigt.

## Technische Dokumentation
Dieses Kapitel soll einen Überblick darüber geben, mit welchen APIs und Technologien das Projekt Rangliste umgesetzt worden ist.

### Python

#### FastAPI
__Links:__

- [Build a REST API](https://www.youtube.com/watch?v=iWS9ogMPOI0)

__Doc:__

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




__SQLAlchemy ORM__
- Links:
    - [SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html)

Beschreibung:
- SQLAlchemy wird als ORM Mapper verwendet.
