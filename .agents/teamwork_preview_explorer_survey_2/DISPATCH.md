## 2026-09-12T08:39:18Z

You are teamwork_preview_explorer_survey_2, Build System & QC Architecture Explorer.

Your working directory is:
`c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh\.agents\teamwork_preview_explorer_survey_2`

You MUST read the authoritative original request first:
`c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh\.agents\ORIGINAL_REQUEST.md`

Objective:
Investigate the build system, templates, and quality control gates:
1. Inspect `core/templates/build.js` and all associated scripts and schemas in `core/` and `templates/` (e.g. `core/templates/`, `core/schema/`, `core/qc/`, or similar paths in `c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh`).
2. Document the build command syntax, options, and behaviors:
   `node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..`
3. Document all 26 QC checks (15 Core QC + 11 User QC):
   - What does each check enforce? (schema, character count 95-115 chars/line, no hyphens/em-dashes, en-dash for dates, bold markers count, content density >= 4000 chars, exact 2-page fit, PDF size > 10KB, tool categories, numbers that matter).
4. Verify the rendering engine dependencies (e.g. WeasyPrint, Node packages) and whether any external tools or environments are needed.
5. Document potential failure modes and strict compliance requirements.

Deliverables:
Write detailed findings to `analysis.md` and a structured summary to `handoff.md` in your working directory `c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh\.agents\teamwork_preview_explorer_survey_2`.
Update `progress.md` with your status.
Send a completion message back to the orchestrator when finished.
