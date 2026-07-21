# INVARIANT_CT_TEST_DATA_OUTCOME_DECLARED_V0

## Machine

```yaml
invariant_code: INVARIANT_CT_TEST_DATA_OUTCOME_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0

core:
  summary: >
    Every test case in a TEST_DATA artifact must declare an explicit expected_outcome.
    The outcome is a contract between the test author and the CT implementation —
    it states whether the CT is expected to succeed or raise a VIOLATION.
    Omitting it makes the test ambiguous: a silent default cannot be audited,
    traced, or verified as intentional by a future compiler or reviewer.

  rule: >
    For every TEST_DATA artifact in the compiled graph: each test case declared
    in the artifact body must include an explicit expected_outcome field.
    Valid values are SUCCESS and VIOLATION. A test case without expected_outcome
    is an undeclared behavioral contract — the compiler MUST NOT silently assume
    SUCCESS. The test author must state the expected outcome explicitly so that
    the conformance test runner can verify the CT behaves as contracted.

  scope:
    - TEST_DATA

```

---

## Summary

The `expected_outcome` field in a CT conformance test case is not optional metadata —
it is the contract assertion. When a CT is expected to raise a `VIOLATION` outcome
(e.g., input fails validation), the test case must declare `expected_outcome: VIOLATION`.
When the CT is expected to succeed, the test case must declare `expected_outcome: SUCCESS`.

A compiler that silently defaults missing `expected_outcome` to `SUCCESS` produces
conformance tests that never test the failure path — `VIOLATION` cases appear to pass
because the runner treats them as success cases.

## Rule

For every TEST_DATA artifact:

1. Every `### Case N:` yaml block MUST include `expected_outcome` as an explicit field.
2. Valid values are `SUCCESS` and `VIOLATION`.
3. The compiler MUST NOT default `expected_outcome` when it is absent — absence is a violation.
4. The test runner MUST use the declared `expected_outcome` to determine whether the
   CT invocation is expected to raise an exception (VIOLATION) or return a result (SUCCESS).

## Enforcement Scope

- **Artifact Types**: TEST_DATA
- **Validation Phase**: compile_time (S4 GOVERN)
- **Enforced By**: ASSERT_CT_TEST_DATA_OUTCOME_DECLARED_V0

## Rationale

This invariant exists because omitting `expected_outcome` is a silent ambiguity.
A test case that expects VIOLATION but lacks the declaration will be compiled as
a SUCCESS test. The CT will raise an exception, the runner will report a conformance
failure — but the failure is not "CT is wrong," it is "test case is underspecified."

Without this invariant, a compiler implementation that encounters a missing
`expected_outcome` has no governance signal telling it to reject the input.
It either defaults silently (Bug 2) or fails cryptically at test run time.

With this invariant, a missing `expected_outcome` is a named compile-time violation:
`fb.topology::INVARIANT_CT_TEST_DATA_OUTCOME_DECLARED_V0` — findable, traceable,
correctable at the source before any test is run.

## Version History

- **V0**: Initial invariant requiring explicit expected_outcome in all CT test cases (2026-06-03)
