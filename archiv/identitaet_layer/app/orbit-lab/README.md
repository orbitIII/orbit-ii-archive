# ORBIT Lab — Browser-Test-App

Interaktiver Überblick über das ORBIT-Fundament: **Funktion**, **Schichten**, **Säulen**, **Prinzipien**, **Litmus-Check**, **Pour Cet Instant**.

## Start

```bash
python3 scripts/serve_orbit_lab.py
```

Öffne: **http://127.0.0.1:8765/app/orbit-lab/**

Port ändern: `ORBIT_LAB_PORT=9000 python3 scripts/serve_orbit_lab.py`

## Was die App tut

| Tab | Funktion |
|-----|----------|
| **Funktion** | Was ORBIT sein soll — Mittelpunkt, Pflicht-Regeln, Phase, Litmus |
| **Schichten** | 6-Schichten-Modell aus `orbit_fundament.json` |
| **Säulen** | Berlin / Paris MAM / ARTHAUS / eigenes Werk + Brücken + Cases |
| **Prinzipien** | Alle `kunst_prinzipien` wählen, Kombinationen sehen |
| **Litmus** | Projektidee testen (Prinzipien, forbidden, Werk-Overlap) |
| **Werk** | *Pour Cet Instant* als Output-Filter |

Daten werden live aus den Repo-JSONs geladen — Änderungen an `orbit_*.json` sind nach Reload sichtbar.

## Wofür ORBIT da ist (Kurz)

1. **Du** + eigenes Werk = Mittelpunkt  
2. **Prinzipien** = Entscheidungs-Operatoren (nicht Stil)  
3. **Säulen** = Referenz zum Extrahieren (Berlin, Paris, Film)  
4. **Litmus** = Passt es — oder ist es Moodboard / Kopie?  
5. **Output** = Gesamtwerk veröffentlichen, dann weiter sammeln  

Siehe auch: `orbit_fundament.json`, `docs/orbit_masterplan.md`
