---
edr: 1
id: 01M5C5QEHK8ASNYH0RJJ6V6Z40
slug: postgres-major-is-16
title: New datastores stay on PostgreSQL 16
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-03-01
valid_to: null
review_by: 2026-09-01
supersedes: []
criticality: warning
checks: []
waivers: []
sources:
  - type: spec
    url: https://example.com/platform/postgres.json
tags: [data]
premises:
  - id: postgres-major-is-16
    statement: The platform still runs PostgreSQL 16.
    every: 1
    probe:
      url: https://example.com/platform/postgres.json
      pointer: /major
      equals: 16
---

# New datastores stay on PostgreSQL 16

## Context

Backup, IAM, and client libraries are built for one major PostgreSQL release. A silent major change would strand those runbooks.

## Decision

A new datastore is PostgreSQL 16 until a superseding decision says otherwise. The premise records the fact that release is still the one in production.

## Alternatives considered

- Pin only the check, and leave the major unstated: the check can keep passing after the reason for the pin has changed.

## Consequences

Operators recheck the published major every day. A mismatch asks for review and does not block a merge.

## Verification

The premise compares `/major` in the published JSON document with `16`.
