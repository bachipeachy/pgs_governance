# CONSTITUTION_FEDERATION_BOUNDARY_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_FEDERATION_BOUNDARY_V0
constitution_code: CONSTITUTION_FEDERATION_BOUNDARY_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: >
    Governs the existence, semantics, and placement rules of federation boundaries.
    Defines sovereign vs delegated authority, governance locality doctrine, cross-boundary
    legality, and the anti-sprawl rule that prevents boundary proliferation.
  scope: system
  enforcement_model: process_enforced

doctrine: >
  A federation boundary is a semantic sovereignty construct, not an implementation
  packaging construct. A boundary exists only when a distinct governance authority exists.

rules:
  - rule_id: BOUNDARY_SEMANTIC_SOVEREIGNTY
    applies_to: federation_boundary
    constraint: >
      A federation boundary MUST correspond to a distinct, named semantic governance
      authority. A boundary MUST NOT be introduced to represent a packaging unit,
      deployment boundary, runtime unit, or repository boundary. The existence of a
      boundary is justified only by the existence of governance authority, not by
      implementation convenience.
    enforced_by: PROCESS_ENFORCED

  - rule_id: BOUNDARY_EXISTS_WHEN_AUTHORITY_EXISTS
    applies_to: federation_boundary
    constraint: >
      A federation boundary MUST NOT be created unless at least one governance artifact
      (constitution, invariant, or assertion) exists within it. Empty or placeholder
      boundaries are constitutional violations. The first governance law triggers boundary
      creation; boundary creation does not precede governance law.
    enforced_by: PROCESS_ENFORCED

  - rule_id: BOUNDARY_SOVEREIGNTY_LEVELS
    applies_to: federation_boundary
    constraint: >
      Exactly one sovereign boundary exists: FB_CONSTITUTION. All other boundaries are
      delegated. Delegated boundaries derive authority from FB_CONSTITUTION and MUST NOT
      exceed that delegation. A second sovereign boundary is a constitutional violation.
    enforced_by: PROCESS_ENFORCED

  - rule_id: BOUNDARY_OPEN_ENDED
    applies_to: federation_boundary
    constraint: >
      Federation boundaries are open-ended. New boundaries MAY be introduced as distinct
      governance authorities emerge. There is no fixed or closed set of federation
      boundaries. This contrasts with Functional Layers (closed) and Execution Concerns
      (closed), which have fixed membership.
    enforced_by: PROCESS_ENFORCED

  - rule_id: BOUNDARY_GOVERNANCE_LOCALITY
    applies_to: governance_artifact
    constraint: >
      A governance artifact belongs in pgs_governance (central) if and only if it governs
      all PGS systems universally. A governance artifact belongs in a domain repository
      (local) if it exists because of domain-specific semantics. Placing domain-specific
      governance centrally is a governance locality violation. Placing universal governance
      locally is also a violation.
    enforced_by: PROCESS_ENFORCED

  - rule_id: BOUNDARY_NO_CROSS_OWNERSHIP
    applies_to: federation_boundary
    constraint: >
      No federation boundary MAY declare governance authority over artifacts owned by
      another boundary without explicit delegation. Cross-boundary references MUST be
      declared. Implicit authority inheritance and ambient cross-boundary governance are
      prohibited.
    enforced_by: PROCESS_ENFORCED

  - rule_id: BOUNDARY_ANTI_SPRAWL
    applies_to: federation_boundary
    constraint: >
      Boundaries MUST NOT be introduced to mirror: organizational structure, repository
      topology, deployment units, runtime packaging, or implementation convenience.
      The only valid justification for a new boundary is a new distinct semantic governance
      authority that cannot be expressed within existing boundaries.
    enforced_by: PROCESS_ENFORCED

  - rule_id: BOUNDARY_ONBOARDING_REQUIRED
    applies_to: federation_boundary
    constraint: >
      Every new FB_* introduced into PGS MUST complete four onboarding steps before
      the boundary is considered compiler-admissible: (1) governance registration —
      directory created under pgs_governance/registry/FB_*/; (2) namespace derivation rule
      declared in STRUCTURE_IDENTITY_V0 mapping the registry module path to a fb.*
      namespace; (3) all governed artifacts within the boundary contain a valid ## Machine
      declaration parseable by S1_EXTRACT; (4) governance compilation succeeds without
      errors for all affected build structures. Omitting any step is a constitutional
      violation — the compiler will fail with E901 or E101 and the boundary is not
      admissible until all steps are satisfied.
    enforced_by: PROCESS_ENFORCED
