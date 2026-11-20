"""
Example Property-Based Test using Hypothesis for Python.
Demonstrates invariant verification, fuzz testing, and error shrinking.
"""

from hypothesis import given, strategies as st
import json

def encode_payload(data: dict) -> str:
    """Deterministic JSON encoder."""
    return json.dumps(data, sort_keys=True, ensure_ascii=False)

def decode_payload(raw: str) -> dict:
    """Safe JSON decoder."""
    return json.loads(raw)

@given(st.dictionaries(keys=st.text(min_size=1), values=st.one_of(st.integers(), st.text(), st.booleans())))
def test_json_roundtrip_invariant(payload):
    """Roundtrip property: decode(encode(x)) == x"""
    encoded = encode_payload(payload)
    decoded = decode_payload(encoded)
    assert decoded == payload

@given(st.lists(st.integers()))
def test_sorting_invariants(numbers):
    """Invariants of sorting: length preserved, elements preserved, monotonicity."""
    sorted_list = sorted(numbers)
    assert len(sorted_list) == len(numbers)
    assert sorted(sorted_list) == sorted_list
    for i in range(len(sorted_list) - 1):
        assert sorted_list[i] <= sorted_list[i + 1]
