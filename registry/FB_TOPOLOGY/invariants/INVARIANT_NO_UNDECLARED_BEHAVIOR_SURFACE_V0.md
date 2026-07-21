# INVARIANT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0

## Machine

```yaml
invariant_code: INVARIANT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    All runtime behavior must originate from declared protocol artifacts.
    Eliminate fallback logic, heuristic resolution, and smart coding that
    makes implicit decisions outside protocol governance.

  enforcement_stage:
    - compiler_validation
    - structure_resolution
    - workflow_execution
    - side_effect_execution

  scope:
    - STRUCTURE
    - WF
    - CC
    - CS
    - RB

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - fallback_defaults_for_protocol_values: "config.get('trace_output_path', 'default') when trace_output_path SHOULD be in STRUCTURE"
    - hardcoded_paths: "literal path strings outside STRUCTURE"
    - implicit_domain: "layer='DOMAINS' without domain field"
    - manual_traversal: ".parent navigation outside LayerResolver"
    - heuristic_selection: "filesystem checks to choose behavior"

  clarification:
    illegal_fallback: "config.get('required_protocol_field', 'default') → field MUST be in STRUCTURE"
    legal_fallback: "config.get('optional_metadata', {}) → truly optional field, not protocol-required"
    rule: "If STRUCTURE/WF/RB SHOULD declare it → fallback is illegal. If genuinely optional → fallback is OK."

examples:
    violation_1:
      code: |
        # ❌ WRONG - Fallback for protocol-required field
        output_config = structure.get('output_configuration', {})
      fix: |
        # ✅ CORRECT - Fail hard if missing
        if 'output_configuration' not in structure:
            raise ValueError("PROTOCOL_INCOMPLETE: 'output_configuration' not declared")
        output_config = structure['output_configuration']

    violation_2:
      code: |
        # ❌ WRONG - Manual path traversal
        module_root = resolver.resolve_layer_root("COMPILER")
        repo_root = module_root.parent
        output_path = repo_root / "testbed" / "outputs"
      fix: |
        # ✅ CORRECT - Use STRUCTURE-declared path
        output_path = paths.resolve_output_path(
            'testbed_output_path',
            structure_artifact,
            domain=domain
        )

    violation_3:
      code: |
        # ❌ WRONG - Lossy domain resolution
        layer_code = "DOMAINS"  # Lost which domain!
      fix: |
        # ✅ CORRECT - Explicit domain binding
        layer_code = "DOMAINS"
        domain = extract_domain_from_path(artifact_source_path)
        if not domain:
            raise ValueError("PROTOCOL_INCOMPLETE: domain required for DOMAINS layer")

    legal_pattern_1:
      code: |
        # ✅ OK - Genuinely optional metadata
        metadata = artifact.get('optional_metadata', {})
      reason: "optional_metadata is not protocol-required, genuinely optional"

    legal_pattern_2:
      code: |
        # ✅ OK - Static error message lookup
        message = ERROR_MESSAGES.get(code, DEFAULT_MESSAGE)
      reason: "Static mapping, not protocol data"

extensions:
  enforcement_locations:
    - "pgs_structure/structure/resolution/path_registry.py::resolve_output_path()"
    - "pgs_structure/structure/resolution/layer_resolver.py::resolve_layer_root()"
    - "pgs_execution/execution/host/runtime_loader.py::load_runtime_binding()"
    - "pgs_execution/execution/host/workflow_runner.py::execute()"
    - "pgs_compiler/compiler/transforms/*::validate()"
    - "pgs_ingress/ingress/gateway/workflow_gateway.py::execute_workflow()"

  error_codes:
    - PROTOCOL_INCOMPLETE: "Required protocol field not declared"
    - UNDECLARED_OUTPUT_PATH: "Output path not declared in STRUCTURE"
    - UNDECLARED_SIDE_EFFECT: "CS runtime attempted undeclared I/O operation"
    - DOMAIN_REQUIRED: "Domain parameter required but not provided"
    - REFERENCE_UNRESOLVED: "Artifact reference does not resolve"

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  ci_override:
    level: ERROR
  enforcement:
    phase: validation
    order: 10
    failure_mode: HARD_FAIL
    level: WARNING
    scope: ALL_ARTIFACTS
```

