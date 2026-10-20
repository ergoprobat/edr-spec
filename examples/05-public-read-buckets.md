---
edr: 1
id: 01M5C5QEHN3Q5G08RVHYRX0HW8
slug: public-read-buckets
title: Allow public-read buckets for static sites
status: rejected
owner: team:security
scope:
  - org: acme
valid_from: 2026-04-01
valid_to: null
review_by: 2026-10-01
supersedes: []
criticality: blocking
checks: []
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/platform/pull/55
tags: [storage]
---

# Allow public-read buckets for static sites

## Context

A proposal asked for public-read object storage so static sites could skip the CDN.

## Decision

The proposal is rejected. Static sites publish through the CDN, and buckets stay private.

## Alternatives considered

- Public-read with a naming prefix: prefixes are not an access boundary, and a wrong prefix publishes data.

## Consequences

The declined proposal stays in the record so a later change cannot treat silence as approval.

## Verification

Rejection is the record. There is no check, because the decision does not allow the access.
