#!/usr/bin/env python3
"""Synthesize bridge operators from queer × heteronormativ poles — ORBIT best-of-both-worlds."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def match_profile(row: dict, pole: dict) -> bool:
    clusters = {row.get("primary_cluster", ""), row.get("secondary_cluster", "")} - {""}
    tags = (row.get("orbit_tags", "") + " " + row.get("notes", "")).lower()
    if clusters & set(pole.get("profile_cluster_match", [])):
        return True
    for tag in pole.get("profile_tag_match", []):
        if tag.lower() in tags:
            return True
    handle = row.get("handle", "")
    if handle in pole.get("handles_priority", []):
        return True
    return False


def weave_operators(weaves: list[dict], weave_ids: list[str]) -> list[str]:
    ops: list[str] = []
    for w in weaves:
        if w.get("id") not in weave_ids:
            continue
        bindings = w.get("branch_bindings") or {}
        for branch in bindings.values():
            if isinstance(branch, dict):
                for key in ("tags", "rule", "opening", "exhibition", "look"):
                    val = branch.get(key)
                    if isinstance(val, list):
                        ops.extend(str(v) for v in val)
                    elif isinstance(val, str) and val:
                        ops.append(val)
        tension = w.get("tension") or {}
        for pole_key in ("pole_a", "pole_b"):
            p = tension.get(pole_key) or {}
            for k in ("mood", "signal", "visual"):
                if p.get(k):
                    ops.append(str(p[k]))
        if w.get("summary"):
            ops.append(w["summary"])
    return list(dict.fromkeys(ops))


def parse_masterplan(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path.name), "found": False}

    text = path.read_text(encoding="utf-8")
    phase_match = re.search(
        r"\|\s\*\*(\d+)\s+([^*|]+?)\*\*\s\|\s\*\*(AKTIV|Ziel|abgeschlossen)\*\*",
        text,
    )
    gate_match = re.search(
        r"\*\*Phase-Gate \(harte Regel\):\*\*\s*(.+?)(?=\n\n|\n---)",
        text,
        re.DOTALL,
    )
    sec8 = re.search(r"## 8\.[^\n]*\n\n(?:[^\n]*\n\n)?((?:\d+\.\s[^\n]+\n)+)", text)
    week_tasks = []
    if sec8:
        week_tasks = [line.strip() for line in sec8.group(1).strip().splitlines() if line.strip()]

    exit_tasks: list[dict] = []
    sec7 = re.search(r"## 7\.[^\n]*\n\n(\|[^\n]+\n\|[-| ]+\n(?:\|[^\n]+\n)+)", text)
    if sec7:
        for row in sec7.group(1).splitlines()[2:]:
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) >= 3 and cells[0] not in ("Task", ""):
                exit_tasks.append({"task": cells[0], "output": cells[1], "file": cells[2]})

    stand_match = re.search(r"\|\s\*\*Stand\*\*\s\|\s(\d{4}-\d{2}-\d{2})\s\|", text)
    return {
        "path": str(path.relative_to(ROOT)),
        "found": True,
        "stand": stand_match.group(1) if stand_match else None,
        "phase": phase_match.group(1).strip() if phase_match else None,
        "phase_name": phase_match.group(2).strip() if phase_match else None,
        "phase_status": phase_match.group(3).strip() if phase_match else None,
        "phase_gate": gate_match.group(1).strip() if gate_match else None,
        "diese_woche": week_tasks,
        "naechster_task": week_tasks[0] if week_tasks else None,
        "phase2_exit_tasks": exit_tasks,
        "session_regel_ref": "docs/orbit_masterplan.md §12",
    }


def bridge_rules_for_task(cfg: dict, task_line: str | None) -> list[str]:
    if not task_line:
        return []
    mapping = (cfg.get("masterplan_binding") or {}).get("bridge_to_tasks", {})
    task_lower = task_line.lower()
    ids: list[str] = list(mapping.get("phase2_all", []))
    if "visual brief" in task_lower:
        ids = mapping.get("visual_brief", ids)
    elif "referenz_spiegel" in task_lower or "referenz_spiegel" in task_lower.replace("-", "_"):
        ids = mapping.get("referenz_spiegel", ids)
    elif "sound" in task_lower:
        ids = mapping.get("sound_entscheidung", ids)
    return list(dict.fromkeys(ids))


def profile_hits(csv_path: Path, pole: dict) -> list[dict]:
    if not csv_path.exists():
        return []
    hits = []
    with csv_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if match_profile(row, pole):
                hits.append(
                    {
                        "handle": row.get("handle"),
                        "clusters": [row.get("primary_cluster"), row.get("secondary_cluster")],
                        "photo_aesthetic": row.get("photo_aesthetic", ""),
                        "mood": row.get("mood", ""),
                    }
                )
    return hits


def build_synthesis(cfg: dict, dna: dict, identitaet: dict, werk: dict | None) -> dict:
    tertiary = (dna.get("core_dna") or {}).get("tension_axis", {}).get("tertiary_axis", {})
    position = (identitaet.get("identitaet_profil") or {}).get("positionierung", {})
    weaves = load_json(ROOT / "orbit_verflechtungen.json").get("weaves", [])
    csv_path = ROOT / "marquardt_aesthetic_profiles.csv"
    mp_path = ROOT / (cfg.get("masterplan_binding") or {}).get("path", "docs/orbit_masterplan.md")
    masterplan = parse_masterplan(mp_path)
    task_rule_ids = bridge_rules_for_task(cfg, masterplan.get("naechster_task"))
    bridge_rows_all = cfg.get("synthesis_rules", {}).get("keep_from_both", [])
    bridge_for_task = [r for r in bridge_rows_all if r.get("id") in task_rule_ids]

    hetero_cfg = cfg["pole_sources"]["heteronormativ"]
    queer_cfg = cfg["pole_sources"]["queer"]

    from_hetero = list(
        dict.fromkeys(
            hetero_cfg.get("operators_from_dna", [])
            + weave_operators(weaves, hetero_cfg.get("weave_ids", []))
        )
    )
    from_queer = list(
        dict.fromkeys(
            queer_cfg.get("operators_from_dna", [])
            + weave_operators(weaves, queer_cfg.get("weave_ids", []))
        )
    )

    werk_binding = None
    if werk:
        pos = werk.get("spannungsachse", {}).get("positionierung", {})
        werk_binding = {
            "title": werk.get("title"),
            "heteronorm_signals": pos.get("heteronorm_signals", []),
            "queer_signals": pos.get("queer_signals", []),
            "bridge_regel": pos.get("regel"),
        }

    return {
        "generated": date.isoformat(date.today()),
        "masterplan": masterplan,
        "masterplan_binding": cfg.get("masterplan_binding"),
        "bridge_for_current_task": {
            "task": masterplan.get("naechster_task"),
            "rule_ids": task_rule_ids,
            "rules": bridge_for_task,
        },
        "axis": cfg.get("axis", {}),
        "orbit_position": tertiary.get("orbit_position") or position.get("primary"),
        "from_heteronormativ": {
            "operators": from_hetero,
            "profile_hits": profile_hits(csv_path, hetero_cfg),
            "weaves": hetero_cfg.get("weave_ids", []),
        },
        "from_queer": {
            "operators": from_queer,
            "profile_hits": profile_hits(csv_path, queer_cfg),
            "weaves": queer_cfg.get("weave_ids", []),
        },
        "bridge_synthesis": bridge_rows_all,
        "forbidden_strip": cfg.get("synthesis_rules", {}).get("strip_always", []),
        "litmus": cfg.get("synthesis_rules", {}).get("litmus", []),
        "werk_binding": werk_binding,
        "next_command": "python3 scripts/orbit_bridge_synthesis.py --markdown",
    }


def to_markdown(data: dict) -> str:
    mp = data.get("masterplan") or {}
    lines = [
        f"# ORBIT Bridge Synthesis — {data.get('generated')}",
        "",
        "**Position:** zwischen queer und heteronormativ (Bridge — best of both worlds)",
        "",
        "## Masterplan (Steuerung)",
        "",
        f"- **Quelle:** `{mp.get('path', 'docs/orbit_masterplan.md')}`"
        + (f" · Stand {mp.get('stand')}" if mp.get("stand") else ""),
    ]
    if mp.get("phase"):
        lines.append(
            f"- **Phase:** {mp.get('phase')} — {mp.get('phase_name')} ({mp.get('phase_status')})"
        )
    if mp.get("phase_gate"):
        lines.append(f"- **Phase-Gate:** {mp.get('phase_gate')}")
    if mp.get("naechster_task"):
        lines.append(f"- **Nächster Task (§8):** {mp.get('naechster_task')}")
    bft = data.get("bridge_for_current_task") or {}
    if bft.get("rules"):
        lines.append("- **Bridge für diesen Task:**")
        for row in bft["rules"]:
            lines.append(f"  - `{row.get('id')}` — {row.get('bridge')}")
    lines.extend(["", "## Aus heteronormativ (Form, Institution, Editorial)", ""])
    for op in data["from_heteronormativ"]["operators"][:20]:
        lines.append(f"- {op}")
    if data["from_heteronormativ"]["profile_hits"]:
        lines.append("")
        lines.append("Profile-Hits:")
        for h in data["from_heteronormativ"]["profile_hits"][:8]:
            lines.append(f"- `@{h['handle']}` — {', '.join(c for c in h['clusters'] if c)}")

    lines.extend(["", "## Aus queer (Community, Subversion, Plattform)", ""])
    for op in data["from_queer"]["operators"][:20]:
        lines.append(f"- {op}")
    if data["from_queer"]["profile_hits"]:
        lines.append("")
        lines.append("Profile-Hits:")
        for h in data["from_queer"]["profile_hits"][:8]:
            lines.append(f"- `@{h['handle']}` — {', '.join(c for c in h['clusters'] if c)}")

    lines.extend(["", "## Bridge — das Beste aus beiden", ""])
    for row in data.get("bridge_synthesis", []):
        lines.append(f"- **{row.get('id')}:** {row.get('bridge')} _(hetero: {row.get('hetero')} + queer: {row.get('queer')})_")

    lines.extend(["", "## Verwerfen (immer)", ""])
    for f in data.get("forbidden_strip", []):
        lines.append(f"- {f}")

    if data.get("werk_binding"):
        wb = data["werk_binding"]
        lines.extend(["", f"## Werk: {wb.get('title')}", ""])
        lines.append(f"- Bridge-Regel: {wb.get('bridge_regel')}")
        for s in wb.get("heteronorm_signals", []):
            lines.append(f"- heteronorm: {s}")
        for s in wb.get("queer_signals", []):
            lines.append(f"- queer: {s}")

    lines.extend(["", "## Litmus", ""])
    for q in data.get("litmus", []):
        lines.append(f"- {q}")

    lines.extend(["", "## Agent-Review", "", "_Platz für Cursor-Automation / manuellen Review._", ""])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="ORBIT bridge synthesis — best of both worlds")
    parser.add_argument("--config", default="orbit_bridge_automation.json")
    parser.add_argument("--werk", default="orbit_werk_pour_cet_instant.json")
    parser.add_argument("--markdown", action="store_true", help="Also write markdown report")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout")
    args = parser.parse_args()

    cfg = load_json(ROOT / args.config)
    dna = load_json(ROOT / "orbit_kultur_dna.json")
    identitaet = load_json(ROOT / "orbit_identitaet.json")
    werk_path = ROOT / args.werk
    werk = load_json(werk_path) if werk_path.exists() else None

    out = build_synthesis(cfg, dna, identitaet, werk)
    out_cfg = cfg.get("outputs", {})

    json_path = ROOT / out_cfg.get("json", "orbit_bridge_synthesis_latest.json")
    json_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {json_path.relative_to(ROOT)}")

    if args.markdown:
        md_path = ROOT / out_cfg.get("markdown", "docs/orbit_bridge_synthesis_latest.md")
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(to_markdown(out), encoding="utf-8")
        print(f"Wrote {md_path.relative_to(ROOT)}")

    if args.stdout:
        print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
