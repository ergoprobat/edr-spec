# EDR v0.1

- Status: Draft RFC
- Version: 0.1.0
- Date: 2026-10-20
- License: CC-BY-4.0 (this text). The JSON Schema and the files under `examples/` and `conformance/` are Apache-2.0.

This document is the normative specification of the ergo Decision Record (EDR) format at draft 0.1.0. An EDR file records one engineering decision: who owns it, where it applies, when it is in force, and which check verifies it. The file is Markdown with YAML frontmatter, and it is a superset of a MADR record.

The key `edr` is the format generation. Every 0.x draft uses `edr: 1`. That number is not the SemVer of this document.

## 1. Artifacts

| Artifact | Location |
| --- | --- |
| This text | `spec/edr-v0.1.md` |
| JSON Schema | `schema/edr-v0.1.schema.json` |
| Positive examples | `examples/` |
| Negative fixtures | `conformance/invalid/` |

The schema `$id` is `https://ergoplatform.io/schema/edr/v0.1.json`. That URI is the canonical name of this schema. The file in this repository is the artifact to validate against. This draft does not use `https://ergoplatform.io/schema/edr/v1.json`. That URI is reserved for the 1.0.0 freeze. The host `ergo.dev` is not a name of this schema.

Breaking changes are allowed before 1.0.0. A breaking change bumps the draft and publishes a new schema file and a new `$id`. A document that validates against 0.1.0 is not required to validate against a later draft.

## 2. Document shape

A valid EDR file is UTF-8 Markdown. It starts with a YAML frontmatter block delimited by a line that is exactly `---`, then the YAML mapping, then a line that is exactly `---`. The body follows that second marker.

The frontmatter MUST be a single YAML mapping whose keys are only the fields in section 4. Unknown keys are invalid. The mapping MUST include every required field, and it MAY include `inferred`.

The body MUST contain exactly one level-1 heading. After that heading, the body MUST contain these level-2 headings, in this order, each exactly once, and each with at least one paragraph or list:

1. `Context`
2. `Decision`
3. `Alternatives considered`
4. `Consequences`
5. `Verification`

A conventional path is `docs/decisions/NNNN-slug.md`, where `NNNN` is a four-digit number and `slug` is the frontmatter slug. A repository MAY store EDR files on another path. This draft does not constrain the path.

A file with no frontmatter is not an EDR document. MADR and Nygard records without frontmatter become EDR documents only after an importer adds frontmatter. This draft does not specify that importer.

## 3. Validation

Validate the parsed frontmatter mapping, not the Markdown bytes, against `schema/edr-v0.1.schema.json` (JSON Schema draft 2020-12). YAML dates MUST be treated as ISO `YYYY-MM-DD` strings before validation. YAML `null` stays null.

A validator conforms to draft 0.1.0 when every file in `examples/` passes and each file in `conformance/invalid/` fails with the reason code in its sibling `.expect` file. `examples/` is the positive corpus. `conformance/invalid/` is the negative corpus. The `.expect` line is one reason code, matched in full: `frontmatter-start`, `additional-properties`, `status`, `owner`, `valid_to`, `scope`, `source-url`, `checks-empty`, `checks-deterministic`, `heading-order`, `missing-heading`, `duplicate-heading`, `one-h1`, or `section-empty`. A different code does not conform. Each required level-2 heading appears once. A line that is exactly `---` is not a paragraph or a list, and after the frontmatter it stays in the body.

## 4. Frontmatter fields

### 4.1 `edr`

Required. Integer, always `1` in this draft.

### 4.2 `id`

Required. A ULID: 26 characters from Crockford base32 (`0-9`, `A-H`, `J-K`, `M-N`, `P-T`, `V-Z`, excluding `I`, `L`, `O`, and `U`). The first character is `0` through `7`. The value is an opaque stable identifier. Do not derive it from the slug.

### 4.3 `slug`

Required. Lowercase kebab-case: words of `a-z` and `0-9`, separated by single hyphens. The slug is stable across status changes. A superseding decision uses a new slug.

### 4.4 `title`

Required. One non-empty line of human-readable text. The level-1 heading SHOULD match the title.

### 4.5 `status`

Required. One of:

