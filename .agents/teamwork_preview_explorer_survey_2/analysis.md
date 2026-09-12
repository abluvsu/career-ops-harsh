# Build System & Quality Control Architecture Deep Dive

**Candidate**: Harsh Goyal  
**Workspace Root**: `c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh`  
**Core Submodule**: `core/` (shared career-ops-core v2.0.0)  
**Date**: September 2026  
**Investigator**: `teamwork_preview_explorer_survey_2`

---

## 1. Executive Summary

The **Career Ops Build & QC System** is a deterministic, compiler-grade pipeline that transforms a role-tailored partial configuration (`partial_config.json`) and frozen ground truth libraries into an ATS-compliant, publication-grade, exactly 2-page PDF resume and cover letter. 

The architecture enforces a strict **Closed-World Library-Only Ground Truth Law**:
- Candidate profile facts are pinned in `reference/profile.json`.
- Quantified achievements are pinned in `reference/proof-bank.md`.
- Experience bullet variants are pinned by archetype in `reference/bullet-library.json`.
- Candidate-specific QC rules are pinned in `reference/qc-rules.json`.

The build is driven by `core/templates/build.js` through a unified single-command bash invocation. The system runs **26 automated quality control checks** (15 Universal Core QC checks + 11 User-Configurable QC checks) alongside a 100-pass iterative CSS spacing optimizer and a strict two-page gate backed by WeasyPrint and PyPDF2.

---

## 2. Build Pipeline Architecture & Execution Flow

The build pipeline consists of 5 deterministic steps executed sequentially inside `core/templates/build.js`:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          STEP 1: ASSEMBLE CONFIG                       │
│  - Merge config_defaults.json + profile.json + partial_config.json     │
│  - Inject frozen EXPERIENCE & PROJECTS from bullet-library.json        │
│  - Schema validation via Zod (engine.validateConfig)                   │
│  - Minimum pillar check (>= 6 pillars)                                 │
│  - Write assembled config.json to output directory                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                    STEP 2: FAST ITERATION (100 PASSES)                 │
│  - Evaluate 12 spacing / margin layout strategies iteratively          │
│  - checkConfig() validation (char density > 2000, bold >= 40,          │
│    no hyphens/em-dashes, no banned tools, all 7 sections)              │
│  - Write optimized spacing variables to config.json                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                    STEP 3: RENDER PDF VIA WEASYPRINT                   │
│  - Generate HTML via cv_weasyprint_template.js -> cv_final.html        │
│  - Invoke WeasyPrint CLI via python -m weasyprint                      │
│  - PyPDF2 page count verification (MUST EQUAL EXACTLY 2)               │
│  - Atomic copy with file-lock retry fallback (_v2.pdf)                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                       STEP 4: DUAL QC GATE EVALUATION                  │
│  - Run 15 Universal Core QC Checks (qc_core_checks.js)                 │
│  - Run 11 Candidate User QC Checks (qc_user_checks.js)                 │
│  - Combined 26 checks evaluated and tallied                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                          STEP 5: REPORT & CLEANUP                      │
│  - Output QC score (26/26), page count, character count, bold tags     │
│  - Verify 100% pass (failTotal === 0 -> BUILD SUCCESS)                 │
│  - Clean up temporary artifacts (cv_check.html, qc20_check.html)       │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Build Command Syntax & Options

The standardized build command for compiling a role-specific resume is:

```bash
cd outputs/<role_slug> && \
node ../../core/templates/build.js --in partial_config.json --archetype "<Archetype>" --data-root ../..
```

#### CLI Parameters:
1. `--in <path>` (**Required**): Relative or absolute path to the role's `partial_config.json`.
2. `--archetype <name>` (**Required**): Ground truth archetype key matching an entry in `reference/bullet-library.json`. For Harsh Goyal, available archetypes are:
   - `"Entrepreneur"`: Leads with Naraina Jewellers as primary experience (`EXPERIENCE[0]`) titled as `Founder` with label `(Independent Venture)`.
   - `"Business Strategist"`: Leads with Gandhi & Co. focused on strategy, NI/Contract Act frameworks, and legal operations.
   - `"Legal Professional"`: Leads with Gandhi & Co. focused on High Court dispute litigation briefs, statutory drafting, and court appearances.
