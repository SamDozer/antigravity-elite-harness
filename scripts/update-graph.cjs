const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const gPath = path.join(repoRoot, 'graphify-out', 'graph.json');
if (!fs.existsSync(gPath)) {
  console.log('graph.json not found, skipping');
  process.exit(0);
}

const g = JSON.parse(fs.readFileSync(gPath, 'utf8'));

// Scan all skills
const skillsRoot = path.join(repoRoot, 'skills');
const skillFiles = [];
function walk(dir) {
  for (const item of fs.readdirSync(dir)) {
    const full = path.join(dir, item);
    if (fs.statSync(full).isDirectory()) walk(full);
    else skillFiles.push(path.relative(repoRoot, full).replace(/\\/g, '/'));
  }
}
if (fs.existsSync(skillsRoot)) walk(skillsRoot);

const existingIds = new Set(g.nodes.map(n => n.id));
let added = 0;

if (!existingIds.has('scripts/validate_skills.py')) {
  g.nodes.push({
    id: 'scripts/validate_skills.py',
    label: 'validate_skills.py',
    community: 'Quality & CI/CD',
    path: 'scripts/validate_skills.py',
    size: 20
  });
  existingIds.add('scripts/validate_skills.py');
}
if (!existingIds.has('rules/global-core.md')) {
  g.nodes.push({
    id: 'rules/global-core.md',
    label: 'global-core.md',
    community: 'Observability & Rules',
    path: 'rules/global-core.md',
    size: 15
  });
  existingIds.add('rules/global-core.md');
}

for (const sf of skillFiles) {
  if (!existingIds.has(sf)) {
    let community = 'Skills: Core';
    if (sf.startsWith('skills/frontend/')) community = 'Skills: Frontend';
    else if (sf.startsWith('skills/comp-bio/')) community = 'Skills: CompBio';

    g.nodes.push({
      id: sf,
      label: path.basename(sf),
      community,
      path: sf,
      size: sf.endsWith('SKILL.md') ? 15 : 10
    });
    existingIds.add(sf);
    added++;

    if (sf.endsWith('SKILL.md')) {
      g.edges.push({
        source: 'scripts/validate_skills.py',
        target: sf,
        label: 'validates'
      });
      g.edges.push({
        source: 'tests/run-audit.cjs',
        target: sf,
        label: 'audits'
      });
    }
  }
}

const commSet = new Set(g.nodes.map(n => n.community));
g.communities = Array.from(commSet);
g.total_nodes = g.nodes.length;
g.total_edges = g.edges.length;
g.timestamp = new Date().toISOString();

const degrees = {};
for (const e of g.edges) {
  degrees[e.source] = (degrees[e.source] || 0) + 1;
  degrees[e.target] = (degrees[e.target] || 0) + 1;
}
const sortedGods = Object.entries(degrees)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 6)
  .map(([id, degree]) => ({ id, degree }));
g.god_nodes = sortedGods;

fs.writeFileSync(gPath, JSON.stringify(g, null, 2), 'utf8');

let report = '# Knowledge Graph Architectural Report: Antigravity Elite Harness\n\n';
report += 'Generated at: ' + g.timestamp + '\n\n';
report += '## Executive Summary\n';
report += '- **Total Graph Nodes:** ' + g.total_nodes + '\n';
report += '- **Total Edges:** ' + g.total_edges + '\n';
report += '- **Detected Functional Communities:** ' + g.communities.length + '\n\n';
report += '## Functional Communities\n';

for (const comm of g.communities) {
  const commNodes = g.nodes.filter(n => n.community === comm);
  report += '### ' + comm + ' (' + commNodes.length + ' components)\n';
  for (const n of commNodes.slice(0, 8)) {
    report += '- `' + n.id + '`\n';
  }
  if (commNodes.length > 8) {
    report += '- *...and ' + (commNodes.length - 8) + ' more*\n';
  }
  report += '\n';
}

report += '## God Nodes / Central Architectural Hubs\n';
for (const gn of g.god_nodes) {
  report += '- **`' + gn.id + '`** (Centrality Degree: ' + gn.degree + ')\n';
}

report += '\n## Suggested Graph Explorations\n';
report += '1. **Trace skills architecture validation:** `scripts/validate_skills.py` -> `skills/frontend/ui-visual-qa/SKILL.md` -> `skills/frontend/ui-visual-qa/scripts/visual_audit.mjs`\n';
report += '2. **Trace biological data governance:** `rules/global-core.md` -> `skills/comp-bio/bio-orchestrator/scripts/inspect_biofile.py` -> `skills/comp-bio/bio-sequence-stats/scripts/stats_guard.py`\n';
report += '3. **Trace 8-vector diff review:** `skills/core/diff-reviewer/scripts/review_diff.py` -> `tests/run-audit.cjs` -> `hooks/pre-tool-guard.cjs`\n';

fs.writeFileSync(path.join(repoRoot, 'graphify-out', 'GRAPH_REPORT.md'), report, 'utf8');
console.log('Updated graphify: ' + g.total_nodes + ' nodes, ' + g.total_edges + ' edges across ' + g.communities.length + ' communities.');
