---
edr: 1
id: 01M5C5QEHTDSV95MCRC4WY3JC7
slug: kyverno-run-as-non-root
title: Workloads in production run as non-root
status: accepted
owner: team:security
scope:
  - org: acme
    repo: acme/clusters
    paths:
      - clusters/**
    env:
      - prod
valid_from: 2026-05-20
valid_to: null
review_by: 2026-11-20
supersedes: []
criticality: blocking
checks:
  - engine: kyverno
    ref: policies/run-as-non-root.yaml
    mode: block
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/clusters/pull/12
tags: [kubernetes]
---

# Workloads in production run as non-root

## Context

A container that runs as root turns a single process bug into node compromise.

## Decision

Production workloads set `runAsNonRoot`. The image user is not root.

## Alternatives considered

- A pod security exception list checked by hand: the list drifts, and a new namespace misses it.

## Consequences

Images that need root must change user before this policy is enforced in the cluster.

## Verification

Kyverno policy `policies/run-as-non-root.yaml` rejects a production pod that does not set `runAsNonRoot`.
