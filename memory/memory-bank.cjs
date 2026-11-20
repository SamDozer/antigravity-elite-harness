#!/usr/bin/env node
/**
 * Antigravity Persistent Intelligent Memory Bank
 * Inspired by AgentMemory / Mem0 architecture.
 * Provides deterministic, cross-session, zero-external-dependency memory retrieval.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const GLOBAL_MEMORY_DIR = path.join('C:', 'Users', 'Hossam', '.gemini', 'config', 'memory');
const GLOBAL_MEMORY_FILE = path.join(GLOBAL_MEMORY_DIR, 'memory-bank.jsonl');

function parseArgs() {
  const args = process.argv.slice(2);
  const action = args[0] || 'help';
  const params = {};

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const keyVal = arg.slice(2).split('=');
      const key = keyVal[0];
      if (keyVal.length > 1) {
        params[key] = keyVal.slice(1).join('=');
      } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        params[key] = args[++i];
      } else {
        params[key] = true;
      }
    }
  }
  return { action, params };
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function loadMemories(projectDir) {
  const memories = [];
  const filesToRead = [GLOBAL_MEMORY_FILE];

  if (projectDir) {
    const localFile = path.join(projectDir, '.memory', 'memory-bank.jsonl');
    if (fs.existsSync(localFile)) {
      filesToRead.push(localFile);
    }
  }

  for (const file of filesToRead) {
    if (fs.existsSync(file)) {
      const lines = fs.readFileSync(file, 'utf8').split('\n');
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed) {
          try {
            memories.push(JSON.parse(trimmed));
          } catch (e) {
            // skip malformed line
          }
        }
      }
    }
  }
  return memories;
}

function saveMemory(entry, targetFile = GLOBAL_MEMORY_FILE) {
  ensureDir(path.dirname(targetFile));
  fs.appendFileSync(targetFile, JSON.stringify(entry) + '\n', 'utf8');
}

function tokenize(text) {
  if (!text) return [];
  return text.toLowerCase()
    .replace(/[^a-z0-9_-]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 2);
}

function scoreMemory(entry, queryTokens, targetProject) {
  let score = 0;
  const entryText = `${entry.title} ${entry.content} ${(entry.tags || []).join(' ')}`.toLowerCase();
  const entryTokens = new Set(tokenize(entryText));

  for (const q of queryTokens) {
    if (entryTokens.has(q)) {
      score += 3;
    } else if (entryText.includes(q)) {
      score += 1;
    }
  }

  if (targetProject && entry.project) {
    if (entry.project.toLowerCase() === targetProject.toLowerCase()) {
      score += 5;
    }
  }

  if (entry.category === 'bug_fix' || entry.category === 'api_gotcha') {
    score += 1.5;
  }

  if (entry.verified) {
    score += 1;
  }

  try {
    const ageDays = (Date.now() - new Date(entry.timestamp).getTime()) / (1000 * 60 * 60 * 24);
    if (ageDays < 7) score += 2;
    else if (ageDays < 30) score += 1;
  } catch (e) {}

  return score;
}

function handleRecord(params) {
  const { project, category, title, content, tags, verified, local } = params;

  if (!title || !content) {
    console.error('Error: --title and --content are required to record a memory.');
    process.exit(1);
  }

  const validCategories = ['bug_fix', 'api_gotcha', 'arch_decision', 'lesson'];
  const cat = validCategories.includes(category) ? category : 'lesson';

  const entry = {
    id: `mem_${Date.now()}_${crypto.randomBytes(3).toString('hex')}`,
    timestamp: new Date().toISOString(),
    project: project || 'global',
    category: cat,
    title: String(title).trim(),
    content: String(content).trim(),
    tags: tags ? String(tags).split(',').map(t => t.trim().toLowerCase()) : [],
    verified: Boolean(verified)
  };

  const targetFile = local ? path.join(process.cwd(), '.memory', 'memory-bank.jsonl') : GLOBAL_MEMORY_FILE;
  saveMemory(entry, targetFile);

  console.log(`Memory recorded successfully [${entry.id}]`);
  console.log(`Project: ${entry.project} | Category: ${entry.category}`);
  console.log(`Title: ${entry.title}`);
}

function handleRecall(params) {
  const query = params.query || '';
  const project = params.project;
  const limit = parseInt(params.limit || '5', 10);
  const jsonOutput = Boolean(params.json);

  if (!query && !project) {
    console.error('Error: specify --query or --project to recall memories.');
    process.exit(1);
  }

  const memories = loadMemories(process.cwd());
  const queryTokens = tokenize(query);

  const scored = memories.map(m => ({
    entry: m,
    score: scoreMemory(m, queryTokens, project)
  }));

  scored.sort((a, b) => b.score - a.score);
  const results = scored.filter(s => s.score > 0).slice(0, limit).map(s => s.entry);

  if (jsonOutput) {
    console.log(JSON.stringify(results, null, 2));
    return;
  }

  if (results.length === 0) {
    console.log(`No memories matched query: "${query}" (Project: ${project || 'any'})`);
    return;
  }

  console.log(`=== Recalled ${results.length} Relevant Memories ===\n`);
  for (const m of results) {
    console.log(`- [${m.category.toUpperCase()}] **${m.title}** (Project: ${m.project})`);
    console.log(`  Date: ${m.timestamp.slice(0, 10)} | Verified: ${m.verified ? 'Yes' : 'No'}`);
    console.log(`  ${m.content}`);
    if (m.tags && m.tags.length > 0) {
      console.log(`  Tags: ${m.tags.join(', ')}`);
    }
    console.log('');
  }
}

function handleList(params) {
  const project = params.project;
  const category = params.category;
  const memories = loadMemories(process.cwd());

  const filtered = memories.filter(m => {
    if (project && m.project.toLowerCase() !== project.toLowerCase()) return false;
    if (category && m.category.toLowerCase() !== category.toLowerCase()) return false;
    return true;
  });

  console.log(`Total memories found: ${filtered.length}\n`);
  for (const m of filtered) {
    console.log(`[${m.id}] ${m.timestamp.slice(0, 10)} | ${m.project} | ${m.category} | ${m.title}`);
  }
}

function handleStats() {
  const memories = loadMemories(process.cwd());
  const projectCounts = {};
  const categoryCounts = {};

  for (const m of memories) {
    projectCounts[m.project] = (projectCounts[m.project] || 0) + 1;
    categoryCounts[m.category] = (categoryCounts[m.category] || 0) + 1;
  }

  console.log('=== Memory Bank Statistics ===');
  console.log(`Total Memories: ${memories.length}`);
  console.log('\nBreakdown by Category:');
  for (const [k, v] of Object.entries(categoryCounts)) {
    console.log(`  - ${k}: ${v}`);
  }
  console.log('\nBreakdown by Project:');
  for (const [k, v] of Object.entries(projectCounts)) {
    console.log(`  - ${k}: ${v}`);
  }
}

function handleSyncGotchas(params) {
  const projectDir = params['project-dir'] || process.cwd();
  const gotchasPath = path.join(projectDir, 'gotchas.md');

  if (!fs.existsSync(gotchasPath)) {
    console.log(`No gotchas.md found at ${gotchasPath}. Generating one from memory bank...`);
    const memories = loadMemories(projectDir);
    let md = '# Project Gotchas & Hard-Won Lessons\n\nGenerated from Antigravity Memory Bank.\n\n';
    for (const m of memories) {
      md += `### ${m.title} (${m.category})\n`;
      md += `- **Date:** ${m.timestamp.slice(0, 10)}\n`;
      md += `- **Context:** ${m.content}\n`;
      if (m.tags && m.tags.length) md += `- **Tags:** \`${m.tags.join('`, `')}\`\n`;
      md += '\n';
    }
    fs.writeFileSync(gotchasPath, md, 'utf8');
    console.log(`Created ${gotchasPath} with ${memories.length} entries.`);
    return;
  }

  const content = fs.readFileSync(gotchasPath, 'utf8');
  const sections = content.split(/^###\s+/m).slice(1);
  let imported = 0;

  for (const sec of sections) {
    const lines = sec.split('\n');
    const header = lines[0].trim();
    const body = lines.slice(1).join('\n').trim();

    if (header && body) {
      const entry = {
        id: `mem_imported_${crypto.randomBytes(3).toString('hex')}`,
        timestamp: new Date().toISOString(),
        project: path.basename(projectDir),
        category: header.toLowerCase().includes('bug') ? 'bug_fix' : 'api_gotcha',
        title: header,
        content: body,
        tags: ['imported', 'gotchas'],
        verified: true
      };
      saveMemory(entry);
      imported++;
    }
  }

  console.log(`Synced ${imported} gotchas from ${gotchasPath} into Memory Bank.`);
}

function main() {
  const { action, params } = parseArgs();

  switch (action) {
    case 'record':
      handleRecord(params);
      break;
    case 'recall':
      handleRecall(params);
      break;
    case 'list':
      handleList(params);
      break;
    case 'stats':
      handleStats();
      break;
    case 'sync-gotchas':
      handleSyncGotchas(params);
      break;
    default:
      console.log(`
Antigravity Memory Bank (AgentMemory / Mem0 Architecture)

Usage:
  node memory-bank.cjs record --project <name> --category <cat> --title <title> --content <desc> [--tags a,b] [--verified]
  node memory-bank.cjs recall --query <search> [--project <name>] [--limit 5] [--json]
  node memory-bank.cjs list [--project <name>] [--category <cat>]
  node memory-bank.cjs stats
  node memory-bank.cjs sync-gotchas [--project-dir <path>]

Categories:
  bug_fix, api_gotcha, arch_decision, lesson
`);
  }
}

main();
