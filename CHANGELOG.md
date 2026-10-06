# Changelog

## SH-1.2 (1 October 2026)

DOI: [10.5281/zenodo.23181969](https://doi.org/10.5281/zenodo.23181969)

SH numbers identify editions of the standard. A minor-number increment does not promise schema or behavioural compatibility; validate each declaration with the schema for its stated version (Technical Specification §11).

### Standard

- Participation without a declaration: assisted declarations and an accessible human route replace automatic rejection in Modes 3 and 4. Missing information never supplies permission (§§1.2, 3.7).
- Company readiness: customer authority is distinguished from company access policies, with three illustrative handling routes (§1.4).
- Two conformance profiles: Participation and Verified authority (§§3.8, 9.1).
- AI disclosure at first contact; assisted declarations record provenance and confirmation (§§3.7, 4).
- Confirmation cannot grant authority; irreversible actions need independently verifiable delegation or approval (§3.6).
- Resolution compatibility: a refused option no longer blocks an acceptable alternative (§5.3).
- Service-purpose data limits apply throughout the interaction (§3.3).
- Safeguarding covers concerns relayed by agents, cannot be waived, and restrictions survive handover and new contacts (§3.4).
- Corrected and qualified external claims; added Meta Muse, Amazon and UK regulatory context (§§1.1, 1.4, 7, 8).
- The separate vulnerability module remains deferred; baseline safeguards apply.

### Technical Specification

- New metadata: `declaration_id`, `declaration_revision`, `declaration_provenance`, `disclosure`, `confirmation`, `unresolved_fields` (§2.3).
- Explicit empty values are allowed and never grant permission; `trust_levels` is optional and the 0.85 recommendation is withdrawn (§§3–5).
- Baseline harm indicators, relayed concerns, handover and cross-contact restrictions (§§6.3–6.5).
- Authority verification, execution boundary, financial limits and private internal limits (§§8.3–8.7).
- Resolution compatibility with allow, deny, hold and escalate decisions (§9.3).
- Security considerations and conformance requirements (§§13, 14).
- Appendix A: core action vocabulary and material terms; extensions use an organisation-controlled namespace.

### Machine-readable files

- New `sh-1.2.schema.json` (`urn:neoswave:service-handshake:sh-1.2:draft-1:declaration`).
- New `sh-1.2.action-assessment.schema.json` (`urn:neoswave:service-handshake:sh-1.2:draft-1:assessment`).
- Publication examples and structural tests; schema definitions and identifiers are retained from review, as specified in Technical Specification §12.
- Schemas, examples and tests are licensed under the Apache License 2.0; documents remain CC BY 4.0.

## SH-1.1 (March 2026)

DOI: [10.5281/zenodo.19046746](https://doi.org/10.5281/zenodo.19046746). Files retained unchanged in this repository.
