analysis_content = """# Harsh Goyal — Candidate Data & Reference Analysis Report

**Agent:** `teamwork_preview_explorer_survey_1` (Candidate Data & Reference Explorer)  
**Target Repository:** `c:\\Users\\mba06\\Dropbox\\My PC (MSI)\\Documents\\Claude\\Projects\\Career Ops\\career-ops-harsh`  
**Date:** 2026-09-12  

---

## 1. Executive Summary

This report delivers a comprehensive audit of Harsh Goyal's candidate profile, ground-truth reference data (`profile.json`, `proof-bank.md`, `bullet-library.json`), archetype definitions, claims linter mechanisms, and predecessor artifacts inherited from the template codebase.

### Key Conclusions:
1. **Naraina Jewellers Ground Truth:** Verified flagship 0-to-1 experience as Founder (`2025 – 2026`, proprietorship in New Delhi) with Rs 25L+ working capital modeling, 3-city manufacturing audit tours (Surat, Mumbai, Delhi), direct factory MOQ negotiations with diamond and bullion manufacturers, 12+ vendor agreements, and retail store commercial setup completed ahead of planned exit.
2. **Gandhi & Co. Litigation Moat:** Verified Associate role (`May 2022 – Aug 2026`) with 90% concentration before the High Court, 50+ litigation briefs, 100+ bench hearings, 15+ commercial agreements/pleadings under Contract Act (1872) and Negotiable Instruments Act (1881), and 30+ client consultations.
3. **Education & Undergrad Clarification:** Harsh holds an **MBA in General Management from IIM Sirmaur (2022)** and a 5-year integrated **B.A. LLB (Hons.) from Amity Law School, Delhi / IP University (2018)**. The reference to `RCOEM / undergrad` in the dispatch prompt is an external predecessor artifact originating from Ashutosh Bhandekar (the predecessor candidate); Harsh Goyal has no affiliation with RCOEM or engineering.
4. **Entrepreneur Archetype Status:** Correctly elevates Naraina Jewellers to `EXPERIENCE[0]` (primary role) with 4 frozen bullets (lengths 98–100 chars, zero hyphens, verified metrics). However, it retains an entry for `naraina_project` under `PROJECTS` (1 bullet, 104 chars), causing Naraina Jewellers to render twice on the CV if projects are rendered.
5. **Claims Linter & Allowlist Defects:** 
   - The token `0` from `0-to-1` is **NOT allowlisted** by `/^[1-9]$/` in `core/agents/lint.js` or `core/templates/engine.js`. Using `0-to-1` in `SUMMARY`, `TAGLINE`, or `WHY_I_FIT` triggers a fatal claims linter error (`unrecognized token "0"`) as well as a Rule 2 hyphen violation. Recommended solution: use **"zero to one"** in all dynamic prose.
   - Predecessor leaks remain hardcoded in `core/agents/lint.js` and `core/templates/engine.js` (`/^63l\\+?$/` and `/^8club$/i`) and in `core/templates/build.js` line 135 (`partialConfig.SARVM_INTRO`).
6. **QC Rule 7 / Core QC12 Constraint on Experience Labels:** Non-fulltime experiences (`type: "independent"`) require the title or label to include substrings like `independent` or `part-time`. If Naraina Jewellers is labeled strictly `(0-to-1 Retail Venture)`, Core QC12 fails. The label must be calibrated as `(Independent 0 to 1 Retail Venture)` or `(0 to 1 Retail Venture | Independent Venture)`.

---

## 2. Detailed Ground-Truth Evidence & Metrics Matrix

### 2.1. Naraina Jewellers (Proprietorship)
- **Role & Title:** `Founder`
- **Organization:** `Naraina Jewellers (Proprietorship)`
- **Dates:** `2025 – 2026` (Uses en-dash `–`, zero hyphens)
- **Type:** `independent`
- **Current Label in profile.json:** `(Independent Venture)`
- **Location:** New Delhi, India (with manufacturing sourcing tours in Surat, Mumbai, and Delhi)
- **Narrative Context:** 0-to-1 retail venture founded and scaled to commercial launch readiness:
  - Sourced gems and precious metals directly from primary manufacturers, bypassing regional wholesale markups.
  - Negotiated Minimum Order Quantities (MOQs) with diamond cutting and polishing factories in Surat and bullion merchants in Mumbai (Zaveri Bazaar).
  - Executed 12+ vendor agreements for raw materials, casting, and finishing.
  - Modeled a Rs 25L+ working capital allocation covering inventory purchases, cash buffer, and retail store setup.
  - Finalized prime retail store location, brand identity/naming, interior architectural renovation, security vault specifications, and statutory licensing before executing a planned commercial exit.
- **Verified Numerical Tokens in proof-bank.md:**
  - `25l+` (Item 6: Rs 25L+ inventory and capital budget modeled)
  - `12+` (Item 9: 12+ vendor agreements executed)
  - `5+` (Item 11: 5+ manufacturing hubs evaluated)
  - `3` (Item 19: 3 major manufacturing cities audited on site: Surat, Mumbai, Delhi)

### 2.2. Gandhi & Co.
- **Role & Title:** `Associate` (or `Associate, Strategy & Legal Operations`)
- **Organization:** `Gandhi & Co.`
- **Dates:** `May 2022 – Aug 2026` (Uses en-dash `–`)
- **Type:** `full-time`
- **Focus & Specialization:** High Court litigation with 90% concentration before High Court benches alongside District Courts.
- **Litigation Docket Scope:** Civil disputes, criminal proceedings, local tenancy laws (Rent Control Acts), and education dockets.
- **Statutory Codes Mastered:** Code of Civil Procedure (CPC), Code of Criminal Procedure (CrPC), Indian Penal Code (IPC), Indian Contract Act (1872), Negotiable Instruments Act (1881), and state rent control enactments.
- **Matter Pipeline Ownership:** 5-stage case lifecycle owned end-to-end:
  1. Strategic case evaluation and client remedy formulation.
  2. Landmark precedent research (SCC Online, Manupatra).
  3. Authoring pleadings, writ petitions, and commercial affidavits.
  4. Registry filing and clearance of technical office objections.
  5. Oral arguments before judicial benches on interim applications and injunctions.
- **In-House Commercial Moat:** Commercial contract drafting and risk mitigation, termination covenant drafting, debt enforcement under Section 138 of NI Act, and commercial dispute settlements.
- **Verified Numerical Tokens in proof-bank.md:**
  - `50+` (Item 4: 50+ case briefs managed before High Court)
  - `100+` (Item 8: 100+ court hearings attended and tracked)
  - `15+` (Item 5: 15+ commercial agreements / pleadings drafted)
  - `30+` (Item 7: 30+ client consultations conducted)
  - `20+` (Item 10: 20+ writ petitions and briefs filed with zero defects)
  - `90%` (Item 15: 90% litigation focus before High Court)
  - `5` (Item 16: 5 stage dispute lifecycle owned end to end)
  - `4` (Item 17: 4 core practice areas handled across dockets)
  - `6` (Item 18: 6 core statutory codes mastered comprehensively)

### 2.3. TATA AIG General Insurance
- **Role & Title:** `Sales & Marketing Intern`
- **Organization:** `TATA AIG General Insurance`
- **Dates:** `Apr 2021 – Jun 2021` (Uses en-dash `–`)
- **Type:** `internship`
- **Label:** `(Internship)`
- **Verified Metrics:**
  - `3+` (Item 12: 3+ insurance distribution channels benchmarked across agency and broker networks)

### 2.4. Education, Academics & Competitive Qualifications
- **IIM Sirmaur (2022):**
  - Degree: `MBA, General Management`
  - Specialization / Focus: Quantitative valuation, financial modeling, unit economics, supply chain analytics.
  - Leadership: Active student member in D2C Igniters Club (driven 10+ campus initiatives; proof-bank.md item 13).
- **Amity Law School, Delhi / Guru Gobind Singh Indraprastha University (2018):**
  - Degree: `B.A. LLB (Hons.)` (5-Year Integrated Law Programme, First Division).
  - Leadership: Chairperson & Co-Chairperson, Model United Nations (chaired 40+ committee delegates; proof-bank.md item 14).
- **Aggarsain Public School, Kurukshetra (2013):**
  - Senior Secondary (12th Board), Central Board of Secondary Education (CBSE).
- **3rd International Mathematics Olympiad (IMO) (2009):**
  - Scored **98.66 percentile nationwide** (proof-bank.md item 1). Proof of quantitative rigor and mathematical acumen.
- **Rajasthan Judicial Services (RJS) Examination (2024):**
  - Cleared the highly competitive state judicial services preliminary examination.
- **All India Bar Examination (AIBE) (2021):**
  - Bar Council of India certification for active legal practice.

---

## 3. Audit of the "Entrepreneur" Archetype

### 3.1. Structure in `reference/bullet-library.json`
The `Entrepreneur` archetype is defined at lines 86–138 of `reference/bullet-library.json`:
- **EXPERIENCE Array:**
  1. `naraina_jewellers`:
     - `title`: `"Founder"`
     - `organization`: `"Naraina Jewellers (Proprietorship)"`
     - `dates`: `"2025 – 2026"`
     - `type`: `"independent"`
     - `label`: `"(Independent Venture)"`
     - `minBullets`: 4
     - Bullets (4 total):
       1. `**Founded retail jewellery venture**, driving location selection, naming, brand identity, and licensing.` (100 chars)
       2. `**Modeled Rs 25L+ inventory and capital budget**, forecasting unit economics, retail margins, and turns.` (100 chars)
       3. `**Audited factories across Surat, Mumbai, and Delhi**, negotiating minimum order quantities with makers.` (100 chars)
       4. `**Negotiated 12+ vendor agreements**, establishing diamond and bullion supply chains for store launch.` (98 chars)
  2. `gandhi_co`:
     - `title`: `"Associate"`
     - `dates`: `"May 2022 – Aug 2026"`
     - `type`: `"full-time"`
     - Bullets (1 total):
       1. `**Advised commercial clients on 30+ disputes**, managing 90% High Court litigation briefs and settlements.` (102 chars)
  3. `tata_aig`:
     - `title`: `"Sales & Marketing Intern"`
     - `dates`: `"Apr 2021 – Jun 2021"`
     - `type`: `"internship"`
     - `label`: `"(Internship)"`
     - Bullets (1 total):
       1. `**Conducted sales channel assessments across 3+ hubs**, mapping broker incentive structures and reach.` (98 chars)
- **PROJECTS Array:**
  1. `naraina_project`:
     - `title`: `"Independent Projects & Ventures"`
     - `organization`: `"Naraina Jewellers"`
     - `dates`: `"2025 – 2026"`
     - `type`: `"independent"`
     - `label`: `"(Independent Venture)"`
     - Bullets (1 total):
       1. `**Naraina Jewellers (Independent Venture):** Full ownership of store site diligence, renovation, and supply.` (104 chars)

### 3.2. Evaluation Against QC Standards
- **Primary Experience Positioning:** Naraina Jewellers is positioned as the primary entry (`EXPERIENCE[0]`).
- **Date Formatting:** Every date uses the unicode en-dash `–` (U+2013). No hyphens (`-`). 100% compliant with Rule 9 and Core QC11.
- **Widow/Orphan Character Budgets:** Every bullet length is strictly between 98 and 104 characters, perfectly sitting inside the single-line budget (95–115 chars). Zero widow violations.
- **Metric Verification:** All metrics (`Rs 25L+`, `12+`, `30+`, `90%`, `3+`) exist in `reference/proof-bank.md`.
- **Redundancy Finding:** In the other two archetypes (`Legal Professional` and `Business Strategist`), Naraina Jewellers is placed in `PROJECTS` because Gandhi & Co. is the full-time primary experience. In `Entrepreneur`, Naraina Jewellers was properly elevated to `EXPERIENCE[0]`, but `naraina_project` was ALSO kept in `PROJECTS`. This causes Naraina Jewellers to render twice on the resume (once in Professional Experience and once in Independent Projects). In `outputs/ops_category_manager/cv_final.html`, both sections were printed.

---

## 4. Claims Linter & Allowlist Audit

### 4.1. The Zero (`0`) Token Defect
- **Mechanism:** `core/agents/lint.js` extracts numeric tokens using regex `NUM_TOKEN_RE`. Tokens are normalized and matched against canonical tokens from `reference/proof-bank.md` or `ALLOWLIST_PATTERNS`.
- **Current Allowlist:**
  ```javascript
  const ALLOWLIST_PATTERNS = [
    /^(19|20)\\d{2}$/,
    /^4(yrs?|years?)$/,
    /^[1-9]$/,
    /^90days?$/,
    /^63l\\+?$/,
    /^8club$/i,
  ];
  ```
- **The Issue:** `/^[1-9]$/` permits digits 1 through 9. Digit `0` is **NOT permitted**.
- **Empirical Test:**
  When `0 to 1` or `0-to-1` appears in any linted field (`SUMMARY`, `TAGLINE`, `WHY_I_FIT`, `ROLE_INTRO`, bullets), `extractTokens` yields `['0', '1']`.
  `'1'` matches `/^[1-9]$/`.
  `'0'` fails and produces: `FAIL: Claims Linter failed: SUMMARY: unrecognized token "0"`.
- **Compounding Defect (Hyphen):** `0-to-1` contains a hyphen `-`, which directly triggers Core QC10 / Rule 2 rejection (`No hyphens or dashes in any generated content`).
- **Solution:** In all dynamic copy (taglines, summaries, why-i-fit, bullets), always write **"zero to one"** in plain words. This bypasses both the token '0' linter failure and the hyphen ban without needing code changes in `core/`.

### 4.2. Predecessor Leaks in Allowlist & Submodule Code
1. **`^63l\\+?$` and `^8club$` in `lint.js` and `engine.js`:**
   - Location 1: `core/agents/lint.js` lines 68–69
   - Location 2: `core/templates/engine.js` line 217
   - Context: These entries originated from Ashutosh Bhandekar (Rs 63L+ ARR at Sarvam AI / Aaostays and The 8 Club). They are unverified for Harsh Goyal.
2. **`partialConfig.SARVM_INTRO` in `build.js`:**
   - Location: `core/templates/build.js` line 135:
     `if (idx === 1 && partialConfig.SARVM_INTRO) copy.intro = partialConfig.SARVM_INTRO;`
   - Context: Hardcoded property name referencing Sarvam AI (Ashutosh's second employer). In Harsh's profile, the second employer is Gandhi & Co.
3. **Predecessor Leaks in `reference/writing-rules.md`:**
   - Line 33: `Built CareerFlowAI (portfolio.example.com), 7-agent AI system with 61% session autonomy` (Ashutosh's project).
   - Line 42: `MBA (IIM Sirmaur) and B.E. Civil Engineering (Ramdeobaba University, Nagpur) are full-time formal education degrees.` (Ashutosh's undergrad institution).
   - Line 44: `Certified Business Analyst Power BI, Azure OpenAI Generative AI Models, IIT Bombay Industry Consulting Project` (Ashutosh's certifications).

---

## 5. QC Rule Interactions & Constraints

### 5.1. Core QC12 Non-Fulltime Role Labeling
In `core/templates/qc_core_checks.js` (lines 81–105):
```javascript
C.EXPERIENCE.forEach(e => {
  const type = (e.type || 'full-time').toLowerCase();
  if (type !== 'full-time') {
    const combined = `${e.title || ''} ${e.label || ''}`.toLowerCase();
    const isLabeled = combined.includes('part-time') || combined.includes('part time') || combined.includes('independent') || combined.includes('consulting') || combined.includes('contract') || combined.includes('internship');
    if (!isLabeled) {
      nonFullTimeUnlabeled = `${e.title || e.id} (${type})`;
    }
  }
});
```
If Naraina Jewellers has `type: "independent"` and the label is changed strictly to `(0-to-1 Retail Venture)`, `combined` is `"founder (0-to-1 retail venture)"`. Since `combined` does not contain the substring `independent`, Core QC12 fails!
**Requirement:** The label must explicitly include `Independent`, for example:
- `"(Independent 0 to 1 Retail Venture)"` or `"(0 to 1 Retail Venture | Independent Venture)"`.

### 5.2. User QC Checks (11 Checks total)
Based on `reference/qc-rules.json`:
1. No `zapier` in config (PASS)
2. No `n8n` in config (PASS)
3. Summary/Why_I_Fit/Exp mentions `50+` (PASS if included)
4. Summary/Why_I_Fit/Exp mentions `15+` (PASS if included)
5. Summary/Why_I_Fit/Exp mentions `30+` (PASS if included)
6. Summary/Why_I_Fit/Exp mentions `98.66%` (PASS if included)
7. Portfolio URL requirement: `userRules.portfolioUrlRequired: false` (Engine check disabled)
8. `ROLE_PILLARS >= 6` (PASS if 6 pillars provided)
9. Cover letter closing text: `"I look forward to discussing how my legal acumen and strategic background can add value."` (PASS)
10. Part-time labeled on experience: `naraina_jewellers` labeled as Independent (PASS)
11. Independent labeled on Projects: `projTitle` contains `independent` (PASS)

---

## 6. Recommendations for Calibration & Downstream Agents

| Area | Observed State | Recommended Action | Responsible Agent / Target |
|---|---|---|---|
| **Undergrad Degree** | Dispatch mentioned `RCOEM / undergrad` | Strictly specify **B.A. LLB (Hons.) from Amity Law School, Delhi (IP University)**. Discard all mentions of RCOEM / Engineering. | Planning & Generation Teams |
| **0-to-1 Phrasing** | Token `0` fails Claims Linter; `-` violates Rule 2 | In all narrative (`TAGLINE`, `SUMMARY`, `WHY_I_FIT`), use **"zero to one"** instead of `0-to-1`. | Generation Team (`partial_config.json`) |
| **Naraina Jewellers Label** | Currently `(Independent Venture)` | Calibrate label to **`(Independent 0 to 1 Retail Venture)`** to satisfy both the positioning directive and Core QC12. | `profile.json` & `bullet-library.json` |
| **Double Naraina Entry** | Appears in both `EXPERIENCE` and `PROJECTS` in `Entrepreneur` | Document that while both can build without breaking, keeping `naraina_project` in `PROJECTS` causes duplicate rendering on the CV. Can be kept or omitted if `PROJECT_TITLE` is labeled. | Generation & Build Pipeline |
| **Cleaning Writing Rules** | Line 42 of `reference/writing-rules.md` references RCOEM & B.E. Civil Eng | Update `reference/writing-rules.md` to reference Harsh Goyal's degrees: MBA (IIM Sirmaur) and B.A. LLB (Amity Law School). | Reference Maintenance |
| **Allowlist Cleanup** | `^63l\\+?$` and `^8club$` in `lint.js` and `engine.js` | Flag for removal in core submodule maintenance. | Submodule Maintenance |
"""

with open(r'c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh\.agents\teamwork_preview_explorer_survey_1\analysis.md', 'w', encoding='utf-8') as f:
    f.write(analysis_content)

print('analysis.md written successfully')
