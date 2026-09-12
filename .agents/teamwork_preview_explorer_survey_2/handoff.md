# Handoff Report: Build System & QC Architecture Investigation

**Agent**: `teamwork_preview_explorer_survey_2`  
**Role**: Build System & QC Architecture Explorer  
**Date**: 2026-09-12  
**Target File**: `handoff.md`  

---

## 1. Observation

1. **Build Entry Point & Core Pipeline (`core/templates/build.js:1-313`)**:
   - `build.js` requires CLI flags `--in <path>` and `--archetype <name>` (`build.js:34-38`).
   - `resolveDataRoot(params['data-root'], templatesDir)` (`build.js:58-73`) resolves the candidate data root. When invoked from `outputs/<role_slug>`, passing `--data-root ../..` is required to access `reference/bullet-library.json` and `reference/qc-rules.json`.
   - The build process executes 5 sequential steps:
     - **Step 1 (Assemble Config)**: Merges defaults, `reference/profile.json`, `partial_config.json`, and frozen bullets from `reference/bullet-library.json[archetype]`. Validates config via `engine.validateConfig` (`build.js:150`) and checks minimum pillars (`build.js:159`).
     - **Step 2 (Fast Iteration)**: Executes 100 passes optimizing 12 spacing/margin parameters (`build.js:177-190`) and validates `checkConfig` (`build.js:192-213`) requiring char count > 2000, bold tags >= 40, all 7 sections present, no banned tools, and zero hyphens/em-dashes (`/[-—]/`).
     - **Step 3 (Render PDF)**: Renders `cv_final.html` using `cv_weasyprint_template.js`, executes `python -m weasyprint` via `child_process.execSync` (`build.js:247`), and verifies page count using `PyPDF2.PdfReader` (`build.js:249-251`). Hard exits if `pageCount !== 2` (`build.js:266-269`).
     - **Step 4 (QC Checks)**: Executes `runCoreChecks` (`qc_core_checks.js`) and `runUserChecks` (`qc_user_checks.js`) (`build.js:276-282`).
     - **Step 5 (Reporting)**: Reports pass/fail score (`build.js:287-308`). If `failTotal === 0`, outputs `BUILD SUCCESS — all 26 QC checks passed.`

2. **Core QC Checks (`core/templates/qc_core_checks.js:1-136`)**:
   Executes exactly 15 universal checks:
   - QC1: Two-page gate (`pageCount === 2`)
   - QC2: PDF size > 10KB & exists (`fs.existsSync(pdfPath) && size > 10240`)
   - QC3: Primary experience bullets minimum (`primaryBullets.length >= minBullets`, default 4)
   - QC4: WHY_I_FIT present and > 200 chars (`WHY_I_FIT.length > 200`)
   - QC5: ROLE_PILLARS count (`ROLE_PILLARS.length >= minPillars`, default 3 structural, 6 in user rules)
   - QC6: NUMBERS_THAT_MATTER >= 2 (`NUMBERS_THAT_MATTER.length >= 2`)
   - QC7: All HTML sections present (`WHY I FIT`, `ROLE PILLARS`, `PROFESSIONAL EXPERIENCE`, `EDUCATION`, `NUMBERS`, `TOOLS`, `CERTIFICATIONS`)
   - QC8: Bold markers >= 40 (`strongCount >= 40`)
   - QC9: Content density >= 4000 chars & zero undefined/null (`charCount >= 4000 && !hasUndefinedOrNull`)
   - QC10: No hyphens/em-dashes in dynamic content (`!/[-—]/.test(...)`)
   - QC11: Date en-dash format (no hyphen-minus `-` in date fields)
   - QC12: Non-fulltime roles labeled clearly (title/label must disclose `part-time`, `independent`, `consulting`, `contract`, or `internship`)
   - QC13: Widow/orphan range check (plain text length forbidden between 116 and 179 chars; must be 95–115 or 180–230 chars)
   - QC14: TOOLS has >= 8 items (comma-separated tool count >= 8)
   - QC15: TOOLS_GROUPED >= 3 categories (`TOOLS_GROUPED.length >= 3`)

3. **User QC Checks (`core/templates/qc_user_checks.js:88-173` & `reference/qc-rules.json:1-28`)**:
   Executes exactly 11 candidate-specific checks for Harsh Goyal:
   - User QC1: `No zapier in config`
   - User QC2: `No n8n in config`
   - User QC3: `Summary mentions 50+`
   - User QC4: `Summary mentions 15+`
   - User QC5: `Summary mentions 30+`
   - User QC6: `Summary mentions 98.66%`
   - User QC7: `Portfolio URL requirement` (`portfolioUrlRequired: false` -> N/A or satisfied)
   - User QC8: `ROLE_PILLARS >= 6`
   - User QC9: `Cover letter closing text` (closing text matches required text or evaluates to true if omitted)
   - User QC10: `Part-time labeled on experience`
   - User QC11: `Independent labeled on Projects`

