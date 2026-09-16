# THE CYBERSECURITY RADAR

> Turn your mind from “that's interesting” to “let's investigate it.”

THE CYBERSECURITY RADAR is a Python-based tool for discovering cybersecurity resources and turning them into potential investigation opportunities.

## Core Loop

```text
Signal -> Question -> Evidence -> Investigation -> Understanding -> Artifact
```

The goal is **not** to collect as much cybersecurity content as possible.

The goal is to find something interesting, investigate it, understand it, and—when useful—produce something from it.

## Features

* Random cybersecurity resource discovery
* Investigation-oriented resource selection
* Deep investigation workflow
* Weekly radar workflow
* Keyword search
* Resource categorization by type, tier, role, and region
* Investigation history

## Quick Start

```bash
python randomizer.py quick
```

Other modes:

```bash
python randomizer.py deep
python randomizer.py weekly
python randomizer.py search <keyword>
```

See all available commands:

```bash
python randomizer.py --help
```

## Project Structure

```text
THE-CYBERSECURITY-RADAR/
├── randomizer.py
├── resources.json
├── README.md
└── docs/
    ├── PROJECT_USAGE_GUIDE.md
    └── RESOURCE_ADDITION_GUIDE.md
```

`picker_history.json` is generated as local runtime history and should normally not be committed.

## Adding Resources

Resources are managed through `resources.json`.

Before adding one, ask:

> **Can this resource lead to something worth investigating?**

See `docs/RESOURCE_ADDITION_GUIDE.md` for the resource schema and guidelines.

## Philosophy

**Investigation over collection.**

The radar is designed to help move from:

```text
Interesting
   ↓
Investigate
   ↓
Understand
   ↓
Create
```

rather than:

```text
Interesting
   ↓
Bookmark
   ↓
Bookmark
   ↓
Bookmark
```

> **Find the signal. Ask the question. Investigate it.**
