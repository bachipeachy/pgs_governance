# INVARIANT_BINDING_SURFACE_CLOSED_V0

## Machine

```yaml
invariant_code: INVARIANT_BINDING_SURFACE_CLOSED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    For each CC node in a WF execution graph, all input bindings must reference
    only declared sources:

    - $.payload.<field>        → field must exist in the WF's IN node payload_schema
    - $.results.<NODE>.<field> → NODE must be a CC node in this WF,
                                  field must exist in NODE's CC core.outputs
    - <literal>                → any non-$ string or non-string value is valid

    No binding may reference an undeclared field, an unknown WF node,
    or an undeclared CC output. No unrecognized $ grammar is permitted.

  enforcement_stage:
    - compiler_validation

  scope:
    - WORKFLOWS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - unknown_payload_field: >
        "$.payload.field where field is not in IN node payload_schema"
    - unknown_wf_node: >
        "$.results.NODE.field where NODE is not a CC node in this WF"
    - unknown_cc_output: >
        "$.results.NODE.field where field is not declared in NODE's CC core.outputs"
    - malformed_results_ref: >
        "$.results without the expected <NODE>.<field> suffix"
    - unrecognized_grammar: >
        "Any $ prefix not matching $.payload.* or $.results.*"

  clarification:
    wf_boundary_only: >
      This invariant covers WF-level node input bindings only.
      CC-internal pipeline step references ($.inputs.*, $.results.step.*)
      are covered by INVARIANT_CC_INPUTS_SATISFIED_V0.
    output_field_not_type: >
      This invariant validates that output fields EXIST in core.outputs.
      It does NOT validate type compatibility between binding source and target.
    literals_always_valid: >
      Non-string values (bool, int, null) and strings without a $ prefix
      are treated as literal constants and are always valid.
```

---

## Purpose

Guarantee that every WF binding references a source that is declared and reachable.
Any undeclared reference is a protocol violation and must stop the build.

---

## Validation Rules

### Rule 1: Payload Field Must Be Declared

```yaml
# WF node
CC_EXAMPLE_V0:
  type: CC
  inputs:
    user_name: $.payload.user_name  # ❌ Not in IN schema

# IN node
IN_START_V0:
  payload_schema:
    user_id: string  # ✓ Has user_id, NOT user_name
```

**Fix**: Add `user_name` to `IN_START_V0.payload_schema` or use `$.payload.user_id`.

---

### Rule 2: Source Node Must Exist in WF

```yaml
CC_TARGET_V0:
  inputs:
    tier: $.results.CC_GHOST_NODE.tier  # ❌ CC_GHOST_NODE not in this WF
```

**Fix**: Use an existing CC node ID or add `CC_GHOST_NODE` to the WF.

---

### Rule 3: Source Node Output Field Must Be Declared

```yaml
CC_TARGET_V0:
  inputs:
    tier: $.results.CC_RESOLVE_TIER_V0.bad_field  # ❌ bad_field not in outputs

# CC_RESOLVE_TIER_V0 core.outputs:
outputs:
  license_tier: string  # ✓ Only license_tier declared
```

**Fix**: Use `$.results.CC_RESOLVE_TIER_V0.license_tier` or add `bad_field` to CC outputs.

---

## Scope

**Applies to**: All WF artifacts, all CC node input bindings

**Does NOT validate**:
- CC-internal pipeline step references (`$.inputs.*`, `$.results.step.*`)
- Field type compatibility
- Execution ordering (reachability handled by INVARIANT_WF_EXECUTION_PATH_VALID_V0)

---

## Version History

- **V0**: Initial implementation (2026-04-29) - WF Binding Surface Closure
