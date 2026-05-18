# STRUCTURE_RUNTIME_EXECUTION_V0

**Artifact Type**: STRUCTURE
**Version**: V0
**Status**: CANONICAL
**Governed By**: fb.constitution::CONSTITUTION_STRUCTURE_V0

---

## Purpose

Defines runtime execution configuration for workflow invocation via transport ingress. This is the bootstrap-eligible STRUCTURE that governs artifact discovery and trace output for runtime execution.

**Scope**: Runtime execution only (not build/compile)

---

## Core

Runtime execution STRUCTURE. Defines WHERE the runtime searches for workflow artifacts and WHERE it writes execution traces.

**Critical Constraint**: This artifact MUST be bootstrap-eligible (no dependency on compiler outputs or build artifacts).

---

## Machine

```yaml
structure_code: STRUCTURE_RUNTIME_EXECUTION_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Runtime execution STRUCTURE configuration
  description: >
    Defines artifact discovery and trace output paths for runtime workflow execution.

artifact_discovery:
  search_roots:
    # Platform layers - source artifacts (.md)
    - layer: GOVERNANCE
      subpath: structures
    - layer: GOVERNANCE
      subpath: registry
    - layer: GOVERNANCE
      subpath: concerns

    - layer: COMPILER
      subpath: registry/registry/compiler

    - layer: EXECUTION
      subpath: registry/registry

    - layer: REUSABLE_TRANSFORMS
      subpath: registry/capability_transforms

    - layer: REUSABLE_SIDE_EFFECTS
      subpath: registry/capability_side_effects

    # Platform layers - compiled artifacts (.json)
    # Resolver contract: layer_root / artifact_type / subpath
    - layer: GOVERNANCE
      artifact_type: compiled
      subpath: artifacts

    - layer: COMPILER
      artifact_type: compiled
      subpath: artifacts

    - layer: EXECUTION
      artifact_type: compiled
      subpath: artifacts

    - layer: REUSABLE_TRANSFORMS
      artifact_type: compiled
      subpath: artifacts/capability_transforms

    - layer: REUSABLE_SIDE_EFFECTS
      artifact_type: compiled
      subpath: artifacts/capability_side_effects

    # Transport layers - source artifacts (.md)
    - layer: INGRESS
      subpath: registry/ingress_gateway

    - layer: EGRESS
      subpath: registry/registry

    # Transport layers - compiled artifacts (.json)
    - layer: INGRESS
      artifact_type: compiled
      subpath: artifacts/workflows

    - layer: INGRESS
      artifact_type: compiled
      subpath: artifacts/capability_contracts

    - layer: INGRESS
      artifact_type: compiled
      subpath: artifacts/runtime_bindings

    - layer: EGRESS
      artifact_type: compiled
      subpath: artifacts

  # Domain discovery configuration (dynamic path expansion)
  # PROTOCOL: Replaces 70+ hardcoded domain paths with declarative discovery
  domain_discovery:
    enabled: true
    mode: workspace_relative
    layer: DOMAINS
    search_pattern: domains/*/

    # Allowed domains (explicit whitelist)
    allowed_domains:
      - blockchain
      - ai_licensing
      - agent_governance

    # Registry subdirectories to search (source artifacts .md)
    # Expands to: domains/{domain}/registry/{subdir}
    # Also searches subregistries: domains/{domain}/registry/{subreg}/{subdir}
    registry_subdirs:
      - workflows
      - intents
      - capability_contracts
      - capability_transforms
      - runtime_bindings
      - events

    # Compiled artifact subdirectories to search (.json)
    # Expands to: domains/{domain}/compiled/artifacts/{subdir}
    compiled_subdirs:
      - workflows
      - intents
      - capability_contracts
      - capability_transforms
      - runtime_bindings
      - events
      - structures  # For domain-specific STRUCTURE artifacts (e.g., STRUCTURE_BLOCKCHAIN_STORAGE_V0)

    # Subregistry discovery (e.g., blockchain has identity/, wallet/, transaction/)
    discover_subregistries: true
    subregistry_pattern: domains/{domain}/registry/*/

  artifact_types:
    - WF
    - IN
    - CC
    - CT
    - CS
    - RB
    - EV

output_configuration:
  # Data root for workflow execution (manifest, registry files, state, etc.)
  build_manifest_path:
    layer: DOMAINS
    subpath: domains/{domain}/testbed/outputs/manifest.json

  # Trace output for execution observability
  trace_output_path:
    layer: DOMAINS
    subpath: domains/{domain}/testbed/outputs/traces

  # Event output for workflow events
  event_output_path:
    layer: EGRESS
    subpath: outputs/events

  # Log output for execution logs
  log_output_path:
    layer: EXECUTION
    subpath: outputs/logs
```

---

## Version History

- **V0**: Initial runtime execution STRUCTURE (2026-03-21)
- **V1**: Flattened domain structure (2026-03-26)
  - Removed 'governance' from domain search_roots
