# THE CYBERSECURITY RADAR — Project Usage Guide

## 1. Overview

THE CYBERSECURITY RADAR is a cybersecurity resource discovery and investigation tool.

Its purpose is not simply to help you find more cybersecurity content.

Its purpose is to help turn:

> **"That's interesting."**

into:

> **"Let's investigate it."**

The radar combines randomized discovery, resource search, investigation workflows, and history tracking.

---

## 2. Project Structure

```text
THE-CYBERSECURITY-RADAR/

├── randomizer.py
├── resources.json
├── README.md
└── docs/
````

### `randomizer.py`

The main application and radar engine.

### `resources.json`

The master database containing the cybersecurity resources and radar configuration.

### `picker_history.json`

Runtime history created by the application.

It records previous selections and investigation activity and should normally remain local rather than being committed to the public repository.

---

## 3. The Core Investigation Loop

The radar is based on:

```text
Signal
  ↓
Question
  ↓
Primary Source
  ↓
Triangulation
  ↓
Hands-on
  ↓
Understanding
  ↓
Artifact
```

Each stage has a different purpose.

### Signal

Discover something potentially interesting.

### Question

Turn the signal into something specific that can be investigated.

### Primary Source

Find the original or most authoritative technical material available.

### Triangulation

Compare the finding with additional sources or evidence.

### Hands-on

Perform practical investigation where appropriate.

Examples:

* PCAP analysis
* Malware analysis
* Reverse engineering
* Lab work
* Detection development
* Vulnerability reproduction

### Understanding

Determine what actually happened, how something works, or why it matters.

### Artifact

Produce something tangible from the investigation.

Examples:

* Writeup
* Research note
* Detection rule
* YARA rule
* Sigma rule
* Script
* PoC
* Diagram
* GitHub repository

---

## 4. Quick Mode

Quick mode is intended for lightweight discovery.

Run:

```bash
python randomizer.py quick
```

The radar selects a resource and provides an investigation-oriented direction.

The important question is not:

> "What should I read?"

but:

> **"What could I investigate using this?"**

Quick mode is useful when you want an unexpected cybersecurity signal without committing to a full investigation.

---

## 5. Deep Investigation Mode

Deep mode is intended for a resource or signal that deserves deeper investigation.

Run:

```bash
python randomizer.py deep
```

A deep investigation records the investigation using the following structure:

```text
Signal
Question
Primary Source
Triangulation
Hands-on
Understanding
Result
Artifact
```

The objective is to move beyond consuming information and produce an actual investigation result.

---

## 6. Weekly Mode

Weekly mode provides a structured way to record radar activity over a week.

Run:

```bash
python randomizer.py weekly
```

The weekly workflow can capture:

* Interesting signals
* Most interesting signal
* Why it was interesting
* Investigation question
* Sources
* Evidence
* Hands-on activity
* Result
* Artifact
* Publication decision

The weekly mode is intended to capture what naturally emerged from using the radar rather than turning the project into a rigid productivity tracker.

---

## 7. Search Mode

The resource database can be searched by keyword.

Example:

```bash
python randomizer.py search malware
```

Search is useful when you already have a specific topic in mind.

Unlike random selection, search allows you to deliberately explore the existing resource database.

---

## 8. Other Useful Commands

The application also provides functionality for inspecting the resource database and its state.

Use:

```bash
python randomizer.py --help
```

to see the currently available commands and options.

The application provides the following additional modes:

* `list` — inspect available resources
* `types` — inspect resource types
* `category` — inspect resources by category
* `history` — inspect investigation and selection history
* `stats` — inspect resource/database statistics

---

## 9. Resource Types

Resources are classified by their primary purpose.

The type helps the radar determine how a resource can be used.

Examples of resource types include resources oriented toward:

* News and signals
* Threat intelligence
* Research
* Community
* Vulnerabilities
* Labs
* PCAPs
* Malware analysis
* Reverse engineering
* Detection
* OSINT
* Primary technical material

A resource can have multiple categories, roles, regions, and tags while maintaining a single primary type.

---

## 10. Resource Tiers

Resources are organized into five tiers.

### Tier 1 — Real-Time Sensor

Fast-moving signals and cybersecurity activity.

### Tier 2 — Operational Radar

Operational security information such as vulnerabilities, IOCs, CERT information, and incidents.

### Tier 3 — Technical Research

Professional cybersecurity research and technical analysis.

### Tier 4 — Community

Cybersecurity communities, conferences, and practitioner ecosystems.

### Tier 5 — Primary Material

Original technical material such as:

* PoCs
* Exploits
* Samples
* PCAPs
* Papers
* Source code
* Detection rules

The tiers represent different positions in the discovery-to-investigation process.

---

## 11. Anti-Collector Philosophy

The radar intentionally tries to avoid this pattern:

```text
Find article
  ↓
Bookmark
  ↓
Find another article
  ↓
Bookmark
  ↓
Find paper
  ↓
Bookmark
  ↓
Never investigate
```

Instead, the intended behavior is:

```text
Find signal
  ↓
Ask question
  ↓
Find evidence
  ↓
Investigate
  ↓
Understand
  ↓
Create artifact
```

The goal is not to maximize the number of resources consumed.

The goal is to maximize the chance that something discovered becomes worth investigating.

---

## 12. History

The application maintains runtime history in:

```text
picker_history.json
```

History can be used to track previous selections and investigation activity.

This file is local runtime state and should generally not be committed to the public repository.

---

## 13. Recommended Usage Pattern

A simple way to use the radar is:

```text
Discover
   ↓
Is it interesting?
   ↓
No ──→ Move on
   │
  Yes
   ↓
Ask a question
   ↓
Find evidence
   ↓
Investigate
   ↓
Understand
   ↓
Create an artifact
```

Not every signal needs to become a deep investigation.

The important part is recognizing when a signal is worth following.

---

## 14. The Main Principle

THE CYBERSECURITY RADAR is not designed to replace your judgment.

It is designed to create opportunities for discovery.

Randomness provides the **signal**.

Curiosity provides the **reason to investigate**.

Evidence provides the **foundation**.

Hands-on work provides the **understanding**.

Artifacts provide the **output**.

> **The radar finds the signal. You decide whether it is worth investigating.**
