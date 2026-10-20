---
edr: 1
id: 01M5C5QEHJ3KBK15JT159AYDR3
slug: pin-base-images
title: Container base images must be pinned by digest
status: proposed
owner: team:platform
scope:
  - org: acme
valid_from: 2026-02-01
valid_to: null
review_by: 2026-08-01
supersedes: []
criticality: warning
checks: []
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/platform/pull/22
tags: [supply-chain]
---

# Container base images must be pinned by digest

## Context

Floating tags such as `latest` change the bytes a build runs without a review of that change.

## Decision

Dockerfiles and Kubernetes manifests pin third-party base images by digest.

## Alternatives considered

- Pin by version tag only: tags can be moved, so the bytes are still not the ones that were reviewed.

## Consequences

Renovate or a similar bot must open digest bumps. Builds fail closed once a check is attached.

## Verification

This record is still proposed, so the check is not written yet. Review confirms the digest rule before it is accepted.
