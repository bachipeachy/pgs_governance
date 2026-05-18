# ASSERT_BINDING_SURFACE_CLOSED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_BINDING_SURFACE_CLOSED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_BINDING_SURFACE_CLOSED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_binding_surface_closed_v0
  callable: execute
```

---

## Purpose

Enforces compile-time validation of WF-level binding surface.

**Validates**:
- All `$.payload.<field>` bindings reference fields declared in IN node `payload_schema`
- All `$.results.<NODE>.<field>` bindings reference a CC node that exists in the WF,
  with `<field>` declared in that CC's `core.outputs`
- No unrecognized `$` binding grammar is present

**Does NOT validate** (out of scope):
- CC-internal pipeline step references (covered by `ASSERT_CC_INPUTS_SATISFIED_V0`)
- Field type compatibility (DATAFLOW concern)
- Execution path reachability (covered by `ASSERT_WF_EXECUTION_PATH_VALID_V0`)

---

## Enforcement

**Stage**: compile_time
**Trigger**: ASSERT phase — after structural pre-computation, before materialization
**Handler**: `assert_binding_surface_closed_v0.execute()`

**Validation Process**:
1. Compiler pre-computes `wf_binding_surface` for all WF artifacts
2. Handler reads pre-computed results from `compilation_context["wf_binding_surface"]`
3. For each WF artifact, translates structural violations to rule violations
4. Any violation → FAIL_BUILD (no warnings, no fallback)

**Violation Response**: FAIL_BUILD

---

## Rationale

**Closes the WF binding surface**: A WF that references an undeclared IN field or
an undeclared CC output cannot be correct. Catching this at compile time eliminates
an entire class of runtime binding errors.

**Complements existing invariants**: `ASSERT_CC_INPUTS_SATISFIED_V0` validates
CC-internal references. This assertion validates WF-boundary references.
Together they close the full data-flow surface.

**Declarative rule, not procedural logic**: The binding rules are declared in
`INVARIANT_BINDING_SURFACE_CLOSED_V0`. The compiler evaluates them. Code obeys.

---

## Version History

- **V0**: Initial implementation (2026-04-29) - WF Binding Surface Closure Assertion
