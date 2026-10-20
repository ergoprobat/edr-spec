---
edr: 1
id: 01M5C5QEHPQGJD3BHXB62GN0EE
slug: s3-sse-s3-allowed
title: SSE-S3 is enough for object storage
status: superseded
owner: team:security
scope:
  - org: acme
valid_from: 2025-06-01
valid_to: 2026-10-01
review_by: 2026-06-01
supersedes: []
criticality: warning
checks: []
waivers: []
sources:
  - type: adr
    url: https://github.com/acme/platform/blob/main/docs/decisions/0006-sse-s3.md
tags: [storage]
---

# SSE-S3 is enough for object storage

## Context

Early buckets used SSE-S3 because customer-managed keys were not available in the landing zone.

## Decision

SSE-S3 was accepted for object storage until customer-managed keys landed. This record is superseded.

## Alternatives considered

- Wait for customer-managed keys before storing anything: that blocked the first migration, which already had a date.

## Consequences

Buckets created under this record are not retroactively wrong. New buckets follow the successor.

## Verification

The successor is `s3-kms-cmk-required`. This file keeps the old decision for audit and sets `valid_to`.
