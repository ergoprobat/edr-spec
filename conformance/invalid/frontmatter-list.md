---
- not a mapping
---

# Public ingress must terminate TLS

## Context

The frontmatter is a list.

## Decision

Every public ingress terminates TLS.

## Alternatives considered

- A mapping: that is what the format requires.

## Consequences

The file is rejected.

## Verification

The checker reports frontmatter-mapping.
