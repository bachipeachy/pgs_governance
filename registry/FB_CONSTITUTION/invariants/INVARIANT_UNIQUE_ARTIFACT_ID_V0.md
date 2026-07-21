# INVARIANT_UNIQUE_ARTIFACT_ID_V0

## Machine

```yaml
invariant_code: INVARIANT_UNIQUE_ARTIFACT_ID_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: Each fqdn_id must be unique across compilation graph

  enforcement_stage:
    - compiler_validation

  scope:
    - ALL_ARTIFACT_KINDS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - duplicate_fqdn: "Multiple artifacts share same fqdn_id"
```

---

## Purpose

Ensures that every artifact in the compilation graph has a globally unique identity (FQDN).
Prevents silent overwrites where multiple physical files claim the same logical identity.
