# ASSERT_UNIQUE_ARTIFACT_ID_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_UNIQUE_ARTIFACT_ID_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.constitution::INVARIANT_UNIQUE_ARTIFACT_ID_V0

implementation:
  module: pgs_governance.registry.handlers.assert_unique_artifact_id_v0
  callable: execute
```

## Summary

Validates each fqdn_id appears exactly once in compilation graph.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All discovered artifacts

---

## Purpose

Enforce INVARIANT_UNIQUE_ARTIFACT_ID_V0 during compilation.
Scans the raw list of discovered artifacts before any dictionary-based processing
to ensure no two artifacts share the same FQDN.