---

## Enforcement Rules

### Rule 1: No Fallback Defaults for Protocol-Required Fields

**Violation Pattern**:
```python
# ❌ WRONG
value = config.get("protocol_required_field", "default_value")
```

**Correct Pattern**:
```python
# ✅ CORRECT
if "protocol_required_field" not in config:
    raise ValueError(
        f"PROTOCOL_INCOMPLETE: 'protocol_required_field' not declared in {artifact_code}. "
        f"Protocol artifacts must explicitly declare all required fields."
    )
value = config["protocol_required_field"]
```

### Rule 2: No Hardcoded Paths

**Violation Pattern**:
```python
# ❌ WRONG
output_path = "/Users/bp/pgs/pgs_compiler/compiled/artifacts"
output_path = Path("pgs_domains/domains/blockchain/outputs")
```

**Correct Pattern**:
```python
# ✅ CORRECT - Declared in STRUCTURE
output_path = paths.resolve_output_path(
    'build_manifest_path',
    structure_artifact,
    domain=domain
)
```

### Rule 3: No Implicit Domain Resolution

**Violation Pattern**:
```python
# ❌ WRONG - Lost domain information
layer_code = "DOMAINS"
layer_root = resolver.resolve_layer_root(layer_code)  # Which domain?
```

**Correct Pattern**:
```python
# ✅ CORRECT - Explicit domain binding
layer_code = "DOMAINS"
domain = extract_domain_from_path(artifact_source_path)
if not domain:
    raise ValueError("PROTOCOL_INCOMPLETE: domain required for DOMAINS layer")
layer_root = resolver.resolve_layer_root(layer_code, domain=domain)
```

### Rule 4: No Manual Path Traversal

**Violation Pattern**:
```python
# ❌ WRONG - Manual .parent calls
module_root = resolver.resolve_layer_root("COMPILER")
repo_root = module_root.parent
output_path = repo_root / "compiled" / "artifacts"
```

**Correct Pattern**:
```python
# ✅ CORRECT - Use LayerResolver API
output_path = resolver.resolve_output_path("artifacts", "COMPILER", structure)
```

### Rule 5: No Heuristic Selection

**Violation Pattern**:
```python
# ❌ WRONG - Filesystem heuristic
for path in module.__path__:
    if (Path(path).parent / "schemas").exists():
        return path  # Guessing based on filesystem
```

**Correct Pattern**:
```python
# ✅ CORRECT - Protocol-declared authority
for path in module.__path__:
    authority_artifact = Path(path) / "layers" / "STRUCTURE_LAYER_AUTHORITY_V0.md"
    if parse(authority_artifact).get("role") == "platform_root":
        return path  # Declared in protocol
```

---

## Clarification: Legal vs Illegal Fallbacks

### Illegal Fallbacks (Protocol-Required Fields)

Fields that SHOULD be declared in protocol artifacts:

**STRUCTURE artifacts**:
- `output_configuration` (required)
- `build_manifest_path` (required in output_configuration)
- `trace_output_path` (required in output_configuration)
- `artifact_discovery.search_roots` (required)

**Workflow artifacts**:
- `runtime_binding` (required - can be in WF or passed as parameter)
- `workflow_code` (required)
- `states` (required)

**Intent artifacts**:
- `core` (required)
- `core.workflow` (required)

**Runtime Binding artifacts**:
- `core.bindings` (required)

### Legal Fallbacks (Truly Optional Fields)

Fields that are genuinely optional:

- `optional_metadata` - Not protocol-required
- Static error message lookups - Not protocol data
- Runtime execution context defaults (e.g., `exit_reason or "COMPLETED"`) - Runtime values

**Test**: If removing the field would make the artifact invalid per constitution → illegal fallback. If field is supplementary → legal fallback.

---

## Version History

- **V0**: Initial invariant declaration (2026-03-24) - Protocol Surface Closure Phase 1
