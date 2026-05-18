# CONSTITUTION_AUTHORITY_GOVERNANCE_V0

## One-Line Doctrine

Authority governance determines whether execution may exist; execution never determines its own authority.

## Foundational Doctrine

> Authority governance governs **execution eligibility**, not execution behavior.

This distinction is critical. Authority answers: *may this actor invoke this workflow?* It does not govern how the workflow behaves, what path it takes, or what it produces. Execution behavior is governed by execution semantics. Authority governs the threshold — the gate before execution begins.

## Machine

```yaml
fqdn: fb.authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0
constitution_code: CONSTITUTION_AUTHORITY_GOVERNANCE_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0

core:
  description: Constitution governing execution authority as a sovereign architectural concern orthogonal to execution, transport, and workflow semantics
  scope: cross_artifact
  governs:
    - WF
    - CC
    - CT
    - CS
    - AC
  enforcement_model: compiler_enforced

rules:
  - rule_id: AUTHORITY_REQUIRED_FOR_EXECUTION
    applies_to:
      - WF
    constraint: every workflow invocation MUST be preceded by a resolved authority boundary evaluation; execution without established authority is a constitutional violation
    enforced_by: ASSERT_AUTHORITY_REQUIRED_FOR_EXECUTION_V0

  - rule_id: NO_WORKFLOW_AUTHORIZATION_LOGIC
    applies_to:
      - WF
      - CC
      - CT
      - CS
    constraint: no execution artifact may contain role checks, permission branching, authorization assertions, or embedded admissibility logic
    enforced_by: ASSERT_NO_WORKFLOW_AUTHORIZATION_LOGIC_V0

  - rule_id: AUTHORITY_STATE_WELL_FORMED
    applies_to:
      - WF
    constraint: authority state envelope MUST be structurally well-formed per SCHEMA_AUTHENTICATED_AUTHORITY_STATE_V0 before execution traversal begins; partial, absent, or malformed authority state is a constitutional violation
    enforced_by: ASSERT_AUTHORITY_STATE_WELL_FORMED_V0

  - rule_id: NO_AMBIENT_AUTHORITY
    applies_to:
      - WF
      - CC
      - CT
      - CS
    constraint: all authority references must be explicit and fully declared; runtime authority discovery, role inference, and ambient authority are forbidden
    enforced_by: ASSERT_NO_AMBIENT_AUTHORITY_V0

  - rule_id: ACTOR_AUTHORITY_SEPARATION
    applies_to:
      - AC
    constraint: actor artifacts must not declare authority semantics; identity and authority are orthogonal governance surfaces; permissions, workflow eligibility, and admissibility rules are forbidden inside AC_ artifacts
    enforced_by: ASSERT_ACTOR_AUTHORITY_SEPARATION_V0

  - rule_id: IDENTITY_AUTHORITY_ORTHOGONALITY
    applies_to:
      - AC
    constraint: identity governance and authority governance are orthogonal surfaces; neither may import semantics from the other; actor type must not function as an implicit authority grant
    enforced_by: ASSERT_ACTOR_AUTHORITY_SEPARATION_V0
```

---

## Scope Boundary

This constitution governs:
- authority as a sovereign architectural concern
- admissibility evaluation before execution entry
- the Authority Boundary sitting before IN (intent)
- prohibition of authorization semantics inside execution artifacts
- explicit authority declaration requirements

This constitution does NOT govern:
- cryptographic mechanisms (PKI, TLS, OAuth, JWT)
- actor identity declaration (governed by CONSTITUTION_ACTOR_IDENTITY_V0)
- workflow execution semantics
- transport admission semantics
- runtime execution topology

---

## 1. Purpose

This constitution establishes authority governance as a sovereign architectural concern orthogonal to execution, transport, and workflow semantics.

Authority governance answers: *may this actor invoke this workflow at all?* This question is answered **before** the Intent (IN) is reached — before DAG traversal begins. Execution assumes admissibility has already succeeded.

Authority is not middleware. Authority is not a runtime policy engine. Authority is not embedded ACL logic. It is a governed admissibility plane that operates before execution and never modifies it.

---

## 2. Core Principles

