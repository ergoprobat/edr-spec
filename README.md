# edr-spec

Open specification and JSON Schema for the ergo Decision Record (EDR) format.

> Status: Draft RFC 0.1.0. Normative text in [spec/edr-v0.1.md](spec/edr-v0.1.md). Schema `$id` is `https://ergoplatform.io/schema/edr/v0.1.json`.

The EDR format is the open record for a binding engineering decision: owner, scope, validity period and the check that verifies it. This repository is the standards process for that format. Prose and schema use different licenses, so the text can be republished and the schema can be embedded in Apache-2.0 implementations.

## What lives here

- [spec/edr-v0.1.md](spec/edr-v0.1.md): Draft RFC 0.1.0. A MADR or Nygard file without frontmatter is not an EDR document until an importer adds frontmatter.
- [schema/edr-v0.1.schema.json](schema/edr-v0.1.schema.json): JSON Schema for the frontmatter.
- [examples/](examples/): 21 positive fixtures. [conformance/invalid/](conformance/invalid/): negative fixtures. Each `.expect` file is the full error message, matched exactly. `tools/validate_examples.py` checks both in CI.

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

Follow the contributor terms in [ergoprobat/.github](https://github.com/ergoprobat/.github/blob/main/CONTRIBUTING.md). Commits need a `Signed-off-by` trailer (`git commit -s`).
