# STRUCTURE_BUILD_PLATFORM_CONFIG_V0

**Artifact Type**: STRUCTURE
**Version**: V0
**Status**: CANONICAL
**Governed By**: fb.constitution::CONSTITUTION_STRUCTURE_V0

---

## Purpose

Defines artifact discovery and output paths for platform compilation.

This STRUCTURE governs:

* Where the compiler discovers artifacts
* Which artifact types are in scope
* Where compiled artifacts are written

**Scope**: Platform build only (domains excluded)

---

## Core

Build-time STRUCTURE configuration.

This artifact is the **single source of truth** for:

* discovery scope
* artifact inclusion
* output location

No fallback or implicit behavior is permitted.

---

## Machine

```yaml
structure_code: STRUCTURE_BUILD_PLATFORM_CONFIG_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

# Structure scope this build materializes — declared here, not hardcoded in the compiler.
structure_scope: platform

core:
  summary: Build-time STRUCTURE configuration (platform scope)
  description: >
    Defines artifact discovery and output paths for platform compilation.

artifact_discovery:

  # STRICT STRUCTURE-DRIVEN DISCOVERY (SCOPED)
  # Platform build excludes domain layers (BLOCKCHAIN, AI_GOVERNANCE)
  # Domain artifacts are built separately via STRUCTURE_BUILD_DOMAINS_CONFIG_V0
  search_layers:
    - GOVERNANCE
    - REUSABLE_TRANSFORMS
    - REUSABLE_SIDE_EFFECTS
    - CAPABILITIES
    - TEST_DATA

  # MINIMAL COMPILER SCOPE (NO DOGFOOD / NO RUNTIME)
  artifact_types:
    - VOCAB
    - CONSTITUTION
    - INVARIANT
    - ASSERT
    - SCHEMA
    - STRUCTURE
    - EXECUTION_POLICY
    - WF
    - IN
    - TI
    - TE
    - CC
    - CT
    - CS
    - EV
    - RB
    - TEST_DATA
    - SURFACE

output_configuration:

  # Compiled canonical artifacts (federated via layer_outputs below)
  # Note: This is a fallback only; layer_outputs takes precedence
  artifacts:
    layer: PROTOCOL_BUILD_ROOT
    subpath: compiled/canonical

  # Conformance tests (federated to transforms layer where TEST_DATA lives)
  conformance:
    layer: REUSABLE_TRANSFORMS
    subpath: compiled/conformance/ct

  # Vocabulary projection files (global system state)
  vocabulary_projection_path:
    layer: GOVERNANCE
    subpath: compiled/vocabulary

  # Tokenized topology projection files
  tokenized_projection_path:
    layer: GOVERNANCE
    subpath: compiled/tokenized

  # Evidence projection files (dual-form observability substrate)
  evidence_projection_path:
    layer: GOVERNANCE
    subpath: compiled/evidence

  # Trust attestation (cryptographic binding of verified tokenized projection)
  trust_attestation_path:
    layer: GOVERNANCE
    subpath: compiled/trust

  # Visualization projection files
  visualization_projection_path:
    layer: GOVERNANCE
    subpath: compiled/visualization

  # Federated layer outputs (each layer writes to its own repository)
  # PGS is 100% federated - artifacts are distributed to their source repositories
  layer_outputs:
    GOVERNANCE:
      layer: GOVERNANCE
      subpath: compiled/canonical
    REUSABLE_TRANSFORMS:
      layer: REUSABLE_TRANSFORMS
      subpath: compiled/canonical
    REUSABLE_SIDE_EFFECTS:
      layer: REUSABLE_SIDE_EFFECTS
      subpath: compiled/canonical
    CAPABILITIES:
      layer: CAPABILITIES
      subpath: compiled/canonical
    TEST_DATA:
      layer: REUSABLE_TRANSFORMS
      subpath: compiled/canonical
    EXECUTION:
      layer: PROTOCOL_BUILD_ROOT
      subpath: compiled/canonical
    AUTHORING:
      layer: PROTOCOL_BUILD_ROOT
      subpath: compiled/canonical
    TRANSPORT:
      layer: PROTOCOL_BUILD_ROOT
      subpath: compiled/canonical
    INGRESS:
      layer: PROTOCOL_BUILD_ROOT
      subpath: compiled/canonical
    EGRESS:
      layer: PROTOCOL_BUILD_ROOT
      subpath: compiled/canonical

  # Bootstrap artifact discovery (minimal hardcoded paths)
  bootstrap_search_roots:
    - layer: GOVERNANCE
      subpath: FB_CONSTITUTION/structures

build_phases:

  - phase: discover
    description: Discover artifacts via STRUCTURE

  - phase: parse
    description: Parse artifacts into canonical machine form

  - phase: normalize
    description: Resolve references to FQDN with deterministic binding

  - phase: validate
    description: Validate artifacts using compiler schema rules

  - phase: assert
    description: Evaluate cross-artifact invariants (surface closure)

  - phase: materialize
    description: Emit deterministic compiled artifacts
    target: "compiled/artifacts/"

  - phase: conformance_generate
    description: Generate CT conformance tests from TEST_DATA

  - phase: conformance_execute
    description: Blindly execute CT-IR conformance tests

```

## Version History

- **V0**: Added conformance phases and TEST_DATA artifact type
