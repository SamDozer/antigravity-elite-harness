/**
 * Example Property-Based Test using fast-check for TypeScript / JavaScript
 * Demonstrates invariant testing and roundtrip serialization checks.
 */

import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';

// System Under Test (SUT) example: URL Query String Serializer
function serializeParams(params: Record<string, string>): string {
  return Object.entries(params)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');
}

function deserializeParams(queryString: string): Record<string, string> {
  if (!queryString) return {};
  const out: Record<string, string> = {};
  for (const pair of queryString.split('&')) {
    const [k, v] = pair.split('=');
    out[decodeURIComponent(k)] = decodeURIComponent(v || '');
  }
  return out;
}

describe('Property-Based Invariants with fast-check', () => {
  it('Roundtrip property: deserialize(serialize(params)) == params', () => {
    fc.assert(
      fc.property(
        fc.dictionary(fc.string({ minLength: 1 }), fc.string()),
        (original) => {
          const serialized = serializeParams(original);
          const recovered = deserializeParams(serialized);
          expect(recovered).toEqual(original);
        }
      ),
      { numRuns: 200 }
    );
  });

  it('Idempotence property: serialize(serialize_params) is deterministic', () => {
    fc.assert(
      fc.property(
        fc.dictionary(fc.string({ minLength: 1 }), fc.string()),
        (params) => {
          const first = serializeParams(params);
          const second = serializeParams(params);
          expect(first).toBe(second);
        }
      )
    );
  });
});
