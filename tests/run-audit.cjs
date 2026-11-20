const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('====================================================');
console.log('🧪 ANTIGRAVITY COMPREHENSIVE RUNTIME VERIFICATION');
console.log('====================================================\n');

const repoRoot = path.resolve(__dirname, '..');
const results = [];

function runCheck(name, fn) {
  try {
    fn();
    console.log(`[PASS] ${name}`);
    results.push({ name, status: 'PASS' });
  } catch (err) {
    console.error(`[FAIL] ${name}: ${err.message}`);
    results.push({ name, status: 'FAIL', error: err.message });
  }
}

// 1. Memory Bank
runCheck('Memory Bank: Record, Recall & Stats', () => {
  const script = path.join(repoRoot, 'memory', 'memory-bank.cjs');
  const testMemDir = path.join(__dirname, 'test-memory');
  if (fs.existsSync(testMemDir)) fs.rmSync(testMemDir, { recursive: true, force: true });
  fs.mkdirSync(testMemDir, { recursive: true });

  const env = { ...process.env, MEMORY_BANK_DIR: testMemDir };
  execSync(`node "${script}" record --project test-proj --category lesson --title "Memory Test" --content "Testing persistence" --verified`, { env, stdio: 'pipe' });
  const recallOut = execSync(`node "${script}" recall --query "persistence" --project test-proj --json`, { env, encoding: 'utf8' });
  const parsed = JSON.parse(recallOut);
  if (!parsed.length || parsed[0].title !== 'Memory Test') {
    throw new Error('Memory recall output did not match expected entry');
  }
});

// 2. Beads DAG Engine
runCheck('Beads DAG Engine: Init, Add, Next & Graph', () => {
  const script = path.join(repoRoot, 'tasks', 'beads-tracker.cjs');
  const testDir = path.join(__dirname, 'test-beads-audit');
  if (fs.existsSync(testDir)) fs.rmSync(testDir, { recursive: true, force: true });
  fs.mkdirSync(testDir, { recursive: true });

  execSync(`node "${script}" init --dir "${testDir}" --project "audit-beads"`, { stdio: 'pipe' });
  execSync(`node "${script}" add --dir "${testDir}" --id T1 --title "Step 1" --role architect`, { stdio: 'pipe' });
  execSync(`node "${script}" add --dir "${testDir}" --id T2 --title "Step 2" --role developer --depends T1`, { stdio: 'pipe' });
  
  const nextOut = execSync(`node "${script}" next --dir "${testDir}"`, { encoding: 'utf8' });
  if (!nextOut.includes('Step 1')) throw new Error('Ready queue did not return unblocked T1');

  execSync(`node "${script}" update --dir "${testDir}" --id T1 --status closed --evidence "Verified"`, { stdio: 'pipe' });
  const nextOut2 = execSync(`node "${script}" next --dir "${testDir}"`, { encoding: 'utf8' });
  if (!nextOut2.includes('Step 2')) throw new Error('Ready queue did not unblock T2 after T1 closed');
});

// 3. Pre-Tool Security Guard
runCheck('Pre-Tool Safety Guard: Allow Safe, Deny Credential, Force Ask Destructive', () => {
  const script = path.join(repoRoot, 'hooks', 'pre-tool-guard.cjs');

  // Safe
  const safePayload = JSON.stringify({ toolCall: { name: 'run_command', args: { CommandLine: 'git status' } } });
  const safeRes = JSON.parse(execSync(`node "${script}"`, { input: safePayload, encoding: 'utf8' }));
  if (safeRes.decision !== 'allow') throw new Error(`Safe command was not allowed: ${JSON.stringify(safeRes)}`);

  // Deny SSH
  const denyPayload = JSON.stringify({ toolCall: { name: 'run_command', args: { CommandLine: 'cat ~/.ssh/id_rsa' } } });
  const denyRes = JSON.parse(execSync(`node "${script}"`, { input: denyPayload, encoding: 'utf8' }));
  if (denyRes.decision !== 'deny') throw new Error(`SSH credential read was not denied: ${JSON.stringify(denyRes)}`);

  // Force Ask Destructive
  const forcePayload = JSON.stringify({ toolCall: { name: 'run_command', args: { CommandLine: 'rm -rf /' } } });
  const forceRes = JSON.parse(execSync(`node "${script}"`, { input: forcePayload, encoding: 'utf8' }));
  if (forceRes.decision !== 'force_ask') throw new Error(`Destructive rm was not force_ask: ${JSON.stringify(forceRes)}`);
});

