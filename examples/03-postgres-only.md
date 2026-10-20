---
edr: 1
id: 01M5C5QEHK8ASNYH0RJJ6V6Z3Z
slug: postgres-only
title: New datastores are PostgreSQL
status: verified
owner: team:platform
scope:
  - org: acme
valid_from: 2026-03-01
valid_to: null
review_by: 2026-09-01
supersedes: []
criticality: blocking
checks:
  - engine: opa
    target: terraform-plan
    ref: policies/postgres_only.rego
    mode: block
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/platform/pull/40
tags: [data]
---

# New datastores are PostgreSQL

## Context

Each extra datastore engine adds backup, IAM, and on-call work the platform team does not staff.

## Decision

A new datastore is PostgreSQL. Another engine needs a superseding decision.

## Alternatives considered

- Allow one cache engine per team: caches still need backups and network policy, and they spread the operational load.

## Consequences

Terraform plans that create a non-PostgreSQL database fail before apply.

## Verification

The OPA policy `policies/postgres_only.rego` runs in block mode on the Terraform plan.
