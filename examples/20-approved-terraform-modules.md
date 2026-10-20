---
edr: 1
id: 01M5C5QEJ3STMNY9HKDJARK8DA
slug: approved-terraform-modules
title: Terraform uses the approved module set
status: accepted
owner: team:platform
scope:
  - org: acme
    paths:
      - terraform/**
valid_from: 2026-09-15
valid_to: null
review_by: 2027-03-15
supersedes: []
criticality: blocking
checks:
  - engine: opa
    target: terraform-plan
    ref: policies/approved_modules.rego
    mode: block
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/platform/pull/90
tags: [iac, terraform, modules]
---

# Terraform uses the approved module set

## Context

Unpinned public modules change provider defaults under a plan that nobody re-read.

## Decision

Terraform roots instantiate modules only from the approved set.

## Alternatives considered

- Vendor the module and stop updating it: vendoring without a source pin still needs a review path for upstream fixes.

## Consequences

A plan that calls a module outside the set fails before apply.

## Verification

OPA policy `policies/approved_modules.rego` runs in block mode on the Terraform plan.
