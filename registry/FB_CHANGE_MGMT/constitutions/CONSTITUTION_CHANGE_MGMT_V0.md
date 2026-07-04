# CONSTITUTION_CHANGE_MGMT_V0

## Machine
```yaml
fqdn: fb.change_mgmt::CONSTITUTION_CHANGE_MGMT_V0
constitution_code: CONSTITUTION_CHANGE_MGMT_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs the PGS change management design and authoring pipeline (Stages 0–7) — from Change Request through the Authoring Mandate; the S8/S9 construction phase is governed by fb.change_mgmt::CONSTITUTION_CONSTRUCTION_V0
  scope: change_management
  enforcement_model: process_enforced

rules:
  - rule_id: STAGE_GATE_MANDATORY
    applies_to: all_stages
    constraint: no stage may begin before the prior stage gate is satisfied; no stage may be skipped
    enforced_by: PROCESS_ENFORCED

  - rule_id: DOSSIER_FIRST
    applies_to: all_change_requests
    constraint: the primary unit is the governed change dossier; all stage documents for one CR live flat inside change_mgmt/dossiers/[domain]/[subdomain]/
    enforced_by: PROCESS_ENFORCED

  - rule_id: PURITY_FILTER_MANDATORY
    applies_to: stages_1_through_4
    constraint: business analysis must contain WHAT only; HOW decisions must be deferred to Design Intent; purity filter enforced by authoring agent throughout
    enforced_by: PROCESS_ENFORCED

  - rule_id: CONSTRUCTION_PHASE_DELEGATED
    applies_to: stages_8_and_9
    constraint: the S8 Build Sheet Set, artifact construction, compiler-gated promotion, and the S9 Construction Record are governed by fb.change_mgmt::CONSTITUTION_CONSTRUCTION_V0, not here; a Change Request closes only after the S9 Construction Record is complete and its artifacts compile clean
    enforced_by: PROCESS_ENFORCED

  - rule_id: GROUNDING_NOT_INHERITED
    applies_to: all_stages
    constraint: a stage that introduces a new claim about an existing artifact must establish grounding against authoritative sources (PI/PPS); grounding does not carry from prior-stage narrative; legitimate synthesis or distillation stages may make zero queries and remain conformant
    enforced_by: PROCESS_ENFORCED

  - rule_id: DISCOVERY_FINDINGS_REQUIRE_PI_VALIDATION
    applies_to: all_stages
    constraint: a newly discovered concern, constraint, assumption, dependency, architectural requirement, or gap shall be confirmed with PI before promotion into governed artifacts; discovery may propose, PI authorizes applicability
    enforced_by: PROCESS_ENFORCED

  - rule_id: CONCERN_TRACEABILITY_REQUIRED
    applies_to: all_stages
    constraint: a concern promoted into later stages must remain traceable to its originating finding, validation, or governing constraint (concern identity, not only artifact identity), so audits of immutability, chain-state, genesis, or integrity need not replay entire dossiers
    enforced_by: PROCESS_ENFORCED

  - rule_id: IDENTITY_PRESERVING_REFERENCE_VALIDATION
    applies_to: all_stages
    constraint: artifact references are validated by resolving identity against the artifact index before classifying; exact, typo-alias, wrong-domain, and proposed-new all preserve identity; only no-identity-anywhere is a fabrication; aggregate not-found counts are inadmissible
    enforced_by: PROCESS_ENFORCED
```

---

## 1. Purpose

This constitution establishes FB_CHANGE_MGMT as a first-class governance boundary over the PGS change management **design and authoring pipeline (Stages 0–7)**. It governs the process from Change Request through the Authoring Mandate — the governed evidence chain that *specifies* the protocol artifacts to be built. The S8/S9 **construction phase** — projecting that design into artifacts and landing them — is governed by its peer constitution, `CONSTITUTION_CONSTRUCTION_V0`.

The pipeline makes pre-BI cognitive work — problem framing, capability discovery, dependency resolution — governed and agent-assisted. Without this constitution, that work is implicit and human-only.

The pipeline is itself a candidate PGS Workflow. The authoring agent operates as a governed actor within the system it helps build.

---

## 2. Scope Boundary

This constitution governs:
- The change management design/authoring pipeline structure (Stages 0 through 7)
- Stage gate sequencing requirements
- The dossier-first ontology for change requests
- Purity constraints across business analysis stages (1–4)
- The Authoring Mandate as mandated (not advisory) build sequence
- CR Closure as the terminal event — the CR closes after construction is complete (mechanics governed by `CONSTITUTION_CONSTRUCTION_V0`)

This constitution does NOT govern:
- The S8/S9 construction phase — Build Sheet Set, construction, compiler-gated promotion, Construction Record (governed by `fb.change_mgmt::CONSTITUTION_CONSTRUCTION_V0`)
- Protocol artifact authoring or compilation (governed by pgs_compiler)
- Runtime execution semantics (governed by fb.topology::CONSTITUTION_EXECUTION_V0)
- Vocabulary admissibility (governed by fb.vocabulary::CONSTITUTION_VOCABULARY_V0)
- Stage template contents (governed by stage template documents in pgs_change_mgmt)
- Mechanism by which Governance Decision Gates are satisfied (human in V0; extensible in future versions)

---

## 3. Core Principles

