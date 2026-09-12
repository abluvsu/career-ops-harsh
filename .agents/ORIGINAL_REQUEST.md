# Original User Request

## Initial Request — 2026-09-12T08:36:06Z

# Teamwork Project Prompt — Final

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: [none — teamwork routes from the description]

Generate and build a publication-grade, ATS-compliant 2-page Generalist Founder's Office CV for Harsh Goyal, highlighting his 0-to-1 entrepreneurial grit founding Naraina Jewellers as primary proof of founder-level operational hustle, financial discipline, vendor negotiation, and execution, reinforced by his High Court litigation precision and IIM Sirmaur MBA.

Working directory: `c:\Users\mba06\Dropbox\My PC (MSI)\Documents\Claude\Projects\Career Ops\career-ops-harsh`
Integrity mode: development

## Context & Positioning Directives
- **Target Startup Environment**: Early-stage Seed to Series A startups looking for an agile, high-bandwidth generalist utility player in the Founder's Office.
- **Flagship Experience**: Lead with Naraina Jewellers titled as `Founder` with label `(0-to-1 Retail Venture)`, showcasing end-to-end ground execution, 3-city manufacturing tours, direct factory MOQ negotiations, Rs 25L+ working capital modeling, and store launch setup ahead of a planned exit.
- **Complementary Moats**: 
  1. High Court litigation at Gandhi & Co. (50+ matters, 100+ hearings, 15+ agreements, Contract Act & NI Act) positioned as unfair advantage in in-house contract risk mitigation, regulatory compliance, and negotiation.
  2. IIM Sirmaur MBA + 98.66% in IMO positioned as quantitative modeling, unit economics, and data-backed business judgment.
- **Rule 2**: Zero hyphens or em-dashes in any generated content. All date ranges must strictly use en-dash (`–`).
- **Rule 3 & 5**: Strictly 2-page PDF, 6 ROLE_PILLARS with exactly 5 bullets each, verified against canonical proof bank.

## Requirements

### R1. Configuration & Narrative Blueprint
Create `outputs/founders_office_generalist/partial_config.json` adhering to SCHEMA_VERSION 3:
- Role: `Founder's Office (Generalist & Operations)`
- Company: `Target Venture`
- Tagline & Summary: Compelling founder-lens narrative highlighting 0-to-1 builder mindset, execution speed, and cross-functional problem solving.
- 6 Role Pillars (5 bullets each, 95–115 chars/line):
  1. Ground Execution & Scrappy Ops
  2. Procurement & Supply Chain
  3. Unit Economics & Cash Flow
  4. Commercial Contracts & Deal Protection
  5. High-Stakes Client & Stakeholder Management
  6. Market Intelligence & Competitor Audits
- Tools: At least 8 tools (MS Excel, Tally ERP, Financial Modeling, Inventory Tracking, Vendor SLAs, Market Intelligence, Contract Review, Regulatory Filings) with 3 grouped categories.
- Numbers That Matter: 4 verified proof points from proof bank.

### R2. Archetype & Bullet Library Calibration
Ensure the `Entrepreneur` archetype in `reference/bullet-library.json` and `reference/profile.json` seamlessly presents Naraina Jewellers as the primary experience with zero date/metric syntax defects, respecting the claims linter allowlist.

### R3. Deterministic Build & QC Pass
Execute `node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..` inside `outputs/founders_office_generalist/`:
- Pass 100% of the 26 QC checks (15 Core QC + 11 User QC).
- Generate `Harsh_Goyal_Founders_Office_Generalist.pdf` with size > 10KB, content density >= 4000 chars, and exact 2-page fit.

## Acceptance Criteria

### Automated Quality Gates
- [ ] Directory `outputs/founders_office_generalist/` exists with valid `partial_config.json` and compiled `config.json`.
- [ ] Build script exits with code 0 and reports `BUILD SUCCESS — all 26 QC checks passed`.
- [ ] `Harsh_Goyal_Founders_Office_Generalist.pdf` exists, has exactly 2 pages, and size > 10KB.
- [ ] Content density >= 4,000 characters and >= 40 bold markers.
- [ ] Zero hyphens (`-`) or em-dashes (`—`) in dynamic bullet content.
- [ ] All numeric tokens verified against `reference/proof-bank.md`.
- [ ] Zero mention of unverified candidate data or predecessor leaks.
