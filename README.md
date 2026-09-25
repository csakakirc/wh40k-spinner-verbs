# wh40k-spinner-verbs

*"In the grim darkness of the far future, there is only… Thinking."*

Warhammer 40,000 themed [spinner verbs](https://code.claude.com/docs/en/settings) for Claude Code,
grouped by faction. Swap Claude's "Pondering…" for "Appeasing the machine spirit…",
"Krumpin' da gitz…" or "Proceeding just as planned…".

## Factions

| Alliance | Factions |
| --- | --- |
| **Imperium** | Adeptus Astartes, Adeptus Mechanicus, Astra Militarum, Adepta Sororitas, Adeptus Custodes, Grey Knights, Inquisition, Imperial Knights |
| **Chaos** | Chaos Space Marines, World Eaters (Khorne), Death Guard (Nurgle), Thousand Sons (Tzeentch), Emperor's Children (Slaanesh) |
| **Xenos** | Orks, Aeldari, Drukhari, Necrons, T'au Empire, Tyranids, Genestealer Cults, Leagues of Votann |

Run `python3 scripts/build.py --list` to see every faction id and verb count.

## Layout

```
factions/<alliance>/<faction>.json   # source of truth: one file per faction
dist/all.json                        # every faction
dist/<alliance>.json                 # imperium, chaos, xenos
dist/<alliance>/<faction>.json       # a single faction
scripts/build.py                     # validates sources and regenerates dist/
```

Every file in `dist/` is a ready-to-use Claude Code settings snippet:

```json
{
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Appeasing the machine spirit", "Chanting binharic cant", "..."]
  }
}
```

`"mode": "append"` mixes the verbs in with Claude's defaults; `"replace"` uses only yours.
Claude Code adds the trailing `…` itself, so the verbs don't include one.

## Install

Pick a snippet and merge it into your user settings (`~/.claude/settings.json`) or a
project's `.claude/settings.json`. With `jq`:

```sh
# One faction
jq -s '.[0] * .[1]' ~/.claude/settings.json dist/imperium/adeptus-mechanicus.json > /tmp/settings.json \
  && mv /tmp/settings.json ~/.claude/settings.json
```

Or pick your own warband (factions and alliances can be mixed) and replace the defaults:

```sh
python3 scripts/build.py --replace orks necrons chaos > /tmp/wh40k.json
jq -s '.[0] * .[1]' ~/.claude/settings.json /tmp/wh40k.json > /tmp/settings.json \
  && mv /tmp/settings.json ~/.claude/settings.json
```

If you don't have a settings file yet, copy the snippet straight to `~/.claude/settings.json`.

## Contributing

1. Add or edit verbs in `factions/<alliance>/<faction>.json`. Keep them short, present
   participle ("Purging the heretic"), and without a trailing ellipsis.
2. Run `python3 scripts/build.py`. It rejects duplicates and ellipses, then regenerates `dist/`.
3. Commit both the source file and `dist/`.

*The Emperor protects. Your context window does not.*
