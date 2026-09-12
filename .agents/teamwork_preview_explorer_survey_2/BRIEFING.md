# BRIEFING — 2026-09-12T08:50:00Z

## Mission
Investigate the build system, templates, and quality control gates in career-ops-harsh, documenting build command syntax/options, 26 QC checks (15 Core QC + 11 User QC), rendering engine dependencies, failure modes, and compliance requirements.

## 🔒 My Identity
- Archetype: explorer
- Roles: Build System & QC Architecture Explorer
- Working directory: c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh\.agents\teamwork_preview_explorer_survey_2
- Original parent: 99a58e74-df31-4ec2-a316-653403292618
- Milestone: Build System & QC Architecture Exploration

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Inspect files and document findings thoroughly
- Only write within working directory .agents/teamwork_preview_explorer_survey_2

## Current Parent
- Conversation ID: 99a58e74-df31-4ec2-a316-653403292618
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh\.agents\ORIGINAL_REQUEST.md`
  - `core/templates/build.js`, `assemble_config.js`, `engine.js`, `cv_weasyprint_template.js`, `weasyprint_env.js`
  - `core/templates/qc_core_checks.js`, `qc_user_checks.js`, `qc_20_checks.js`, `config_defaults.json`
  - `reference/qc-rules.json`, `bullet-library.json`, `profile.json`, `proof-bank.md`, `archetypes.md`
  - `core/agents/lint.js`, `challenger-gate.ts`, `schemas/`
  - `outputs/ops_category_manager/` (verified 2-page PDF, partial_config.json, config.json)
- **Key findings**:
  - Build command: `node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..`
  - `--data-root ../..` is required when running from `outputs/<role_slug>` to locate workspace `reference/`.
  - 26 QC checks decoded: 15 Universal Core QC + 11 Candidate User QC.
  - Environment verified: Python 3.14.6, Node v24.15.0, WeasyPrint 69.0, PyPDF2 3.0.1, Pango 15800.
  - Failure modes mapped: widow zone (116–179 chars), hyphens/em-dashes in dynamic content, date hyphen-minus, page count mismatch, unverified tokens in Claims Linter.
- **Unexplored areas**: None. Exploration fully complete.

## Key Decisions Made
- Authored detailed `analysis.md` documenting build pipeline, all 26 QC checks, rendering architecture, and failure modes.
- Authored 5-component `handoff.md`.
- Ready to report back to orchestrator.

## Artifact Index
- DISPATCH.md — Record of inbound dispatches
- BRIEFING.md — Situational awareness index
- progress.md — Task progress & heartbeat
- analysis.md — Deep investigation findings
- handoff.md — Structured handoff report
