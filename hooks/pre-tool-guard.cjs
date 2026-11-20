#!/usr/bin/env node
/**
 * Antigravity Pre-Tool Execution Safety Guard
 * Intercepts tool calls on stdin and enforces OS-level policies.
 */

const fs = require('fs');

let rawInput = '';
process.stdin.setEncoding('utf8');

process.stdin.on('data', chunk => {
  rawInput += chunk;
});

process.stdin.on('end', () => {
  try {
    if (!rawInput.trim()) {
      process.stdout.write(JSON.stringify({ decision: 'allow' }));
      return;
    }

    const payload = JSON.parse(rawInput);
    const toolCall = payload.toolCall || {};
    const toolName = toolCall.name || '';
    const args = toolCall.args || {};

    // 1. Audit run_command
    if (toolName === 'run_command' && args.CommandLine) {
      const cmd = args.CommandLine;

      // Rule A: Hard Deny - Private Credential Access
      const credentialPatterns = [
        /\.ssh[\\/](id_rsa|id_ed25519|id_ecdsa|id_dsa)/i,
        /\b(type|cat|Get-Content)\s+.*\.ssh/i,
        /Windows[\\/]System32[\\/]config[\\/](SAM|SYSTEM|SECURITY)/i
      ];

      for (const pattern of credentialPatterns) {
        if (pattern.test(cmd)) {
          const result = {
            decision: 'deny',
            reason: 'HARD SECURITY GATE: Access to private SSH keys and Windows system credential stores is strictly blocked.'
          };
          process.stdout.write(JSON.stringify(result));
          return;
        }
      }

      // Rule B: Force Ask - Destructive Bulk File Deletions
      const destructiveDeletePatterns = [
        /rm\s+-rf\s+[\/\\]/i,
        /rmdir\s+\/s\s+\/q\s+([a-zA-Z]:[\\\/]|\/|\$HOME|~)/i,
        /Remove-Item\s+.*-Recurse\s+.*(-Force)?\s+([a-zA-Z]:[\\\/]|\/|\$HOME|~)/i,
        /format\s+[a-zA-Z]:/i,
        /diskpart/i
      ];

      for (const pattern of destructiveDeletePatterns) {
        if (pattern.test(cmd)) {
          const result = {
            decision: 'force_ask',
            reason: 'DESTRUCTIVE OPERATION WARNING: Recursive system deletion or disk formatting command detected. Explicit human authorization required.'
          };
          process.stdout.write(JSON.stringify(result));
          return;
        }
      }

      // Rule C: Force Ask - Destructive Git History Rewrites
      const gitDestructivePatterns = [
        /git\s+push\s+.*(--force|-f)\b/i,
        /git\s+reset\s+--hard\b/i,
        /git\s+clean\s+.*-fdx?/i
      ];

      for (const pattern of gitDestructivePatterns) {
        if (pattern.test(cmd)) {
          const result = {
            decision: 'force_ask',
            reason: 'GIT INTEGRITY WARNING: Irreversible Git history modification (force push or hard reset) detected. Explicit human confirmation required.'
          };
          process.stdout.write(JSON.stringify(result));
          return;
        }
      }

      // Rule D: Force Ask - Unverified Remote Execution (curl | sh)
      const pipeExecPatterns = [
        /(curl|wget|Invoke-WebRequest|iwr)\b.*\|\s*(sh|bash|iex|Invoke-Expression)\b/i
      ];

      for (const pattern of pipeExecPatterns) {
        if (pattern.test(cmd)) {
          const result = {
            decision: 'force_ask',
            reason: 'UNVERIFIED REMOTE SCRIPT WARNING: Piping remote downloads directly to a shell interpreter detected. Inspect script source before proceeding.'
          };
          process.stdout.write(JSON.stringify(result));
          return;
        }
      }
    }

    // Default: Allow
    process.stdout.write(JSON.stringify({ decision: 'allow' }));
  } catch (err) {
    // Fail closed or allow safely with logging
    process.stdout.write(JSON.stringify({ decision: 'allow' }));
  }
});
