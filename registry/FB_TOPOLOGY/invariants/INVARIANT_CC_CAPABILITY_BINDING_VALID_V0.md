# INVARIANT_CC_CAPABILITY_BINDING_VALID_V0

## Machine

```yaml
invariant_code: INVARIANT_CC_CAPABILITY_BINDING_VALID_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Each CC pipeline step must bind exactly ONE capability:
    - Either CT (transform) for pure computation
    - Or CS (side_effect) for I/O operations
    - Never both (violates single responsibility)
    - Never zero (step has no implementation)

    Binding must use valid FQDN that resolves to existing artifact.

  enforcement_stage:
    - compiler_validation

  scope:
    - CAPABILITY_CONTRACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - zero_bindings: "Pipeline step has no capability binding (neither transform nor side_effect)"
    - dual_bindings: "Pipeline step binds both CT and CS (violates single responsibility)"
    - invalid_fqdn: "Capability FQDN does not resolve to existing artifact"

  clarification:
    single_responsibility: >
      Each pipeline step is atomic capability invocation.
      One step = one capability = one CT or one CS.
      Multiple capabilities = multiple steps.
    fqdn_resolution: >
      Capability binding validation delegates to INVARIANT_FQDN_ONLY_REFERENCES_V0.
      This invariant validates cardinality (exactly one), that invariant validates resolution.
```

---

## Purpose

Ensure CC pipeline steps are well-formed capability bindings.

**Core Principle**: One step, one capability, one execution.

---

## Validation Rules

### Rule 1: Exactly One Binding

Each pipeline step must have exactly one of:
- `transform` field (CT binding)
- `side_effect` field (CS binding)

**Violation - Zero Bindings**:
```yaml
# ❌ FORBIDDEN
pipeline:
  - step: validate_input
    inputs:
      data: $.inputs.data
    # ❌ No transform, no side_effect - what capability?
```

**Violation - Dual Bindings**:
```yaml
# ❌ FORBIDDEN
pipeline:
  - step: process_and_save
    transform: CT_PROCESS_V0      # ❌ Transform
    side_effect: CS_SAVE_V0       # ❌ Side effect
    # ❌ Both bindings - violates single responsibility
```

**Correct**:
```yaml
# ✅ One capability per step
pipeline:
  - step: process
    transform: CT_PROCESS_V0      # ✓ Pure computation
    inputs:
      data: $.inputs.data

  - step: save
    side_effect: CS_SAVE_V0       # ✓ I/O operation
    inputs:
      data: $.results.process.data
```

**Detection**: Count `transform` and `side_effect` fields per step. Assert count == 1.

---

### Rule 2: Valid FQDN (Delegated)

Capability FQDN must resolve to existing CT or CS artifact.

**Violation**:
```yaml
# ❌ FORBIDDEN
pipeline:
  - step: process
    transform: CT_NONEXISTENT_V0  # ❌ CT not found
```

**Detection**: Delegate to `INVARIANT_FQDN_ONLY_REFERENCES_V0` (existing validation).

---

## Scope

**Applies to**:
- All CC artifacts (platform + domains)
- All pipeline steps
- Both `transform` and `side_effect` bindings

**Does NOT validate**:
- Input/output availability (Phase 5)
- Mapping correctness (out of scope)
- CT/CS implementation correctness (execution layer)

---

## Rationale

**Architectural purity**

### Single Responsibility
- One step = one capability
- Clear, atomic operations
- No hidden complexity

### Execution Clarity
- Each step has unambiguous implementation
- Trace shows exact capability invoked
- No guessing what happened

### Type Safety Foundation
- CT always returns outputs
- CS may have side effects
- Different contracts, enforced by binding type

### Composability
- Steps are independently testable
- Same capability reusable across CCs
- No coupling between steps

---

## Version History

- **V0**: Initial implementation (2026-04-12) - CC Capability Binding Validation
