---
edr: 1
id: 01M5C5QEHZ5NR9NJEM2ZWM04EW
slug: readme-summaries-are-advisory
title: Generated README summaries never block a merge
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-08-01
valid_to: null
review_by: 2027-02-01
supersedes: []
criticality: advisory
checks:
  - engine: llm-advisory
    target: readme
    ref: prompts/readme-summary.txt
    mode: advise
waivers: []
sources:
  - type: spec
    url: https://github.com/acme/app/blob/main/docs/readme-policy.md
tags: [docs]
---

# Generated README summaries never block a merge

## Context

A model can draft a README summary, and it can also invent a requirement that the code does not implement.

## Decision

README summaries produced by a model are advisory. A person merges. The model does not fail the check.

## Alternatives considered

- Let the model block when its confidence is high: confidence is not an audit trail, and a wrong block stops a release.

## Consequences

The prompt and the model output are stored as advice. They are not a verdict.

## Verification

The `llm-advisory` engine runs `prompts/readme-summary.txt` in advise mode. It is not a deterministic check.
