# ASSERT_HANDLER_REGISTRY_CLOSED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_HANDLER_REGISTRY_CLOSED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: V0

governed_by:
  - fb.constitution::INVARIANT_HANDLER_REGISTRY_CLOSED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_handler_registry_closed_v0
  callable: execute
```

## Summary

Verifies every ASSERT artifact in the compiled set has its implementation handler
registered in the static HANDLER_REGISTRY before the ASSERT phase executes.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All build contexts

---

## Purpose

Enforce INVARIANT_HANDLER_REGISTRY_CLOSED_V0 during compilation.

Scans all ASSERT artifacts in the compiled set. For each, resolves the
`implementation.module` declared in its frontmatter against the static
HANDLER_REGISTRY. Any ASSERT artifact whose handler is absent from the registry
is a conformance violation — the build cannot proceed with an incomplete enforcement
surface.

This assertion enforces the closed-world assumption: the registry is the sole
authority for handler resolution. Dynamic discovery via importlib or filesystem
scanning is forbidden.
