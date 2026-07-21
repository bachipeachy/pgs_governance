# INVARIANT_IN_WORKFLOW_BINDING_V0

## Machine

```yaml
invariant_code: INVARIANT_IN_WORKFLOW_BINDING_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Every IN artifact used as a WF entry node must resolve to a declared IN artifact,
    and each IN artifact may be the entry point of at most one workflow. Shared entry
    intents create ambiguous admission semantics.

  enforcement_stage:
    - compiler_validation

  scope:
    - INTENTS
    - WORKFLOWS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - shared_entry_intent: "Same IN FQDN referenced as start_node by multiple WFs"
    - unresolvable_in: "IN FQDN referenced by WF does not resolve to a declared IN artifact"

  clarification:
    single_binding: >
      An IN artifact is a workflow-specific admission contract. Sharing it
      across workflows would couple admission semantics of distinct workflows.
    fqdn_resolution: >
      The IN node code in the WF nodes map must resolve to a declared IN artifact
      via FQDN. This invariant enforces both resolution and uniqueness.
```

---

## Purpose

Ensure entry intents are dedicated per-workflow and resolvable.

---

## Validation Rules

### Rule: IN Resolves to Declared Artifact

IN node FQDN in each WF must resolve to an IN artifact in the compilation graph.

**Violation**:
```yaml
nodes:
  IN_MISSING_V0:    # Not declared anywhere
    type: IN
```

### Rule: IN Used by At Most One WF

No IN FQDN may appear as start_node in more than one workflow.

**Violation**:
- `WF_REGISTER_ACTOR_V0` start_node → `IN_REGISTER_V0`
- `WF_REGISTER_DEVICE_V0` start_node → `IN_REGISTER_V0`  ← WRONG: same IN

---

## Scope

**Applies to**: All IN artifacts, all WF artifacts

**Does NOT validate**: IN schema content (see INVARIANT_IN_SCHEMA_REQUIRED_V0)

---

## Version History

- **V0**: Initial implementation (2026-05-04)
