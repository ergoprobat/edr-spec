---
edr: 1
id: 01M5C5QEHQBK805ASAN1H5B7KM
slug: legacy-ftp-drop
title: Partners may upload over FTP
status: deprecated
owner: team:platform
scope:
  - org: acme
valid_from: 2024-01-01
valid_to: 2026-01-31
review_by: 2026-01-31
supersedes: []
criticality: advisory
checks: []
waivers: []
sources:
  - type: adr
    url: https://github.com/acme/platform/blob/main/docs/decisions/0007-ftp.md
tags: [transfer]
---

# Partners may upload over FTP

## Context

A partner integration used FTP because that was the only protocol they offered in 2024.

## Decision

The FTP drop is deprecated. No successor is required, because the partner moved to HTTPS uploads.

## Alternatives considered

- Keep FTP behind a bastion: the bastion still terminates a protocol the platform no longer operates.

## Consequences

The listener is gone. The record stays so an audit can show when the exception ended.

## Verification

Deprecation is recorded by `status` and `valid_to`. There is no replacement slug.
