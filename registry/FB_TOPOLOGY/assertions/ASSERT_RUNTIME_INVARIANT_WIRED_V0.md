# ASSERT_RUNTIME_INVARIANT_WIRED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_RUNTIME_INVARIANT_WIRED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_RUNTIME_INVARIANT_WIRED_V0

scope:
  applies_to:
    - PLATFORM

implementation:
  module: pgs_governance.registry.handlers.assert_runtime_invariant_wired_v0
  callable: execute
```

## Summary

For every INVARIANT whose `core.enforcement_stage` contains `runtime_outcome`,
verifies the declared `core.runtime_binding` is wired to a real enforcement point:

1. the `enforced_by` CC exists and declares `violation_outcome` in its `result_surface`;
2. the `enforcing_workflow` contains that CC as a node and routes `violation_outcome`
   to `terminal_node`;
3. `terminal_node` exists in that workflow.

Reads only artifact data (WF/CC frontmatter). Does not change the compiler or the
runtime — enforcement remains the existing CC outcome routing; this assertion only
proves the binding so that no runtime invariant is decorative.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All INVARIANT artifacts with a runtime enforcement stage

## Version History

- **V0**: Initial runtime-invariant wiring assertion (2026-06-14)