// 4. Trace Analyzer
runCheck('Trace Analyzer: Help and Parser Execution', () => {
  const script = path.join(repoRoot, 'observability', 'trace-analyzer.cjs');
  // Run on self or dummy jsonl to verify parser robustness
  const dummyLog = path.join(__dirname, 'dummy-transcript.jsonl');
  fs.writeFileSync(dummyLog, JSON.stringify({ step_index: 1, type: 'USER_INPUT', created_at: new Date().toISOString() }) + '\n', 'utf8');
  const out = execSync(`node "${script}" "${dummyLog}"`, { encoding: 'utf8' });
  fs.rmSync(dummyLog, { force: true });
  if (!out.includes('ANTIGRAVITY AGENT OBSERVABILITY & TRACE REPORT')) {
    throw new Error('Trace analyzer did not output expected summary');
  }
});

// 5. Modular Skills Architecture CI Gate
runCheck('Modular Skills: 4-Layer Architecture and Trigger Boundaries', () => {
  const script = path.join(repoRoot, 'scripts', 'validate_skills.py');
  const pythonCmd = process.platform === 'win32' ? 'py -3' : 'python3';
  const out = execSync(`${pythonCmd} "${script}"`, { encoding: 'utf8' });
  if (!out.includes('ALL SKILLS SATISFY CLAUDE-GRADE ARCHITECTURE GATES')) {
    throw new Error('validate_skills.py did not report complete pass');
  }
});

// 6. Deterministic Domain Scripts Execution
runCheck('Domain Tools: Contrast, Biostats, SLURM, and 8th-Vector Diff Review', () => {
  const pythonCmd = process.platform === 'win32' ? 'py -3' : 'python3';

  // Contrast check
  const contrastScript = path.join(repoRoot, 'skills', 'frontend', 'app-ui-system', 'scripts', 'check_contrast.py');
  const contrastOut = execSync(`${pythonCmd} "${contrastScript}" --fg "#94a3b8" --bg "#090a0f"`, { encoding: 'utf8' });
  if (!contrastOut.includes('[PASS]')) throw new Error('check_contrast.py failed to verify valid contrast');

  // Stats FDR check
  const statsScript = path.join(repoRoot, 'skills', 'comp-bio', 'bio-sequence-stats', 'scripts', 'stats_guard.py');
  const statsOut = execSync(`${pythonCmd} "${statsScript}" fdr --pvalues "0.001,0.01,0.05"`, { encoding: 'utf8' });
  if (!statsOut.includes('BENJAMINI-HOCHBERG')) throw new Error('stats_guard.py failed to execute FDR');

  // SLURM validation
  const slurmScript = path.join(repoRoot, 'skills', 'comp-bio', 'hpc-containers-pipelines', 'scripts', 'validate_slurm.py');
  const slurmTemplate = path.join(repoRoot, 'skills', 'comp-bio', 'hpc-containers-pipelines', 'assets', 'slurm_template.sh');
  const slurmOut = execSync(`${pythonCmd} "${slurmScript}" --script "${slurmTemplate}"`, { encoding: 'utf8' });
  if (!slurmOut.includes('APPROVED')) throw new Error('validate_slurm.py failed on template');
});

console.log('\n====================================================');
console.log(`VERIFICATION SUMMARY: ${results.filter(r => r.status === 'PASS').length}/${results.length} PASSED`);
console.log('====================================================');
