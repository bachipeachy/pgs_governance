# INVARIANT_CS_SURFACE_CLOSED_V0

## Machine

```yaml
invariant_code: INVARIANT_CS_SURFACE_CLOSED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    CS surface must be closed: all executable capability side effects must be
    explicitly declared, all declared CS must have runtime implementations, and
    no undeclared CS may execute.

  enforcement_stage:
    - compiler_assertion

  scope:
    - CAPABILITY_SIDE_EFFECTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - undeclared_cs: "CS exists in registry but not in allowed list"
    - missing_implementation: "CS declared but runtime implementation missing"
    - excess_declaration: "CS in allowed list but not discovered"
    - implicit_execution: "CS executed without explicit declaration"

  clarification:
    closed_surface_definition: >
      Closed CS surface means: Declared_CS_set == Executable_CS_set.
      No more, no less. All behavior is finite, enumerable, and auditable.
    runtime_check_scope: >
      Runtime implementations must exist for all declared CS. The expected
      pattern is: CS_X_V0 → implementation/side_effects/.../CS_X_V0/runtime.py
    security_model: >
      CS surface closure enables finite enumeration of all side effects,
      making the system's behavior bounded and auditable. No dynamic CS
      discovery is permitted at runtime.

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  scope:
    applies_to:
    - PLATFORM
  allowed_capability_side_effects:
  - capability_side_effects::CS_APPENDONLY_JSONL_V0
  - capability_side_effects::CS_CONCURRENT_WORKFLOWS_V0
  - capability_side_effects::CS_MUTABLE_JSON_V0
  - capability_side_effects::CS_REGISTRY_V0
  - capability_side_effects::CS_SEND_EMAIL_V0
  - capability_side_effects::CS_WORKFLOW_GATEWAY_V0
  - capability_side_effects::CS_WORKFLOW_LOOP_V0
  - pgs_capabilities.registry.name_service.capability_side_effects::CS_NAME_REGISTRY_V0
```

---

## Purpose

Ensure CS surface is closed during compilation.

**Core Principle**: System behavior = finite, enumerable, auditable set of declared side effects.

---

## Enforcement Rules

### Rule 1: No Undeclared CS

Every CS artifact discovered during compilation must be in the allowed list.

**Violation**:
```yaml
# CS exists in registry but not declared
capability_side_effects::CS_UNDECLARED_V0 (discovered, not in allowed list)
```

**Detection**: After discovery phase, check all CS artifacts against allowed list.

---

### Rule 2: No Missing Implementations

Every CS in the allowed list must have a runtime implementation.

**Violation**:
```
# CS declared but runtime missing
capability_side_effects::CS_DECLARED_V0
Expected: pgs_side_effects/implementation/side_effects/.../CS_DECLARED_V0/runtime.py
Actual: File not found
```

**Detection**: After discovery, verify runtime.py exists for each declared CS.

---

### Rule 3: No Excess Declarations

Every CS in the allowed list must be discovered during compilation.

**Violation**:
```yaml
# CS declared but artifact doesn't exist
allowed_capability_side_effects:
  - capability_side_effects::CS_REMOVED_V0  # Not discovered!
```

**Detection**: After discovery, check all allowed CS were found.

---

## Scope

**Applies to**:
- All CS artifacts in platform compilation
- All CS runtime implementations in REUSABLE_SIDE_EFFECTS layer
- Compiler ASSERT phase enforcement

**Exempt**:
- Domain-specific CS (handled by domain build configuration)
- Test-only CS (if explicitly marked)

---

## Security Model

**Closed CS surface enables**:
- Finite enumeration: "What can this system do?" → Read one file
- Behavioral bounds: No undeclared side effects possible
- Audit surface: Complete list of all external interactions
- Static analysis: All side effects known at compile time

**Prevents**:
- Runtime CS discovery (dynamic behavior)
- Heuristic resolution (implicit fallbacks)
- Hidden side effects (undeclared capabilities)
- Behavioral drift (code doing more than protocol declares)

---

## Version History

- **V0**: Initial invariant (2026-04-05) - CS Surface Closure enforcement
