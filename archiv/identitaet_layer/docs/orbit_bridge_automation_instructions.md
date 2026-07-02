# ORBIT Bridge Automation — Agent Instructions

**Name:** ORBIT Bridge — Best of Both Worlds  
**Trigger:** Montags 9:00 (`0 9 * * 1`)  
**Repo:** `orbitIII/orbit-ii-archive` · Branch `orbit/trackid-import-analysis`  
**Autorität:** Bei Widerspruch gilt `docs/orbit_masterplan.md` bis er aktualisiert wird.

---

## Mission (ein Satz)

Extrahiere Operatoren aus **queer** und **heteronormativ**, synthetisiere **Bridge** (best of both worlds), und prüfe ob die Synthese den **aktuellen Masterplan-Task** füttert — ohne Personen-Mittelpunkt, ohne Phase-Gate-Verletzung.

---

## Schritt 1 — Steuerung lesen

Lies in dieser Reihenfolge:

1. `docs/orbit_masterplan.md` — vollständig; **§12 Session-Regel ist bindend**
2. `orbit_bridge_automation.json` — Spec, `masterplan_binding`, `synthesis_rules`, `pole_sources`
3. `orbit_extraktion.json` — Extraktions-Haltung (Operator, nicht Person)
4. `orbit_identitaet.json` → `identitaet_profil.positionierung` — Bridge zwischen queer × heteronormativ
5. `orbit_werk_pour_cet_instant.json` — Anker-Werk, Shoot Aug 2026

Notiere aus dem Masterplan:
- **Phase** und Status (aktuell: Phase 2 Destillieren)
- **Phase-Gate** (§2): kein neuer Weave, kein Scrape, keine Foto-Spec ohne Pour Cet Instant — bis Visual Brief + `referenz_spiegel`
- **Nächster Task** (§8, strikt Priorität von oben)
- **Nicht jetzt** (§9)

---

## Schritt 2 — Synthese erzeugen

```bash
python3 scripts/orbit_bridge_synthesis.py --markdown
```

Outputs:
- `orbit_bridge_synthesis_latest.json`
- `docs/orbit_bridge_synthesis_latest.md`

---

## Schritt 3 — Bridge prüfen (beide Pole)

In `docs/orbit_bridge_synthesis_latest.md` verifizieren:

| Check | Kriterium |
|---|---|
| Hetero-Pol | Operatoren aus Form, Institution, Editorial (nicht nur Personen) |
| Queer-Pol | Operatoren aus Community, Subversion, Plattform |
| Bridge | Jede Regel in `bridge_synthesis` kombiniert **hetero + queer** — kein Kompromiss (beide halb) |
| Strip | Forbidden strip angewendet: rainbow-washing, hetero-only-default, queer-as-gimmick, door-as-status, social-capital-as-currency, competition-as-default |
| Werk | `werk_binding` passt zu Pour Cet Instant |

**Litmus Bridge:**
- Habe ich von BEIDEN Polen etwas genommen — oder nur einen?
- Ist es Bridge — oder Kompromiss?
- Passt zu `identitaet_profil` / Pour Cet Instant?

---

## Schritt 4 — Masterplan-Alignment

Im Report-Block **Masterplan (Steuerung)** prüfen:

- Phase + Gate korrekt gespiegelt?
- **Nächster Task (§8)** stimmt mit Masterplan überein?
- **Bridge für diesen Task** — Regeln aus `masterplan_binding.bridge_to_tasks`:

| Task (§8) | Bridge-Regeln |
|---|---|
| Visual Brief | `form_queer_feeling`, `visual_tension` |
| referenz_spiegel | `institution_community`, `credit_kindness` |
| Sound-Entscheidung | `narrative_bridge` |
| immer Phase 2 | zusätzlich `visibility`, `narrative_bridge` |

**Wenn Bridge den Task nicht füttert:** Im Agent-Review kurz benennen welche Regel/Operator fehlt — **ohne** neuen Weave, ohne neuen JSON-Layer, ohne Scrape.

**Wenn §8-Task erledigt werden kann und Gate erlaubt:** Nur dann am Task arbeiten (z. B. Visual Brief schreiben → `filme/pour_cet_instant/visual_brief.md`). Sonst nur Review, kein Scope-Creep.

---

## Schritt 5 — Phase-Gate (harte Stopps)

**Nicht tun** in diesem Lauf:

- Neuer Weave (NACHTS, Disturbing Beauty, …)
- Instagram-Scrape / Marquardt-Following vervollständigen
- Kameras/CI-Recherche ohne August-Shoot-Bezug
- Bio/Instagram/Persona live (Phase 3)
- Referenz-Person als Mittelpunkt

**Erlaubt:** Operator-Extraktion aus bestehendem Scan-Batch 01 · Bridge-Synthese · Masterplan-Task wenn Gate offen · Agent-Review schreiben

---

## Schritt 6 — Output: Agent-Review

Ergänze in `docs/orbit_bridge_synthesis_latest.md` den Abschnitt **Agent-Review** (bestehenden Inhalt ersetzen oder anhängen):

```markdown
## Agent-Review

**Datum:** YYYY-MM-DD  
**Phase:** [aus Masterplan]  
**Nächster Task (§8):** [Task + Status: offen / in Arbeit / done]

### Masterplan
- Gate eingehalten: ja/nein — [kurz warum]
- Bridge füttert Task: ja/nein — [welche Regeln]

### Best of both worlds
- **Hetero genommen:** [1–2 Operatoren, nicht Personen]
- **Queer genommen:** [1–2 Operatoren]
- **Bridge:** [1 Satz — Spannung, nicht Kompromiss]

### Nächster Schritt (max. 1)
[Konkrete Aktion für User oder nächsten Lauf — aligned mit §8]

### Litmus §10
Ist das ich — oder extrahiere ich nur ihren Mythos? [1 Satz Antwort]
```

Commit nur wenn User explizit bittet.

---

## Schritt 7 — Entscheidungsfilter (§10, 60 Sekunden)

Vor jeder Empfehlung kurz prüfen:

1. Affekt Lead?
2. Bleak, Joy oder Bridge?
3. Medium Lead = Film?
4. Verletzt `forbidden_personal`?
5. In 3 Jahren noch so?
6. **Ich — oder ihr Mythos?**

---

## Referenz-Dateien (Material, nicht Ziel)

| Datei | Rolle |
|---|---|
| `orbit_verflechtungen.json` | 4 Weaves = Case Studies (eingefroren) |
| `marquardt_aesthetic_profiles.csv` | Scan-Batch 01 Profile-Hits |
| `orbit_kultur_dna.json` | Spannungsachsen, Kunst-Prinzipien |
| `orbit_umverteilung.json` | Umverteilung, Freundlichkeit statt Konkurrenz |

---

*Instructions-Version: 2026-06-27 · Spec: `orbit_bridge_automation.json`*