4. **Runtime Dependencies Tested**:
   - `python --version`: `Python 3.14.6`
   - `node --version`: `v24.15.0`
   - `weasyprint`: `69.0` with `Pango 15800` and `pydyf 0.12.1`
   - `PyPDF2`: `3.0.1`
   - `weasyprint_env.js`: Tested dynamic DLL resolution for Windows (`libgobject-2.0-0.dll` resolved via PATH scanning).
   - Sample output verification: `outputs/ops_category_manager/Harsh_Goyal_Ops_Category_Manager.pdf` verified as exactly 2 pages (`len(reader.pages) === 2`) and 32,268 bytes (> 10KB).

5. **Claims Linter Verification (`core/agents/lint.js:1-128`)**:
   - Running `npm test` in `core/` executed `engine.test.js`, where claims linter correctly threw: `FAIL: Claims Linter failed: SUMMARY: unrecognized token "5cr+"...` because `5cr+` is not in Harsh Goyal's canonical `reference/proof-bank.md`. This confirms that unverified numbers are strictly blocked by the runtime compiler.

---

## 2. Logic Chain

1. **Step 1 — Build Invariant Verification**:  
   From Observation 1 and 4, `build.js` is the unified single-entry compiler for generating publication-grade CVs. When invoked as `node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..` inside `outputs/<role_slug>`, it correctly loads ground truth from `reference/` and resolves all template dependencies.
2. **Step 2 — QC Count Invariant Verification**:  
   From Observation 2 and 3, `qc_core_checks.js` produces 15 check results and `qc_user_checks.js` produces 11 check results based on `reference/qc-rules.json`. Summing $15 + 11 = 26$ checks. All 26 checks must pass for `build.js` to report success.
3. **Step 3 — Layout & Typographical Bounds**:  
   From Observation 1 and 2 (QC10, QC11, QC13), the build enforces mathematical constraints: bullet character length cannot be between 116 and 179 characters (widow elimination); dynamic text cannot contain hyphens or em-dashes (`/[-—]/`); dates must use Unicode en-dash (`–`); and final PDF page count must be exactly 2 pages.
4. **Step 4 — Environment Feasibility**:  
   From Observation 4, all required system runtimes (Node 24, Python 3.14, WeasyPrint 69, PyPDF2 3, Pango 15800) are already operational and validated in the environment without requiring any additional installation or configuration.

---

## 3. Caveats

1. **Working Directory Discipline**: Commands must be run inside the role output directory (e.g. `cd outputs/founders_office_generalist && node ../../core/templates/build.js ...`). Running directly in the workspace root without the target directory context would write output artifacts to the root.
2. **Predecessor Leakage Protection**: As demonstrated during `npm test`, legacy test configurations referencing obsolete candidate tokens (e.g. `5cr+`, `61%`, `800+`) will trigger `Claims Linter failed`. The target `partial_config.json` must strictly draw tokens from Harsh Goyal's `reference/proof-bank.md` (`Rs 25L+`, `50+`, `15+`, `30+`, `100+`, `12+`, `3 cities`, `98.66%`).
3. **Puppeteer Fit-Guard**: Puppeteer is in `devDependencies` for optional visual height checks (`engine.runFitGuard`), but the primary build pipeline relies on WeasyPrint + PyPDF2 for deterministic page counting and PDF generation.

---

## 4. Conclusion

The build system, templates, and 26 QC checks are fully operational and strictly enforced. To fulfill the prompt requirements for `outputs/founders_office_generalist`:
- Archetype: `"Entrepreneur"`
- Build command:
  ```bash
  cd outputs/founders_office_generalist && \
  node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..
  ```
- The generated `partial_config.json` must feature exactly 6 pillars with 5 bullets each, adhere to character length budgets (95–115 chars/bullet), eliminate all hyphens/em-dashes, include all 4 mandatory summary metrics (`50+`, `15+`, `30+`, `98.66%`), and ground every metric in `reference/proof-bank.md`.

---

## 5. Verification Method

To independently verify the build architecture and environment:

1. **Verify WeasyPrint & Environment**:
   ```bash
   python -m weasyprint --info
   ```
   *Expected*: WeasyPrint version 69.0, Python 3.14.6, Pango 15800.

2. **Verify Sample Output Page Count**:
   ```bash
   python -c "from PyPDF2 import PdfReader; print('Pages:', len(PdfReader(r'outputs/ops_category_manager/Harsh_Goyal_Ops_Category_Manager.pdf').pages))"
   ```
   *Expected*: `Pages: 2`.

3. **Verify QC Rules Mapping**:
   Inspect `reference/qc-rules.json` and count rules:
   - 2 banned tools (`zapier`, `n8n`) -> 2 checks
   - 4 required metrics (`50+`, `15+`, `30+`, `98.66%`) -> 4 checks
   - 1 portfolio requirement -> 1 check
   - 1 minimum pillar check -> 1 check
   - 1 cover letter closing check -> 1 check
   - 2 disclosure checks (`partTimeLabel`, `independentLabel`) -> 2 checks
   *Total*: 11 User QC checks + 15 Core QC checks = 26 checks.
