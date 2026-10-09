# The Service Handshake

An open interaction standard for service interactions where one or more parties are represented by AI agents.

**Current edition: SH-1.2 — 1 October 2026**

- First published 16 March 2026 (SH-1.1). DOI: [10.5281/zenodo.19046746](https://doi.org/10.5281/zenodo.19046746)
- Current version SH-1.2, published 1 October 2026. DOI: [10.5281/zenodo.23181969](https://doi.org/10.5281/zenodo.23181969)

The Markdown documents reproduce the publication PDFs; only presentation has been adapted for GitHub.

## Read the standard

| File | Contents |
|---|---|
| [THE-SERVICE-HANDSHAKE-v1.2.md](THE-SERVICE-HANDSHAKE-v1.2.md) | The complete main paper |
| [TECHNICAL-SPECIFICATION-v1.2.md](TECHNICAL-SPECIFICATION-v1.2.md) | The complete companion technical specification |
| [CHANGELOG.md](CHANGELOG.md) | Key changes from SH-1.1 |
| [sh-1.2.schema.json](sh-1.2.schema.json) | Declaration schema |
| [sh-1.2.action-assessment.schema.json](sh-1.2.action-assessment.schema.json) | Action-assessment schema |
| [examples/](examples/) | Illustrative declarations and assessment records |
| [tests/](tests/) | Structural acceptance and rejection tests |

SH-1.2 adds assisted participation, AI disclosure, independently checkable authority, service-purpose data limits, safeguarding and restrictions that survive human handover. It assesses the proposed resolution against both parties' boundaries. See the papers for the full requirements and evidence limits.

The SH-1.1 documents and schema remain available unchanged. Files in `docs/` describe an earlier illustrative Mode 4 simulation; they are not SH-1.2 implementation guidance.

## Schemas and structural tests

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests
```

Validate declarations against their stated version. As Technical Specification §12 explains, the SH-1.2 schemas retain their review identifiers (`urn:neoswave:service-handshake:sh-1.2:draft-1:declaration` and `urn:neoswave:service-handshake:sh-1.2:draft-1:assessment`). These identifiers do not imply a hosted schema endpoint.

The tests check JSON structure and example consistency. They do not authenticate evidence or test real execution controls. Schema acceptance does not establish conformance or permission to act.

## Conformance claims

A public claim must identify the version, profile (Participation or Verified authority), use cases and actions covered. A badge may link to that scope statement and must not imply assurance beyond it. See main paper §9.1 and Technical Specification §14.

## Citation and licences

McCann, M. (2026). *The Service Handshake* (Version 1.2). Neos Wave Ltd. https://doi.org/10.5281/zenodo.23181969

Documents and the SH-1.1 schema use CC BY 4.0; see [LICENSE-docs](LICENSE-docs). SH-1.2 schemas, examples and tests use Apache 2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). The Service Handshake name, logo and badges are not licensed under those licences. Adaptations must be identified as modified and must not be presented as an official edition or as endorsed by Neos Wave.

Contributions should identify the version tested, method, failures and proposed corrections. Open an issue or contact [Neos Wave](https://neoswave.com).
