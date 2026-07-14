# Restauranttester

Eigenständiges Side-Projekt – nicht Teil von Orbit.

Kleine Web-App zum Eintragen von Restaurant-Testergebnissen. Per Link teilen und gemeinsam bearbeiten.

## Features

- Testrunde erstellen mit Name
- Restaurants bewerten (Essen, Service, Ambiente, Preis-Leistung)
- Notizen und Tester-Name
- Link teilen – alle mit dem Link sehen dieselben Daten
- Automatisches Speichern & Live-Aktualisierung alle 3 Sekunden
- Öffentlicher Tunnel beim Start (für Mobile / ohne Port-Forwarding)

## Starten

```bash
cd restaurant-tester
npm install
npm start
```

`npm start` startet den Server auf `0.0.0.0:3847` und legt einen öffentlichen Tunnel an.
Die URL erscheint in der Konsole als `Öffentlicher Link: https://…`.

Nur lokal (ohne Tunnel):

```bash
npm run start:local
```

Dann im Browser: `http://localhost:3847`

## Link teilen

Nach dem Erstellen einer Runde „Link teilen“ klicken.
Der geteilte Link zeigt auf die öffentliche Tunnel-URL (falls aktiv), z. B.:

`https://xxxxx.trycloudflare.com/s/abc12345`

## Hinweise

- Daten liegen in `restaurant-tester/data/` (JSON pro Runde)
- Tunnel-URLs können sich nach Neustart ändern
