# SPEC.md — Career Ops Specification for Harsh Goyal

## 0. Overview
Autonomous Career Operating System for **Harsh Goyal**.

## 1. Candidate Ground Truth
- Target Archetypes: Defined in `reference/archetypes.md` (Legal Professional, Business Strategist, Entrepreneur)
- Verified Proof Bank: `reference/proof-bank.md` (10+ verified achievements)
- Frozen Bullets: `reference/bullet-library.json`
- Candidate Profile: `reference/profile.json`

## 2. Build Pipeline
Builds execute via the shared core submodule:
```bash
cd outputs/<role_slug> && \
node ../../core/templates/build.js --in partial_config.json --archetype "<Archetype>" --data-root ../..
```
Stack: Node.js + WeasyPrint + Zod.
Output: Pixel-perfect 2-page PDF in `outputs/<role_slug>/`.
