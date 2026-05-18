# CONSTITUTION_SECURITY_DOMAIN_V0

## Machine

```yaml
constitution_code: CONSTITUTION_SECURITY_DOMAIN_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0
fqdn: fb.security_domain::CONSTITUTION_SECURITY_DOMAIN_V0

core:
  summary: Governs information-control regimes, classification domains, compartment boundaries, secure flow and projection legality
  description: |
    Declares which information-control regime is active for a compiled snapshot.
    Governs classification domain membership, compartment boundary legality,
    cross-domain flow authorization, and secure trace projection constraints.

    FB_SECURITY_DOMAIN is also the sole owner of snapshot visibility classification.
    Visibility is an information-control concern; it belongs here and nowhere else.
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: SECURITY_DOMAIN_MUST_BE_DECLARED
    applies_to: compiled_snapshot
    constraint: >
      Every compiled snapshot MUST declare exactly one active security domain contract.
      A snapshot with no security domain declaration is a compiler validation failure.
    enforced_by: compiler_validation

  - rule_id: CROSS_DOMAIN_FLOW_REQUIRES_AUTHORIZATION
    applies_to: compiled_snapshot
    constraint: >
      Cross-domain data flow is not permitted unless the active security domain contract
      explicitly sets cross_domain_flow_allowed: true with an explicit authorization.
      In V0 UNCLASSIFIED_LOCAL mode, cross-domain flow is prohibited.
    enforced_by: compiler_validation

  - rule_id: VISIBILITY_OWNED_BY_SECURITY_DOMAIN
    applies_to: federation_boundary
    constraint: >
      Snapshot visibility and classification are information-control concerns.
      They MUST be declared only within FB_SECURITY_DOMAIN contracts.
      No other federation boundary (placement, trust, admissibility, topology) may
      declare or override visibility classifications.
    enforced_by: process_enforced

  - rule_id: TRACE_PROJECTION_RESPECTS_DOMAIN
    applies_to: runtime
    constraint: >
      Trace projection MUST NOT emit fields that violate the active security domain
      boundary. In V0 UNCLASSIFIED_LOCAL mode, all trace fields are emittable.
      In future classified modes, trace projection rules will be governed here.
    enforced_by: process_enforced

  - rule_id: RUNTIME_READS_SECURITY_DOMAIN_PASSIVELY
    applies_to: runtime
    constraint: >
      Runtime MAY read the active security domain contract for trace metadata emission.
      Runtime MUST NOT branch on security domain mode or perform classification
      enforcement. Classification enforcement is a compile-time governance concern.
    enforced_by: process_enforced
```

---

## Purpose

This constitution governs information-control regimes for PGS execution. It answers
the question: *within what information-control context is this snapshot permitted to execute,
and what visibility constraints apply?*

In V0, the only active regime is `UNCLASSIFIED_LOCAL` — execution is local, unclassified,
and trace output is unrestricted. This declaration seeds the governance axis that will
eventually govern classified execution (CONTROLLED, CONFIDENTIAL, SECRET, COMPARTMENTED).

## §1. Sole Owner of Visibility Classification

Snapshot visibility (`INTERNAL`, `FEDERATED_PUBLIC`) is an information-control concern
and belongs exclusively to this boundary. Other federation boundaries — placement, trust,
admissibility — do not carry visibility or classification declarations. This is a
deliberate separation of concerns enforced by the anti-duplication rule above.

## §2. V0 Security Domain

The only authorized security domain in V0 is `UNCLASSIFIED_LOCAL`.

This means:
- No classification labels are required on artifacts or payloads
- Cross-domain flow authorization is not needed (no domains to cross)
- Trace output may emit all fields without redaction
- Snapshot visibility is `INTERNAL` — consumed within the local federation only

## §3. Compiler Behavior

The compiler MUST:
- Discover the active security domain contract in this boundary
- Validate that exactly one contract is active
- Materialize security domain mode into the snapshot federation profile under:

```yaml
federation_profile:
  security_domain: UNCLASSIFIED_LOCAL
```

## §4. Runtime Behavior

The runtime MUST:
- Record `federation_profile.security_domain` in trace metadata
- Emit trace fields without restriction (UNCLASSIFIED_LOCAL has no redaction rules)
- NOT perform classification enforcement or domain-boundary checking

## §5. Future Expansion Path

```
UNCLASSIFIED_LOCAL
  → CONTROLLED
  → CONFIDENTIAL
  → SECRET
  → COMPARTMENTED
```

Each step requires a new security domain contract and new compiler validation passes
for cross-domain flow legality and trace projection constraints.

## §6. Versioning

Changes to security domain semantics require a new constitution version and migration rationale.
