---
edr: 1
id: 01M5C5QEHHNXJ3D7X2ZCMGXQT8
slug: body-horizontal-rule
title: A body rule is not a second frontmatter closer
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-01-15
valid_to: null
review_by: 2026-07-15
supersedes: []
criticality: warning
checks: []
waivers: []
sources:
  - type: spec
    url: https://github.com/acme/platform/blob/main/docs/adr/0021-body-rule.md
tags: [format]
---

# A body rule is not a second frontmatter closer

## Context

The frontmatter closer is the first line that is exactly `---`.

---

A later horizontal rule stays in the body, and the headings after it still count.

```text
# Fake title
## Decision
```

A heading inside a fence is an example, not a second title.

## Decision

Parsers keep every heading that follows a body horizontal rule.

## Alternatives considered

- Treat every `---` line as a closer: that drops the Decision section when an author uses a rule.

## Consequences

Authors can use a horizontal rule inside a section.

## Verification

This file is a positive fixture. The Decision heading remains after the rule.
