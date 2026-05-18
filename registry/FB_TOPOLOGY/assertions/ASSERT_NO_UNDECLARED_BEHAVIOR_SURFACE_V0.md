# ASSERT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0

## Machine

```yaml
artifact_code: ASSERT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_no_undeclared_behavior_surface_v0
  callable: execute

enforcement:
  phase: validation
  order: 10
  failure_mode: HARD_FAIL
  level: WARNING  # Dev-friendly for now
  scope: ALL_ARTIFACTS

ci_override:
  level: ERROR  # Strict in CI/production
```

---

## Summary

Validates that all runtime behavior originates from declared protocol artifacts.

Eliminates fallback logic, heuristic resolution, and "smart" coding that makes implicit decisions outside protocol governance.

---

## Enforcement

- **Phase**: Validation (after parsing, before materialization)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All artifacts (STRUCTURE, WF, CC, CS, RB)
- **Level**: WARNING (dev), ERROR (CI)

---

## Validation Rules

### Rule 1: No Fallback Defaults for Protocol-Required Fields

**Violation**:
```python
# ❌ WRONG - Silent fallback for required field
output_config = structure.get('output_configuration', {})
```

**Correct**:
```python
# ✅ CORRECT - Fail hard if missing
if 'output_configuration' not in structure:
    raise ValueError("PROTOCOL_INCOMPLETE: output_configuration not declared")
output_config = structure['output_configuration']
```

### Rule 2: No Hardcoded Paths

**Violation**:
```python
# ❌ WRONG - Literal path
output_path = Path("pgs_compiler/compiled/artifacts")
```

**Correct**:
```python
# ✅ CORRECT - STRUCTURE-declared path
output_path = resolver.resolve_output_path(
    "layer_outputs",
    layer_code,
    structure
)
```

### Rule 3: No Implicit Domain Resolution

**Violation**:
```python
# ❌ WRONG - Lost domain information
layer_code = "DOMAINS"
output_path = resolver.resolve_layer_root(layer_code)  # Which domain?
```

**Correct**:
```python
# ✅ CORRECT - Explicit domain
layer_code = "DOMAINS"
domain = artifact.get("domain_name")
if not domain:
    raise ValueError("PROTOCOL_INCOMPLETE: domain required")
output_path = resolver.resolve_output_path(layer_code, structure, domain=domain)
```

### Rule 4: No Manual Path Traversal

**Violation**:
```python
# ❌ WRONG - Manual .parent navigation
module_root = resolver.resolve_layer_root("COMPILER")
repo_root = module_root.parent  # Outside LayerResolver!
```

**Correct**:
```python
# ✅ CORRECT - Use resolver API
output_path = resolver.resolve_output_path("artifacts", "COMPILER", structure)
```

### Rule 5: No Heuristic Selection

**Violation**:
```python
# ❌ WRONG - Filesystem heuristic
for path in module.__path__:
    if (Path(path) / "schemas").exists():  # Guessing!
        return path
```

**Correct**:
```python
# ✅ CORRECT - Protocol-declared authority
for path in module.__path__:
    authority = Path(path) / "STRUCTURE_LAYER_AUTHORITY_V0.md"
    if parse(authority).get("role") == "platform_root":
        return path  # Declared!
```

---

## Handler Behavior

**Currently**: This is a **meta-assertion** enforced through code review and architecture patterns.

**Future**: Static analysis tool could scan for:
- `.get()` calls with defaults on protocol-required fields
- Hardcoded path literals (excluding imports)
- `.parent` calls outside LayerResolver
- Filesystem existence checks for decision-making

**For now**: Code review + constitutional adherence.

---

## Error Messages

### Protocol Incomplete
```
❌ ASSERT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0: Protocol incomplete

Field: output_configuration
Artifact: STRUCTURE_BUILD_PLATFORM_CONFIG_V0
Violation: Required field missing, fallback used instead

Fix: Add output_configuration to STRUCTURE artifact
```

### Hardcoded Path
```
❌ ASSERT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0: Hardcoded path detected

File: pgs_compiler/compiler/phases/materialize.py:42
Code: output_path = Path("pgs_compiler/compiled/artifacts")
Violation: Path hardcoded instead of declared in STRUCTURE

Fix: Declare path in STRUCTURE, resolve via LayerResolver
```

### Implicit Domain
```
❌ ASSERT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0: Implicit domain resolution

Artifact: WF_CREATE_WALLET_V0
Layer: DOMAINS
Violation: Domain not specified, resolution ambiguous

Fix: Add domain_name field to artifact metadata
```

---

## Rationale

### Behavioral Integrity

**Problem without surface closure**:
- Code makes decisions outside protocol governance
- Behavior emerges from fallback logic
- System behavior ≠ protocol declaration

**Solution with surface closure**:
- All behavior declared in protocol artifacts
- Code executes declarations (never decides)
- System behavior = protocol declaration

### Constitutional Enforcement

This assertion enforces core constitutional principle:

**"Protocol declares intent, code executes - never decides"**

Every decision must originate from STRUCTURE/WF/CC/CS/RB artifacts, not Python code.

---

## Legal vs Illegal Fallbacks

### Illegal (Protocol-Required)
- `structure.get('output_configuration', {})`
- `wf.get('runtime_binding', 'default')`
- `rb.get('bindings', {})`

### Legal (Genuinely Optional)
- `artifact.get('optional_metadata', {})`
- `ERROR_MESSAGES.get(code, DEFAULT_MESSAGE)`
- `exit_reason or "COMPLETED"` (runtime value)

**Test**: If removing the field invalidates the artifact → illegal fallback.

---

## Implementation Note

**This is meta-enforcement**: governance validating code adherence to protocol.

Currently enforced through:
1. Code review (architectural patterns)
2. Constitutional adherence (developer training)
3. Parity checks (this assert ensures declaration exists)

**Future**: Static analysis could automate detection.

---

## Version History

- **V0**: Initial implementation (2026-04-12) - Behavioral Surface Closure Enforcement
