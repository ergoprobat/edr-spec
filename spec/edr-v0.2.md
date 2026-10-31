# EDR v0.2

- Status: Draft RFC
- Version: 0.2.0
- Date: 2026-10-31
- License: CC-BY-4.0 (this text). The JSON Schema and the files under `examples/` and `conformance/` are Apache-2.0.

This document is the normative specification of the Engineering Decision Record (EDR) format at draft 0.2.0. An EDR file records one engineering decision: who owns it, where it applies, when it is in force, which check verifies it, and which premises it rests on. The file is Markdown with YAML frontmatter, and it is a superset of a MADR record.

The key `edr` is the format generation. Every 0.x draft uses `edr: 1`. That number is not the SemVer of this document.

## 1. Artifacts

| Artifact | Location |
| --- | --- |
| This text | `spec/edr-v0.2.md` |
| JSON Schema | `schema/edr-v0.2.schema.json` |
| Positive examples | `examples/` and `examples/v0.2/` |
| Negative fixtures | `conformance/invalid/` and `conformance/invalid/v0.2/` |

The schema `$id` is `https://ipsoplatform.io/schema/edr/v0.2.json`. That URI is the canonical name of this schema. The file in this repository is the artifact to validate against. This draft does not use `https://ipsoplatform.io/schema/edr/v1.json`. That URI is reserved for the 1.0.0 freeze.

Draft 0.1.0 is unchanged. Every document that validates against draft 0.1.0 also validates against this draft. A document that sets `premises` does not validate against draft 0.1.0. A later draft may stop accepting a 0.2.0 document. Breaking changes are allowed before 1.0.0. A breaking change bumps the draft and publishes a new schema file and a new `$id`.

## 2. Document shape

A valid EDR file is UTF-8 Markdown. It starts with a YAML frontmatter block delimited by a line that is exactly `---`, then the YAML mapping, then a line that is exactly `---`. The body follows that second marker.

The frontmatter MUST be a single YAML mapping whose keys are only the fields in section 4. Unknown keys are invalid. The mapping MUST include every required field, and it MAY include `inferred` and `premises`.

The body MUST contain exactly one level-1 heading. After that heading, the body MUST contain these level-2 headings, in this order, each exactly once, and each with at least one paragraph or list:

1. `Context`
2. `Decision`
3. `Alternatives considered`
4. `Consequences`
5. `Verification`

A conventional path is `docs/decisions/NNNN-slug.md`, where `NNNN` is a four-digit number and `slug` is the frontmatter slug. A repository MAY store EDR files on another path. This draft does not constrain the path.

A file with no frontmatter is not an EDR document. MADR and Nygard records without frontmatter become EDR documents only after an importer adds frontmatter. This draft does not specify that importer.

## 3. Validation

Validate the parsed frontmatter mapping, not the Markdown bytes, against `schema/edr-v0.2.schema.json` (JSON Schema draft 2020-12). YAML dates MUST be treated as ISO `YYYY-MM-DD` strings before validation. YAML `null` stays null. Premise ids MUST be unique within `premises`. An `equals` value MUST be at most 1024 bytes when encoded as UTF-8 JSON with no insignificant whitespace, using the key order of the file. JSON Schema draft 2020-12 does not express either rule, so a conforming validator checks both after the schema.

A validator conforms to draft 0.2.0 when every file in `examples/` and every file in `examples/v0.2/` passes, each file in `conformance/invalid/` fails with the same reason code recorded for draft 0.1.0, and each file in `conformance/invalid/v0.2/` fails with the reason code in its sibling `.expect` file. `examples/` is the draft 0.1.0 positive corpus, and it is valid here. `examples/v0.2/` is the premises positive corpus, and those files fail draft 0.1.0. `conformance/invalid/` is the shared negative corpus. `conformance/invalid/v0.2/` is the premises negative corpus. The `.expect` line is one reason code, matched in full: `frontmatter-start`, `frontmatter-close`, `frontmatter-mapping`, `additional-properties`, `status`, `owner`, `valid_to`, `scope`, `source-url`, `checks-empty`, `checks-deterministic`, `heading-order`, `missing-heading`, `duplicate-heading`, `one-h1`, `section-empty`, `premises`, or `premise-id`. `scope` covers a bad scope array and a bad item inside it. `premises` covers a bad premises array and a bad item inside it, including `every` outside 1 to 365, a statement outside 1 to 500 characters, more than 20 premises, a probe that does not have exactly one of `equals` or `semver`, an `equals` value over 1024 bytes, and a `semver` string the pattern rejects. `additional-properties` covers an unknown key at the root or inside an object. `premise-id` covers a repeated premise id. A different code does not conform. Each required level-2 heading appears once. A line that is exactly `---` is not a paragraph or a list, and after the frontmatter it stays in the body.

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

### 4.16 `premises`

Optional. Omit it, or set an array of at most 20 premise objects. An empty array and an omitted key both mean the decision records no premises. An array of 21 or more is invalid.

Each premise object requires `id`, `statement`, `every`, and `probe`. Unknown keys are invalid. `id` uses the same lowercase kebab-case as `slug` and MUST be unique within the array. `statement` is a string of 1 to 500 characters, counted as JSON Schema string length (Unicode code points). `every` is an integer from 1 to 365 inclusive, the interval in days at which a consumer rechecks the premise.

`probe` requires `url` and `pointer`, and exactly one of `equals` or `semver`. Unknown keys are invalid, including `script`, `header`, and `authorization`. A probe with both comparisons, or with neither, is invalid.

`url` matches `https://` followed by one or more non-whitespace characters, the same pattern as a source URL. This schema does not reject userinfo, a fragment, a port other than 443, or a host that is an IP address. An `https` URL with any of those is valid in this draft. This draft does not fetch the URL. A consumer that fetches the URL MUST take it verbatim and MUST refuse userinfo, a fragment, a host that is not a DNS name, a port other than 443, a redirect, and any resolved address that is not a public unicast address. It MUST send no cookies and no `Authorization` header. The time limit is 10 seconds and the body limit is 1 MiB. Those obligations are the probe rules in ADR-0053. They are not schema checks.

`pointer` is a JSON Pointer (RFC 6901). The empty pointer is valid and refers to the whole JSON document. A non-empty pointer is a sequence of `/` and reference tokens. `~` in a token is escaped as `~0`, and `/` in a token is escaped as `~1`.

`equals` is any JSON value. Keys inside that value are comparison data, not probe fields. The UTF-8 JSON encoding of that value, with no insignificant whitespace and with object keys in file order, MUST be at most 1024 bytes. `semver` is one string: an operator immediately followed by `MAJOR.MINOR.PATCH`, then an optional pre-release, with no space and no build metadata. The operator is `=`, `>`, `>=`, `<`, or `<=`. Each numeric identifier is `0` or a number without a leading zero. A pre-release is a hyphen and one or more dot-separated identifiers. `1.2.3+build` and `>=1.2.3 <2.0.0` are invalid. In YAML, quote a value that begins with `>`.

Changing a premise changes the decision version. A premise is not a check.

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

The body of that record is `examples/11-s3-kms-cmk-required.md`. It omits `premises`, so it has none. A record with one premise is `examples/v0.2/premise-equals.md`. A record whose premise uses `semver` is `examples/v0.2/premise-semver.md`.
