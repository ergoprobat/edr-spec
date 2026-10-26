---
edr: 1
id: 01M5C5QEHRM0FQ6ZEGCRFF00QY
slug: eslint-no-floating-promises
title: TypeScript must not drop promises
status: accepted
owner: team:platform
scope:
  - org: acme
    paths:
      - services/**
valid_from: 2026-04-15
valid_to: null
review_by: 2026-10-15
supersedes: []
criticality: warning
checks:
  - engine: eslint
    target: typescript
    ref: eslint.json
    mode: warn
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/app/pull/18
tags: [typescript]
---

# TypeScript must not drop promises

## Context

A floating promise hides a failed call until a later request observes the missing side effect.

## Decision

TypeScript services enable the rule that flags a promise which is neither awaited nor returned.

## Alternatives considered

- Rely on review comments: reviewers miss them in large diffs, and the failure shows up in production.

## Consequences

Existing violations warn until the backlog is cleared. New code should not add more.

## Verification

Compile reads `eslint.json` and writes `eslint.config.mjs`. The check is in warn mode on `services/**`.