- **Execution Eligibility, Not Execution Behavior:** Authority governs whether execution may begin — not how execution proceeds. After admissibility succeeds, authority is settled. Execution topology is fixed. Authority does not reach into execution.
- **Pre-Execution Evaluation:** Authority is evaluated before the Intent gate. Execution begins only after authority is resolved. The runtime consumes resolved authority state; it never evaluates authority.
- **Execution Never Self-Authorizes:** Execution topology may not vary based on authority state. Workflows, CCs, CTs, and CSs may not authenticate actors, authorize themselves, or branch on authority semantics.
- **Authority Immutability:** Authority state becomes immutable once execution begins. No elevation, negotiation, reinterpretation, or mutation of authority state is permitted during execution traversal.
- **No Ambient Authority:** All authority is explicit. No implicit admin state. No role inference. No runtime authority discovery. If authority is not declared, it does not exist.
- **Two Authority Planes:** Execution authority (what an actor may invoke) and observation authority (what an actor may observe) are distinct. Holding execution authority does not imply observation authority. Both must be explicitly granted.
- **Orthogonality:** Authority governance, execution semantics, transport semantics, and trace semantics are orthogonal planes. They must not collapse into each other.
- **Transport Neutrality:** Authority semantics function identically across CLI, HTTP, MQ, agents, and future transports without workflow changes.
- **Identity-Authority Separation:** Actor identity governance (what an actor is) and authority governance (what an actor may do) are orthogonal. Neither may import semantics from the other.

---

## 3. Authority Boundary Position

```
TI
↓
Authority Boundary   ← governed by this constitution
↓
AC (Actor)
↓
IN                   ← admission gate (governed by CONSTITUTION_ADMISSION_V0)
↓
WF → CC → CT/CS → EV → TE
```

The Authority Boundary sits **before IN**. Admission governs preconditions within a workflow. Authority governance governs whether the actor may reach the workflow at all.

---

## 4. What Authority Governance Governs

| Concern             | Authority Position                        |
|---------------------|-------------------------------------------|
| Identification      | actor + canonical admission               |
| Authentication      | authority admissibility                   |
| Authorization       | execution authority + observation authority |
| Confidentiality     | TE + observation authority governance     |
| Non-Repudiation     | EV + authority trace binding + provenance |
| Integrity           | snapshots + assertions + invariants       |

### Two Distinct Authority Planes

**Execution Authority** — governs what an actor may invoke:
- authorized_workflows: explicit list of workflow FQDNs the actor may execute
- Evaluated at the Authority Boundary before IN
- Enforced by the authority registry

**Observation Authority** — governs what an actor may observe:
- visibility_scope: what output projections and TE results the actor may receive
- trace_scope: what execution trace data the actor may access
- Evaluated at TE — not at the execution boundary
- Distinct from execution authority; one may be granted without the other

**Authority Provenance** — the accountability chain:
- Records the source, timestamp, and chain of authority for every admissibility decision
- Required in every execution trace as `authority_provenance`
- Foundation of non-repudiation semantics across execution and post-execution

---

## 5. Forbidden Patterns

The following are constitutional violations:

- `if actor == "admin":` inside any WF, CC, CT, or CS
- Runtime role inference or permission lookup inside execution
- Dynamic policy evaluation or policy scripting at runtime
- Ambient authority (implicit admin state, default permissions)
- Authority discovery at runtime (unresolved authority references)
- Execution topology variation based on authority state after admissibility succeeds
- Transport owning authority semantics

---

## 6. V0 Scope

V0 intentionally permits:
- static JSON authority database
- plaintext identity material
- local authority stores
- governance-layer assertions as stubs (enforced fully in Phase 4)

V0 intentionally excludes:
- PKI, TLS, OAuth, JWT
- distributed identity or federated trust
- revocation infrastructure
- remote authority negotiation

Future cryptographic evolution (signatures, hardware keys, federated trust) is compatible with this constitution's architecture without redesign.

---

## 7. Relationship to Actor Identity Governance

`CONSTITUTION_ACTOR_IDENTITY_V0` governs what an actor **is** — its declared identity, type, and structural attributes.

`CONSTITUTION_AUTHORITY_GOVERNANCE_V0` governs what an actor **may do** — its admissibility for execution, workflow authorization, and observation rights.

These are orthogonal constitutions governing orthogonal concerns. Neither may reference or depend on the governance semantics of the other.

---

## End of Constitution
