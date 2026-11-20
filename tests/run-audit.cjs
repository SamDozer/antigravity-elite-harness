const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('====================================================');
console.log('🧪 ANTIGRAVITY COMPREHENSIVE RUNTIME VERIFICATION');
console.log('====================================================\n');

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
  const script = 'C:\\Users\\Hossam\\.gemini\\config\\scripts\\memory\\memory-bank.cjs';
  execSync(`node "${script}" record --project test-proj --category lesson --title "Memory Test" --content "Testing persistence" --verified`, { stdio: 'pipe' });
  const recallOut = execSync(`node "${script}" recall --query "persistence" --project test-proj --json`, { encoding: 'utf8' });
  const parsed = JSON.parse(recallOut);
  if (!parsed.length || parsed[0].title !== 'Memory Test') {
    throw new Error('Memory recall output did not match expected entry');
  }
});

// 2. Beads DAG Engine
runCheck('Beads DAG Engine: Init, Add, Next & Graph', () => {
  const script = 'C:\\Users\\Hossam\\.gemini\\config\\scripts\\tasks\\beads-tracker.cjs';
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

// 3. Pre-Tool Safety Guard
runCheck('Pre-Tool Safety Guard: Allow Safe, Deny Credential, Force Ask Destructive', () => {
  const script = 'C:\\Users\\Hossam\\.gemini\\config\\scripts\\pre-tool-guard.cjs';

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
runCheck('Trace Analyzer: Parses Conversation Logs', () => {
  const script = 'C:\\Users\\Hossam\\.gemini\\config\\scripts\\trace-analyzer.cjs';
  const transcriptPath = 'C:\\Users\\Hossam\\.gemini\\antigravity\\brain\\2a5de88f-20c2-4e14-8edf-3ef81e73644a\\.system_generated\\logs\\transcript.jsonl';
  const out = execSync(`node "${script}" "${transcriptPath}"`, { encoding: 'utf8' });
  if (!out.includes('ANTIGRAVITY AGENT OBSERVABILITY & TRACE REPORT') || !out.includes('Total Steps')) {
    throw new Error('Trace analyzer did not output expected summary');
  }
});

console.log('\n====================================================');
console.log(`VERIFICATION SUMMARY: ${results.filter(r => r.status === 'PASS').length}/${results.length} PASSED`);
console.log('====================================================');
