# Plan: Harsh Goyal Founder's Office Generalist CV Build

## Objective
Build a publication-grade, ATS-compliant 2-page Generalist Founder's Office CV for Harsh Goyal, achieving 100% pass across all 26 QC checks (15 core + 11 user QC), zero hyphens/em-dashes, exact metric fidelity to proof bank, and seamless Entrepreneur archetype calibration.

## Phases

### Phase 1: Survey & Codebase Investigation
- Spawn 3 Explorers:
  - Explorer 1: Inspect `reference/profile.json`, `reference/proof-bank.md`, and `reference/bullet-library.json` for Naraina Jewellers, Entrepreneur archetype, and metric definitions.
  - Explorer 2: Inspect `core/templates/build.js`, QC rules (26 checks), and Schema v3 requirements.
  - Explorer 3: Inspect existing output examples (e.g. any existing `outputs/` directories) to identify templates, partial_config conventions, and common pitfalls.
- Synthesize findings into `PROJECT.md`.

### Phase 2: Archetype Calibration & Configuration Generation
- Dispatch Worker to:
  - Calibrate `reference/bullet-library.json` and `reference/profile.json` (if needed for Entrepreneur archetype, ensure Naraina Jewellers is primary with label `(0-to-1 Retail Venture)` and correct en-dashes).
  - Draft `outputs/founders_office_generalist/partial_config.json` adhering to SCHEMA_VERSION 3:
    - Role: `Founder's Office (Generalist & Operations)`
    - Company: `Target Venture`
    - Tagline & Summary: Compelling founder-lens narrative
    - 6 Role Pillars (5 bullets each, 95–115 chars/line, zero hyphens/em-dashes)
    - Tools (at least 8 tools in 3 categories)
    - Numbers That Matter (4 verified proof bank metrics)
- Verify line budget (95–115 characters per bullet) and character bans.

### Phase 3: Build Execution & Deterministic QC Verification
- Worker runs build command:
  `cd outputs/founders_office_generalist && node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..`
- Confirm all 26 QC checks pass (exit code 0).
- Confirm PDF generated: `Harsh_Goyal_Founders_Office_Generalist.pdf` with size > 10KB, content density >= 4000 chars, >= 40 bold markers, exact 2 pages.

### Phase 4: Independent Review, Challenge & Forensic Audit
- Spawn Reviewers (2) to verify ATS keywords, structure, and editorial elegance.
- Spawn Challengers (2) to run adversarial validation (character budget, regex for hyphens/em-dashes, page count).
- Spawn Forensic Auditor (`teamwork_preview_auditor`) to verify zero metric fabrication, strict proof-bank alignment, zero predecessor leaks.

### Phase 5: Final Presentation & Parent Notification
- Synthesize all findings in `GATE_STATUS.md` and `handoff.md`.
- Present final publication-grade summary and notify parent via `send_message`.
