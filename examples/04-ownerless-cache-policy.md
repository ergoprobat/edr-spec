---
edr: 1
id: 01M5C5QEHMATM981RGBG5WHSW3
slug: ownerless-cache-policy
title: Shared caches need an explicit eviction policy
status: needs-review
owner: team:platform
scope:
  - org: acme
valid_from: 2025-11-01
valid_to: null
review_by: 2026-05-01
supersedes: []
criticality: advisory
checks: []
waivers: []
sources:
  - type: spec
    url: https://github.com/acme/platform/blob/main/docs/cache.md
tags: [cache]
---

# Shared caches need an explicit eviction policy

## Context

A shared cache without an eviction policy grows until it pages, and nobody can say which keys are safe to drop.

## Decision

Every shared cache documents its eviction policy and its memory cap.

## Alternatives considered

- Rely on the engine default: defaults differ by engine, so two caches that look the same fail differently.

## Consequences

The review date has passed and no check is attached, so the record stays in needs-review until the owner confirms it.

## Verification

Confirmation is a human review. No deterministic check is attached yet.