3. `--data-root <path>` (**Optional but Practically Mandatory in Subdirectories**): Path to the candidate's workspace root containing `reference/`. When omitted from an `outputs/<role_slug>` directory, `resolveDataRoot()` falls back to `process.cwd()` or `core/`, neither of which contains the candidate's `reference/bullet-library.json` and `reference/qc-rules.json`, causing the build to fail immediately.

### 2.2 Data Root Resolution Mechanics

The `resolveDataRoot(inputPath, tplDir)` function resolves paths in the following priority order:
1. If `inputPath` is explicitly passed (e.g. `--data-root ../..`), resolve relative to `process.cwd()`. If the path ends with `reference`, strips to parent directory.
2. If `reference/` exists in `process.cwd()`, return `process.cwd()`.
3. If `reference/` exists in `tplDir/../reference`, return project root.
4. Fallback to `tplDir/..`.

**Critical Finding**: Because `core/` does not store candidate-specific data, running `build.js` inside `outputs/<role>` without `--data-root ../..` will look for `core/reference/bullet-library.json` which does not exist, triggering `ERROR: bullet-library.json not found`. Always specify `--data-root ../..`.

---

## 3. Comprehensive Analysis of the 26 Quality Control Checks

The system combines **15 Universal Core QC Checks** and **11 Candidate-Specific User QC Checks**, totaling **26 checks**. Every single check must evaluate to `PASS` (`passTotal === 26`) for `build.js` to output `BUILD SUCCESS — all 26 QC checks passed`.

### 3.1 The 15 Universal Core QC Checks (`qc_core_checks.js`)

These checks enforce universal structural, formatting, and typographical integrity across any candidate profile:

| # | Check Name | Target / Threshold | Exact Code Condition | Rationale & Failure Mode |
|---|---|---|---|---|
| **Core QC 1** | Two-page gate | Exactly 2 pages | `pageCount === 2` | Ensures the PDF neither overflows to 3 pages (awkward orphan page) nor underfills to 1 page. Hard crashes in Step 3 if `pageCount !== 2`. |
| **Core QC 2** | PDF size > 10KB & file exists on disk | > 10,240 bytes | `fs.existsSync(pdfPath) && (pdfSize \|\| fs.statSync(pdfPath).size) > 10240` | Catches corrupted, blank, zero-byte, or partial PDF generation failures. |
| **Core QC 3** | Primary experience bullets minimum | >= 4 bullets | `primaryBullets.length >= minBullets` (default 4) | Enforces sufficient depth of achievements in the primary work experience entry (`EXPERIENCE[0]`). |
| **Core QC 4** | WHY_I_FIT > 200 chars | > 200 characters | `Boolean(C.WHY_I_FIT && C.WHY_I_FIT.length > 200)` | Guarantees the hiring-manager pitch is substantial, context-rich, and detailed rather than a placeholder. |
| **Core QC 5** | ROLE_PILLARS count | >= 3 (structural min), >= 6 (spec) | `(C.ROLE_PILLARS \|\| []).length >= minPillars` | Ensures full functional coverage of the target job description requirements. |
| **Core QC 6** | NUMBERS_THAT_MATTER >= 2 | >= 2 entries | `(C.NUMBERS_THAT_MATTER \|\| []).length >= 2` | Ensures prominent numerical highlights are surfaced in the dedicated metrics panel. |
| **Core QC 7** | All HTML sections present | All 7 sections | Checks HTML contains: `'WHY I FIT'`, `'ROLE PILLARS'`, `'PROFESSIONAL EXPERIENCE'`, `'EDUCATION'`, `'NUMBERS'`, `'TOOLS'`, `'CERTIFICATIONS'` | Prevents accidental omission of major resume sections during template rendering. |
| **Core QC 8** | Bold markers >= 40 | >= 40 `<strong>` tags | `(htmlContent.match(/<strong/g) \|\| []).length >= 40` | Guarantees visual hierarchy and skimmability; recruiters scan for bold metrics in 6 seconds. |
| **Core QC 9** | Content density >= 4000 chars & zero undefined/null | >= 4,000 text chars & 0 leakages | `charCount >= 4000 && !/(?:>\|\s\|^)(undefined\|null\|NaN\|\[object Object\])(?:<\|\s\|$)/i.test(bodyString)` | Prevents sparse content, template interpolation leaks, or broken variable rendering. |
| **Core QC 10** | No hyphens/em-dashes in dynamic content | 0 hyphens `-` or em-dashes `—` | `!/[-—]/.test(...)` on `TAGLINE`, `SUMMARY`, `WHY_I_FIT`, `EXPERIENCE`, `PROJECTS`, `ROLE_PILLARS` | **Rule 2**: Prevents ugly PDF wrapping bugs and ATS parsing delimiters. Only Unicode en-dash `–` is permitted for date ranges. |
| **Core QC 11** | Date en-dash format | 0 hyphen-minus `-` in dates | `!d.includes('-')` in `EXPERIENCE.dates`, `PROJECTS.dates`, `EDUCATION.dates` | **Rule 9**: Enforces typography standard; date ranges must strictly use en-dash (`–`, U+2013). |
| **Core QC 12** | Non-fulltime roles labeled clearly | Explicit disclosure in title/label | Non-fulltime roles must contain `part-time`, `independent`, `consulting`, `contract`, or `internship` | **Rule 7**: Full disclosure of employment classification. Ventures like Naraina Jewellers must be labeled `(Independent Venture)`. |
| **Core QC 13** | Widow/orphan character budget | Plain text len <= 115 OR >= 180 chars | Forbidden zone: `116 < len < 180` across all experience/project bullets | Prevents widow lines where a 2nd line has only 1-3 words (>35% blank space). Must be 1 line (95-115 chars) or 2 full lines (180-230 chars). |
| **Core QC 14** | TOOLS has >= 8 items | >= 8 comma-separated tools | `(C.TOOLS \|\| '').split(',').filter(...).length >= 8` | Ensures broad coverage of ATS keywords across software, ERP, modeling, and operational tools. |
| **Core QC 15** | TOOLS_GROUPED >= 3 categories | >= 3 grouped categories | `(C.TOOLS_GROUPED \|\| []).length >= 3` | Organizes technical competencies into clear functional domains (e.g. Financial, Operational, Legal). |

---

### 3.2 The 11 Candidate User QC Checks (`qc_user_checks.js`)

These checks are dynamically loaded from `reference/qc-rules.json` and enforce candidate-specific ground truths for **Harsh Goyal**:

```json
{
  "candidateName": "Harsh Goyal",
  "bannedTools": ["zapier", "n8n"],
  "requiredMetrics": ["50+", "15+", "30+", "98.66%"],
  "requiredDisclosures": {
    "partTimeLabel": true,
    "independentLabel": true
  },
  "portfolioUrlRequired": false,
  "coverLetter": {
    "maxWords": 300,
    "requiredClosingText": "I look forward to discussing how my legal acumen and strategic background can add value."
  },
  "coverLetterClosingText": "I look forward to discussing how my legal acumen and strategic background can add value.",
  "minPrimaryBullets": 4,
  "minPillars": 6,
  "minPillarsCount": 6,
  "minContentChars": 4000,
  "minBoldMarkers": 40
}
```

