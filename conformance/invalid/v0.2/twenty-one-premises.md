---
edr: 1
id: 01M5C5QEHHNXJ3D7X2ZCMGXQT7
slug: tls-on-public-ingress
title: Public ingress must terminate TLS
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-01-15
valid_to: null
review_by: 2026-07-15
supersedes: []
criticality: blocking
checks: []
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/platform/pull/10
tags: [tls]
premises:
  - id: fact-01
    statement: Fact 01 still holds.
    every: 30
    probe:
      url: https://example.com/facts/01.json
      pointer: /value
      equals: true
  - id: fact-02
    statement: Fact 02 still holds.
    every: 30
    probe:
      url: https://example.com/facts/02.json
      pointer: /value
      equals: true
  - id: fact-03
    statement: Fact 03 still holds.
    every: 30
    probe:
      url: https://example.com/facts/03.json
      pointer: /value
      equals: true
  - id: fact-04
    statement: Fact 04 still holds.
    every: 30
    probe:
      url: https://example.com/facts/04.json
      pointer: /value
      equals: true
  - id: fact-05
    statement: Fact 05 still holds.
    every: 30
    probe:
      url: https://example.com/facts/05.json
      pointer: /value
      equals: true
  - id: fact-06
    statement: Fact 06 still holds.
    every: 30
    probe:
      url: https://example.com/facts/06.json
      pointer: /value
      equals: true
  - id: fact-07
    statement: Fact 07 still holds.
    every: 30
    probe:
      url: https://example.com/facts/07.json
      pointer: /value
      equals: true
  - id: fact-08
    statement: Fact 08 still holds.
    every: 30
    probe:
      url: https://example.com/facts/08.json
      pointer: /value
      equals: true
  - id: fact-09
    statement: Fact 09 still holds.
    every: 30
    probe:
      url: https://example.com/facts/09.json
      pointer: /value
      equals: true
  - id: fact-10
    statement: Fact 10 still holds.
    every: 30
    probe:
      url: https://example.com/facts/10.json
      pointer: /value
      equals: true
  - id: fact-11
    statement: Fact 11 still holds.
    every: 30
    probe:
      url: https://example.com/facts/11.json
      pointer: /value
      equals: true
  - id: fact-12
    statement: Fact 12 still holds.
    every: 30
    probe:
      url: https://example.com/facts/12.json
      pointer: /value
      equals: true
  - id: fact-13
    statement: Fact 13 still holds.
    every: 30
    probe:
      url: https://example.com/facts/13.json
      pointer: /value
      equals: true
  - id: fact-14
    statement: Fact 14 still holds.
    every: 30
    probe:
      url: https://example.com/facts/14.json
      pointer: /value
      equals: true
  - id: fact-15
    statement: Fact 15 still holds.
    every: 30
    probe:
      url: https://example.com/facts/15.json
      pointer: /value
      equals: true
  - id: fact-16
    statement: Fact 16 still holds.
    every: 30
    probe:
      url: https://example.com/facts/16.json
      pointer: /value
      equals: true
  - id: fact-17
    statement: Fact 17 still holds.
    every: 30
    probe:
      url: https://example.com/facts/17.json
      pointer: /value
      equals: true
  - id: fact-18
    statement: Fact 18 still holds.
    every: 30
    probe:
      url: https://example.com/facts/18.json
      pointer: /value
      equals: true
  - id: fact-19
    statement: Fact 19 still holds.
    every: 30
    probe:
      url: https://example.com/facts/19.json
      pointer: /value
      equals: true
  - id: fact-20
    statement: Fact 20 still holds.
    every: 30
    probe:
      url: https://example.com/facts/20.json
      pointer: /value
      equals: true
  - id: fact-21
    statement: Fact 21 still holds.
    every: 30
    probe:
      url: https://example.com/facts/21.json
      pointer: /value
      equals: true
---

# Public ingress must terminate TLS

## Context

Public entry points that still speak plain HTTP expose tokens and session cookies on the path.

## Decision

Every public ingress terminates TLS. Plain HTTP on a public listener only redirects to HTTPS.

## Alternatives considered

- Keep HTTP for public health checks: those checks do not need a public listener, and a redirect covers browsers.

## Consequences

Clients trust the platform certificate. Private health checks stay off the public port.

## Verification

A listener on port 80 that does not redirect fails review until a check exists for this record.
