---
edr: 1
id: 01M5C5QEJ16AE9QADJWJJN6490
slug: replace-legacy-ftp
title: Partner uploads use HTTPS
status: accepted
owner: team:platform
scope:
  - org: acme
valid_from: 2026-02-01
valid_to: null
review_by: 2026-08-01
supersedes: [legacy-ftp-drop, ownerless-cache-policy]
criticality: blocking
checks: []
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/platform/pull/80
tags: [transfer]
---

# Partner uploads use HTTPS

## Context

The FTP drop is deprecated, and the cache-policy record no longer describes how partners deliver files.

## Decision

Partners upload over HTTPS. This record replaces `legacy-ftp-drop` and `ownerless-cache-policy`.

## Alternatives considered

- SFTP on the old host: that keeps a second file-transfer stack for one partner.

## Consequences

`supersedes` lists both older slugs. The FTP listener is not part of the new path.

## Verification

No check is attached yet. The replacement is the HTTPS upload endpoint named in the pull request.