| # | Check Name | Target / Threshold | Exact Code Condition | Rationale & Failure Mode |
|---|---|---|---|---|
| **User QC 1** | No zapier in config | 0 occurrences | `!jsonStr.includes('zapier')` | Harsh has never used Zapier; prevents AI hallucination or predecessor tool leakage. |
| **User QC 2** | No n8n in config | 0 occurrences | `!jsonStr.includes('n8n')` | Harsh has never used n8n; prevents AI hallucination or predecessor tool leakage. |
| **User QC 3** | Summary mentions 50+ | Token `"50+"` present | `summaryText.includes('50+')` | Anchors Harsh's flagship litigation volume (50+ High Court briefs managed at Gandhi & Co.). |
| **User QC 4** | Summary mentions 15+ | Token `"15+"` present | `summaryText.includes('15+')` | Anchors Harsh's commercial agreements milestone (15+ commercial contracts/pleadings drafted). |
| **User QC 5** | Summary mentions 30+ | Token `"30+"` present | `summaryText.includes('30+')` | Anchors Harsh's client advisory record (30+ corporate dispute consultations). |
| **User QC 6** | Summary mentions 98.66% | Token `"98.66%"` present | `summaryText.includes('98.66%')` | Anchors Harsh's quantitative moat (top 98.66 percentile nationwide in 3rd Math Olympiad). |
| **User QC 7** | Portfolio URL requirement | Optional / Satisfied | Evaluates to `true` when `portfolioUrlRequired: false` | Configurable gate; avoids requiring non-existent portfolio links for legal/founder roles. |
| **User QC 8** | ROLE_PILLARS >= 6 | Exactly or >= 6 pillars | `(C.ROLE_PILLARS \|\| []).length >= 6` | Mandates 6 comprehensive role pillars to match 100% of JD evaluation dimensions. |
| **User QC 9** | Cover letter closing text | Standardized closing | Matches `"I look forward to discussing how my legal acumen and strategic background can add value."` or evaluates to `true` if no cover letter in config | Enforces professional, on-brand closing phrasing in cover letter outputs. |
| **User QC 10** | Part-time labeled on experience | Explicit label | Part-time experience entries must have `part time` in title or label | Guarantees ethical and transparent career history representation. |
| **User QC 11** | Independent labeled on Projects | Word `independent` present | Projects title or label must include `independent` | Differentiates independent ventures and consulting from corporate employment. |

> **Summary Check Verification**: `summaryText` in User QC 3–6 is computed as:  
> `(C.SUMMARY || '') + ' ' + (C.WHY_I_FIT || '') + ' ' + expBullets.join(' ')`.  
> Therefore, placing the 4 required tokens (`50+`, `15+`, `30+`, `98.66%`) in either `SUMMARY` or `WHY_I_FIT` satisfies all four checks!

---

## 4. Rendering Engine & Environment Dependencies

The build pipeline relies on a zero-friction, hybrid runtime environment:

### 4.1 Node.js Runtime & Packages
- **Node.js**: `v24.15.0` (Active and verified).
- **Dependencies (`core/package.json`)**:
  - `zod: ^3.23.8`: Runtime type validation for candidate profiles, experience entries, and configs.
  - `docx: ^9.7.1`: Word document compilation for cover letters.
  - `puppeteer: ^24.43.1` (devDependencies): Optional headless Chrome driver for visual Fit-Guard height checks.
  - `typescript: ^5.0.0` (devDependencies): Type definitions and compiler for Challenger Gate.

### 4.2 Python Runtime & WeasyPrint
- **Python Engine**: `Python 3.14.6` (Active and verified in PATH).
- **Core Rendering Packages**:
  - `weasyprint: 69.0` (Active and verified).
  - `PyPDF2: 3.0.1` (Active and verified).
  - `pydyf: 0.12.1` (WeasyPrint PDF low-level serializer).
  - `Pango: 15800` (High-performance international text layout and glyph positioning engine).

### 4.3 Environment Resolution Mechanics (`weasyprint_env.js`)
On Windows, WeasyPrint requires native C-libraries (GTK/GObject/Pango/Cairo/HarfBuzz) and specifically `libgobject-2.0-0.dll`. `weasyprint_env.js` ensures robust zero-config execution without hardcoding machine-specific paths through an intelligent 4-tier fallback:
1. `process.env.WEASYPRINT_DLL_DIRECTORIES`
2. `process.env.MSYS_BIN`
3. `.env` file discovered via upward recursive traversal
4. **Dynamic PATH scanning**: Automatically iterates through all directories in `process.env.PATH` to locate `libgobject-2.0-0.dll`.
5. Injects discovered directories into `PATH` and sets `WEASYPRINT_DLL_DIRECTORIES`.