| Status | Meaning |
| --- | --- |
| `proposed` | Waiting for approval |
| `accepted` | Approved. No deterministic check is enforcing it yet |
| `verified` | At least one deterministic check enforces it |
| `needs-review` | Stale, missing an owner, failing its check, or past `review_by` |
| `rejected` | Declined, and kept so the decline stays auditable |
| `superseded` | Replaced. `valid_to` MUST be a date |
| `deprecated` | Withdrawn with no successor required |

These tokens use hyphens. They are the file vocabulary. A product may show different words in a user interface. Those display words are not valid `status` values.

`verified` MUST include at least one check whose `engine` is not `llm-advisory`.

### 4.6 `owner`

Required. A team reference matching `team:` plus a lowercase kebab-case name, such as `team:platform`. The owner is a team, not a person.

### 4.7 `scope`

Required. A non-empty array of scope objects. Each object has at least one of `org`, `repo`, `paths`, and `env`. Unknown keys are invalid.

- `org` and `repo` are non-empty strings. `repo` MAY be a glob, such as `acme/infra-*`.
- `paths` and `env` are non-empty arrays of non-empty strings.

How a selector matches a repository, path, or environment is product behavior. This draft constrains the shape only. One scope object MAY set only `org`.

### 4.8 `valid_from`, `valid_to`, `review_by`

Required. `valid_from` and `review_by` are dates (`YYYY-MM-DD`). `valid_to` is a date or `null`. `null` means the decision has no end date. When `status` is `superseded`, `valid_to` MUST be a date.

`valid_from` and `valid_to` are valid time: when the decision binds the world. They are not the time the file was written.

### 4.9 `supersedes`

Required. An array of slugs, possibly empty. Each slug is a decision this record replaces. The field points backward, from the successor to the older slug. A record whose own `status` is `superseded` MAY leave `supersedes` empty. The successor lists the old slug.

### 4.10 `criticality`

Required. One of `blocking`, `warning`, or `advisory`.

### 4.11 `checks`

Required. An array of check objects, possibly empty. An empty array means nothing verifies the decision yet.

Each check object requires `engine` and MAY set `target`, `ref`, `job`, and `mode`. Unknown keys are invalid. An implementation ignores optional keys that do not apply to that engine.

`engine` is one of: `opa`, `semgrep`, `archunit`, `depcruise`, `checkov`, `kyverno`, `eslint`, `importlinter`, `ci-binding`, `llm-advisory`.

`mode` is one of `block`, `warn`, or `advise`. `llm-advisory` is not a deterministic check.

`target` and `ref` name the subject and the rule artifact. `job` names an existing CI job that supplies evidence (`ci-binding`).

### 4.12 `waivers`

Required. An array of waiver objects, possibly empty. A waiver object requires `reason`, `approver`, `valid_from`, and `valid_to`. All four are non-empty strings except the two dates, which are `YYYY-MM-DD`. `valid_to` on a waiver is a date, not null. `approver` MAY be a person or a team reference. Unknown keys are invalid.

### 4.13 `sources`

Required. A non-empty array of source objects. Each object requires `type` (a non-empty string, such as `pr`, `spec`, or `adr`) and `url` (an `https` URI). Unknown keys are invalid.

### 4.14 `tags`

Required. An array of kebab-case strings, possibly empty.

### 4.15 `inferred`

Optional boolean. Omit it, or set `false`, when a person wrote every value. An importer sets `true` when it invented a value that was not in the source document. Absence means `false`.

## 5. Minimal document

```yaml
---
edr: 1
id: 01JAB3K9ZQ7Y6T0V5M8W2E4R1N
slug: s3-kms-cmk-required
title: S3 buckets in production must use KMS customer-managed keys
status: accepted
owner: team:platform
scope:
  - org: acme
    repo: acme/infra-*
    paths: ["terraform/**"]
    env: [prod]
valid_from: 2026-11-01
valid_to: null
review_by: 2027-05-01
supersedes: [s3-sse-s3-allowed]
criticality: blocking
checks:
  - engine: opa
    target: terraform-plan
    ref: policies/s3_kms.rego
  - engine: ci-binding
    job: checkov / CKV_AWS_145
waivers: []
sources:
  - type: pr
    url: https://github.com/acme/infra/pull/812
tags: [security, dora-art9]
---
```

The body of that record is `examples/11-s3-kms-cmk-required.md`.
