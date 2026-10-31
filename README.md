# edr-spec

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/ipsofacto-io/edr-spec/badge)](https://scorecard.dev/viewer/?uri=github.com/ipsofacto-io/edr-spec)

Open specification and JSON Schema for the Engineering Decision Record (EDR) format.

> Status: Draft RFC 0.2.0. Normative text in [spec/edr-v0.2.md](spec/edr-v0.2.md). Schema `$id` is `https://ipsoplatform.io/schema/edr/v0.2.json`. Draft RFC 0.1.0 remains published at [spec/edr-v0.1.md](spec/edr-v0.1.md) and `https://ipsoplatform.io/schema/edr/v0.1.json`.

The EDR format is the open record for a binding engineering decision: owner, scope, validity period, the check that verifies it, and the premises it rests on. This repository is the standards process for that format. Prose and schema use different licenses, so the text can be republished and the schema can be embedded in Apache-2.0 implementations.

## What lives here

- [spec/edr-v0.2.md](spec/edr-v0.2.md): Draft RFC 0.2.0. Optional `premises`. A file that validates against 0.1.0 also validates against 0.2.0. A MADR or Nygard file without frontmatter is not an EDR document until an importer adds frontmatter.
- [spec/edr-v0.1.md](spec/edr-v0.1.md): Draft RFC 0.1.0, unchanged. It has no `premises` key.
- [schema/edr-v0.2.schema.json](schema/edr-v0.2.schema.json) and [schema/edr-v0.1.schema.json](schema/edr-v0.1.schema.json): JSON Schema for each draft's frontmatter.
- [examples/](examples/): 21 positive fixtures, valid for both drafts. [examples/v0.2/](examples/v0.2/): premises fixtures, valid for 0.2.0 only. [conformance/invalid/](conformance/invalid/): negative fixtures for both drafts. [conformance/invalid/v0.2/](conformance/invalid/v0.2/): premises negatives. Each `.expect` file is one stable reason code from section 3 of the draft, matched exactly. `tools/validate_examples.py` checks both drafts in CI.

An external implementer runs the suite with:

```bash
python -m pip install --disable-pip-version-check PyYAML==6.0.3 jsonschema==4.26.0
python3 tools/validate_examples.py
```

## License

| Material | License | Text |
| --- | --- | --- |
| Specification prose, including this README | CC-BY-4.0 | [LICENSE-CC-BY](LICENSE-CC-BY) |
| JSON Schema and the conformance corpus | Apache-2.0 | [LICENSE-APACHE](LICENSE-APACHE) |

[LICENSE](LICENSE) states the split. Copyright 2026 Luca Bertelli.

## Contributing

Follow the contributor terms in [ipsofacto-io/.github](https://github.com/ipsofacto-io/.github/blob/main/CONTRIBUTING.md). Commits need a `Signed-off-by` trailer (`git commit -s`).
