# INVARIANT_PROTOCOL_SURFACE_CLOSED_V0

## Machine

```yaml
invariant_code: INVARIANT_PROTOCOL_SURFACE_CLOSED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Protocol surface must be closed: all artifact references must resolve
    to valid FQDNs in the compilation graph. No dangling references, no
    short names in reference fields.

  enforcement_stage:
    - compiler_validation

  scope:
    - ALL_ARTIFACT_KINDS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - dangling_reference: "Reference to artifact not in compilation graph"
    - short_name_reference: "Reference using short name instead of FQDN"
    - unresolved_dependency: "Dependency declared but not discoverable"
    - ambiguous_reference: "Short name resolving to multiple FQDNs"

  clarification:
    bootstrap_artifacts: >
      Bootstrap artifacts (STRUCTURE, WF, RB for bootstrap phase) are exempt
      from closure checks during bootstrap discovery phase only.
    external_references: >
      External system references (URLs, file paths outside PGS) must be
      marked as external in artifact metadata, not treated as FQDN references.
    transitive_closure: >
      Closure includes transitive references. If A → B → C, all three must
      be in compilation graph.
```

---

## Purpose

Ensure protocol surface is closed during compilation.

**Core Principle**: Every reference must resolve to a known artifact in the compilation graph.

---

## Enforcement Rules

### Rule 1: No Dangling References

Every reference must resolve to an artifact in the compilation graph.

**Violation**:
```yaml
references:
  - "pgs.platform.compiler::CT_MISSING_V0"  # Not found!
```

**Detection**: After discovery phase, check all references against graph.

---

### Rule 2: No Short Name References

All references must use FQDN format (`fb.vocabulary::artifact_code`).

**Violation**:
```yaml
references:
  - "CT_TRANSFORM_V0"  # Short name!
```

**Expected**:
```yaml
references:
  - "pgs.platform.compiler::CT_TRANSFORM_V0"  # FQDN
```

**Detection**: After normalization, check for `::` in all reference strings.

---

### Rule 3: No Ambiguous References

Short names that could resolve to multiple FQDNs are forbidden.

**Violation**:
```yaml
# Ambiguous: CT_SCAN_V0 exists in multiple namespaces
references:
  - "CT_SCAN_V0"
```

**Detection**: Cross-reference discovery results to detect duplicates.

---

### Rule 4: Transitive Closure

If A references B, and B references C, all three must be in the graph.

**Violation**:
```yaml
# A → B (in graph)
# B → C (C missing!)
```

**Detection**: Recursive reference traversal until closure confirmed.

---

## Scope

**Applies to**:
- All discovered artifacts (platform + domains)
- All reference fields (explicit + derived)
- All compilation phases after normalization

**Exempt**:
- Bootstrap artifacts during bootstrap phase only
- External references (explicitly marked)
- Runtime-only references (not compile-time dependencies)

---

## Version History

- **V0**: Initial invariant (2026-03-31) - ASSERT Activation Phase
