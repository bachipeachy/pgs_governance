# INVARIANT_ATOM_OUTPUT_PURITY_V0

Architectural Invariant

## Machine

```yaml
artifact_code: INVARIANT_ATOM_OUTPUT_PURITY_V0
artifact_type: INVARIANT
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  summary: Atoms must return explicit outputs in ALL cases, never raise exceptions for business logic
  rule: CT atom execute() functions must return dict outputs for all code paths including error states
  scope:
    - CT
```

## Summary

CT atom implementations must be pure functions that return explicit output dictionaries in ALL execution paths. Exceptions may only be raised for INPUT VALIDATION (missing required inputs, wrong types), never for business logic or "failure" states.

## Rule

For all CT atom implementations:
1. `execute()` must return dict in ALL business logic paths
2. Exceptions allowed ONLY for input validation (missing keys, wrong types)
3. Business logic "failures" must return explicit outputs (e.g., `{"is_eligible": false}`)
4. NO exceptions for quota exhaustion, training incomplete, etc.
5. Output structure must match CC contract in success AND "failure" cases

## Enforcement Scope

- **Artifact Types**: CT
- **Code Layer**: pgs_transforms/implementation/transforms/atoms/
- **Validation Phase**: Phase 5 (ASSERT)
- **Enforcement**: MANDATORY (build fails on violation)

## Examples

### ✅ VALID - Pure Function

```python
def execute(inputs: dict, context=None) -> dict:
    # Input validation (exceptions OK)
    if "training_completed" not in inputs:
        raise ValueError("Missing required input 'training_completed'")

    if not isinstance(inputs["training_completed"], bool):
        raise TypeError("training_completed must be bool")

    # Business logic (explicit outputs)
    is_eligible = inputs["training_completed"]

    return {
        "is_eligible": is_eligible  # ✅ Explicit output in ALL cases
    }
```

### ❌ INVALID - Exception for Business Logic

```python
def execute(inputs: dict, context=None) -> dict:
    training_completed = inputs["training_completed"]

    if not training_completed:
        raise ValueError("Training not completed")  # ❌ VIOLATION

    return {"is_eligible": True}
```

### ❌ INVALID - Missing "Failure" Output

```python
def execute(inputs: dict, context=None) -> dict:
    quota = inputs["quota"]
    assigned = inputs["assigned_count"]

    if assigned >= quota:
        raise ValueError("Quota exhausted")  # ❌ VIOLATION

    return {"quota_available": True}
    # ❌ No explicit output for quota exhausted case
```

## Rationale

Output purity ensures:
- Predictable execution (no exception-based control flow)
- Explicit state modeling (all outcomes are data)
- Testability (all paths return data)
- Traceability (no hidden execution paths)
- Constitutional principle: Line 105 of CC contract requires explicit outputs

## Detection Strategy

Scan CT atom code for:
- `raise` statements outside input validation block
- Exception raises after business logic starts
- Missing return statement in conditional branches
- Try/except blocks that re-raise business exceptions

## Related Artifacts

- `fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0` - Defines pure transform behavior
- `governance::CC_*_V0` - Declares required output structure
