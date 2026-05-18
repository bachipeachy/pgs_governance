# INVARIANT_NO_SMART_EXECUTION_V0

Architectural Invariant

## Machine

```yaml
artifact_code: INVARIANT_NO_SMART_EXECUTION_V0
artifact_type: INVARIANT
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  summary: Execution layer must not interpret type declarations or perform conversions
  rule: Runtime executors must pass inputs to transforms without type-based interpretation or conversion
  scope:
    - CS
    - RUNTIME
```

## Summary

Execution layer code (atom_registry, workflow_runner, etc.) must be "dumb executors" - they pass inputs to transforms and return outputs without interpreting type metadata or performing conversions.

## Rule

For all execution layer code:
1. NO type-based input conversion (e.g., hex_string → bytes)
2. NO type-based output conversion (e.g., bytes → hex_string)
3. NO interpretation of CC type declarations as execution instructions
4. NO caching of type metadata for runtime decisions
5. Type declarations are METADATA ONLY for validation

All canonicalization must happen inside atom implementations.

## Enforcement Scope

- **Artifact Types**: CS (Capability Side Effects - executors)
- **Code Layer**: pgs_execution
- **Validation Phase**: Phase 5 (ASSERT)
- **Enforcement**: MANDATORY (build fails on violation)

## Examples

### ✅ VALID - Dumb Executor

```python
def adapter(ctx, step: dict):
    # Resolve inputs without type interpretation
    resolved_inputs = {}
    for key, value in step.items():
        if key in RESERVED_KEYS:
            continue
        resolved_inputs[key] = resolve_value(value)

    # Call atom - atom handles its own canonicalization
    result = execute_fn(inputs=resolved_inputs)

    # Store result without conversion
    ctx.set_value(step["as"], result)
```

### ❌ INVALID - Smart Executor

```python
# ❌ Type-based input conversion
input_types = load_contract_input_types(atom_code)
for key, value in inputs.items():
    if input_types[key] == "hex_string":
        inputs[key] = bytes.fromhex(value[2:])  # ❌ VIOLATION

# ❌ Type-based output conversion
output_types = load_contract_output_types(atom_code)
for key, value in result.items():
    if output_types[key] == "hex_string":
        result[key] = "0x" + value.hex()  # ❌ VIOLATION
```

## Rationale

Dumb executors ensure:
- Single source of truth (atoms own their canonicalization)
- No hidden transformations
- Explicit type handling in atoms
- No executor-atom coupling via type metadata
- Constitutional principle: "Code is executor, not decision maker"

## Detection Strategy

Scan execution layer code for:
- Calls to `load_contract()` or type metadata loaders
- Conditional logic based on type names (if type == "hex_string")
- `.hex()` calls on values (output conversion)
- `bytes.fromhex()` calls on values (input conversion)
- `_OUTPUT_TYPES_CACHE` or similar type caching

## Related Artifacts

- `fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0` - Defines pure atom behavior
- `fb.topology::CONSTITUTION_RUNTIME_BINDING_V0` - Defines executor boundaries
