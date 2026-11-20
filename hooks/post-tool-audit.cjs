#!/usr/bin/env node
/**
 * Antigravity Post-Tool Execution Auditor
 * Inspects file writes and modifications for secret leaks and security hygiene.
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
      process.stdout.write(JSON.stringify({}));
      return;
    }

    const payload = JSON.parse(rawInput);
    const toolCall = payload.toolCall || {};
    const toolName = toolCall.name || '';
    const args = toolCall.args || {};

    let contentToCheck = '';
    if (args.Content) contentToCheck += args.Content;
    if (args.Replacement) contentToCheck += args.Replacement;

    if (contentToCheck) {
      const secretPatterns = [
        { name: 'Google API Key', regex: /AIzaSy[0-9A-Za-z-_]{33}/ },
        { name: 'OpenAI Secret Key', regex: /sk-[a-zA-Z0-9]{32,}/ },
        { name: 'GitHub Personal Token', regex: /ghp_[a-zA-Z0-9]{36}/ },
        { name: 'AWS Access Key ID', regex: /AKIA[0-9A-Z]{16}/ },
        { name: 'Generic Private Key Block', regex: /-----BEGIN\s+(RSA|EC|OPENSSH|PGP)?\s*PRIVATE KEY-----/i }
      ];

      for (const pattern of secretPatterns) {
        if (pattern.regex.test(contentToCheck)) {
          console.error(`\n[SECURITY ALERT] Post-tool audit detected potential secret leak (${pattern.name}) written to ${args.Path || 'file'}. Ensure this is loaded via environment variables or secret managers.`);
          break;
        }
      }
    }

    process.stdout.write(JSON.stringify({}));
  } catch (err) {
    process.stdout.write(JSON.stringify({}));
  }
});
