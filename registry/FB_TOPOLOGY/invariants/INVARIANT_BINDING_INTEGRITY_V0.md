# INVARIANT_BINDING_INTEGRITY_V0

## Machine

```yaml
invariant_code: INVARIANT_BINDING_INTEGRITY_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Runtime Binding (RB) artifacts must declare bindings only to artifacts
    that exist in the compiled graph, and all binding keys must use
    fully-qualified domain names (FQDNs). Bindings to non-existent
    artifacts or short-name references are inadmissible — they indicate
    broken execution surface.

  enforcement_stage:
    - compiler_validation

  scope:
    - RUNTIME_BINDINGS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - short_name_binding: "RB binding key uses short name instead of FQDN"
    - dangling_binding: "RB binding key references artifact not in compiled graph"

  clarification:
    fqdn_requirement: >
      Binding keys must contain '::' (the FQDN separator). Short names
      are never admissible in binding declarations — they create ambiguity
      across domain boundaries.
    existence_requirement: >
      Every binding key must resolve to a node in the compiled graph.
      Bindings to removed, renamed, or misspelled artifacts are structural
      errors that would cause runtime failures.
```

---

## Purpose

Ensure RB binding surfaces are structurally sound. Every binding must point to a real, addressable artifact via its FQDN.

**Core Principle**: Binding integrity is a compile-time guarantee — no dangling references reach runtime.

---

## Validation Rules

### Rule 1: FQDN-Only Binding Keys

All `core.bindings` keys in RB artifacts must contain `::` (FQDN separator).

**Violation**: `CT_GENERATE_ID_V0` instead of `capability_transforms::CT_GENERATE_ID_V0`

### Rule 2: Binding Target Existence

All `core.bindings` keys must reference artifacts present in the compiled graph.

**Violation**: `blockchain::CT_NONEXISTENT_V0` when that artifact does not exist.

---

## Version History

- **V0**: Initial implementation (2026-05-21) - Extracted from compiler S4 GOVERN hardcoded RB validation