```

---

**Header Block (Documentation)**
- **Constitution ID:** CONSTITUTION_FEDERATION_BOUNDARY_V0
- **Tier:** Sovereign Authority
- **Applies To:** All federation boundaries in the PGS governance model
- **Status:** Active — Foundational
- **Supersedes:** NONE
- **Governed By:** fb.constitution::CONSTITUTION_GOVERNANCE_V0
- **Dependencies:** CONSTITUTION_GOVERNANCE_V0

---

## Foundational Doctrine

**A federation boundary is a semantic sovereignty construct, not an implementation packaging construct.**

A federation boundary declares that a distinct governance authority exists — one with jurisdiction over a named set of protocol semantics. The boundary is not a folder, not a package, not a deployment unit, and not a repository. It is a declaration of semantic sovereignty.

This distinction is critical. If boundaries proliferate to mirror organizational structure, repository topology, or implementation convenience, the governance model corrupts. Boundaries become arbitrary. Placement decisions lose meaning. The semantic clarity of the registry erodes.

**The anti-sprawl rule:** A federation boundary exists only when a distinct governance authority exists.

---

## §1. Sovereignty Model

### 1.1 Two Levels of Sovereignty

The PGS federation model has exactly two sovereignty levels:

| Level | Boundary | Description |
|-------|----------|-------------|
| Sovereign | FB_CONSTITUTION | Root authority. Governs all other boundaries. One only. |
| Delegated | All others | Authority derived from FB_CONSTITUTION. Governs within declared scope. |

FB_CONSTITUTION is the one sovereign boundary. It cannot be superseded, replicated, or distributed. All other federation boundaries are delegated — they derive authority from FB_CONSTITUTION and MUST NOT exceed that delegation.

A second sovereign boundary is a constitutional violation.

### 1.2 Delegated Authority Limits

A delegated boundary:
- MAY declare constitutions, invariants, and assertions within its governance scope
- MAY reference artifacts from other boundaries via declared cross-boundary references
- MAY NOT override or supersede FB_CONSTITUTION rules
- MAY NOT claim governance authority over artifacts owned by another boundary without explicit delegation

---

## §2. Boundary Existence Rule

### 2.1 When A Boundary May Be Created

A federation boundary MUST NOT be created speculatively. It MUST NOT be created:
- In anticipation of future governance rules
- To scaffold empty structure
- To mirror a repository, package, or deployment unit
- To signal intent without substance

A boundary is created when and only when:

> The first governance artifact (constitution, invariant, or assertion) that belongs within that boundary's authority is authored.

The governance law creates the boundary. The boundary does not precede the law.

### 2.2 What Constitutes A Distinct Governance Authority

A distinct governance authority exists when a named set of protocol semantics:
1. Has rules that apply universally across that semantic domain
2. Cannot be subsumed within an existing boundary without semantic confusion
3. Requires its own constitution to define its scope and constraints

---

## §3. Open-Ended vs Closed Structures

Federation boundaries are **open-ended**. The current set (FB_CONSTITUTION, FB_TOPOLOGY, FB_TRANSPORT, FB_AUTHORITY, FB_VOCABULARY, FB_CONFORMANCE, FB_IDENTITY, FB_BLOCKCHAIN, FB_AI_GOVERNANCE, FB_CHANGE_MGMT) is not fixed. New boundaries emerge as distinct governance authorities emerge.

This contrasts with:

| Structure | Membership |
|-----------|------------|
| Federation Boundaries | Open-ended — new boundaries emerge as governance matures |
| Functional Layers | Closed — defined in STRUCTURE_DISCOVERY_V0 |
| Execution Concerns | Closed — defined in FB_TOPOLOGY constitutions |

The open-ended nature of federation boundaries is a feature, not a gap. It allows governance to grow with the protocol without requiring upfront declaration of all possible governance authorities.

---

## §4. Governance Locality Doctrine

### 4.1 The Central/Local Rule

| Governance Type | Correct Location |
|-----------------|-----------------|
| Universal platform governance law | pgs_governance |
| Reusable cross-domain governance | pgs_governance |
| Domain-specific governance law | domain repository |
| Domain orchestration policy | domain repository |
| Domain execution rules | domain repository |

The test for central placement is strict: **a governance artifact belongs in pgs_governance if and only if it governs all PGS systems universally.**

If a governance rule exists because blockchain needs it, or AI governance needs it, or any specific domain needs it — it belongs in that domain's repository.

### 4.2 Domain Governance Capability

Domain repositories are governance-capable. A domain repository MAY contain:
- Local constitutions (domain semantic law)
- Local invariants (domain-specific constraints)
- Local assertions (domain build-time checks)

Domain governance artifacts are introduced when the first domain-specific governance law exists — not before.

### 4.3 Domain Governance Escalation

A governance rule that begins domain-local MAY be escalated to central governance if it is determined to apply universally. Escalation requires:
1. Evidence that the rule governs all PGS systems, not just one domain
2. Removal from the domain repository
3. Introduction into the appropriate federation boundary in pgs_governance

Escalation is explicit and versioned. It is not automatic.

---

## §5. Cross-Boundary Reference Legality

### 5.1 What Is Permitted

A governance artifact in one boundary MAY reference an artifact from another boundary when:
- The reference is to a universally applicable governance law
- The reference direction is delegated → sovereign (not sovereign → delegated)
- The reference is declared explicitly in the artifact's `governed_by` or dependency fields

### 5.2 What Is Prohibited

- Circular cross-boundary governance references
- Implicit authority inheritance across boundaries
- A delegated boundary overriding a sovereign boundary's rules
- Ambient governance (rules that apply across boundaries without explicit declaration)

---

## §6. Anti-Sprawl Doctrine

Federation boundaries MUST NOT proliferate to mirror:

- **Organizational structure** — teams, squads, or product groups do not constitute governance authorities
- **Repository topology** — having a separate repo does not entitle a domain to a separate boundary in pgs_governance
- **Deployment units** — service boundaries, microservices, or infrastructure boundaries are not governance boundaries
- **Runtime packaging** — how code is packaged or deployed is irrelevant to governance placement
- **Implementation convenience** — grouping artifacts for discoverability or tooling reasons is not a governance justification

The question to ask before creating a boundary is:

> **Does a distinct semantic governance authority exist here — one with jurisdiction over a named set of protocol semantics that cannot be expressed within existing boundaries?**

If the answer is no, the boundary MUST NOT be created.

---

## §7. Boundary Evolution Doctrine

### 7.1 Boundaries Are Stable Once Created

A federation boundary that has been created with governance content is stable. Its governance artifacts are immutable (new versions for changes). The boundary itself persists.

### 7.2 Boundaries Are Not Reorganized Freely

Moving governance artifacts between boundaries is a governance-visible change. It changes FQDNs, which are immutable references in artifacts across the system. Such moves require:
- New versioned artifacts at the new FQDN
- Explicit deprecation of old FQDNs
- Cross-repo reference updates

Boundary reorganization is high-cost. Invest in correct placement at authoring time.

### 7.3 Future Boundaries Are Anticipated But Not Pre-Created

The federation model anticipates future boundaries as protocol complexity grows. Examples that may emerge:

- Boundaries governing cryptographic trust
- Boundaries governing execution placement policy
- Boundaries governing classified or restricted execution

These are anticipated but MUST NOT be pre-created. They come into existence when governance law demands them.

---

## §8. Current Boundary Inventory

As of V0, the declared federation boundaries are:

| Boundary | Authority | Governance Scope |
|----------|-----------|-----------------|
| FB_CONSTITUTION | Sovereign | Root protocol semantics, governance meta-rules, artifact identity, FQDN |
| FB_TOPOLOGY | Delegated | Execution topology, WF/CC legality, CT/CS surface closure, routing, binding |
| FB_TRANSPORT | Delegated | Ingress/egress semantics, transport boundary rules, admission |
| FB_AUTHORITY | Delegated | Actor authority, execution admissibility, authority state |
| FB_VOCABULARY | Delegated | Protocol terminology, execution state vocabulary |
| FB_CONFORMANCE | Delegated | Test data, conformance assertion rules |
| FB_IDENTITY | Delegated | Actor identity semantics, identity/authority separation |
| FB_BLOCKCHAIN | Delegated | Blockchain domain build configuration |
| FB_AI_GOVERNANCE | Delegated | AI governance domain build configuration |
| FB_CHANGE_MGMT | Delegated | Governed SDLC change management pipeline — Change Request through Authoring Manifest |

Note: FB_BLOCKCHAIN and FB_AI_GOVERNANCE currently contain only build configuration structures. They represent domain boundaries within pgs_governance's build system. Domain-specific governance laws for these domains reside in their respective domain repositories. FB_CHANGE_MGMT governs the protocol authoring lifecycle itself — the governed pipeline from human intent to admissible protocol artifact.

---

## §9. Closing Principle

Federation boundaries are not discovered by looking at the filesystem.
They are not inferred from repository structure.
They are not assigned by organizational mandate.

They emerge when governance authority emerges.

Governance authority justifies boundaries.
Boundaries do not justify governance authority.

---

## End of Constitution