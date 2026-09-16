# Contributing to THE CYBERSECURITY RADAR

Thanks for your interest in contributing!

THE CYBERSECURITY RADAR is built around one main idea:

> **Turn cybersecurity signals into opportunities for investigation.**

## What You Can Contribute

Contributions can include:

- Adding useful cybersecurity resources
- Improving existing resource metadata
- Fixing bugs
- Improving the radar engine
- Improving validation
- Improving documentation
- Suggesting new investigation workflows

## Adding Resources

Most resource contributions should be made in `resources.json`.

Before adding a resource, check:

- Does it provide genuine cybersecurity value?
- Can it lead to investigation, analysis, or hands-on work?
- Is it already in the database?
- Is the `type` appropriate?
- Are the categories, roles, regions, and tags relevant?

**Quality is more important than quantity.**

Avoid adding resources simply to make the database larger.

For more details, see:

`docs/RESOURCE_ADDITION_GUIDE.md`

## Avoid Duplicates

If an existing resource already covers the same website or service, update the existing entry instead of creating a duplicate.

Use categories, roles, regions, and tags to represent multiple uses of the same resource.

## Code Contributions

The project separates resource data from application behavior.

Generally:

- **Resource/data changes → `resources.json`**
- **Application behavior changes → `randomizer.py`**

Avoid changing the Python code when a change can be handled through resource metadata.

## Testing

Before submitting a change, make sure the affected functionality still works.

For resource changes, check that:

- The JSON remains valid.
- Resource IDs remain unique.
- Required fields are present.
- Field types are correct.
- The application can load the database successfully.

For code changes, test the relevant commands and workflows.

## Runtime History

`picker_history.json` contains local runtime history.

It should normally **not be committed** to the repository.

## Pull Requests

When submitting a pull request, briefly explain:

1. **What changed?**
2. **Why was it changed?**
3. **How was it tested?**

For new resources, also explain why the resource is useful for cybersecurity investigation.

## Contribution Philosophy

Keep the project's core principles in mind:

- **Investigation over collection**
- **Quality over quantity**
- **Evidence over assumptions**
- **Hands-on over passive consumption**
- **Simple over unnecessary complexity**

The most important question is:

> **Does this contribution help turn "that's interesting" into "let's investigate it"?**

## Happy Contributing!
