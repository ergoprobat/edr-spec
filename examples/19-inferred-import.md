---
edr: 1
id: 01M5C5QEJ21R2PZAAC1NKVBWDG
slug: pin-github-actions
title: GitHub Actions must be pinned
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-09-01
valid_to: null
review_by: 2027-03-01
supersedes: []
criticality: warning
checks: []
waivers: []
sources:
  - type: adr
    url: https://github.com/acme/platform/blob/main/docs/adr/0019-pin-actions.md
tags: [supply-chain]
inferred: true
---

# GitHub Actions must be pinned

## Context

This record was imported from a MADR file that had a title and a decision and no owner. The importer filled the missing fields and set `inferred` to true.

## Decision

Workflows pin third-party actions to a commit SHA.

## Alternatives considered

- Pin to a major version tag: the tag can move, so the reviewed commit is not the commit that runs.

## Consequences

A reviewer still confirms the inferred owner and dates before this record is treated as written by a person.

## Verification

Import marked the file. A check is not attached yet.
