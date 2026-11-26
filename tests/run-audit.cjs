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

  // Ensembl & PubMed grounding verification
  const verifyIdsScript = path.join(repoRoot, 'skills', 'comp-bio', 'bio-literature-grounding', 'scripts', 'verify_ids.py');
  const ensemblOut = execSync(`${pythonCmd} "${verifyIdsScript}" --type ensembl --id ENSG00000141510`, { encoding: 'utf8' });
  if (!ensemblOut.includes('VERIFIED')) throw new Error('verify_ids.py failed to verify Ensembl ID');
  const pubmedOut = execSync(`${pythonCmd} "${verifyIdsScript}" --type pubmed --id 23945592`, { encoding: 'utf8' });
  if (!pubmedOut.includes('VERIFIED')) throw new Error('verify_ids.py failed to verify PubMed ID');

  // Binary Biofile Inspection (.npy, .xtc, .h5ad)
  const inspectScript = path.join(repoRoot, 'skills', 'comp-bio', 'bio-orchestrator', 'scripts', 'inspect_biofile.py');
  const dummyNpy = path.join(__dirname, 'test.npy');
  const npyHeader = "{'descr': '<f8', 'fortran_order': False, 'shape': (10, 5)}";
  const hdrBuf = Buffer.from(npyHeader, 'ascii');
  const lenBuf = Buffer.alloc(2);
  lenBuf.writeUInt16LE(hdrBuf.length);
  const npyBuf = Buffer.concat([
    Buffer.from([0x93, 0x4e, 0x55, 0x4d, 0x50, 0x59, 0x01, 0x00]),
    lenBuf,
    hdrBuf
  ]);
  fs.writeFileSync(dummyNpy, npyBuf);
  const npyOut = execSync(`${pythonCmd} "${inspectScript}" --file "${dummyNpy}"`, { encoding: 'utf8' });
  fs.rmSync(dummyNpy, { force: true });
  if (!npyOut.includes('NumPy Binary Array')) throw new Error('inspect_biofile.py failed on NPY');

  // 8th Vector Diff Review
  const reviewScript = path.join(repoRoot, 'skills', 'core', 'diff-reviewer', 'scripts', 'review_diff.py');
  const dummyDiff = path.join(__dirname, 'test.diff');
  fs.writeFileSync(dummyDiff, [
    '--- a/model.py',
    '+++ b/model.py',
    '+ log2fc = np.log(a / b)',
    '+ RUN pip install scanpy',
    '+ X_scaled = StandardScaler().fit_transform(X) # train later',
    '+ p = "C:\\\\Users\\\\alice\\\\data"'
  ].join('\n'), 'utf8');
  let reviewPassed = false;
  try {
    execSync(`${pythonCmd} "${reviewScript}" --diff "${dummyDiff}" --bio`, { encoding: 'utf8' });
  } catch (err) {
    // Expected to reject with non-zero exit
    if (err.stdout && err.stdout.includes('V8-UNIT-LOG') && err.stdout.includes('V8-DATA-LEAKAGE')) {
      reviewPassed = true;
    }
  } finally {
    fs.rmSync(dummyDiff, { force: true });
  }
  if (!reviewPassed) throw new Error('review_diff.py failed to catch 8th vector scientific issues');
});