- **Stage Gate Mandatory:** No stage may begin before the prior stage gate is satisfied. No stage may be skipped.
- **Dossier-First:** The primary unit is the governed change dossier. All stage documents for one CR live flat inside `change_mgmt/dossiers/[domain]/[subdomain]/`.
- **Purity Filter:** Business analysis stages (1–4) must contain WHAT only. HOW decisions are deferred to Design Intent (Stage 6b). The purity filter is enforced by the authoring agent throughout.
- **Authoring Mandate is Mandated:** Stage 7 produces the only admissible build sequence consistent with the dependency graph — not one plan among alternatives. Divergence from the Authoring Mandate is a governance event, recorded downstream in the S9 Construction Record.
- **Construction is Delegated:** Stages 8–9 (Build Sheet Set → construct → promote → Construction Record) are governed by `CONSTITUTION_CONSTRUCTION_V0`. This pipeline hands the Authoring Mandate to construction; it does not itself build.
- **CR Closure follows Construction:** A Change Request closes only after the S9 Construction Record is complete and its artifacts compile clean. CR closure is this constitution's terminal event; the construction mechanics it depends on are governed by `CONSTITUTION_CONSTRUCTION_V0`.
- **PPS Snapshot as Baseline Oracle:** The PPS snapshot is the authoritative baseline for gap analysis. The vocabulary_snapshot is too shallow for this purpose.
- **Governance Decision Gates:** Gates are human in V0. Future versions may satisfy them by committee, federation, or policy engine. The gate is a governance concern, not a human-presence requirement.
- **Grounding Is Not Inherited:** A stage that introduces a new claim about an existing artifact must establish grounding against authoritative sources (PI/PPS). Grounding does not carry from prior-stage narrative. Legitimate synthesis or distillation stages may make zero queries and remain conformant — the focus is new claims, not query counts.
- **Discovery Findings Require PI Validation:** A newly discovered concern, constraint, assumption, dependency, architectural requirement, or gap shall be confirmed with PI before promotion into governed artifacts. Discovery may propose; PI authorizes applicability.
- **Concern Traceability Required:** A concern promoted into later stages must remain traceable to its originating finding, validation, or governing constraint — concern identity, not only artifact identity — so that audits of immutability, chain-state, genesis, or integrity need not replay entire dossiers.
- **Identity-Preserving Reference Validation:** Artifact references are validated by resolving identity against the artifact index before classifying. Exact, typo-alias, wrong-domain, and proposed-new references all preserve identity; only no-identity-anywhere is a fabrication. Aggregate not-found counts are inadmissible.

---

## 4. Pipeline Structure

```
Change Request
    ↓ Stage 0 — Classification (CR type gates which stages run)
    ↓ Stage 1 — Input Elicitation (Problem + Outcome + Known Facts)
    ↓ Stage 2 — Domain Model Discovery (Actors, Entities, Resources, Events, Relationships)
    ↓ [Stage 3 — Analysis Loop — convergence, not linear]
         3a  Capability Discovery
         3b  Dependency Discovery
         3c  Constraint Discovery
         3d  PPS Baseline Comparison
         3e  Gap Register + Discovery Saturation check
              → SATURATED: exit loop
              → NOT SATURATED: continue loop
    ↓ Stage 4 — Business Model (canonical artifact)
    ↓ Stage 4b — Authoring Scope (IN SCOPE / FUTURE CR boundary)
    ↓ Stage 5 — Business Intent (human-readable projection of scoped BM)
    ↓ [Governance Decision Gate]
    ↓ Stage 6 — Governance Intent (WHERE: domain/subdomain/ownership/boundaries)
    ↓ [Governance Decision Gate]
    ↓ Stage 6b — Design Intent (HOW: artifact family mapping + design decisions)
    ↓ [Governance Decision Gate]
    ↓ Stage 7 — Authoring Mandate (topological sort of DI dependency graph)
    ═══ handoff to the Construction phase (CONSTITUTION_CONSTRUCTION_V0) ═══
    ↓ Stage 8 — Build Sheet Set  →  construct  →  compiler-gated promotion
    ↓ Stage 9 — Construction Record (evidence)
    ↓ CR Closure — the Change Request closes after the S9 Construction Record is complete and its artifacts compile clean
```

**Discovery Saturation** (Stage 3 exit criterion) requires ALL THREE simultaneously:
1. No unresolved CRITICAL gaps in the gap register
2. No unresolved analyst questions
3. No dependency expansion in the last review pass

---

## 5. Separation of Concerns

| Stage | Question Answered |
|-------|-------------------|
| Stages 1–4 | WHAT — business analysis |
| Stage 6 | WHERE — governance placement (domain, subdomain, ownership, boundaries) |
| Stage 6b | HOW — artifact family mapping, design decisions |
| Stage 7 | BUILD ORDER — topological sort of the DI dependency graph |
| CR Closure | CLOSED — the CR closes after construction; whether execution matched design is recorded in the S9 Construction Record (governed by `CONSTITUTION_CONSTRUCTION_V0`) |

Violations:
- Artifact family names (CC_, WF_, CT_, CS_) in Stages 1–6 are purity violations.
- Build order in Stage 6b is a scope violation.
- HOW decisions in Stages 1–4 are purity violations; they are redirected to the Design Decisions Register.

---

## 6. Protocol Boundaries (Non-Goals)

This pipeline does NOT:
- Auto-generate protocol artifacts (CC, CT, CS JSON files) — that is the S8/S9 construction phase (`CONSTITUTION_CONSTRUCTION_V0`), not this design/authoring pipeline
- Auto-compile or auto-deploy
- Bypass Governance Decision Gates
- Treat vocabulary_snapshot as authoritative (PPS snapshot is the Baseline Oracle)
- Map artifact families during business analysis stages

---

## 7. V0 Scope

V0 intentionally governs:
- Human-in-the-loop pipeline (agent-assisted, human-gated)
- Single change request per dossier
- pgs_change_mgmt as the reference implementation

V0 intentionally defers:
- Parallel change request processing
- Federation-level governance gates

(Automated artifact generation from the Authoring Mandate is realized in the construction phase, governed by `CONSTITUTION_CONSTRUCTION_V0`.)

---

## End of Constitution
