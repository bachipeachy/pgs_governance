# CONSTITUTION_CONSTRUCTION_V0

## Machine
```yaml
fqdn: fb.change_mgmt::CONSTITUTION_CONSTRUCTION_V0
constitution_code: CONSTITUTION_CONSTRUCTION_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Governs the PGS construction phase — the deterministic transformation of the governed Execution Specification (S6b/S7) into protocol artifacts (S8 Build Sheet Set), their compiler-gated promotion, and the S9 Construction Record. Construction consists of Lowering (deterministic expansion of uniquely-derivable information) and Serialization (deterministic encoding into governed artifact form); it is never authoring — the builder decides nothing.
  scope: construction
  enforcement_model: process_and_compiler_enforced

rules:
  - rule_id: PROJECTION_COMPLETENESS
    applies_to: all_construction_stages
    constraint: every downstream stage consumes only declared structured projections (gov_projection handoffs); no stage may recover information by re-parsing a narrative document
    enforced_by: PROCESS_ENFORCED

  - rule_id: PROJECTION_FIDELITY
    applies_to: stage_8
    constraint: a projection is valid only if Projection(markdown) == Projection(JSON) over the stage's emit-fields; a projection that does not equal its governed source over the intended fields is invalid, not merely incomplete
    enforced_by: PROCESS_ENFORCED

  - rule_id: PROJECTION_SEMANTIC_CONSISTENCY
    applies_to: stage_8
    constraint: the S8 Build Sheet Set must preserve the S7 semantic graph with no addition, loss, or mutation of semantic entities; structural closure alone can pass a semantically-drifted artifact, so semantic preservation across the S7 to S8 projection is a distinct gate
    enforced_by: PROCESS_ENFORCED

  - rule_id: UNIQUELY_DETERMINED_OR_STOP
    applies_to: construction
    constraint: the primitive construction theorem. Construction may introduce information into a protocol artifact ONLY when that information is uniquely determined by governed inputs and constitutional rules; if zero or more than one valid outcome exists, construction SHALL STOP and report a gap — selecting among alternatives is design, owned upstream by the Execution Specification (S6b). Construction realizes this as deterministic LOWERING (expansion of a governed default where the graph is silent, plus propagation of declared information along edges) followed by SERIALIZATION (encoding the result; it introduces no information). Every lowering rule is an instance of this theorem (exactly-one-or-STOP); CONSTRUCTION_IS_NON_AUTHORIAL_TRANSCRIPTION and the default-expansion guardrail derive from it; it interlocks with PROJECTION_COMPLETENESS — a closed projection is one where every construction step has exactly one answer, so a multi-outcome ambiguity is exactly a gap. The catalog of lowering rules (DEFAULT_EXECUTION_EXPANSION, BINDING_PROPAGATION, TYPE_PROPAGATION, …) lives in CONSTRUCTION_MODEL_V0 and extends the doctrine, never this constitution.
    enforced_by: PROCESS_ENFORCED

  - rule_id: CONSTRUCTION_IS_NON_AUTHORIAL_TRANSCRIPTION
    applies_to: construction
    constraint: a derivation of UNIQUELY_DETERMINED_OR_STOP. Construction is transcription of a complete specification, not authoring. Sub-rule (no design in construction) — the S8 Build Sheet is assembled not authored; a decision required during construction is a GAP resolved upstream (S5-S7); a missing element is a STOP, never a guess. Enforcement outcome (no invention) — zero design invention is demonstrated empirically by independent-builder convergence, never proven statically
    enforced_by: PROCESS_ENFORCED

  - rule_id: CONSTRUCTION_CLOSURE_STATIC
    applies_to: stage_8
    constraint: a Build Sheet reaches CONSTRUCTION_READY only when three statically-checkable asserts hold — ASSERT_STRUCTURE_COMPLETE, ASSERT_PROVENANCE_COMPLETE, ASSERT_DECISION_COMPLETE (no GAP of any class remains); a set is CONSTRUCTION_READY when every sheet passes all three
    enforced_by: compiler_validation

  - rule_id: BUILDER_NON_AUTHORITATIVE
    applies_to: construction
    constraint: the builder produces an artifact but never self-reports conformance; conformance is measured externally — structural invention against the sheet, convergence against a second builder, admissibility by the compiler. Authority lives in the specification and the gates, not in the builder; builders are interchangeable
    enforced_by: PROCESS_ENFORCED

  - rule_id: SINGLE_COMPILATION_CONTEXT
    applies_to: construction_validation
    constraint: all construction validation MUST occur against a read-only canonical snapshot plus an ephemeral overlay, never against mutable registry state; a single truth context is required so validation is deterministic and a candidate cannot be valid in staging yet invalid in canonical
    enforced_by: PROCESS_ENFORCED

  - rule_id: COMPILER_GATED_PROMOTION
    applies_to: promotion
    constraint: only a candidate the compiler admits (compile clean plus pi validate strict) may be promoted into the canonical registry; a non-admissible candidate is rolled back and its diagnostics recorded for regeneration; the registry only ever retains validated artifacts; generate, never patch; promotion follows validation, never precedes it
    enforced_by: compiler_validation

  - rule_id: PROMOTION_SEMANTICS_GOVERNED_BY_CM
    applies_to: promotion
    constraint: this constitution is the law of promotion — what may land, the preconditions (a green candidate), rollback-on-red, and generate-never-patch are governed here
    enforced_by: PROCESS_ENFORCED

  - rule_id: PROMOTION_EXECUTION_IMPLEMENTED_BY_SDLC
    applies_to: promotion
    constraint: the mechanics of the cross-repo registry mutation are executed by the SDLC promotion layer, not by change management; change management is the law, the SDLC layer is the execution system; the present bridge is a transitional executor and change management MUST NOT own the mutation
    enforced_by: PROCESS_ENFORCED

  - rule_id: CONSTRUCTION_RECORD_EVIDENCE_ONLY
    applies_to: stage_9
    constraint: the S9 Construction Record records what actually happened during construction — evidence only; it contains no new design, schema, routing, binding, or composition decision; a deviation from the Build Sheet is explicit and approved, never silent; a missing design decision discovered during construction is returned upstream (S5-S7) and re-enters through S8, never resolved in S9
    enforced_by: PROCESS_ENFORCED

  - rule_id: CONSTRUCTION_LADDER_ENDS_AT_CLOSED
    applies_to: construction
    constraint: the construction readiness ladder is DESIGNED to BUILDABLE to CONSTRUCTION_READY to CONSTRUCTION_CLOSED; runtime lifecycle (DEPLOYED, RUNTIME_VALIDATED) is out of this constitution's authority and is governed downstream by fb.topology::CONSTITUTION_EXECUTION_V0 and fb.topology::CONSTITUTION_TRACE_EXECUTION_V0
    enforced_by: PROCESS_ENFORCED
```

