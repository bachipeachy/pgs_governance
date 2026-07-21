# INVARIANT_ARTIFACT_CONTENT_HASH_DECLARED_V0

## Machine

```yaml
invariant_code: INVARIANT_ARTIFACT_CONTENT_HASH_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_COMPILER_V0

core:
  description: >
    Every artifact in the compiled snapshot MUST have a content_hash field that is
    non-empty. An artifact without a content_hash is not fully materialized — it
    cannot participate in deterministic identity verification, incremental build
    checks, or snapshot integrity audits. A snapshot with any artifact missing a
    content_hash is incomplete and does not satisfy the materialization obligation.

  enforcement_stage:
    - compiler_assert

  scope:
    - ALL_BUILD_CONTEXTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - missing_content_hash: "Compiled artifact has no content_hash field"
    - empty_content_hash: "Compiled artifact has content_hash set to empty string or null"
    - partial_snapshot: "Some artifacts in the compiled set are content-hashed and others are not"
```

---

## Purpose

Enforces the materialization completeness obligation derived from `COMPILER_LOSSLESS_EMISSION`
and the determinism guarantees in §7 of CONSTITUTION_COMPILER_V0.

A `content_hash` declared on every compiled artifact is the minimal verifiable evidence that:
1. The artifact was fully materialized (not partially built)
2. The artifact's identity is stable across compiler runs given identical inputs
3. The snapshot can be integrity-audited without re-running the compiler

An artifact missing a `content_hash` cannot be verified for identity or compared across
snapshot versions. It is an incomplete materialization, not a valid compiled artifact.

## Relationship to CONSTITUTION_COMPILER_V0

Directly enforces `COMPILER_LOSSLESS_EMISSION` (all declared semantics preserved in
materialized output) and `COMPILER_DETERMINISM` (identical inputs → identical outputs)
by making content-hash completeness a compile-time assertion rather than a runtime
assumption.
