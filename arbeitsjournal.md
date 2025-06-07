# 23.05.2025

## Done
- Ranglisete `HTML` JS neu ausprogrammieren da pro Gewichtsklasse nur ein Eintrag angezeigt wurde. Jedes Mal wenn ich in der selben Gewichtsklasse einen neuen Kunden hinzugefügt habe, die dazugehörige Messung eingetragen habe, wurde immer nur ein Kunde angzeigt

Von:

````JS
 ${teilnehmer.map((t, i) => {
    const platz = i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : i + 1;
    const prozent = Math.min(100, (t.max_schlagkraft / 450) * 100).toFixed(1);
    const barWidth = Math.min(100, (t.max_schlagkraft / 450) * 100);
    const barId = `bar-${geschlecht}-${klasse}-${i}`.replace(/\s+/g, "-");

// und

 teilnehmer.forEach((t, i) => {
    const barId = `bar-${geschlecht}-${klasse}-${i}`.replace(/\s+/g, "-");
    const barWidth = Math.min(100, (t.max_schlagkraft / 450) * 100);
    const el = document.getElementById(barId);


````

Zu:


````JS
${teilnehmer.map((t, i) => {
    const platz = i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : i + 1;
    const prozent = Math.min(100, (t.max_kgf / 450) * 100).toFixed(1);
    const barWidth = Math.min(100, (t.max_kgf / 450) * 100);
    const sanitize = str => str.replace(/[^a-zA-Z0-9]/g, "-");
    const barId = `bar-${sanitize(geschlecht)}-${sanitize(klasse)}-${i}`;

// Und

teilnehmer.forEach((t, i) => {
    const sanitize = str => str.replace(/[^a-zA-Z0-9]/g, "-");
    const barId = `bar-${sanitize(geschlecht)}-${sanitize(klasse)}-${i}`;

````

---

- In [messung_eintragen.html](/static/messung_eintragen.html) das DIV für die Messung angepasst. So können drei Schläge des Sportlers 
eingetrsgen werden:

````html
<div class="container">
    <h1>💥 Messung eintragen</h1>
    <form method="post" action="/messung">
      <label for="kunde_id">Kunden auswählen</label>
      <select name="kunde_id" id="kunde_id" required>
        <option value="">Kunde auswählen...</option>
      </select>

      <label>Schlagenergie (Joule)</label>
      <input type="number" name="schlag_1" step="0.1" placeholder="1. Schlag (z. B. 300.0)" required>
      <input type="number" name="schlag_2" step="0.1" placeholder="2. Schlag (z. B. 280.0)" required>
      <input type="number" name="schlag_3" step="0.1" placeholder="3. Schlag (z. B. 290.0)" required>

      <p style="font-size: 0.9rem; color: #555; margin-top: 1rem;">
        Hinweis: Die Eingabe erfolgt in Joule. Der Durchschnitt und die Schlagkraft in Kilogramm-Kraft (kgf) werden automatisch berechnet und gespeichert.
      </p>

      <button type="submit">💾 Messung speichern</button>
    </form>
    
  </div>
````
Im Endpoint `@app.post("/messung")` werden dann einmal die mittlere und maximale(die wird noch nicht angezeigt) Schlagkraft ermittelt:

````python
 avg_joule = round((schlag_1 + schlag_2 + schlag_3) / 3, 1)
 max_joule = round(max(schlag_1, schlag_2, schlag_3), 1)
````




- Zusätzlich in messung.html ein footer eingebaut. (Optional)


## Worked
- 2 Stunden

# 25.05.2025

## Done

- Neues Script erstellt um Fake Kunden zu erstellen um lokal die App testen zu können.
- Admin Button hinzugefügt.
- Footer in Rangliste angepasst.

## Worked
- 3 Stund

# 07.06.2025

## ToDo  ✅

- Deployment-Fehler beheben.
- Wenn eine Person mehrmals Schlägt soll immer nur das letzte Ergebnis in der Rangliste aufgeführt werden. Der gleiche Kunde soll bei $n$ Versuchen nicht $n$ Mal
in der Rangliste aufgelistet werden.
-  Als Frau möchte ich mich nicht mir Mike Tyson messen müssen sondern mit einer Bekannten Boxerin wir z.B Regina Halmich, um ein für eine Frau vergleichbares Ergebnis zu erhalten.

- Als Leichtgewicht, sowohl Frauen als auch Männer, möchte ich mich nicht mit einem Schwergewicht messen müssen, um einen fairen Vergleich zu haben. Daher sollte ein Gewichtkoeffizient eingebaut werden, um die Vergleichbarkeit zu gewährleisten.Gewichtkoeffizient einbauen:

  - Tyson Gewicht: $113Kg$
  - Person Gewicht: $70Kg$
  - Koeffizient: $1,6143$
  - Schlagkraft: $200Kg$

Formel: $113/70=1,6143x200kg$

Schlagkraft: $200*1.6143=322.86$

- Als Benutzer möchte ich, dass die Verlinkung zur Admin-Seite beim Button oben rechts bei der Registrierung und der Rangliste entfernt wird, damit die Benutzeroberfläche klarer und benutzerfreundlicher ist.

- Responsivität bei der Mobileansicht prüfen (Balken)

- Als User möchte ich dass sich die Rangliste alle 10 Sekunden aktualisiert damit ich immer den aktuellsten Stand sehen kann.

- Als Benutzer möchte ich, dass auf der Registrierungsseite das Eingabefeld für den Vornamen zuoberst steht und nicht das für den Nachnamen, damit die Eingabe für den Kunden logischer und intuitiver ist.

- Haftungsausschluss für die Nutzung des PowerKube am MUV-Festival 2025


## Done

✅ Wenn eine Person mehrmals Schlägt soll immer nur das letzte Ergebnis in der Rangliste aufgeführt werden. Der gleiche Kunde soll bei $n$ Versuchen nicht $n$ Mal
in der Rangliste aufgelistet werden.

✅ Als Leichtgewicht, sowohl Frauen als auch Männer, möchte ich mich nicht mit einem Schwergewicht messen müssen, um einen fairen Vergleich zu haben. Daher sollte ein Gewichtkoeffizient eingebaut werden, um die Vergleichbarkeit zu gewährleisten.Gewichtkoeffizient einbauen:
 
 ```python
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
 ```

✅ Als User möchte ich dass sich die Rangliste alle 10 Sekunden aktualisiert damit ich immer den aktuellsten Stand sehen kann.

 ```javascript
// Erste Initialisierung
    ladeRangliste();
// Alle 10 Sekunden neu laden
    setInterval(ladeRangliste, 10000);
 ```

 ✅ Responsivität bei der Mobileansicht prüfen (Balken)
 - CSS rangliste angepasst.







