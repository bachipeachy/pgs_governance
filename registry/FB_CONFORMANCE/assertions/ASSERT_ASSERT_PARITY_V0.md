# ASSERT_ASSERT_PARITY_V0

## Machine

```yaml
artifact_code: ASSERT_ASSERT_PARITY_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.conformance::INVARIANT_ASSERT_PARITY_V0

implementation:
  module: pgs_governance.registry.handlers.assert_assert_parity_v0
  callable: execute

enforcement:
  phase: meta_validation
  order: 1
  failure_mode: HARD_FAIL
  scope: GOVERNANCE_ARTIFACTS
  level: WARNING  # Allows dev iteration, warnings don't block build

ci_override:
  level: ERROR  # CI/production enforces strict parity
```

---

## Summary

Validates governance symmetry: every INVARIANT has exactly one matching ASSERT (and vice versa).

This is meta-governance - governance validating itself before validating artifacts.

---

## Enforcement

- **Phase**: Meta-validation (runs BEFORE artifact validation)
- **Failure Mode**: HARD FAIL (build stops immediately)
- **Scope**: All INVARIANT and ASSERT artifacts in governance layer

---

## Validation Rules

### Rule 1: One-to-One Correspondence

For every `INVARIANT_X_V0`, exactly one `ASSERT_X_V0` must exist.
For every `ASSERT_X_V0`, exactly one `INVARIANT_X_V0` must exist.

**Detection**:
```python
invariant_names = {i.code.replace("INVARIANT_", "") for i in invariants}
assert_names = {a.code.replace("ASSERT_", "") for a in asserts}

orphaned_invariants = invariant_names - assert_names  # Must be empty
orphaned_asserts = assert_names - invariant_names    # Must be empty
```

### Rule 2: Naming Convention Match

Names must follow exact pattern:
- Invariant: `INVARIANT_{NAME}_V{N}`
- Assert: `ASSERT_{NAME}_V{N}`

Where `{NAME}` and `{N}` are identical.

---

## Handler Behavior

The assertion performs two checks:

### 1. No Orphaned Invariants
**All INVARIANT artifacts must have matching ASSERT**

Scans governance/invariants/ for INVARIANT_*.md files and verifies each has a matching ASSERT_*.md file.

Violation: INVARIANT without matching ASSERT (declaration without enforcement).

### 2. No Orphaned Asserts
**All ASSERT artifacts must have matching INVARIANT**

Scans governance/assertions/ for ASSERT_*.md files and verifies each has a matching INVARIANT_*.md file.

Violation: ASSERT without matching INVARIANT (enforcement without declaration).

---

## Error Messages

### Orphaned Invariant
```
❌ ASSERT_ASSERT_PARITY_V0: Orphaned invariant detected

Invariants without matching asserts:
  - INVARIANT_WF_EXECUTION_PATH_VALID_V0
  - INVARIANT_CC_NO_IMPLICIT_CHAINING_V0

Violation: Invariant declared but not enforced
Fix: Create matching ASSERT_*.md files
```

### Orphaned Assert
```
❌ ASSERT_ASSERT_PARITY_V0: Orphaned assert detected

Asserts without matching invariants:
  - ASSERT_OLD_SURFACE_CLOSURE_V0

Violation: Assert exists but no invariant declares it
Fix: Delete orphaned ASSERT or create matching INVARIANT
```

### Naming Mismatch
```
❌ ASSERT_ASSERT_PARITY_V0: Naming mismatch detected

Mismatched pairs:
  - INVARIANT_WF_PATH_VALID_V0 vs ASSERT_WF_EXECUTION_PATH_V0

Violation: Names don't match pattern
Fix: Rename to match exactly (excluding INVARIANT_/ASSERT_ prefix)
```

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
1. Meta-validate: governance self-consistency (parity check) ← THIS
2. Artifact-validate: artifacts against constitutions
3. Conformance-validate: runtime behavior matches declarations

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
1. validate_governance_parity()              # THIS ASSERT
2. validate_artifacts_against_invariants()   # Other asserts
```

If governance is inconsistent, artifact validation is meaningless.

---

## Version History

- **V0**: Initial implementation (2026-04-12) - Meta-Assertion for Parity
