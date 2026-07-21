# INVARIANT_ASSERT_PARITY_V0

## Machine

```yaml
invariant_code: INVARIANT_ASSERT_PARITY_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    For every INVARIANT_*, exactly one ASSERT_* must exist (and vice versa).

    Naming must match:
    - INVARIANT_FOO_V0 ↔ ASSERT_FOO_V0

    This ensures governance symmetry between declaration (invariant)
    and enforcement (assert).

  enforcement_stage:
    - compiler_meta_validation

  scope:
    - GOVERNANCE_ARTIFACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - orphaned_invariant: "INVARIANT without matching ASSERT (declaration without enforcement)"
    - orphaned_assert: "ASSERT without matching INVARIANT (enforcement without declaration)"
    - naming_mismatch: "INVARIANT and ASSERT exist but names don't match pattern"

  clarification:
    governance_symmetry: >
      Invariants declare what must be true.
      Asserts enforce what must be true.
      Every declaration requires enforcement.
      Every enforcement must have declaration.
    meta_validation: >
      This is meta-governance: governance validating governance.
      Ensures governance layer is self-consistent before validating artifacts.

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  ci_override:
    level: ERROR
  enforcement:
    phase: meta_validation
    order: 1
    failure_mode: HARD_FAIL
    scope: GOVERNANCE_ARTIFACTS
    level: WARNING
```

---

## Purpose

Ensure governance symmetry between invariant declarations and assert enforcement.

**Core Principle**: Every rule declared must be enforceable. Every enforcement must have a rule.

---

## Validation Rules

### Rule 1: One-to-One Correspondence

For every `INVARIANT_X_V0`, exactly one `ASSERT_X_V0` must exist.
For every `ASSERT_X_V0`, exactly one `INVARIANT_X_V0` must exist.

**Violation - Orphaned Invariant**:
```
✓ INVARIANT_WF_EXECUTION_PATH_VALID_V0.md exists
✗ ASSERT_WF_EXECUTION_PATH_VALID_V0.md missing

❌ FORBIDDEN: Invariant without enforcement
```

**Violation - Orphaned Assert**:
```
✗ INVARIANT_OLD_RULE_V0.md deleted
✓ ASSERT_OLD_RULE_V0.md still exists

❌ FORBIDDEN: Assert without declaration
```

**Correct**:
```
✓ INVARIANT_CC_CAPABILITY_BINDING_VALID_V0.md
✓ ASSERT_CC_CAPABILITY_BINDING_VALID_V0.md

✅ Paired declaration + enforcement
```

**Detection**:
```python
invariant_names = {i.code.replace("INVARIANT_", "") for i in invariants}
assert_names = {a.code.replace("ASSERT_", "") for a in asserts}

orphaned_invariants = invariant_names - assert_names  # Must be empty
orphaned_asserts = assert_names - invariant_names    # Must be empty
```

---

### Rule 2: Naming Convention Match

Names must follow exact pattern:
- Invariant: `INVARIANT_{NAME}_V{N}`
- Assert: `ASSERT_{NAME}_V{N}`

Where `{NAME}` and `{N}` are identical.

**Violation - Naming Mismatch**:
```
✓ INVARIANT_WF_PATH_VALID_V0.md
✓ ASSERT_WF_EXECUTION_PATH_V0.md

❌ FORBIDDEN: Names don't match
(WF_PATH_VALID ≠ WF_EXECUTION_PATH)
```

**Correct**:
```
✓ INVARIANT_WF_EXECUTION_PATH_VALID_V0.md
✓ ASSERT_WF_EXECUTION_PATH_VALID_V0.md

✅ Exact name match (WF_EXECUTION_PATH_VALID)
```

**Detection**: String match after removing prefix and suffix.

---

## Scope

**Applies to**:
- All INVARIANT artifacts in governance layer
- All ASSERT artifacts in governance layer

**Does NOT validate**:
- Invariant/assert content correctness (different concern)
- Whether asserts actually enforce their invariants (runtime verification)
- Version compatibility (handled by versioning system)

---

## Rationale

### Governance Integrity

**Problem without parity**:
- Developer writes INVARIANT but forgets ASSERT → rule never enforced
- Developer deletes INVARIANT but leaves ASSERT → enforcement without justification
- Protocol appears to have rules, but runtime doesn't enforce them

**Solution with parity**:
- Build fails if INVARIANT lacks ASSERT
- Build fails if ASSERT lacks INVARIANT
- Governance is always self-consistent

### Build-Time Detection

Parity violation is governance defect, not artifact defect.
Must be caught before any artifact validation runs.

**Validation order**:
1. Meta-validate: governance self-consistency (parity check)
2. Artifact-validate: artifacts against constitutions
3. Conformance-validate: runtime behavior matches declarations

### Developer Experience

**Clear feedback**:
```
❌ Build failed: INVARIANT_ASSERT_PARITY_V0 violated

Orphaned invariants (missing asserts):
  - INVARIANT_WF_EXECUTION_PATH_VALID_V0
  - INVARIANT_CC_NO_IMPLICIT_CHAINING_V0

Orphaned asserts (missing invariants):
  - ASSERT_OLD_SURFACE_CLOSURE_V0

Fix: Create missing files or delete orphaned files.
```

### Constitutional Enforcement

This invariant enforces governance constitution itself:
- Governance must be complete (no missing enforcement)
- Governance must be minimal (no orphaned enforcement)
- Governance must be consistent (1:1 correspondence)

---

## Implementation Note

**This is meta-governance**: governance validating governance structure.

Must run BEFORE any invariant/assert enforcement:
```python
# Build pipeline order:
1. validate_governance_parity()     # This invariant
2. validate_artifacts_against_invariants()  # Other invariants
```

If governance is inconsistent, artifact validation is meaningless.

---

## Version History

- **V0**: Initial implementation (2026-04-12) - Meta-Invariant for Parity