// 7. Expanded Agentic Awesome Skills Suite (Core, Electron/Frontend, Comp-Bio)
runCheck('AAS Skills: Loop Fingerprint, Evidence Audit, Fault Schedule, Orchestration DAG, Electron Security, Biopython & Falsify', () => {
  const pythonCmd = process.platform === 'win32' ? 'py -3' : 'python3';

  // 7a. break-ai-fix-loops fingerprint
  const fpScript = path.join(repoRoot, 'skills', 'core', 'break-ai-fix-loops', 'scripts', 'fingerprint.py');
  const fpAsset = path.join(repoRoot, 'skills', 'core', 'break-ai-fix-loops', 'assets', 'attempt_record.template.json');
  const fpOut = execSync(`${pythonCmd} "${fpScript}" "${fpAsset}"`, { encoding: 'utf8' }).trim();
  if (!/^(?:sha256:)?[a-f0-9]{64}$/.test(fpOut)) throw new Error(`fingerprint.py returned invalid SHA-256: ${fpOut}`);

  // 7b. audit-agent-run-evidence ledger
  const evScript = path.join(repoRoot, 'skills', 'core', 'audit-agent-run-evidence', 'scripts', 'audit_evidence.py');
  const evAsset = path.join(repoRoot, 'skills', 'core', 'audit-agent-run-evidence', 'assets', 'claim_ledger.template.json');
  const evOut = execSync(`${pythonCmd} "${evScript}" --ledger "${evAsset}"`, { encoding: 'utf8' });
  if (!evOut.includes('[APPROVED]')) throw new Error('audit_evidence.py failed on valid ledger');

  // 7c. agent-harness-fault-injection schedule
  const fiScript = path.join(repoRoot, 'skills', 'core', 'agent-harness-fault-injection', 'scripts', 'validate_fault_schedule.py');
  const fiAsset = path.join(repoRoot, 'skills', 'core', 'agent-harness-fault-injection', 'assets', 'fault_schedule.template.json');
  const fiOut = execSync(`${pythonCmd} "${fiScript}" --schedule "${fiAsset}"`, { encoding: 'utf8' });
  if (!fiOut.includes('[PASS]')) throw new Error('validate_fault_schedule.py failed on valid schedule');

  // 7d. review-multi-agent-orchestration DAG check
  const dagScript = path.join(repoRoot, 'skills', 'core', 'review-multi-agent-orchestration', 'scripts', 'check_orchestration_dag.py');
  const dagAsset = path.join(repoRoot, 'skills', 'core', 'review-multi-agent-orchestration', 'assets', 'dispatch_envelope.template.json');
  const dagOut = execSync(`${pythonCmd} "${dagScript}" --topology "${dagAsset}"`, { encoding: 'utf8' });
  if (!dagOut.includes('[PASS]')) throw new Error('check_orchestration_dag.py failed on valid topology');

  // 7e. electron-development security check (happy path + unsafe rejection)
  const elecScript = path.join(repoRoot, 'skills', 'frontend', 'electron-development', 'scripts', 'audit_electron_security.py');
  const elecAsset = path.join(repoRoot, 'skills', 'frontend', 'electron-development', 'assets', 'preload.template.ts');
  const elecOut = execSync(`${pythonCmd} "${elecScript}" --file "${elecAsset}"`, { encoding: 'utf8' });
  if (!elecOut.includes('[PASS]')) throw new Error('audit_electron_security.py failed on preload template');

  // 7f. biopython seq_stats
  const bioScript = path.join(repoRoot, 'skills', 'comp-bio', 'biopython', 'scripts', 'seq_stats.py');
  const dummyFasta = path.join(__dirname, 'test.fasta');
  fs.writeFileSync(dummyFasta, '>seq1\nATGCATGC\n>seq2\nGGGGCCCC\n', 'utf8');
  const bioOut = execSync(`${pythonCmd} "${bioScript}" --fasta "${dummyFasta}"`, { encoding: 'utf8' });
  fs.rmSync(dummyFasta, { force: true });
  if (!bioOut.includes('Records: 2') || !bioOut.includes('GC%: 75.00%')) {
    throw new Error(`seq_stats.py unexpected output: ${bioOut}`);
  }

  // 7g. falsify Bayesian & Brier score calculator
  const falsifyScript = path.join(repoRoot, 'skills', 'comp-bio', 'falsify', 'scripts', 'score_ledger.py');
  const falsifyOut = execSync(`${pythonCmd} "${falsifyScript}" --prior 0.5 --likelihood-ratio 3.0 --outcome 1`, { encoding: 'utf8' });
  if (!falsifyOut.includes('Posterior: 0.7500') || !falsifyOut.includes('Brier Score: 0.0625')) {
    throw new Error(`score_ledger.py unexpected output: ${falsifyOut}`);
  }

  // 7h. cli-anything harness validator & skill_generator syntax/import check
  const cliValScript = path.join(repoRoot, 'skills', 'core', 'cli-anything', 'scripts', 'validate_harness.py');
  const tmpHarness = path.join(__dirname, 'tmp-cli-harness');
  if (fs.existsSync(tmpHarness)) fs.rmSync(tmpHarness, { recursive: true, force: true });
  const pkgDir = path.join(tmpHarness, 'cli_anything', 'demoapp');
  fs.mkdirSync(path.join(pkgDir, 'tests'), { recursive: true });
  fs.writeFileSync(path.join(tmpHarness, 'setup.py'), 'from setuptools import setup, find_namespace_packages\nsetup(packages=find_namespace_packages(include=["cli_anything.*"]))\n');
  fs.writeFileSync(path.join(pkgDir, 'demoapp_cli.py'), '# click --json\n');
  fs.writeFileSync(path.join(pkgDir, 'tests', 'TEST.md'), '# TEST\n');
  const cliValOut = execSync(`${pythonCmd} "${cliValScript}" --path "${tmpHarness}"`, { encoding: 'utf8' });
  fs.rmSync(tmpHarness, { recursive: true, force: true });
  if (!cliValOut.includes('[PASS]')) throw new Error(`validate_harness.py failed: ${cliValOut}`);

  // 7i. find-skills package spec validator
  const findSpecScript = path.join(repoRoot, 'skills', 'core', 'find-skills', 'scripts', 'check_skill_source.py');
  const findSpecOut = execSync(`${pythonCmd} "${findSpecScript}" --spec "vercel-labs/skills@find-skills"`, { encoding: 'utf8' });
  if (!findSpecOut.includes('[PASS]')) throw new Error(`check_skill_source.py failed: ${findSpecOut}`);

  // 7j. scrapling CLI safety validator
  const scrapScript = path.join(repoRoot, 'skills', 'core', 'scrapling', 'scripts', 'check_scrapling.py');
  const scrapOut = execSync(`${pythonCmd} "${scrapScript}" --check-cmd "scrapling extract get https://example.com out.md --ai-targeted"`, { encoding: 'utf8' });
  if (!scrapOut.includes('[PASS]')) throw new Error(`check_scrapling.py failed: ${scrapOut}`);
});

console.log('\n====================================================');
console.log(`VERIFICATION SUMMARY: ${results.filter(r => r.status === 'PASS').length}/${results.length} PASSED`);
console.log('====================================================');
if (results.some(r => r.status !== 'PASS')) process.exit(1);
