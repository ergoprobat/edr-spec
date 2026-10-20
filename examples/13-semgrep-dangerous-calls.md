---
edr: 1
id: 01M5C5QEHW8KEP1SQDM9702PJE
slug: semgrep-dangerous-calls
title: Application code must not call a shell with a string
status: proposed
owner: team:security
scope:
  - org: acme
valid_from: 2026-06-15
valid_to: null
review_by: 2026-12-15
supersedes: []
criticality: warning
checks:
  - engine: semgrep
    ref: rules/no-shell-string.yaml
    mode: warn
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/app/pull/44
  - type: spec
    url: https://github.com/acme/app/blob/main/docs/security.md
tags: [security]
---

# Application code must not call a shell with a string

## Context

A shell invoked with one string interpolates untrusted input as code.

## Decision

Application code does not pass a single string to a shell. Argument arrays are the allowed form. This record is still proposed.

## Alternatives considered

- An allowlist of commands: the allowlist does not stop the shell from parsing metacharacters inside an argument.

## Consequences

Semgrep warns on the current pattern. Promotion to block waits until the existing calls are gone.

## Verification

Rule `rules/no-shell-string.yaml` runs in warn mode. The proposal links both the pull request and the security note.
