# INVARIANT_CC_NO_MISSING_DEPENDENCIES_V0

## Machine

```yaml
invariant_code: INVARIANT_CC_NO_MISSING_DEPENDENCIES_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    No CC node may reference outputs from:
    - Non-existent CC (FQDN resolution failure)
    - CC that appears later in execution path (forward reference)
    - CC that is on different branch (unreachable reference)

    This validates DEPENDENCY ORDERING and REACHABILITY only.
    Does NOT validate field existence (handled by INVARIANT_CC_INPUTS_SATISFIED_V0).

  enforcement_stage:
    - compiler_validation

  scope:
    - WORKFLOWS
    - CAPABILITY_CONTRACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - nonexistent_cc: "WF node references CC that does not exist (FQDN resolution failure)"
    - forward_reference: "WF node references $.results.CC_XXX.* where CC_XXX appears later in execution path"
    - unreachable_reference: "WF node references $.results.CC_XXX.* where CC_XXX is on different branch"

  clarification:
    ordering_not_existence: >
      This invariant validates DEPENDENCY ORDERING (earlier/later in execution path).
      It does NOT validate field EXISTENCE (handled by INVARIANT_CC_INPUTS_SATISFIED_V0).
      Example: $.results.later_cc.field violates THIS invariant (ordering).
               $.results.earlier_cc.missing_field violates INPUTS_SATISFIED (existence).

    per_path_validation: >
      Each execution path validated independently.
      Dependency valid in path A may be invalid in path B.
      No false positives from unreachable branches.

    fqdn_delegation: >
      Non-existent CC detection delegated to INVARIANT_FQDN_ONLY_REFERENCES_V0.
      This invariant focuses on ordering/reachability of VALID CCs.
```

---

## Purpose

Ensure all CC dependencies are satisfied before execution.

**Core Principle**: No forward references, no unreachable references.

---

## Validation Rules

### Rule 1: No Forward References

CC node inputs cannot reference outputs from CCs that appear later in execution path.

**Violation**:
```yaml
# WF nodes
CC_VALIDATE_V0:
  type: CC
  inputs:
    data: $.results.CC_PROCESS_V0.data  # ❌ CC_PROCESS appears later

CC_PROCESS_V0:
  type: CC
  outputs:
    data: ...
```

**Correct**:
```yaml
# WF nodes
CC_PROCESS_V0:  # Appears first
  type: CC
  outputs:
    data: ...

CC_VALIDATE_V0:  # Appears later
  type: CC
  inputs:
    data: $.results.CC_PROCESS_V0.data  # ✓ CC_PROCESS already executed
```

**Detection**:
- Walk execution graph in topological order
- Track which CCs have been executed
- For each CC input reference, ensure referenced CC already executed

---

### Rule 2: No Cross-Branch References

CC node inputs cannot reference outputs from CCs on different branch.

**Violation**:
```yaml
# WF nodes
CC_A_V0:
  type: CC
  next:
    SUCCESS: CC_B_V0
    VIOLATION: CC_C_V0

CC_B_V0:
  type: CC
  inputs:
    data: $.results.CC_C_V0.data  # ❌ CC_C on different branch

CC_C_V0:
  type: CC
  outputs:
    data: ...
```

**Correct**:
```yaml
# WF nodes
CC_A_V0:
  type: CC
  outputs:
    data: ...
  next:
    SUCCESS: CC_B_V0
    VIOLATION: CC_C_V0

CC_B_V0:
  type: CC
  inputs:
    data: $.results.CC_A_V0.data  # ✓ CC_A is on same branch (parent)

CC_C_V0:
  type: CC
  inputs:
    data: $.results.CC_A_V0.data  # ✓ CC_A is on same branch (parent)
```

**Detection**:
- Derive all execution paths from start_node to EXIT
- For each path, validate references only point to nodes on SAME path
- Different paths validated independently

---

### Rule 3: FQDN Resolution (Delegated)

Non-existent CC detection delegated to existing invariant.

**Handled by**: `INVARIANT_FQDN_ONLY_REFERENCES_V0`

This invariant does NOT re-validate FQDN resolution.

---

## Scope

**Applies to**:
- All WF artifacts (workflow-level validation)
- All CC node references in WF execution graph
- All JSONPath references starting with `$.results.*`

**Does NOT validate**:
- Field existence (handled by INVARIANT_CC_INPUTS_SATISFIED_V0)
- Field type matching (DATAFLOW concern, out of scope)
- FQDN resolution (handled by INVARIANT_FQDN_ONLY_REFERENCES_V0)

---

## Validation Algorithm

**Per-Path Dependency Tracking**:

```python
def validate_dependency_ordering(wf_graph):
    # Derive all execution paths
    all_paths = derive_execution_paths(wf_graph)

    for path in all_paths:
        executed_ccs = set()

        for node in path.nodes:
            if node.type == "CC":
                # Validate all input references
                for input_ref in node.inputs.values():
                    if input_ref.startswith("$.results."):
                        referenced_cc = extract_cc_code(input_ref)

                        # Check if CC already executed in THIS path
                        if referenced_cc not in executed_ccs:
                            raise DependencyViolation(
                                f"Forward reference: {referenced_cc} not yet executed"
                            )

                # Add this CC to executed set
                executed_ccs.add(node.code)
```

**Key principle**: Per-path validation (not global ordering).

---

## Rationale

**Compile-time dependency safety**

### Early Detection
- Catch forward references before runtime
- No "dependency not available" during execution
- Fast feedback for protocol authors

### Execution Confidence
- All dependencies satisfied before node execution
- Deterministic execution order
- No runtime discovery of missing dependencies

### Path Isolation
- Each branch validates independently
- No false positives from unreachable code
- Clear execution semantics per path

### Foundation for Tracing
- Trace can show dependency chain
- Each reference's source is guaranteed to exist
- Clear cause/effect relationships

---

## Version History

- **V0**: Initial implementation (2026-04-12) - CC Dependency Ordering Validation
