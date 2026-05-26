# STRUCTURE_BUILD_VOCABULARY_AGGREGATE_V0

Cross-structure vocabulary aggregation configuration.

## Header

- **Artifact Code:** STRUCTURE_BUILD_VOCABULARY_AGGREGATE_V0
- **Artifact Kind:** STRUCTURE
- **Governed By:** fb.constitution::CONSTITUTION_STRUCTURE_V0
- **Version:** V0
- **Status:** canonical
- **Authority:** foundational

---

## Purpose

Declares the federated vocabulary aggregation phase.

Vocabulary generation is NOT per-structure compilation — it is federated ontology
aggregation. This artifact governs a Phase Type B aggregation: it consumes declared
compiled output surfaces from all contributing domain structures and produces the
cross-system vocabulary snapshot.

This artifact is the **sole declaration** of:
- Which compiled artifact directories contribute to vocabulary
- What artifact types are scanned per source
- Where the aggregated vocabulary output is written

No per-structure STRUCTURE artifact should declare `vocabulary_artifacts_path`.

---

## Machine

```yaml
structure_code: STRUCTURE_BUILD_VOCABULARY_AGGREGATE_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

aggregation_type: VOCABULARY

core:
  summary: Federated vocabulary aggregation (cross-structure Phase Type B)
  description: >
    Aggregates CT, CS, CC, WF, and IN codes from all compiled domain outputs
    and produces vocabulary_symbols.json and vocabulary_semantic_index.json.
    Requires all contributing domain structures to have been compiled first.

# Declared source directories for each artifact type.
# Each entry is a list of (layer, subpath) pairs that are unioned during aggregation.
# Paths are resolved via path registry — no hardcoded filesystem assumptions.
artifact_source_dirs:
  capability_transforms:
    - layer: REUSABLE_TRANSFORMS
      subpath: compiled/canonical/capability_transforms

  capability_side_effects:
    - layer: REUSABLE_SIDE_EFFECTS
      subpath: compiled/canonical/capability_side_effects

  capability_contracts:
    - layer: CAPABILITIES
      subpath: compiled/canonical/capability_contracts

  workflows:
    - layer: BLOCKCHAIN
      subpath: compiled/canonical/workflows
    - layer: AI_GOVERNANCE
      subpath: compiled/canonical/workflows

  intents:
    - layer: BLOCKCHAIN
      subpath: compiled/canonical/intents
    - layer: AI_GOVERNANCE
      subpath: compiled/canonical/intents

output_configuration:
  vocabulary_projection_path:
    layer: GOVERNANCE
    subpath: compiled/vocabulary
```

---

## Doctrine

**Vocabulary generation is federated ontology aggregation, not structure compilation.**

The compiler pipeline has two phase types:
- **Phase Type A** — per-structure compilation (DISCOVER → MATERIALIZE)
- **Phase Type B** — cross-structure aggregation (consumes declared output surfaces)

This artifact governs a Phase Type B aggregation. It is invoked after all Phase Type A
builds complete. It MUST NOT be passed to the per-structure `_run_compile()` path.

## Version History

- **V0**: Initial federated vocabulary aggregation declaration (Option D implementation)
