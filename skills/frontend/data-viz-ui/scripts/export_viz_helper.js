#!/usr/bin/env node
/**
 * export_viz_helper.js - CLI & module helper for exporting visualization data.
 * Converts JSON records to standard RFC 4180 CSV and wraps raw SVG fragments
 * into standalone, downloadable SVG files with XML namespaces.
 */

const fs = require('fs');
const path = require('path');

function jsonToCsv(records) {
  if (!Array.isArray(records) || records.length === 0) return '';
  const headers = Object.keys(records[0]);
  const rows = [headers.join(',')];

  for (const r of records) {
    const values = headers.map(h => {
      let val = r[h] !== undefined && r[h] !== null ? String(r[h]) : '';
      if (val.includes(',') || val.includes('"') || val.includes('\n')) {
        val = `"${val.replace(/"/g, '""')}"`;
      }
      return val;
    });
    rows.push(values.join(','));
  }
  return rows.join('\n');
}

function wrapStandaloneSvg(svgFragment) {
  if (svgFragment.includes('xmlns="http://www.w3.org/2000/svg"')) {
    return svgFragment;
  }
  return svgFragment.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2 || !['--csv', '--svg'].includes(args[0])) {
    console.log('Usage: node export_viz_helper.js --csv <input.json> [output.csv]');
    console.log('       node export_viz_helper.js --svg <input.svg> [output.svg]');
    process.exit(0);
  }

  const mode = args[0];
  const inputPath = args[1];
  const outputPath = args[2] || (mode === '--csv' ? 'export.csv' : 'export.svg');

  const content = fs.readFileSync(inputPath, 'utf8');
  if (mode === '--csv') {
    const data = JSON.parse(content);
    const csv = jsonToCsv(data);
    fs.writeFileSync(outputPath, csv, 'utf8');
    console.log(`[PASS] Exported ${data.length} records to ${outputPath}`);
  } else {
    const cleanSvg = wrapStandaloneSvg(content);
    fs.writeFileSync(outputPath, cleanSvg, 'utf8');
    console.log(`[PASS] Exported standalone SVG to ${outputPath}`);
  }
}

module.exports = { jsonToCsv, wrapStandaloneSvg };
