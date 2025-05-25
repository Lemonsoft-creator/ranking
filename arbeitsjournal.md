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
