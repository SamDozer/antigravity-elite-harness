#!/usr/bin/env node
/**
 * Antigravity Beads Durable Task Engine
 * Implements a dependency-aware Directed Acyclic Graph (DAG) for agent tasks.
 * Prevents context loss across compaction, crashes, and multi-session workflows.
 */

const fs = require('fs');
const path = require('path');

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

function getTaskFilePath(dir) {
  const baseDir = dir || process.cwd();
  return path.join(baseDir, 'tasks.json');
}

function loadTasks(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (err) {
    console.error(`Error reading ${filePath}: ${err.message}`);
    process.exit(1);
  }
}

function saveTasks(filePath, data) {
  data.updated_at = new Date().toISOString();
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

function handleInit(params) {
  const filePath = getTaskFilePath(params.dir);
  if (fs.existsSync(filePath) && !params.force) {
    console.log(`tasks.json already exists at ${filePath}. Use --force to reinitialize.`);
    return;
  }

  const project = params.project || path.basename(params.dir || process.cwd());
  const initialData = {
    project,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    tasks: []
  };

  saveTasks(filePath, initialData);
  console.log(`Initialized Beads task graph at ${filePath} for project "${project}".`);
}

function handleAdd(params) {
  const filePath = getTaskFilePath(params.dir);
  const data = loadTasks(filePath);
  if (!data) {
    console.error(`tasks.json not found at ${filePath}. Run 'init' first.`);
    process.exit(1);
  }

  const { id, title, role, desc, depends, inputs, outputs } = params;
  if (!id || !title || !role) {
    console.error('Error: --id, --title, and --role are required.');
    process.exit(1);
  }

  if (data.tasks.some(t => t.id === id)) {
    console.error(`Error: Task with id "${id}" already exists.`);
    process.exit(1);
  }

  const depList = depends ? String(depends).split(',').map(s => s.trim()).filter(Boolean) : [];
  for (const dep of depList) {
    if (!data.tasks.some(t => t.id === dep)) {
      console.warn(`Warning: Dependency "${dep}" is not yet defined in tasks.json.`);
    }
  }

  const newTask = {
    id: String(id).trim(),
    title: String(title).trim(),
    description: desc ? String(desc).trim() : '',
    assigned_role: String(role).trim(),
    status: 'pending', // pending, in_progress, blocked, ready_for_review, verified, closed
    depends_on: depList,
    inputs: inputs ? String(inputs).split(',').map(s => s.trim()).filter(Boolean) : [],
    outputs: outputs ? String(outputs).split(',').map(s => s.trim()).filter(Boolean) : [],
    verification_evidence: null,
    created_at: new Date().toISOString()
  };

  data.tasks.push(newTask);
  saveTasks(filePath, data);
  console.log(`Task [${newTask.id}] "${newTask.title}" added successfully (Role: ${newTask.assigned_role}).`);
}

function handleNext(params) {
  const filePath = getTaskFilePath(params.dir);
  const data = loadTasks(filePath);
  if (!data) {
    console.error(`tasks.json not found at ${filePath}.`);
    process.exit(1);
  }

  const closedSet = new Set(
    data.tasks.filter(t => t.status === 'closed' || t.status === 'verified').map(t => t.id)
  );

  const ready = data.tasks.filter(t => {
    if (t.status !== 'pending') return false;
    // all dependencies must be closed/verified
    return t.depends_on.every(dep => closedSet.has(dep));
  });

  if (ready.length === 0) {
    const inProgress = data.tasks.filter(t => t.status === 'in_progress');
    const blocked = data.tasks.filter(t => t.status === 'blocked');
    const underReview = data.tasks.filter(t => t.status === 'ready_for_review');

    console.log('No pending tasks are currently ready to pick up.');
    if (inProgress.length > 0) console.log(`- In Progress: ${inProgress.map(t => t.id).join(', ')}`);
    if (underReview.length > 0) console.log(`- Awaiting Review: ${underReview.map(t => t.id).join(', ')}`);
    if (blocked.length > 0) console.log(`- Blocked: ${blocked.map(t => t.id).join(', ')}`);
    return;
  }

  console.log(`=== Ready Next Tasks (${ready.length}) ===\n`);
  for (const t of ready) {
    console.log(`- [${t.id}] **${t.title}**`);
    console.log(`  Assigned Role: ${t.assigned_role}`);
    if (t.description) console.log(`  Description: ${t.description}`);
    if (t.depends_on.length) console.log(`  Dependencies Met: ${t.depends_on.join(', ')}`);
    if (t.inputs.length) console.log(`  Inputs: ${t.inputs.join(', ')}`);
    if (t.outputs.length) console.log(`  Expected Outputs: ${t.outputs.join(', ')}`);
    console.log('');
  }
}

function handleUpdate(params) {
  const filePath = getTaskFilePath(params.dir);
  const data = loadTasks(filePath);
  if (!data) {
    console.error(`tasks.json not found at ${filePath}.`);
    process.exit(1);
  }

  const { id, status, evidence, reason } = params;
  if (!id) {
    console.error('Error: --id is required.');
    process.exit(1);
  }

  const task = data.tasks.find(t => t.id === id);
  if (!task) {
    console.error(`Error: Task "${id}" not found.`);
    process.exit(1);
  }

  const validStatuses = ['pending', 'in_progress', 'blocked', 'ready_for_review', 'verified', 'closed'];
  if (status && !validStatuses.includes(status)) {
    console.error(`Error: Invalid status "${status}". Allowed: ${validStatuses.join(', ')}`);
    process.exit(1);
  }

  if (status) task.status = status;
  if (evidence) task.verification_evidence = evidence;
  if (reason) task.block_reason = reason;

  if (status === 'closed' && !task.verification_evidence && !params.force) {
    console.warn(`Warning: Closing task [${id}] without explicit verification evidence. Use --evidence "..." or --force.`);
  }

  saveTasks(filePath, data);
  console.log(`Task [${task.id}] updated to status: ${task.status}.`);
}

function handleGraph(params) {
  const filePath = getTaskFilePath(params.dir);
  const data = loadTasks(filePath);
  if (!data) {
    console.error(`tasks.json not found at ${filePath}.`);
    process.exit(1);
  }

  console.log(`=== Beads DAG: ${data.project} ===\n`);

  // Mermaid representation
  console.log('```mermaid');
  console.log('graph TD');
  for (const t of data.tasks) {
    const statusLabel = t.status.toUpperCase();
    console.log(`  ${t.id}["${t.id}: ${t.title} (${statusLabel})"]`);
    for (const dep of t.depends_on) {
      console.log(`  ${dep} --> ${t.id}`);
    }
  }
  console.log('```\n');

  // ASCII status list
  const statusEmoji = {
    pending: '⏳',
    in_progress: '🔄',
    blocked: '⛔',
    ready_for_review: '🔍',
    verified: '✅',
    closed: '🏁'
  };

  for (const t of data.tasks) {
    const icon = statusEmoji[t.status] || '•';
    const deps = t.depends_on.length ? ` (needs: ${t.depends_on.join(', ')})` : '';
    console.log(`${icon} [${t.id}] ${t.title} [${t.assigned_role}] - ${t.status}${deps}`);
  }
}

function handleStatus(params) {
  const filePath = getTaskFilePath(params.dir);
  const data = loadTasks(filePath);
  if (!data) {
    console.error(`tasks.json not found at ${filePath}.`);
    process.exit(1);
  }

  const total = data.tasks.length;
  const completed = data.tasks.filter(t => t.status === 'closed' || t.status === 'verified').length;
  const pct = total === 0 ? 0 : Math.round((completed / total) * 100);

  console.log(`\nProject: ${data.project} | Progress: ${completed}/${total} (${pct}%)\n`);
  console.log('ID\tStatus\t\tRole\t\tTitle');
  console.log('------------------------------------------------------------------');
  for (const t of data.tasks) {
    console.log(`${t.id}\t${t.status.padEnd(14)}\t${t.assigned_role.padEnd(14)}\t${t.title}`);
  }
  console.log('');
}

function main() {
  const { action, params } = parseArgs();

  switch (action) {
    case 'init':
      handleInit(params);
      break;
    case 'add':
      handleAdd(params);
      break;
    case 'next':
      handleNext(params);
      break;
    case 'update':
      handleUpdate(params);
      break;
    case 'graph':
      handleGraph(params);
      break;
    case 'status':
      handleStatus(params);
      break;
    default:
      console.log(`
Antigravity Beads Task Engine (DAG Dependency Tracker)

Usage:
  node beads-tracker.cjs init [--dir <path>] [--project <name>] [--force]
  node beads-tracker.cjs add --id <id> --title <title> --role <role> [--depends d1,d2] [--inputs f1] [--outputs f2]
  node beads-tracker.cjs next [--dir <path>]
  node beads-tracker.cjs update --id <id> --status <status> [--evidence <proof>] [--reason <text>]
  node beads-tracker.cjs graph [--dir <path>]
  node beads-tracker.cjs status [--dir <path>]

Statuses:
  pending, in_progress, blocked, ready_for_review, verified, closed
`);
  }
}

main();
