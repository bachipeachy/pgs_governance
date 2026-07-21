# INVARIANT_CT_SURFACE_CLOSED_V0

## Machine

```yaml
invariant_code: INVARIANT_CT_SURFACE_CLOSED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    CT surface must be closed: all executable capability transforms must be
    explicitly declared, all declared CT must have runtime implementations, and
    no undeclared CT may execute.

  enforcement_stage:
    - compiler_assertion

  scope:
    - CAPABILITY_TRANSFORMS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - undeclared_ct: "CT exists in registry but not in allowed list"
    - missing_implementation: "CT declared but runtime implementation missing"
    - excess_declaration: "CT in allowed list but not discovered"
    - implicit_execution: "CT executed without explicit declaration"

  clarification:
    closed_surface_definition: >
      Closed CT surface means: Declared_CT_set == Executable_CT_set.
      No more, no less. All computation is finite, enumerable, and auditable.
    runtime_check_scope: >
      Runtime implementations must exist for all declared CT. The expected
      pattern is: CT_X_V0 → implementation/transforms/.../ct_x_v0.py (executable function)
    logic_model: >
      CT surface closure enables finite enumeration of all transforms,
      making the system's computation bounded and auditable. No dynamic CT
      discovery is permitted at runtime.

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  scope:
    applies_to:
    - PLATFORM
  allowed_capability_transforms:
  - capability_transforms::CT_EXEC_EMIT_V0
  - capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0
  - capability_transforms::CT_PURE_CHECK_QUOTA_AVAILABLE_V0
  - capability_transforms::CT_PURE_CHECK_TRAINING_STATUS_V0
  - capability_transforms::CT_PURE_COMPARE_EQUAL_V0
  - capability_transforms::CT_PURE_DERIVE_CHILD_KEY_V0
  - capability_transforms::CT_PURE_DERIVE_MASTER_KEY_V0
  - capability_transforms::CT_PURE_ECDSA_SIGN_V0
  - capability_transforms::CT_PURE_ENTROPY_TO_MNEMONIC_V0
  - capability_transforms::CT_PURE_EVALUATE_INACTIVITY_V0
  - capability_transforms::CT_PURE_EXTRACT_V0
  - capability_transforms::CT_PURE_FILTER_RECORDS_V0
  - capability_transforms::CT_PURE_GENERATE_ENTROPY_V0
  - capability_transforms::CT_PURE_GENERATE_ID_V0
  - capability_transforms::CT_PURE_KECCAK256_HASH_V0
  - capability_transforms::CT_PURE_LOOKUP_V0
  - capability_transforms::CT_PURE_MAP_RESULT_TO_HTTP_V0
  - capability_transforms::CT_PURE_PASSTHROUGH_V0
  - capability_transforms::CT_PURE_MNEMONIC_TO_SEED_V0
  - capability_transforms::CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
  - capability_transforms::CT_PURE_PUBKEY_TO_ETH_ADDRESS_V0
  - capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0
  - capability_transforms::CT_PURE_VALIDATE_RECORD_STRUCTURE_V0
  - capability_transforms::CT_PURE_VALIDATE_SET_MEMBERSHIP_V0
```

---

## Purpose

Ensure CT surface is closed during compilation.

**Core Principle**: System computation = finite, enumerable, auditable set of declared transforms.

---

## Enforcement Rules

### Rule 1: No Undeclared CT

Every CT artifact discovered during compilation must be in the allowed list.

**Violation**:
```yaml
# CT exists in registry but not declared
capability_transforms::CT_UNDECLARED_V0 (discovered, not in allowed list)
```

**Detection**: After discovery phase, check all CT artifacts against allowed list.

---

### Rule 2: No Missing Implementations

Every CT in the allowed list must have a runtime implementation.

**Violation**:
```
# CT declared but runtime missing
capability_transforms::CT_DECLARED_V0
Expected: pgs_transforms/implementation/transforms/atoms/ct_declared_v0.py
Actual: File not found
```

**Detection**: After discovery, verify implementation file exists for each declared CT.

---

### Rule 3: No Excess Declarations

Every CT in the allowed list must be discovered during compilation.

**Violation**:
```yaml
# CT declared but artifact doesn't exist
allowed_capability_transforms:
  - capability_transforms::CT_REMOVED_V0  # Not discovered!
```

**Detection**: After discovery, check all allowed CT were found.

---

## Scope

**Applies to**:
- All CT artifacts in platform compilation
- All CT runtime implementations in REUSABLE_TRANSFORMS layer
- Compiler ASSERT phase enforcement

**Exempt**:
- Domain-specific CT (handled by domain build configuration)
- Test-only CT (if explicitly marked)

---

## Logic Model

**Closed CT surface enables**:
- Finite enumeration: "What can this system compute?" → Read one file
- Computational bounds: No undeclared transforms possible
- Logic surface: Complete list of all transformations
- Static analysis: All computation known at compile time

**Prevents**:
- Runtime CT discovery (dynamic behavior)
- Heuristic resolution (implicit fallbacks)
- Hidden computation (undeclared transforms)
- Behavioral drift (code computing more than protocol declares)

---

## Version History

- **V0**: Initial invariant (2026-04-05) - CT Surface Closure enforcement