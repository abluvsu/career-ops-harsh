# Career Ops — Harsh Goyal

An open-source, automated career operations and CV compilation repository for **Harsh Goyal**, powered by the [Career Ops Core Engine](https://github.com/abluvsu/career-ops-core).

This repository implements deterministic 2-page CV builds, 26-rule automated quality control gates (Core QC + Candidate QC), proof bank validation, and archetype-driven tailoring for roles in **Founder's Office**, **General Operations**, **Category Management**, and **Corporate / Commercial Law**.

---

## Architecture

Career Ops uses a dual-repository architecture separating personal candidate data from generic compilation logic:

* **Candidate Repository (career-ops-harsh)**: Houses biographical data, verified metrics, archetype bullets, interview stories, and targeted CV outputs.
* **Core Submodule (core/ -> [career-ops-core](https://github.com/abluvsu/career-ops-core))**: Provides WeasyPrint / Puppeteer PDF generation, Zod schemas, quality checks, claims linters, and generic skills.

---

## Quick Start

### 1. Clone with Submodules
`ash
git clone --recurse-submodules https://github.com/abluvsu/career-ops-harsh.git
cd career-ops-harsh
`
If already cloned without submodules:
`ash
git submodule update --init --recursive
`

### 2. Install Dependencies
`ash
cd core
npm install
cd ..
`

### 3. Build a Tailored 2-Page CV
Navigate to any target role output directory and run the compilation engine:
`ash
cd outputs/founders_office_generalist
node ../../core/templates/build.js --in partial_config.json --archetype "Entrepreneur" --data-root ../..
`

---

## Repository Structure

\\\
career-ops-harsh/
├── core/                       # Git submodule pointing to career-ops-core
├── reference/                  # Candidate ground truth
│   ├── profile.json            # Biographical & contact details
│   ├── proof-bank.md           # Canonical verified achievement metrics
│   ├── bullet-library.json     # Archetype-frozen bullet points
│   ├── interview-stories.md    # Structured SPOARL interview stories
│   └── qc-rules.json           # Candidate-specific validation gates
├── outputs/                    # Role-specific application builds
│   ├── founders_office_generalist/
│   ├── bd_key_account_manager/
│   ├── compliance_legal_manager/
│   └── ops_category_manager/
├── AGENTS.md                   # Autonomous agent orchestration rules
├── SPEC.md                     # Candidate specifications and targets
└── LICENSE                     # MIT License
\\\

---

## Open Source License

This project is licensed under the [MIT License](LICENSE).
