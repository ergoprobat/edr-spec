# edr-spec

Open specification and JSON Schema for the ergo Decision Record (EDR) format.

> Status: skeleton. The specification draft, JSON Schema and conformance corpus land in a later change.

The EDR format is the open record for a binding engineering decision: owner, scope, validity period and the check that verifies it. This repository is the standards process for that format. Prose and schema use different licenses, so the text can be republished and the schema can be embedded in Apache-2.0 implementations.

## What will live here

- Versioned specification prose, including a migration guide from MADR and Nygard ADRs
- JSON Schema for the format
- A conformance corpus of positive and negative fixtures

## License

| Material | License | Text |
| --- | --- | --- |
| Specification prose, including this README | CC-BY-4.0 | [LICENSE-CC-BY](LICENSE-CC-BY) |
| JSON Schema and the conformance corpus | Apache-2.0 | [LICENSE-APACHE](LICENSE-APACHE) |

[LICENSE](LICENSE) states the split. Copyright 2026 Luca Bertelli.

## Contributing

Follow the contributor terms in [ergoprobat/.github](https://github.com/ergoprobat/.github/blob/main/CONTRIBUTING.md). Commits need a `Signed-off-by` trailer (`git commit -s`).
