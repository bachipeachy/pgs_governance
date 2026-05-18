# ASSERT_COMPILER_NO_EXECUTION_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_COMPILER_NO_EXECUTION_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: V0

governed_by:
  - fb.constitution::INVARIANT_COMPILER_NO_EXECUTION_V0

implementation:
  module: pgs_governance.registry.handlers.assert_compiler_no_execution_v0
  callable: execute
```

## Summary

Verifies compiled CT and CS artifacts do not carry execution-time state fields
in their materialized frontmatter.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All build contexts

---

## Purpose

Enforce INVARIANT_COMPILER_NO_EXECUTION_V0 during compilation.

Scans all CT and CS artifacts in the compiled set. Checks each artifact's
frontmatter for execution-state fields that would only be present if the artifact
was executed during compilation: `trace_id`, `execution_result`, `runtime_output`,
`invocation_id`, `execution_state`, `runtime_state`.

CT and CS artifacts are pure declarations at compile time. A compiled artifact's
frontmatter must reflect declared structure, not execution output. Presence of
execution-state fields indicates the compiler invoked the artifact's implementation
during compilation — a constitutional violation.

This assertion is structural and checkable from the artifact alone.