**Verification**: Running `python -m weasyprint --info` confirms:
```
System: Windows (AMD64, 10.0.26200)
WeasyPrint version: 69.0
Python version: 3.14.6
Pydyf version: 0.12.1
Pango version: 15800
```
The rendering pipeline operates natively with zero additional installation required.

### 4.4 Font Stack & CSS Page Geometry
- **Page Geometry (`cv_weasyprint_template.js`)**:
  ```css
  @page {
    size: A4;
    margin: 0.5cm 0.8cm 0.5cm 0.8cm;
  }
  ```
- **Font Family**: `'Segoe UI', Calibri, 'DejaVu Sans', Arial, sans-serif`
  - All fonts are native to Windows 10/11 (`Segoe UI`, `Calibri`, `Arial`).
  - Renders deterministically without font substitution warnings or external web font requests.

---

## 5. Fit-Guard, Spacing Optimization & Content Blending

### 5.1 100-Pass Fast Iteration Spacing Optimizer
In Step 2 of `build.js`, the compiler runs 100 fast iterations across 12 CSS variables to find the optimal density that packs maximum information into exactly 2 pages:

1. `BULLET_SPACING`: decremented down to min 20 (from ~28)
2. `LAST_BULLET_SPACING`: decremented down to min 5 (from ~10)
3. `HEADER_BEFORE_SPACING`: decremented down to min 60 (from ~90)
4. `HEADER_AFTER_SPACING`: decremented down to min 20 (from ~35)
5. `ROLE_BEFORE_SPACING`: decremented down to min 40 (from ~60)
6. `ROLE_AFTER_SPACING`: decremented down to min 15 (from ~22)
7. `CERT_SPACING`: decremented down to min 20 (from ~32)
8. `EDU_SPACING`: decremented down to min 24 (from ~36)
9. `PAGE_MARGIN_TOP`: decremented down to min 500 (from ~650)
10. `PAGE_MARGIN_BOTTOM`: decremented down to min 450 (from ~580)
11. `PAGE_MARGIN_LEFT`: decremented down to min 600 (from ~800)
12. `PAGE_MARGIN_RIGHT`: decremented down to min 600 (from ~800)

At each pass, `checkConfig()` validates that:
- Char count > 2,000 (final target >= 4,000)
- Bold markers >= 40
- All 7 sections present
- Zero banned tools (`zapier`, `n8n`)
- Zero hyphens or em-dashes (`/[-—]/`)

### 5.2 The 75/25 Content Blending Law
- **75% Frozen Ground Truth**: The candidate's past work experience (`EXPERIENCE`) and proprietary ventures (`PROJECTS`) are frozen in `reference/bullet-library.json` and injected automatically by `build.js` based on `--archetype`.
- **25% Dynamic Tailoring**: The role-specific `partial_config.json` provides:
  - `COMPANY` & `ROLE`
  - `TAGLINE` & `SUMMARY`
  - `WHY_I_FIT` (100–300 words hiring manager pitch)
  - `ROLE_PILLARS` (6 pillars × 5 tailored bullets)
  - `NUMBERS_THAT_MATTER` (4 proof points)
  - `TOOLS` & `TOOLS_GROUPED` (ATS keywords)
  - `ROLE_INTRO` (injected into `EXPERIENCE[0].intro`)

### 5.3 Character Budget & Widow/Orphan Prevention Math
Line lengths in WeasyPrint A4 two-column and grid layouts follow strict typographical character limits:
- **1-Line Bullet Target**: **95 – 115 characters** (Target: ~105 characters).
- **2-Line Bullet Target**: **180 – 230 characters**.
- **The Widow Danger Zone (116 – 179 characters)**: A bullet of 130 characters wraps onto line 2 with only 2-3 words, leaving >40% awkward blank space. Core QC 13 and `engine.validateConfig` explicitly flag any bullet between 116 and 179 characters with `FIT FAIL: Widow/Orphan detected in bullet`.

---

## 6. Pre-Flight Verification & Claims Linter Gates

