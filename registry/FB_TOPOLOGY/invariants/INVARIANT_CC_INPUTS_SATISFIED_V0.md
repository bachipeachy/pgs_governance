# INVARIANT_CC_INPUTS_SATISFIED_V0

## Machine

```yaml
invariant_code: INVARIANT_CC_INPUTS_SATISFIED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    For each CC node in WF execution graph:
    - All $.payload.* references must exist in IN payload schema
    - All $.results.CC_XXX.* references must satisfy:
      - CC_XXX appears earlier in execution path (dependency ordering)
      - Field exists in CC_XXX outputs
      - CC_XXX is reachable (on same execution path, not different branch)

    This validates AVAILABILITY only, not TYPE SAFETY.
    Field existence ≠ field type correctness.

  enforcement_stage:
    - compiler_validation

  scope:
    - WORKFLOWS
    - CAPABILITY_CONTRACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - undefined_payload_field: "CC references $.payload.field that does not exist in IN schema"
    - undefined_cc_output: "CC references $.results.CC_XXX.field where field does not exist in CC_XXX outputs"
    - forward_reference: "CC references $.results.CC_XXX.* where CC_XXX appears later in execution path"
    - unreachable_reference: "CC references $.results.CC_XXX.* where CC_XXX is on different branch (unreachable)"

  clarification:
    availability_not_type_safety: >
      This invariant validates that referenced fields EXIST.
      It does NOT validate that field TYPES match.
      Example: $.payload.user_id exists ✓, but string vs int is NOT checked.
    per_path_validation: >
      Each execution path validated independently.
      Dependency valid in path A may be invalid in path B.
      No false positives from unreachable branches.
    jsonpath_reference_model: >
      CC inputs use JSONPath to reference data:
      - $.payload.* → from IN node payload
      - $.results.step_name.* → from prior pipeline step outputs
      - $.inputs.* → from CC inputs (WF node bindings)
```

---

## Purpose

Ensure all CC input references resolve to available data sources.

**Core Principle**: No undefined references at compile time.

---

## Validation Rules

### Rule 1: Payload Field Availability

CC inputs referencing `$.payload.*` must match IN payload schema.

**Violation**:
```yaml
# WF node
CC_EXAMPLE_V0:
  type: CC
  inputs:
    user_name: $.payload.user_name  # ❌ Field not in IN schema

# IN node payload_schema
IN_START_V0:
  payload_schema:
    user_id: string    # ✓ Has user_id
    # ❌ Missing user_name
```

**Correct**:
```yaml
# WF node
CC_EXAMPLE_V0:
  inputs:
    user_id: $.payload.user_id  # ✓ Exists in IN schema

# IN node
IN_START_V0:
  payload_schema:
    user_id: string  # ✓ Declared
```

**Detection**: For each `$.payload.X` reference, check X exists in IN node's payload_schema.

---

### Rule 2: CC Output Field Availability

CC inputs referencing `$.results.step_name.field` must satisfy:
1. `step_name` appears earlier in pipeline
2. `field` exists in step's outputs

**Violation - Forward Reference**:
```yaml
pipeline:
  - step: validate
    transform: CT_VALIDATE_V0
    inputs:
      data: $.results.process.data  # ❌ process hasn't run yet

  - step: process
    transform: CT_PROCESS_V0
    outputs:
      data: $.capability_result.value
```

**Violation - Missing Output**:
```yaml
pipeline:
  - step: validate
    transform: CT_VALIDATE_V0
    outputs:
      is_valid: $.capability_result.value
      # ❌ No 'data' output

  - step: process
    transform: CT_PROCESS_V0
    inputs:
      data: $.results.validate.data  # ❌ Field doesn't exist
```

**Correct**:
```yaml
pipeline:
  - step: validate
    transform: CT_VALIDATE_V0
    outputs:
      data: $.capability_result.value  # ✓ Declared

  - step: process
    transform: CT_PROCESS_V0
    inputs:
      data: $.results.validate.data  # ✓ Exists, earlier in pipeline
```

**Detection**:
1. Walk pipeline in order, track available outputs
2. For each `$.results.step_name.field`, check:
   - `step_name` seen earlier (dependency ordering)
   - `field` in step's outputs

---

### Rule 3: Branch Reachability (WF-Level)

CC references must be reachable on same execution path.

**Violation**:
```yaml
# WF nodes
CC_A_V0:
  next:
    SUCCESS: CC_B_V0
    VIOLATION: CC_C_V0

CC_B_V0:
  inputs:
    data: $.results.CC_C_V0.data  # ❌ CC_C on different branch

CC_C_V0:
  outputs:
    data: ...
```

**Detection**: For each execution path, validate references only point to nodes on SAME path.

---

## Scope

**Applies to**:
- All WF artifacts (workflow-level validation)
- All CC artifacts (pipeline-level validation)
- All JSONPath references in inputs

**Does NOT validate**:
- Field type matching (string vs object vs array)
- Field schema conformance (nested structure)
- Transformation correctness (mapping logic)
- **This is DATAFLOW concern (explicitly out of scope)**

---

## Validation Algorithm

**Per-Path Traversal**:

```python
def validate_data_availability(wf_graph, in_node):
    # Extract IN payload schema
    available_fields = {
        f"$.payload.{field}": field
        for field in in_node.payload_schema.keys()
    }

    # Walk each execution path independently
    for path in derive_all_paths(wf_graph):
        path_fields = available_fields.copy()

        for node in path.nodes:
            if node.type == "CC":
                # Validate all input references
                for input_ref in node.inputs.values():
                    if is_jsonpath(input_ref):
                        assert input_ref in path_fields, \
                            f"Undefined reference: {input_ref}"

                # Add this node's outputs to available set
                cc_artifact = resolve_cc(node.code)
                for step in cc_artifact.pipeline:
                    for output_field in step.outputs.keys():
                        path_fields[f"$.results.{step.step}.{output_field}"] = True
```

**Key principle**: Per-path validation (not global topological order).

---

## Rationale

**Compile-time data flow safety**

### Early Detection
- Catch undefined references before runtime
- No "field not found" during execution
- Fast feedback for protocol authors

### Execution Confidence
- All data dependencies explicit
- No runtime discovery of missing fields
- Bounded, predictable behavior

### Foundation for Tracing
- Trace can show data lineage
- Each field's source is known
- Clear cause/effect chain

### NOT Type Safety
- Intentionally limited scope
- Availability ≠ correctness
- Type system is separate concern (if needed)

---

## Version History

- **V0**: Initial implementation (2026-04-12) - CC Inputs Satisfied Validation
