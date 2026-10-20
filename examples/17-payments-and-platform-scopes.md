---
edr: 1
id: 01M5C5QEJ0Z1GGY05MEQ0245A8
slug: payments-prod-logging
title: Payment production logs omit card data
status: accepted
owner: team:security
scope:
  - org: acme
  - org: acme
    repo: acme/payments
    env:
      - prod
valid_from: 2026-08-15
valid_to: null
review_by: 2027-02-15
supersedes: []
criticality: blocking
checks:
  - engine: opa
    target: application-log
    ref: policies/no_pan.rego
    mode: block
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/payments/pull/3
tags: [payments, privacy]
---

# Payment production logs omit card data

## Context

A primary account number in a production log is a disclosure, even when the log store is private.

## Decision

Payment services do not write a primary account number to production logs. The rule applies to the whole org and, again, to `acme/payments` in production.

## Alternatives considered

- Mask all but the last four digits: the remaining digits are still card data, and logs are not a display surface.

## Consequences

Two scope objects record the org-wide rule and the production payments repository.

## Verification

OPA policy `policies/no_pan.rego` blocks a log line that matches a primary account number.