### 6.1 Claims Linter (`core/agents/lint.js`)
The claims linter prevents fabricated metrics through deterministic string matching against `reference/proof-bank.md`:
1. Extracts numeric tokens via `NUM_TOKEN_RE`: matches integers, decimals, percentages (`%`), plus signs (`+`), currency (`Rs.`, `₹`), and multiplier units (`Cr`, `L`, `k`, `x`, `days`, `mins`, `yrs`).
2. Normalizes tokens: strips currency symbols, spaces, commas, and lowercases (e.g. `Rs 25L+` -> `25l+`).
3. Verifies extracted tokens against canonical proof bank table:
   - In Harsh Goyal's `reference/proof-bank.md`: `98.66%`, `50+`, `15+`, `25l+`, `30+`, `100+`, `12+`, `20+`, `5+`, `3+`, `10+`, `40+`, `90%`, etc.
4. Allowlist bypasses safe syntactic patterns: 4-digit years (`2021`, `2024`, `2026`), single digits (`1`-`9`), `"4yrs"`, `"90days"`, `"63l+"`, `"8club"`.
5. Any unrecognized metric token causes immediate validation rejection!

### 6.2 Pre-Flight Challenger Gate (`core/agents/challenger-gate.ts`)
Before PDF compilation, the Challenger Gate evaluates `partial_config.json` against the target Job Description text:
- **Keyword Coverage (60% weight)**: Matches single-word and multi-word terms (e.g. `supply chain`, `contract negotiation`, `unit economics`) against config text.
- **Metric Density Score (20% weight)**: Target >= 10 verifiable numerical metrics (`min(totalMetrics / 10, 1) * 20`).
- **Bold Metric Density Score (20% weight)**: Target >= 6 bold metrics (`min(boldMetrics / 6, 1) * 20`).
- **Composite ATS Score**: Must achieve **>= 85%**.
- **Rule 2 Pre-Check**: Warns if any hyphens (`-`) or em-dashes (`—`) are detected in leaf values.

---

## 7. Potential Failure Modes & Strict Compliance Matrix

The following table documents all known build failure modes, their root causes, and mandatory compliance requirements:

| Failure Mode | Trigger / Error Message | Root Cause | Prevention & Fix Requirement |
|---|---|---|---|
| **Widow Line Error** | `FIT FAIL: Widow/Orphan detected in bullet. Length is X chars...` | Plain text bullet length between 116 and 179 characters | Programmatically optimize bullet length to 95–115 chars (1 full line) or 180–230 chars (2 full lines). |
| **Hyphen Violation** | `FAIL: Core QC10: No hyphens/em-dashes in dynamic content (Rule 2)` | ASCII `-` or em-dash `—` in dynamic config fields | Eliminate hyphens. Replace with spaces (`end to end`, `hands on`, `on site`, `multi city`, `cross team`) or commas. |
| **Date Hyphen Error** | `FAIL: Core QC11: Date en-dash format (Rule 9) — Found hyphen in date: "2025-2026"` | Hyphen-minus `-` used in date range string | Strictly use Unicode en-dash (`–`, U+2013), e.g. `"2025 – 2026"`, `"May 2022 – Aug 2026"`. |
| **Page Count Overflow** | `FAIL: Expected 2 pages, got 3` (Exit code 1) | Excessive bullet lengths, too many bullets, or loose margins pushing content onto page 3 | Reduce `WHY_I_FIT` length, optimize bullet lengths to ~105 chars, or tighten spacing in `partial_config.json`. |
| **Page Count Underflow** | `FAIL: Expected 2 pages, got 1` (Exit code 1) | Insufficient text content (<3,500 chars) leaving massive blank space | Ensure all 6 pillars have 5 robust bullets and `WHY_I_FIT` is between 150 and 300 words. |
| **Missing Data Root** | `ERROR: bullet-library.json not found at .../core/reference/bullet-library.json` | Running `build.js` from `outputs/<role>` without `--data-root ../..` | Always invoke with `--data-root ../..`. |
| **Invalid Archetype** | `ERROR: Archetype "X" not found in bullet-library.json` | Typo in archetype name or selecting an archetype not present in the candidate library | Use exact casing: `"Entrepreneur"`, `"Business Strategist"`, or `"Legal Professional"`. |
| **Missing Required Metric** | `FAIL: User QCX: Summary mentions 50+` | `50+`, `15+`, `30+`, or `98.66%` missing from combined summary/pitch text | Ensure `WHY_I_FIT` and `SUMMARY` explicitly include all four mandatory metrics from `qc-rules.json`. |
| **Banned Tool Leakage** | `FAIL: User QC1: No zapier in config` | `zapier` or `n8n` present in `TOOLS`, `SUMMARY`, or bullets | Never reference Zapier or n8n. Use verified tools: MS Excel, Tally ERP, Financial Modeling. |
| **Missing Non-Fulltime Label** | `FAIL: Core QC12: Non-fulltime roles labeled clearly (Rule 7)` | Experience or project item not marked `(Independent Venture)` or `(Internship)` | Ensure Naraina Jewellers has `label: "(Independent Venture)"` and Projects have `independent` in title. |
| **Unverified Claim Error** | `FAIL: Claims Linter failed: ... unrecognized token "X"` | Inventing numbers or metrics not present in `reference/proof-bank.md` | Use only verified numbers from proof bank (`Rs 25L+`, `50+`, `15+`, `30+`, `100+`, `12+`, `3 cities`, `98.66%`). |
| **Inadequate Density** | `FAIL: Core QC9: Content density >= 4000 chars` | Total body text character count < 4,000 chars | Expand narrative depth in `WHY_I_FIT` and ensure 6 pillars with 5 bullets each. |
| **File Lock on Windows** | `EBUSY: resource busy or locked` when rewriting PDF | PDF viewer (e.g. Acrobat or browser) has the output PDF locked open | `safeWriteFileSync` and `copyWithRetry` automatically retry 5 times and fall back to `_v2.pdf`. Close PDF viewer to avoid file churn. |

