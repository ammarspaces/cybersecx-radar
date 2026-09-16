# Resource Addition Guide

This guide explains how to add cybersecurity resources to `resources.json` without breaking the radar's structure or investigation philosophy.

## 1. Before Adding a Resource

Ask:

- Is this resource genuinely useful?
- Can it lead to investigation, analysis, or hands-on work?
- Does the resource already exist?
- What is its primary purpose?
- Which categories, roles, regions, and tags describe it accurately?

**Quality is more important than quantity.**

Do not add a resource simply because it is popular or interesting.

---

## 2. Resource Structure

A resource normally contains:

```json
{
  "id": "unique-resource-id",
  "name": "Resource Name",
  "domain": "example.com",
  "path": "/path",
  "type": "resource_type",
  "categories": [],
  "regions": [],
  "tier": 1,
  "role": [],
  "tags": [],
  "health": {}
}
````

Each field has a specific purpose.

### `id`

A unique identifier for the resource.

Do not reuse an existing ID.

### `name`

The human-readable name of the resource.

### `domain`

The resource's domain.

### `path`

The relevant path on the domain.

### `type`

The resource's primary function.

The type affects how the radar can use the resource.

### `categories`

Topics or areas associated with the resource.

### `regions`

Geographic or regional relevance.

### `tier`

The resource's position within the radar's resource hierarchy.

### `role`

The cybersecurity roles for which the resource may be useful.

This is a list, even when there is only one role.

### `tags`

Additional keywords describing the resource.

### `health`

Metadata used to track the resource's operational status.

---

# 3. Choosing the Type

Choose the type based on the **primary purpose**.

For example:

* A security news site should primarily represent a signal source.
* A vulnerability database should represent an operational security resource.
* A malware repository should represent material useful for malware investigation.
* A PCAP repository should represent hands-on investigation material.
* A research organization's publication feed should represent technical research.

Do not classify a resource based only on one possible use.

---

# 4. Choosing the Tier

The radar uses five conceptual tiers:

| Tier | Purpose                               |
| ---- | ------------------------------------- |
| 1    | Real-time signals and sensors         |
| 2    | Operational security information      |
| 3    | Technical research                    |
| 4    | Community and practitioner ecosystems |
| 5    | Primary technical material            |

The tier should reflect where the resource fits within the discovery-to-investigation process.

---

# 5. Categories, Roles, Regions, and Tags

These fields provide additional context.

Use them to describe the resource accurately rather than adding every possible label.

### Categories

Use relevant cybersecurity topics.

### Roles

Use relevant professional roles.

Example:

```json
"role": [
  "soc_analyst",
  "security_analyst"
]
```

### Regions

Use regions that are genuinely relevant to the resource.

### Tags

Use useful keywords that help describe or discover the resource.

---

# 6. Avoid Duplicates

Before adding a resource, search `resources.json`.

If the resource already exists:

**Update the existing entry instead of creating another one.**

If one resource is useful for multiple purposes, use its existing metadata:

* Multiple categories
* Multiple roles
* Multiple regions
* Multiple tags

Do not create separate entries for each use case.

---

# 7. Investigation Value

A good resource should ideally provide a path toward doing something.

For example:

```text
Resource
   ↓
Interesting Signal
   ↓
Investigation Question
   ↓
Evidence
   ↓
Hands-on Activity
   ↓
Understanding
   ↓
Artifact
```

Potential investigation activities include:

* PCAP analysis
* Malware analysis
* Reverse engineering
* OSINT
* Vulnerability reproduction
* Detection engineering
* SIEM investigation
* NDR investigation
* Script development
* Lab exercises

A resource does not necessarily need to support every stage.

The important thing is that it can contribute meaningfully to the investigation process.

---

# 8. Health Metadata

Every resource should contain a `health` object.

Example:

```json
"health": {
  "signal": null,
  "noise": null,
  "activity": null,
  "keep": null,
  "last_checked": null,
  "notes": null
}
```

Health information is operational metadata.

Do not use it as a replacement for the resource's normal classification.

---

# 9. Researchers

If a resource is associated with specific researchers, the appropriate researcher association can be represented through the project's researcher metadata.

The `researchers` collection is maintained separately from the individual resource entry.

For resources without a specific researcher association, do not invent researcher attribution.

The project may use:

```json
"researchers": []
```

when there are no researcher records to maintain.

---

# 10. Adding a Resource vs. Changing Code

Adding a resource normally requires changing only:

```text
resources.json
```

You should not modify:

```text
randomizer.py
```

just because a new resource was added.

The general rule is:

> **Data changes belong in `resources.json`. Behavior changes belong in `randomizer.py`.**

Code changes are appropriate only when the radar itself needs new behavior.

---

# 11. Validation

After adding a resource, verify:

* [ ] JSON is valid
* [ ] ID is unique
* [ ] Required fields exist
* [ ] `role` is a list
* [ ] `health` is an object
* [ ] Type is appropriate
* [ ] Tier is appropriate
* [ ] Categories are relevant
* [ ] Regions are relevant
* [ ] Tags are useful
* [ ] Resource is not a duplicate
* [ ] The application can load `resources.json`

---

# 12. Golden Rule

When deciding whether to add a resource, ask:

> **"Does this increase the radar's ability to discover something worth investigating?"**

If the answer is yes, the resource may belong in the radar.

If the answer is simply:

> **"It's another interesting cybersecurity website."**

then it may not need to be added.