# ASSERT_CC_NO_MISSING_DEPENDENCIES_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CC_NO_MISSING_DEPENDENCIES_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CC_NO_MISSING_DEPENDENCIES_V0

implementation:
  module: pgs_governance.registry.handlers.assert_cc_no_missing_dependencies_v0
  callable: execute
```

---

## Purpose

Enforces compile-time validation of CC dependency ordering and reachability.

**Validates**:
- No forward references (CC_B references CC_C that appears later)
- No cross-branch references (CC_B references CC_C on different branch)

**Delegates**:
- FQDN resolution to INVARIANT_FQDN_ONLY_REFERENCES_V0
- Field existence to INVARIANT_CC_INPUTS_SATISFIED_V0

---

## Enforcement

**Stage**: compile_time
**Trigger**: During validation phase of build pipeline
**Handler**: `assert_cc_no_missing_dependencies_v0.execute()`

**Validation Process**:
1. For each WF artifact, extract execution graph
2. Derive all execution paths from start_node to EXIT
3. For each path:
   - Track executed CCs in topological order
   - For each CC node, validate input references:
     - $.results.step_name.* → step must appear earlier in THIS path
     - No references to steps on different branches
4. Aggregate violations across all paths

**Violation Response**: FAIL_BUILD

---

## Rationale

**Compile-time dependency safety**: Catch forward and unreachable references before runtime

**Per-path validation**: Each execution path validated independently to avoid false positives

**Deterministic execution**: All dependencies guaranteed to be satisfied before node execution

---

## Version History

- **V0**: Initial implementation (2026-04-12) - CC Dependency Ordering Assertion
