# ASSERT_CC_NO_IMPLICIT_CHAINING_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CC_NO_IMPLICIT_CHAINING_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CC_NO_IMPLICIT_CHAINING_V0

implementation:
  module: pgs_governance.registry.handlers.assert_cc_no_implicit_chaining_v0
  callable: execute
```

## Summary

Validates CC artifacts contain no orchestration logic:
1. No `next_step` field (explicit chaining)
2. No `next` field (state transitions)
3. No `transitions` field (workflow logic)
4. No `flow` field (control flow)
5. No `conditional` field (branching)
6. No `loop` field (iteration)

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CC artifacts

## Handler Behavior

### 1. Scan Frontmatter

Check CC frontmatter for forbidden fields:
- `next_step`
- `next`
- `transitions`
- `flow`
- `conditional`
- `loop`

Violation: Any forbidden field present.

### 2. Scan Pipeline Steps

Check each pipeline step for forbidden fields (same list as above).

Violation: Step-level orchestration logic.

### 3. Aggregate Violations

Collect all violations across all CC artifacts.

Return result with violation details.

## Error Messages

### Next Step Field
```
❌ ASSERT_CC_NO_IMPLICIT_CHAINING_V0: Implicit chaining detected
   CC: CC_EXAMPLE_V0
   Field: next_step
   Value: CC_NEXT_V0
   Violation: CC contains next_step field (implicit chaining)
   Fix: Remove next_step field, define flow in WF nodes
```

### State Transitions
```
❌ ASSERT_CC_NO_IMPLICIT_CHAINING_V0: State transitions detected
   CC: CC_EXAMPLE_V0
   Field: next
   Violation: CC contains next field (workflow construct)
   Fix: Remove next field, transitions belong in WF
```

### Control Flow
```
❌ ASSERT_CC_NO_IMPLICIT_CHAINING_V0: Control flow detected
   CC: CC_EXAMPLE_V0
   Field: flow
   Violation: CC contains flow field (orchestration logic)
   Fix: Remove flow field, orchestration belongs in WF
```

## Rationale

**Architectural purity**

### Clean Separation
- CC = capability (what)
- WF = orchestration (when, how)
- No mixing, no exceptions

### Constitutional Enforcement
- CC is pure capability wrapper
- Zero execution context knowledge
- Zero next-step decisions

### Foundation for Surface Closure
- CC surface = pipeline steps only
- No hidden orchestration paths
- Deterministic, bounded behavior

## Version History

- **V0**: Initial implementation (2026-04-12) - CC No Implicit Chaining