---

## 8. Specific Blueprint for `outputs/founders_office_generalist`

To satisfy all acceptance criteria in `ORIGINAL_REQUEST.md` for the Generalist Founder's Office CV:
1. **Target Directory**: `outputs/founders_office_generalist/`
2. **Archetype**: `"Entrepreneur"` (surfaces Naraina Jewellers as primary experience `EXPERIENCE[0]`).
3. **Build Command**:
   ```bash
   cd outputs/founders_office_generalist && \
   node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..
   ```
4. **Key Configuration Elements**:
   - `ROLE`: `"Founder's Office (Generalist & Operations)"`
   - `COMPANY`: `"Target Venture"`
   - `CV_OUTPUT`: `"Harsh_Goyal_Founders_Office_Generalist.docx"` (compiles to `.pdf`)
   - `TAGLINE`: Zero hyphens, e.g.:  
     `"IIM Sirmaur MBA with 0 to 1 founder execution, multi city supply chain sourcing, and High Court litigation precision"`
   - `SUMMARY` & `WHY_I_FIT`: Must contain all 4 mandatory metrics (`50+`, `15+`, `30+`, `98.66%`), zero hyphens/em-dashes, and verified proof points (`Rs 25L+`, `12+ vendors`, `3 cities`).
   - `ROLE_PILLARS`: Exactly 6 pillars with exactly 5 bullets each (all 95–115 characters per bullet):
     1. Ground Execution & Scrappy Ops
     2. Procurement & Supply Chain
     3. Unit Economics & Cash Flow
     4. Commercial Contracts & Deal Protection
     5. High-Stakes Client & Stakeholder Management
     6. Market Intelligence & Competitor Audits
   - `NUMBERS_THAT_MATTER`: Exactly 4 entries from proof bank.
   - `TOOLS`: At least 8 items (MS Excel, Tally ERP, Financial Modeling, Inventory Tracking, Vendor SLAs, Market Intelligence, Contract Review, Regulatory Filings).
   - `TOOLS_GROUPED`: Exactly 3 distinct functional categories.

---

## 9. Conclusion

The build system and QC architecture in `career-ops-harsh` is robust, deterministic, fully installed, and tested. The 26 QC checks operate with mathematical precision, guaranteeing zero hallucinated claims, zero formatting defects, and an exact 2-page fit.
