# INVARIANT_CC_NO_UNUSED_OUTPUTS_V0

## Machine

```yaml
invariant_code: INVARIANT_CC_NO_UNUSED_OUTPUTS_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    CC pipeline step outputs should be consumed by downstream nodes.

    Unused outputs indicate:
    - Incomplete workflow (missing consumer)
    - Dead code (unnecessary computation)
    - Potential optimization opportunity

    This is CODE SMELL detection, not a hard violation.
    Enforcement level: WARNING (not FAIL_BUILD).

  enforcement_stage:
    - compiler_validation

  scope:
    - WORKFLOWS
    - CAPABILITY_CONTRACTS

  violation_response: WARN


  anti_patterns:
    - unused_output: "CC step produces output field that no downstream node consumes"
    - terminal_output: "CC produces output in terminal node (no consumers possible)"
    - dead_computation: "CC performs computation whose result is never used"

  clarification:
    warning_not_error: >
      This invariant emits WARNINGS, not ERRORS.
      Build succeeds even with unused outputs.
      Warnings help identify optimization opportunities.

    legitimate_unused: >
      Some unused outputs are legitimate:
      - Terminal state outputs (for final result)
      - Debugging/logging outputs (for observability)
      - Future extensibility (planned for later use)

    detection_scope: >
      Detects unused outputs within SINGLE workflow.
      Does NOT track cross-workflow consumption.
      Cross-WF analysis is separate concern.
```

---

## Purpose

Detect unused CC outputs as code smell indicator.

**Core Principle**: Computation without consumption may indicate incomplete or inefficient workflow.

---

## Detection Rules

### Rule 1: Output Consumption Tracking

For each CC node, track which outputs are consumed by downstream nodes.

**Example - Unused Output**:
```yaml
# WF nodes
CC_GENERATE_DATA_V0:
  type: CC
  outputs:
    data: ...
    metadata: ...     # ⚠️ Never consumed
    timestamp: ...    # ⚠️ Never consumed

CC_PROCESS_DATA_V0:
  type: CC
  inputs:
    data: $.results.CC_GENERATE_DATA_V0.data  # ✓ Consumed
  # metadata and timestamp never referenced
```

**Warning**:
- `CC_GENERATE_DATA_V0.metadata` - produced but never consumed
- `CC_GENERATE_DATA_V0.timestamp` - produced but never consumed

**Legitimate Use Cases** (warnings acceptable):
```yaml
# Terminal node - outputs are final result
CC_FINALIZE_V0:
  type: CC
  outputs:
    final_result: ...     # OK - terminal output
    execution_time: ...   # OK - observability

# Debugging output
CC_DEBUG_V0:
  outputs:
    debug_info: ...       # OK - for debugging
```

---

### Rule 2: Cross-Step References

Track consumption within CC pipeline steps AND across WF nodes.

**Within CC Pipeline**:
```yaml
# CC artifact
pipeline:
  - step: generate
    outputs:
      raw_data: ...
      metadata: ...   # ⚠️ Not used in later steps

  - step: process
    inputs:
      data: $.results.generate.raw_data  # ✓ Consumes raw_data
    # metadata never referenced
```

**Across WF Nodes**:
```yaml
# WF nodes
CC_A_V0:
  outputs:
    field1: ...
    field2: ...   # ⚠️ Not consumed by any downstream node

CC_B_V0:
  inputs:
    data: $.results.CC_A_V0.field1  # ✓ Consumes field1
```

---

## Detection Algorithm

**Output Consumption Analysis**:

```python
def detect_unused_outputs(wf_graph):
    # Track all produced outputs
    produced = {}  # {cc_code: {step_name: [field1, field2, ...]}}

    # Track all consumed references
    consumed = set()  # {"$.results.step_name.field", ...}

    # Pass 1: Collect all outputs
    for node in wf_graph.nodes:
        if node.type == "CC":
            cc_artifact = resolve_cc(node.code)
            for step in cc_artifact.pipeline:
                step_name = step.get("step")
                outputs = step.get("outputs", {})

                if step_name not in produced:
                    produced[step_name] = []
                produced[step_name].extend(outputs.keys())

    # Pass 2: Collect all consumptions
    for node in wf_graph.nodes:
        if node.type == "CC":
            for input_ref in node.inputs.values():
                if input_ref.startswith("$.results."):
                    consumed.add(input_ref)

    # Pass 3: Detect unused
    unused = []
    for step_name, fields in produced.items():
        for field in fields:
            ref = f"$.results.{step_name}.{field}"
            if ref not in consumed:
                unused.append({
                    "step": step_name,
                    "field": field,
                    "severity": "WARNING"
                })

    return unused
```

---

## Rationale

**Code quality indicator**

### Early Detection
- Identify incomplete workflows during build
- Catch dead code before runtime
- Fast feedback for protocol authors

### Optimization Opportunity
- Remove unnecessary computation
- Simplify workflows
- Reduce execution overhead

### Not a Hard Violation
- Some unused outputs are legitimate
- Warnings don't block builds
- Author decides if action needed

### Foundation for Refactoring
- Identify candidates for removal
- Guide workflow simplification
- Support incremental cleanup

---

## Enforcement Level

**WARNING (not ERROR)**:
- Build succeeds with warnings
- Warnings logged but not blocking
- Author discretion to act or ignore

**Future Consideration**:
- May promote to ERROR if pattern is consistently harmful
- May add exemption mechanism for legitimate cases
- Current phase: gather data, not enforce strictly

---

## Version History

- **V0**: Initial implementation (2026-04-12) - Unused Output Detection (Warning Level)
