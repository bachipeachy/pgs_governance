# ASSERT_COMPILER_GOVERNANCE_DECLARED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_COMPILER_GOVERNANCE_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: V0

governed_by:
  - fb.constitution::INVARIANT_COMPILER_GOVERNANCE_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_compiler_governance_declared_v0
  callable: execute
```

## Summary

Verifies CONSTITUTION_COMPILER_V0 is present in the compiled artifact set and
declares a non-empty rules list — enforcing COMPILER_SELF_APPLICABLE.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All build contexts

---

## Purpose

Enforce INVARIANT_COMPILER_GOVERNANCE_DECLARED_V0 during compilation.

Locates `fb.constitution::CONSTITUTION_COMPILER_V0` in the compiled artifact set
and verifies its machine block is well-formed (non-empty rules list). Absence of
the compiler constitution from the compiled set is a self-governance violation —
the compiler cannot assert its own conformance without its governing constitution
being present.

This assertion is structural: it checks the artifact exists and has a non-empty
declaration surface. It does NOT verify that the runtime interprets the constitution
to determine execution order.
