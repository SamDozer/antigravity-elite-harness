#!/usr/bin/env node
/**
 * Antigravity Conversation Trace & Observability Analyzer
 * Parses Antigravity transcript.jsonl to extract execution metrics, tool latencies, and error patterns.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

async function analyzeTranscript(filePath) {
  if (!fs.existsSync(filePath)) {
    console.error(`Error: Transcript file not found at: ${filePath}`);
    process.exit(1);
  }

  const fileStream = fs.createReadStream(filePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let totalSteps = 0;
  const toolCounts = {};
  const failedTools = [];
  let userTurns = 0;
  let modelResponses = 0;
  let firstTimestamp = null;
  let lastTimestamp = null;

  for await (const line of rl) {
    if (!line.trim()) continue;
    try {
      const step = JSON.parse(line);
      totalSteps++;

      if (step.created_at) {
        if (!firstTimestamp) firstTimestamp = new Date(step.created_at);
        lastTimestamp = new Date(step.created_at);
      }

      if (step.type === 'USER_INPUT') {
        userTurns++;
      } else if (step.type === 'PLANNER_RESPONSE') {
        modelResponses++;
      }

      if (step.tool_calls && Array.isArray(step.tool_calls)) {
        for (const tc of step.tool_calls) {
          const toolName = tc.name || 'unknown_tool';
          toolCounts[toolName] = (toolCounts[toolName] || 0) + 1;
        }
      }

      if (step.status === 'ERROR') {
        failedTools.push({
          step: step.step_index,
          error: (step.content || '').slice(0, 150)
        });
      }
    } catch (e) {
      // ignore partial lines
    }
  }

  const durationSec = (firstTimestamp && lastTimestamp) 
    ? Math.round((lastTimestamp - firstTimestamp) / 1000) 
    : 0;

  console.log('\n==========================================================');
  console.log(' ANTIGRAVITY AGENT OBSERVABILITY & TRACE REPORT           ');
  console.log('==========================================================');
  console.log(`Transcript File : ${filePath}`);
  console.log(`Total Steps     : ${totalSteps}`);
  console.log(`User Turns      : ${userTurns}`);
  console.log(`Model Responses : ${modelResponses}`);
  console.log(`Session Duration: ${Math.floor(durationSec / 60)}m ${durationSec % 60}s`);

  console.log('\n[Tool Usage Breakdown]:');
  const sortedTools = Object.entries(toolCounts).sort((a, b) => b[1] - a[1]);
  if (sortedTools.length === 0) {
    console.log('  (No tool calls recorded)');
  } else {
    for (const [name, count] of sortedTools) {
      console.log(`  - ${name.padEnd(25)}: ${count}`);
    }
  }

  console.log(`\n[Execution Failures / Retries]: ${failedTools.length}`);
  if (failedTools.length > 0) {
    for (const f of failedTools.slice(0, 5)) {
      console.log(`  - Step ${f.step}: ${f.error.replace(/\n/g, ' ')}...`);
    }
    if (failedTools.length > 5) {
      console.log(`  ... and ${failedTools.length - 5} more`);
    }
  }
  console.log('==========================================================\n');
}

const targetPath = process.argv[2];
if (!targetPath) {
  console.log('Usage: node trace-analyzer.cjs <path/to/transcript.jsonl>');
  process.exit(1);
}

analyzeTranscript(targetPath);
