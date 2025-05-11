# 08.05.2025

## Done
- Das komplette Projekt neu strukturiert.
- Eine virtuelle Umgebung (venv) im Backend-Ordner angelegt, um eine isolierte Python-Umgebung bereitzustellen.   - Dies ermöglicht die Verwaltung von Bibliotheken innerhalb dieses Containers, der unabhängig vom Host-System läuft.

    - Zudem erlaubt die Verwendung der requirements.txt-Datei die Installation von Abhängigkeiten ausschließlich in der erstellten Umgebung.

- Das Pushen in das Repo war nicht mehr möglich. Git Client meldete immmer ein Fehler. Es stellte sich herraus, das die default limitierte `postBuffersize` zu gering war (wahrscheinlisch nach dem hinzufügen der venv). _Buffer-Size_ von Git erhöht:

````bash
git config --global http.postBuffer 157286400
````

## Worked
- 3 Stunden.