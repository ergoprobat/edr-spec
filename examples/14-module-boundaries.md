---
edr: 1
id: 01M5C5QEHXR4BEBEVDRB5QS7N7
slug: module-boundaries
title: TypeScript modules honor the dependency graph
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-07-01
valid_to: null
review_by: 2027-01-01
supersedes: []
criticality: warning
checks:
  - engine: depcruise
    ref: .dependency-cruiser.cjs
    mode: warn
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/app/pull/51
tags: [architecture, javascript, boundaries]
---

# TypeScript modules honor the dependency graph

## Context

A UI package that imports a database client pulls server code into the browser bundle.

## Decision

The dependency-cruiser graph is the allowed import map for TypeScript packages.

## Alternatives considered

- A README diagram: the diagram is stale the week after it is drawn, and CI cannot see it.

## Consequences

Violations warn until the two known cycles are removed.

## Verification

`.dependency-cruiser.cjs` is the rule file, tagged for architecture, JavaScript, and boundaries.