---

## 1. Purpose

This constitution establishes **construction** as a first-class governance authority within the
`FB_CHANGE_MGMT` boundary, peer to `CONSTITUTION_CHANGE_MGMT_V0`. Where the change-management
constitution governs the S0–S7 **design/authoring pipeline** (human-gated decisions), this
constitution governs the S8–S9 **construction phase**: the mechanized projection of governed design
into protocol artifacts, their compiler-gated promotion, and the evidence record of what was built.

The two constitutions encode a real architectural seam: **design is open; construction must
converge.** In design (S0–S7) a human authority decides *what*, *where*, and *how*. In construction
(S8–S9) **the builder decides nothing** — every step, input, output, and routing outcome is already
governed, and a missing element is a `STOP`, never an invention. That opposition in posture toward
decision authority is why construction is governed separately.

Construction is what makes builders interchangeable. A Qwen-family model, a DeepSeek-family model,
Claude, or a future deterministic generator are all just transcribers behind the same gates; authority
lives in the specification and the gates, not in the thing that fills them in.

---

## 2. Scope Boundary

This constitution governs:
- The S8 Build Sheet Set as a **construction projection** (assembled from S2/S5/S6b/S7; no new design)
- The projection gates — Projection Completeness, Projection Fidelity, Projection Semantic Consistency
- Construction Closure — the static asserts that raise a Build Sheet to `CONSTRUCTION_READY`
- The construction act — non-authorial transcription, builder abstention (`STOP`), and empirical
  zero-invention (independent-builder convergence → `CONSTRUCTION_CLOSED`)
- **Promotion law** — the preconditions and outcomes of landing a candidate in the canonical registry
  (green-only, rollback-on-red, generate-never-patch, single compilation context)
- The S9 Construction Record as an **evidence-only** artifact

This constitution does NOT govern:
- Design decisions, business analysis, or intent — governed by `CONSTITUTION_CHANGE_MGMT_V0` (S0–S7)
- Protocol artifact admissibility semantics per kind — governed by the `FB_TOPOLOGY` constitutions
  (`CONSTITUTION_WORKFLOW_V0`, `CONSTITUTION_CAPABILITY_CONTRACT_V0`, …) and the compiler
- **Promotion execution** — the cross-repo registry mutation mechanics belong to the SDLC/Promotion
  layer, not change management (this constitution states the law, not the mechanism)
- **Runtime lifecycle** — `DEPLOYED → RUNTIME_VALIDATED` is governed downstream by
  `fb.topology::CONSTITUTION_EXECUTION_V0` / `CONSTITUTION_TRACE_EXECUTION_V0`

---

## 3. Core Principles

- **Uniquely Determined or Stop (the primitive theorem):** construction may introduce information
  *only* where it is uniquely determined by governed inputs; zero or more than one valid outcome is a
  design choice → `STOP` and report a gap. Construction realizes this as **Lowering** (expansion of a
  governed default where the graph is silent + propagation of declared information along edges) then
  **Serialization** (encoding — inventing nothing). Every principle below is a consequence — non-authorial
  transcription, the default-expansion guardrail, and projection completeness all reduce to "exactly
  one answer, or stop."
