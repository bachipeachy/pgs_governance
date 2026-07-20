# STRUCTURE_BUILD_AI_GOVERNANCE_CONFIG_V0

Build configuration for AI governance domain artifacts.

## Header

- **Artifact Code:** STRUCTURE_BUILD_AI_GOVERNANCE_CONFIG_V0
- **Artifact Kind:** structure
- **Governed By:** fb.constitution::CONSTITUTION_STRUCTURE_V0
- **Version:** V0
- **Status:** canonical
- **Authority:** foundational

---

## Purpose

Defines layer composition and build parameters for building AI governance domain artifacts (workflows, intents, capability contracts, transforms, side effects).

---

## Machine

```yaml
structure_code: STRUCTURE_BUILD_AI_GOVERNANCE_CONFIG_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

# Structure scope this build materializes — declared here, not hardcoded in the compiler.
structure_scope: ai_governance

core:
  summary: AI Governance domain build configuration
  description: AI Governance artifact build (STRUCTURE-governed)

  target_workflow: WF_BUILD_AI_GOVERNANCE_V0
  target_layer_node: BUILD_AI_GOVERNANCE

  build_mode: ai_governance

scope:
  target_node: BUILD_AI_GOVERNANCE
  included_layers:
    - STRUCTURE
    - GOVERNANCE
    - EXECUTION
    - AI_GOVERNANCE

artifact_discovery:
  search_layers:
    - GOVERNANCE
    - REUSABLE_TRANSFORMS
    - REUSABLE_SIDE_EFFECTS
    - CAPABILITIES
    - AI_GOVERNANCE

  artifact_types:
    - WF
    - IN
    - TI
    - TE
    - CC
    - CT
    - CS
    - EV
    - RB
    - AC
    - STRUCTURE
    - CONSTITUTION
    - VOCAB
    - INVARIANT
    - ASSERT
    - TEST_DATA
    - SURFACE

output_configuration:
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
    AI_GOVERNANCE:
      layer: AI_GOVERNANCE
      subpath: compiled/canonical

  trace_logs_path:
    layer: EXECUTION
    subpath: outputs/traces

  conformance:
    layer: REUSABLE_TRANSFORMS
    subpath: compiled/conformance/ct

  vocabulary_projection_path:
    layer: AI_GOVERNANCE
    subpath: compiled/vocabulary

  tokenized_projection_path:
    layer: AI_GOVERNANCE
    subpath: compiled/tokenized

  evidence_projection_path:
    layer: AI_GOVERNANCE
    subpath: compiled/evidence

  trust_attestation_path:
    layer: AI_GOVERNANCE
    subpath: compiled/trust

  visualization_projection_path:
    layer: AI_GOVERNANCE
    subpath: compiled/visualization

build_phases:
  - phase: discover
  - phase: validate
  - phase: materialize
  - phase: verify_materialization
  - phase: compile_molecules
  - phase: generate_vocabulary_snapshot
  - phase: generate_conformance

validation:
  constitution_validation: true
  vocabulary_validation: true
  schema_validation: true
  cross_layer_validation: true
  runtime_semantic_validation: true

execution_context:
  runtime_execution: false
  build_time_only: true
  execution_layer_loaded: true
```

---

## Version History

- **V0**: Initial AI governance domain build configuration (2026-04-23)
  - Federated domain build support
  - Independent AI_GOVERNANCE layer compilation
