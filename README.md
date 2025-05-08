# Rangliste

## Einleitung

## Dokumentation
Dieses Kapitel soll einen Überblick darüber geben, mit welchen APIs und Technologien das Projekt Rangliste umgesetzt worden ist.

### Python

#### FastAPI
__Links:__

- [Build a REST API](https://www.youtube.com/watch?v=iWS9ogMPOI0)

__Doc:__

- JS ruft das Backend FastAPI auf und FastAPI gibt eine Response(Result) zurück(hier nach möglichkeit noch ein Bild zur ilustration ergänzen.)

- venv enviroment anlegen im backendfolder für eine isolierte Python Umgebung, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html).

````bash
cd backend
````
anschliessend die virtuelle Umgebung einrichten:

````bash
python3 -m venv venv
````
Sobald die virtuelle Umgebung eingrichtet wurde, muss diese noch aktiviert werden:

````bash
# for mac
source venv/bin/activate
````
Danach ist die virtuelle Umgebung aktiviert. Im terminal ist am linken rand die (venv) zu sehen, was eine erfolgreiche Aktivierung bedeutet:

````bash
# for mac
(venv) bitwielder >
````







__SQLAlchemy ORM__
- Links:
    - [SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html)

Beschreibung:
- SQLAlchemy wird als ORM Mapper verwendet.