- **Projection Completeness:** every downstream stage consumes declared structured projections; no
  stage recovers information by re-parsing narrative. Markdown is documentation, not input.
- **Projection Fidelity:** `Projection(markdown) == Projection(JSON)` over the stage's emit-fields. A
  projection that does not equal its governed source over the intended fields is *invalid*, not merely
  incomplete.
- **Projection Semantic Consistency:** S8 preserves the S7 semantic graph — no addition, loss, or
  mutation of semantic entities. Structural closure alone can pass a semantically-drifted artifact.
- **Construction is Non-Authorial Transcription:** the builder materialises a complete specification;
  it introduces no design. A required element missing from the sheet is a `STOP`, never a guess.
- **Construction Reliability = Specification Completeness × Builder Abstention Fidelity:** either
  factor at zero makes the product zero. A complete sheet handed to a hallucinating builder is
  unreliable; a perfectly-abstaining builder handed an incomplete sheet produces nothing.
- **The Builder is Never Authoritative:** conformance is measured externally — structural invention,
  convergence, compiler admissibility — and recorded as evidence independent of the builder.
- **Single Compilation Context:** validation runs against a read-only canonical snapshot + ephemeral
  overlay, never mutable registry state — so promotion is deterministic.
- **Compiler-Gated Promotion:** only a green candidate lands; red is rolled back with diagnostics; the
  next iteration regenerates. The registry only ever retains validated artifacts.
- **Promotion Law vs Promotion Execution:** change management is the law of promotion; the SDLC layer
  is its execution system. The two must not be conflated.
- **Construction Record is Evidence Only:** S9 records what happened; it moves no design authority
  after implementation.

---

## 4. Gate Order

```
Governance → Projection Fidelity → Projection Semantic Consistency → Construction Closure
          → Structural Invention → Convergence → Compiler → Evidence
             (the pipeline)         (the specification)      (the build)   (protocol)  (the record)
```

Each gate validates exactly one thing and owns nothing else:

| Gate | Validates | Owner |
|------|-----------|-------|
| Projection Fidelity | the **pipeline** — every projection carries the same governed information | `evaluator/projection_fidelity.py` |
| Projection Semantic Consistency | the **semantic graph** — S8 neither adds, loses, nor mutates S7 entities | S8 projection + oracle |
| Construction Closure | the **specification** — the Build Sheet leaves no design decision to the builder | `evaluator/build_sheet_oracle.py` (3 static asserts) |
| Structural Invention | the **build** — the artifact added no design beyond the sheet | `evaluator/invention_oracle.py` |
| Convergence | builder **agreement** — independent builders produced the same artifact | `evaluator/convergence.py` |
| Compiler | protocol **admissibility** — the candidate compiles clean and validates strict | `pgs_compiler` |
| Evidence | the **record** — what was built, measured externally (S9) | Construction Record |

Runtime execution and trace validation are **downstream of this constitution** and out of scope.

---

## 5. The Authority Chain

```
Human → Design (S1–S7) → Execution Specification (S6b) → Construction → Compiler → Machine → Runtime
                                                          ├─ Lowering (derive uniquely)
                                                          └─ Serialization (encode)
```

Design owns *which* solution exists (many valid); the **Execution Specification** (S6b) fixes it —
topology, stores, bindings, entities, orchestration, capabilities (the graph is one view of it).
**Construction** then transforms it deterministically and decides nothing: **Lowering** expands only
uniquely-derivable information, **Serialization** encodes the result. Conformance is measured externally
(invention, convergence, compiler admissibility) and recorded as evidence (S9) independent of the
builder — which is why builders are interchangeable. The full owner hierarchy and the extensible
lowering-rule catalog live in `CONSTRUCTION_MODEL_V0`.

---

## 6. Layer Boundaries

| Concern | Owner | Authority |
|---------|-------|-----------|
| What may be promoted; preconditions; rollback | **Change Management** (this constitution) | law |
| The cross-repo registry mutation mechanics | **SDLC / Promotion layer** | execution |
| Runtime lifecycle (`DEPLOYED → RUNTIME_VALIDATED`) | **`CONSTITUTION_EXECUTION_V0`** (`FB_TOPOLOGY`) | downstream |

The current construction→registry bridge is a **transitional executor** of promotion. Its long-term
home is a dedicated Promotion step in the SDLC pipeline (Authoring → Construction → **Promotion** →
Compiler → Verification). Change management governs promotion; it must not own the cross-repo mutation.

---

## 7. Non-Goals (V0)

This constitution does NOT:
- Author or design protocol artifacts (that is upstream, S0–S7)
- Judge artifacts itself — the compiler is the acceptance gate
- Govern promotion *mechanics* or runtime lifecycle (separate authorities)
- Assert universal builder interchangeability — the thesis is supported by evidence across two model
  families on the evaluated construction tasks, and broadens by experiment (convergence matrix,
  injected-gap abstention), not by decree

V0 intentionally governs the human-reviewed, agent-assisted construction phase with `pgs_change_mgmt`
(the change-management engine) as the reference implementation and the compiler as the sole gate.

---

## End of Constitution
