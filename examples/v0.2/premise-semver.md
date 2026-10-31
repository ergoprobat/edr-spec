---
edr: 1
id: 01M5C5QEHK8ASNYH0RJJ6V6Z41
slug: postgres-at-least-16
title: PostgreSQL clients require at least 16.0.0
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-03-01
valid_to: null
review_by: 2027-03-01
supersedes: []
criticality: warning
checks: []
waivers: []
sources:
  - type: spec
    url: https://example.com/platform/postgres.json
tags: [data]
premises:
  - id: postgres-at-least-16
    statement: Production PostgreSQL is at least 16.0.0.
    every: 365
    probe:
      url: https://example.com/platform/postgres.json
      pointer: /version
      semver: ">=16.0.0"
---

# PostgreSQL clients require at least 16.0.0

## Context

Client libraries in this estate use features that landed in PostgreSQL 16. An older server would fail those calls at runtime.

## Decision

The decision stands while the published server version is greater than or equal to 16.0.0. The premise records that version constraint.

## Alternatives considered

- Compare the version with `equals`: a patch release would look like a changed fact even when the decision still holds.

## Consequences

Operators recheck the published version once a year. A mismatch asks for review and does not block a merge.

## Verification

The premise compares `/version` in the published JSON document with the constraint `>=16.0.0`.
