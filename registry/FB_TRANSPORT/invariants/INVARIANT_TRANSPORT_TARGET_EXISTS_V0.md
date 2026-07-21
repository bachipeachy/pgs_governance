# INVARIANT_TRANSPORT_TARGET_EXISTS_V0

## Machine

```yaml
invariant_code: INVARIANT_TRANSPORT_TARGET_EXISTS_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Every TI_ artifact MUST declare an explicit workflow binding, and the declared
    workflow MUST exist in the compiled artifact set.

    Transport ingress is the system boundary. It must be fully closed at compile time:
    - The target workflow is declared statically (no inference, no fallback resolution)
    - The declared workflow FQDN resolves to an existing WF artifact
    - No TI_ artifact may be admitted without a resolvable target

    This invariant ensures that no transport ingress point leads to a dead end at
    runtime. Every admitted payload has a guaranteed, verified execution target.

  enforcement_stage:
    - compiler_validation

  scope:
    - TRANSPORT_INGRESS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - missing_workflow_binding: >
        TI artifact omits core.workflow field
    - unresolvable_workflow_ref: >
        TI core.workflow declares a WF FQDN that does not exist in the snapshot
    - dynamic_workflow_ref: >
        TI core.workflow uses a runtime-computed reference ($ prefix)
    - null_or_empty_workflow: >
        TI core.workflow is declared but empty or null
```

---

## Purpose

Every transport ingress must have a verified, static workflow target. A TI_ artifact
with no resolvable workflow binding is a dead letter — a boundary with no destination.
The compiler enforces this at build time so runtime never encounters an unroutable payload.

---

## Scope

**Applies to:** All TI_ artifacts

**Does NOT apply to:**
- TE_ artifacts (egress has no workflow binding)
- WF_ artifacts (workflows declare their own steps, not transport bindings)
