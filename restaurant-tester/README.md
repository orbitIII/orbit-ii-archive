# Restauranttester

Eigenständiges Side-Projekt – nicht Teil von Orbit.

Ergebnisse eintragen, **offline nutzen**, **lokal langfristig speichern**, per Link teilen.

## Features

- Testrunde erstellen und Restaurants bewerten
- **Local-first:** alles landet im Browser (`localStorage`) – bleibt nach Reload erhalten
- **Offline:** Service Worker / PWA – App weiter nutzbar ohne Netz
- **Export:** JSON-Backup + CSV-Download
- **Import:** Backup-Datei wieder einlesen
- Optionaler Server-Sync / Cloudflare-Tunnel zum Teilen

## Starten

```bash
cd restaurant-tester
npm install
npm start
```

`npm start` startet Server + öffentlichen Tunnel (**Pinggy**, Fallback localtunnel – kein Cloudflare).  
In der Konsole bzw. im App-Banner erscheint `TEILBARER LINK`.

Nur lokal: `npm run start:local` → `http://localhost:3847`

Hinweis: Gratis-Tunnel können nach einiger Zeit ablaufen. Für Dauerbetrieb lokal `npm start` laufen lassen und den aktuellen Link teilen.

## Offline & langfristig speichern

1. App einmal online öffnen (installiert den Service Worker)
2. Optional: **App installieren** (Button / Browser-Menü → Zum Home-Bildschirm)
3. Einträge werden automatisch **lokal** gespeichert
4. Für echte Langzeit-Sicherung: **JSON exportieren** und die Datei speichern (Files/Drive/Mail)
5. Später: **Backup importieren** auf demselben oder anderem Gerät

Ohne Export bleiben Daten im Browser-Speicher des Geräts (überleben Reload, nicht zwingend App-/Browser-Datenlöschung).

## Link teilen

„Link teilen“ kopiert die aktuelle URL (Tunnel/Host + `/s/<id>`).  
Andere Bearbeiter brauchen Online-Zugang zum Server; deine lokale Kopie bleibt unabhängig davon erhalten.
