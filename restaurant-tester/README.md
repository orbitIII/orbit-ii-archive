# Restauranttester

Eigenständiges Side-Projekt – nicht Teil von Orbit.

Kleine Web-App zum Eintragen von Restaurant-Testergebnissen. Per Link teilen und gemeinsam bearbeiten.

## Features

- Testrunde erstellen mit Name
- Restaurants bewerten (Essen, Service, Ambiente, Preis-Leistung)
- Notizen und Tester-Name
- Link teilen – alle mit dem Link sehen dieselben Daten
- Automatisches Speichern & Live-Aktualisierung alle 3 Sekunden

## Starten

```bash
cd restaurant-tester
npm install
npm start
```

Dann im Browser öffnen: `http://localhost:3847`

## Link teilen

Nach dem Erstellen einer Runde erscheint die URL z. B. als:

`http://localhost:3847/s/abc12345`

Diesen Link an andere schicken – alle können gleichzeitig Einträge hinzufügen oder bearbeiten.
