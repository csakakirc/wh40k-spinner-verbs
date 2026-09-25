#!/usr/bin/env python3
"""Build Claude Code `spinnerVerbs` settings snippets from the faction files.

Usage:
  python3 scripts/build.py                     # regenerate everything in dist/
  python3 scripts/build.py orks necrons        # print a snippet for chosen factions/alliances
  python3 scripts/build.py --replace orks      # same, but replace Claude's default verbs
  python3 scripts/build.py --list              # list available faction and alliance ids
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACTIONS = ROOT / "factions"
DIST = ROOT / "dist"


def load_factions():
    factions = {}
    for path in sorted(FACTIONS.glob("*/*.json")):
        data = json.loads(path.read_text())
        verbs = data["verbs"]
        for verb in verbs:
            if not verb.strip() or verb.endswith(("…", "...")):
                sys.exit(f"{path}: bad verb {verb!r} (Claude Code adds the ellipsis)")
        dupes = {v for v in verbs if verbs.count(v) > 1}
        if dupes:
            sys.exit(f"{path}: duplicate verbs {sorted(dupes)}")
        factions[path.stem] = {"alliance_id": path.parent.name, **data}
    return factions


def snippet(verbs, mode="append"):
    return {"spinnerVerbs": {"mode": mode, "verbs": verbs}}


def resolve(ids, factions):
    verbs = []
    for ident in ids:
        matches = [f for key, f in factions.items() if ident in (key, f["alliance_id"], "all")]
        if not matches:
            sys.exit(f"unknown faction or alliance: {ident} (try --list)")
        for faction in matches:
            verbs += [v for v in faction["verbs"] if v not in verbs]
    return verbs


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def build_dist(factions):
    for old in DIST.glob("**/*.json"):
        old.unlink()
    write(DIST / "all.json", snippet(resolve(["all"], factions)))
    for alliance in sorted({f["alliance_id"] for f in factions.values()}):
        write(DIST / f"{alliance}.json", snippet(resolve([alliance], factions)))
    for key, faction in factions.items():
        write(DIST / faction["alliance_id"] / f"{key}.json", snippet(faction["verbs"]))
    total = sum(len(f["verbs"]) for f in factions.values())
    print(f"Built dist/ from {len(factions)} factions ({total} verbs)")


def main(argv):
    factions = load_factions()
    mode = "append"
    if "--replace" in argv:
        argv.remove("--replace")
        mode = "replace"
    if argv == ["--list"]:
        for alliance in sorted({f["alliance_id"] for f in factions.values()}):
            print(f"{alliance}:")
            for key, f in factions.items():
                if f["alliance_id"] == alliance:
                    print(f"  {key:<22} {f['name']} ({len(f['verbs'])})")
        return
    if not argv:
        build_dist(factions)
        return
    print(json.dumps(snippet(resolve(argv, factions), mode), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
