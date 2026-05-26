"""
trace_oracle.py — Trace validation oracle (registry layer)

This module provides trace validation for conformance testing.

ARCHITECTURAL BOUNDARY:
- Structure: Implements test case loading (structure.loading.test_case_provider)
- Governance: Implements trace validation logic (this file)

Refactored to use structure.loading for file loading.
"""

from __future__ import annotations

import json
from typing import List, Dict, Any

# Import test case loading from structure
from pgs_governance.implementation.structure.loading.test_case_provider import (
    TestCase,
    load_test_cases,
    TestCaseLoadError,
)


class TraceOracleError(AssertionError):
    """Custom exception for trace oracle failures (registry validation)."""
    pass


def _is_sub_dict(sub: Dict[str, Any], main: Dict[str, Any]) -> bool:
    """
    Check if `sub` is a sub-dictionary of `main`.

    Governance validation helper: Used for pattern matching in trace validation.

    Args:
        sub: Expected sub-dictionary (pattern).
        main: Actual dictionary (full event).

    Returns:
        True if all items in sub exist in main.
    """
    return all(item in main.items() for item in sub.items())


def assert_trace_subsequence(
    actual_trace: List[Dict[str, Any]],
    expected_trace: List[Dict[str, Any]],
) -> None:
    """
    Assert that the expected trace is a subsequence of the actual trace.

    GOVERNANCE VALIDATION:
    This function enforces conformance by verifying that all events in
    `expected_trace` appear in `actual_trace` in the same relative order.

    An expected event matches an actual event if the expected event is a
    "sub-dictionary" of the actual event. This means all key-value pairs
    in the expected event must exist in the actual event.

    Args:
        actual_trace: Actual execution trace from runtime.
        expected_trace: Expected trace pattern from test case.

    Raises:
        TraceOracleError: If expected trace pattern not found in actual trace.

    Example:
        Expected: [{"event": "START"}, {"event": "DONE"}]
        Actual:   [{"event": "START", "time": 123}, {"event": "LOG"}, {"event": "DONE", "time": 456}]
        → PASS (subsequence found, extra fields and events ignored)
    """
    if not actual_trace:
        raise TraceOracleError("Actual trace is empty or missing.")

    expected_cursor = 0
    actual_cursor = 0

    while expected_cursor < len(expected_trace) and actual_cursor < len(actual_trace):
        expected_event = expected_trace[expected_cursor]
        actual_event = actual_trace[actual_cursor]

        if _is_sub_dict(expected_event, actual_event):
            expected_cursor += 1

        actual_cursor += 1

    if expected_cursor < len(expected_trace):
        failed_event = expected_trace[expected_cursor]
        raise TraceOracleError(
            f"Trace subsequence mismatch.\n"
            f"Failed to find expected event #{expected_cursor + 1}: {json.dumps(failed_event)}\n\n"
            f"Expected Trace Pattern:\n{json.dumps(expected_trace, indent=2)}\n\n"
            f"Actual Trace:\n{json.dumps(actual_trace, indent=2)}"
        )


# Re-export for convenience
__all__ = [
    "TestCase",
    "load_test_cases",
    "TestCaseLoadError",
    "TraceOracleError",
    "assert_trace_subsequence",
]


if __name__ == "__main__":
    # This will be the test runner entry point.
    # It will:
    # 1. Parse command-line arguments for the test file path.
    # 2. Load the test cases using `load_test_cases` (from structure).
    # 3. For each test case:
    #    a. Instantiate and run the `ProtocolEmulator` (from Step 2).
    #    b. Get the `actual_trace` from the emulator.
    #    c. Call `assert_trace_subsequence` to validate the result.
    #    d. Print test status.
    print("Trace Oracle - Protocol-First Test Runner (Foundation)")
    print("Ready for ProtocolEmulator integration (Step 2).")
