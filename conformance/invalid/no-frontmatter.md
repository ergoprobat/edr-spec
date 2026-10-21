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
