# ASSERT_ARTIFACT_CONTENT_HASH_DECLARED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_ARTIFACT_CONTENT_HASH_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: V0

governed_by:
  - fb.constitution::INVARIANT_ARTIFACT_CONTENT_HASH_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_artifact_content_hash_declared_v0
  callable: execute
```

## Summary

Verifies every compiled artifact in the snapshot carries a non-empty content_hash —
confirming full materialization of the compiled set.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All build contexts

---

## Purpose

Enforce INVARIANT_ARTIFACT_CONTENT_HASH_DECLARED_V0 during compilation.

Scans every artifact in the compiled set. Any artifact missing a `content_hash`
field, or with a `content_hash` that is empty or null, is an incomplete
materialization — the MATERIALIZE phase did not fully process it.

A snapshot where any artifact lacks a `content_hash` cannot be integrity-audited,
used for incremental build comparison, or treated as a deterministic output.
The build must fail rather than emit a partial snapshot.
