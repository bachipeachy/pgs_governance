# ASSERT_CC_INPUTS_SATISFIED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CC_INPUTS_SATISFIED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CC_INPUTS_SATISFIED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_cc_inputs_satisfied_v0
  callable: execute
```

---

## Purpose

Enforces compile-time validation of JSONPath reference availability in CC inputs.

**Validates**:
- All `$.payload.*` references exist in IN node payload schema
- All `$.results.step_name.*` references point to valid prior steps with declared outputs
- All references are reachable on execution path (no cross-branch references)

**Does NOT validate** (out of scope):
- Field type matching (DATAFLOW concern)
- Schema conformance (DATAFLOW concern)
- Transformation correctness (DATAFLOW concern)

---

## Enforcement

**Stage**: compile_time
**Trigger**: During validation phase of build pipeline
**Handler**: `assert_cc_inputs_satisfied_v0.execute()`

**Validation Process**:
1. For each WF artifact, extract execution graph
2. Extract IN node payload schema
3. Walk execution paths in topological order
4. For each CC node, validate all input references:
   - `$.payload.*` → exists in IN payload schema
   - `$.results.step_name.*` → step exists earlier in path + field in step outputs
5. Aggregate violations across all paths

**Violation Response**: FAIL_BUILD

---

## Rationale

**Early detection**: Catch undefined references at compile time, not runtime

**Execution confidence**: All data dependencies explicit and validated

**Foundation for tracing**: Clear data lineage from source to consumer

**Bounded behavior**: No runtime discovery of missing fields

---

## Version History

- **V0**: Initial implementation (2026-04-12) - CC Inputs Satisfaction Assertion
