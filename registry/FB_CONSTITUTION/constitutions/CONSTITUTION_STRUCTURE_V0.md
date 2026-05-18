# CONSTITUTION_STRUCTURE_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_STRUCTURE_V0
constitution_code: CONSTITUTION_STRUCTURE_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs STRUCTURE artifacts — system configuration and artifact discovery declarations
  scope: artifact
  governs:
    - STRUCTURE
  enforcement_model: compiler_enforced

rules:
  - rule_id: STRUCTURE_EXPLICIT_PATHS
    applies_to: STRUCTURE
    constraint: all paths MUST be explicitly declared; no implicit defaults, heuristics, or fallback
    enforced_by: TBD

  - rule_id: STRUCTURE_NO_ABSOLUTE_PATHS
    applies_to: STRUCTURE
    constraint: absolute filesystem paths are forbidden; all paths MUST be layer-relative
    enforced_by: TBD

  - rule_id: STRUCTURE_NO_ESCAPE
    applies_to: STRUCTURE
    constraint: subpaths MUST NOT contain ".." layer escapes
    enforced_by: TBD

  - rule_id: STRUCTURE_LAYER_DECLARED
    applies_to: STRUCTURE
    constraint: every path declaration MUST reference a valid declared layer code
    enforced_by: TBD

  - rule_id: STRUCTURE_DETERMINISTIC_RESOLUTION
    applies_to: STRUCTURE
    constraint: given identical STRUCTURE artifact, path resolution MUST be deterministic
    enforced_by: TBD

  - rule_id: STRUCTURE_BOOTSTRAP_ELIGIBLE
    applies_to: STRUCTURE
    constraint: runtime STRUCTURE artifacts MUST be loadable without compiler
    enforced_by: TBD

  - rule_id: STRUCTURE_FQDN_REFERENCES
    applies_to: STRUCTURE
    constraint: all artifact references in STRUCTURE MUST use FQDN
    enforced_by: ASSERT_FQDN_ONLY_REFERENCES_V0
```

---

## 1. Purpose

This constitution governs STRUCTURE artifacts — the configuration authority for the entire protocol system.

A STRUCTURE artifact declares how the protocol discovers, loads, and routes artifacts. It is the sole source of path governance, layer resolution, and artifact discovery configuration.

For structural field definitions see: `fb.constitution::SCHEMA_STRUCTURE_V0`
For usage examples and path patterns see: `doc/STRUCTURE_GUIDE.md`

---

## 2. Core Principles

- **Explicit Declaration:** All paths and layers MUST be explicitly declared. No implicit defaults.
- **Layer-Relative Paths:** All paths are relative to a declared layer root. Absolute paths are forbidden.
- **Layer Isolation:** Subpaths MUST NOT use `..` to escape layer boundaries.
- **Deterministic Resolution:** Same STRUCTURE artifact MUST produce identical resolution output.
- **Bootstrap Eligibility:** Runtime STRUCTURE artifacts MUST be loadable without the compiler.

---

## 3. Relationship to Other Constitutions

- `CONSTITUTION_COMPILER_V0` — compiler consumes STRUCTURE for artifact discovery (STRUCTURE_FQDN_TREE_AUTHORITY rule)
- `STRUCTURE_LAYER_AUTHORITY_V0` — declares valid layer codes that STRUCTURE artifacts may reference
- `CONSTITUTION_GOVERNANCE_V0` — root authority

---

## Version History

- **V0**: Initial rules-only constitution for STRUCTURE artifacts (2026-03-24)
  - Establishes 7 enforcement rules: explicit paths, no absolute paths, no escape, layer declared, deterministic resolution, bootstrap eligible, FQDN references
  - Schema extracted to SCHEMA_STRUCTURE_V0.json
  - Examples and implementation notes extracted to doc/STRUCTURE_GUIDE.md

---

## End of Constitution
