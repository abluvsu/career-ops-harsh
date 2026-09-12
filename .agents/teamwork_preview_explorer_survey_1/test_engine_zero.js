const engine = require('../../core/templates/engine.js');
const defaults = require('../../core/templates/config_defaults.json');
const profile = require('../../reference/profile.json');
const bl = require('../../reference/bullet-library.json');

const testConf = {
  ...defaults,
  CV_OUTPUT: "Harsh_Goyal_Founders_Office_Generalist.docx",
  PORTFOLIO_URL_REQUIRED: false,
  COMPETENCIES: [["c1", "c2", "c3"], ["c4", "c5", "c6"], ["c7", "c8", "c9"]],
  PROFILE: profile,
  ROLE: "Founder's Office",
  COMPANY: "Target Venture",
  TAGLINE: "Generalist utility player",
  SUMMARY: "Compelling founder lens narrative highlighting zero to one builder mindset and execution.",
  WHY_I_FIT: "More than many chars of text here to satisfy the length requirement. 50+ matters, 15+ agreements, 30+ consultations, 98.66% in IMO, 25L+ capital, 100+ court appearances, 12+ vendor deals, 3-city sourcing tour across Surat Mumbai Delhi.",
  ROLE_PILLARS: [
    { title: "Pillar 1", bullets: ["b1", "b2", "b3", "b4", "b5"] },
    { title: "Pillar 2", bullets: ["b1", "b2", "b3", "b4", "b5"] },
    { title: "Pillar 3", bullets: ["b1", "b2", "b3", "b4", "b5"] },
    { title: "Pillar 4", bullets: ["b1", "b2", "b3", "b4", "b5"] },
    { title: "Pillar 5", bullets: ["b1", "b2", "b3", "b4", "b5"] },
    { title: "Pillar 6", bullets: ["b1", "b2", "b3", "b4", "b5"] }
  ],
  EXPERIENCE: bl['Entrepreneur'].EXPERIENCE,
  PROJECTS: bl['Entrepreneur'].PROJECTS,
  NUMBERS_THAT_MATTER: [
    { value: "50+", label: "Matters" },
    { value: "15+", label: "Agreements" }
  ],
  TOOLS: "MS Excel, Tally ERP, Financial Modeling, Inventory Tracking, Vendor SLAs, Market Intelligence, Contract Review, Regulatory Filings",
  TOOLS_GROUPED: [
    { category: "Finance", items: "MS Excel, Tally ERP" },
    { category: "Legal", items: "Contract Review, Regulatory Filings" },
    { category: "Ops", items: "Vendor SLAs, Inventory Tracking" }
  ]
};

try {
  engine.validateConfig(testConf);
  console.log('ENGINE VALIDATION PASSED');
} catch (e) {
  console.error('ENGINE VALIDATION THREW:', e.message);
}
