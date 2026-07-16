# STRUCTURE_DISCOVERY_V0

**Artifact Type**: STRUCTURE
**Version**: V0
**Status**: CANONICAL
**Authority**: CONSTITUTIONAL

---

## Purpose

Single source of truth for artifact discovery. Defines which layers are searched, how layer codes map to physical registry modules, and the rules governing artifact scanning.

---

## Machine

```yaml
structure_code: STRUCTURE_DISCOVERY_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Consolidated artifact discovery configuration
  description: >
    Single source of truth for artifact discovery, replacing fragmented
    registry location and layer authority discovery definitions.

discovery:
  layers:
    GOVERNANCE:
      registry_module: pgs_governance.registry
      layer_category: platform

    REUSABLE_TRANSFORMS:
      registry_module: pgs_transforms.registry
      # Physical layout of capability-transform implementations within this layer's package.
      # Authoritative source for CT module-path materialization (no compiler-side layout knowledge).
      implementation_namespace: transforms.atoms
      layer_category: platform

    REUSABLE_SIDE_EFFECTS:
      registry_module: pgs_side_effects.registry
      layer_category: platform

    CAPABILITIES:
      registry_module: pgs_capabilities.registry
      layer_category: platform

    COMPILER:
      registry_module: pgs_compiler.registry
      layer_category: platform

    STRUCTURE:
      registry_module: pgs_structure.structure
      layer_category: platform

    INGRESS:
      registry_module: pgs_ingress.registry
      layer_category: platform

    EXECUTION:
      registry_module: pgs_runtime
      layer_category: platform

    BLOCKCHAIN:
      registry_module: pgs_blockchain.registry
      module_path_pattern: "{registry_module}.{subdomain}"
      implementation_namespace: capability_transforms.atoms
      layer_category: domain

      # Subdomain enumeration (STRUCTURE-declared, no filesystem scanning)
      allowed_subdomains:
        - identity
        - transaction
        - wallet

    AI_GOVERNANCE:
      registry_module: pgs_ai_governance.registry
      module_path_pattern: "{registry_module}.{domain}"
      implementation_namespace: capability_transforms.atoms
      layer_category: domain

      # Domain enumeration (STRUCTURE-declared, no filesystem scanning)
      allowed_domains:
        - ai_licensing
        - agent_governance
        - agent_admission

    TEST_DATA:
      registry_module: pgs_transforms.testbed.ct_test_data
      layer_category: platform

  rules:
    # Pattern updated to support multi-word types (TEST_DATA)
    filename_pattern: "^(?P<type>TEST_DATA|[A-Z]+)_(?P<name>[A-Z0-9_]+)_V(?P<version>\\d+)\\.md$"
    
    excluded_directories:
      - .git
      - __pycache__
      - node_modules
      - .venv
      - metadata

    format_precedence:
      - json
      - markdown

    format_extensions:
      json: .json
      markdown: .md

    resolution:
      method: importlib
      fallback: forbidden

    scope:
      type: platform_only

    validation:
      require_registry: true
      on_missing_registry: FAIL

    ordering:
      deterministic: true
```
