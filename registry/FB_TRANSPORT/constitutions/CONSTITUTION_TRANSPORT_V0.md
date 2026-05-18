# CONSTITUTION_TRANSPORT_V0

## Machine

```yaml
constitution_code: CONSTITUTION_TRANSPORT_V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0
version: 0

core:
  summary: Constitution governing Transport Ingress (TI) and Transport Egress (TE) artifacts
  description: |
    Defines the structure and semantics for Transport artifacts, which declare
    the protocol membrane between external clients and internal workflows.
    Covers ingress admission contracts, egress projection contracts, HTTP mapping,
    and gateway invocation boundaries.
  artifact_kind: TI_TE

required_fields:
  - artifact_code
  - version
  - governed_by
  - core

field_constraints:
  artifact_code:
    pattern: ^(TI|TE)_[A-Z0-9_]+_V[0-9]+$
    description: Transport artifact identifier (TI_ or TE_ prefix)
  core:
    required_subfields:
      - summary
      - description
```

## Purpose

This constitution governs Transport Ingress (TI) and Transport Egress (TE) artifacts,
which declare the protocol membrane between external clients and internal workflows.

Transport artifacts define:
- Ingress admission contracts (route, method, schema validation, canonical envelope)
- Egress projection contracts (response schema, rendering envelope, serialization)
- HTTP status mapping rules
- Gateway invocation boundaries

This constitution is domain-independent and applies uniformly across all transport protocols.

## 0. Machine Contract

The following sections are normative and machine-enforced:

Section 3 — Artifact Identity & Immutability

Section 4 — Structural Constraints

Section 6 — Execution Boundaries

Section 8 — Membrane Semantics

Section 9 — Observability & Replay Policy

Section 10 — Validation & Enforcement

Only machine-parsable content is authoritative.
Prose, commentary, and examples are non-normative and MUST NOT be used for execution, validation, or inference.

## 1. Scope & Authority

### 1.1 What This Constitution Governs

TI_ artifact identity and structure

TE_ artifact identity and structure

Transport-to-workflow binding boundaries

Admission schema declaration

Egress projection schema declaration

Route registration semantics

### 1.2 What This Constitution Does NOT Govern

Workflow logic

Execution ordering

Side effects

Business rules

Blockchain state

Event observation records (governed by CONSTITUTION_EVENT_V0)

## 2. Canonical Definitions

### 2.1 Governance Terminology

Transport Ingress (TI)
A declarative admission contract for an external entry point into the protocol.
Declares: accepted format, normalized payload schema, explicit target mapping, envelope rules.

Transport Egress (TE)
A declarative projection contract for outbound response rendering.
Declares: response schema, rendering envelope, serialization contract, deterministic error projection.

Admission Schema
A structural validation contract for inbound requests.

Canonical Admission Envelope
The transport-agnostic payload shape produced by TI normalization.
This is the ONLY thing the runtime sees after transport admission.

### 2.2 Vocabulary Authority

TI identifiers MUST use prefix TI_ and format TI_<NAME>_V<MAJOR>

TE identifiers MUST use prefix TE_ and format TE_<NAME>_V<MAJOR>

TI artifacts use artifact_kind: intent

TE artifacts use artifact_kind: transport_egress

EV_ (event) artifacts are NOT transport artifacts. They are governed by CONSTITUTION_EVENT_V0.

## 3. Artifact Identity & Immutability

### 3.1 Naming Rules

TI identifiers MUST be versioned and immutable

TE identifiers MUST be versioned and immutable

### 3.2 Version Semantics

MAJOR: Breaking change to schema or route

MINOR: Backward-compatible additions

PATCH: Documentation only

## 4. Structural Constraints

### 4.1 TI Permitted Contents

A TI artifact MUST declare:

Route specification (method, path, content_type)

Admission schema (field-level validation rules)

Target workflow binding

Outcomes (ACK/NACK)

### 4.2 TI Forbidden Structures

TI artifacts MUST NOT contain:

Execution steps

Capability references

Side effects

Conditional logic

### 4.3 TE Permitted Contents

A TE artifact MUST declare:

Response schema (field-level specification)

Rendering envelope

Serialization contract

Deterministic error projection rules

### 4.4 TE Forbidden Contents

TE artifacts MUST NOT contain:

Execution instructions

Conditional routing logic

References to future actions

Side-effect declarations

Execution state mutation

## 5. Behavioral Guarantees (Advisory)

TI artifacts are inert until bound by a governed Workflow

TE artifacts do not cause behavior — they project execution results

Transport is the protocol membrane — it MUST NOT interpret business semantics

## 6. Execution Boundaries

### 6.1 TI Non-Executability

TI artifacts MUST NOT be directly executable

Engines MUST route TI nodes to admission validation only

### 6.2 Binding Requirement

TI artifacts MAY ONLY be consumed by governed Workflows

TI artifacts bind to workflows — not to CCs or CSs directly

### 6.3 Admission Ownership

Admission validation MUST be performed by governed Capability Contracts (CC)

Server implementations MUST NOT interpret admission schemas directly

### 6.4 Ownership Transfer

Transport owns the canonical admission envelope until admission completes.

After admission:
- Execution owns the envelope immutably
- Transport may no longer mutate execution inputs
- Runtime may not enrich or reinterpret transport metadata

## 7. Composition Rules

TI artifacts MUST NOT compose other artifacts

TE artifacts MUST NOT compose other artifacts

## 8. Membrane Semantics

### 8.1 Transport Exit Reasons

HTTP_xxx exit reasons are transport-domain only

HTTP_xxx reasons MUST NOT be added to VOCAB_EXECUTION_STATES_V0

### 8.2 CS Ownership Boundary

CS artifacts invoked by transport workflows are infrastructure-owned

Transport only binds to infrastructure CS via runtime bindings

Transport MUST NOT own execution mechanisms

### 8.3 Weight Constraint

Transport is a membrane — it MUST remain thinner than domain modules

## 9. Observability & Replay Policy

TI receipt MUST be traceable

TE emission MUST generate trace records

Transport trace records MUST be replayable

Observation records (request received, response sent) are EV_ artifacts — not TE_.

## 10. Validation & Enforcement

### 10.1 Static Validation

Schema validation

Identity validation

Route uniqueness validation

### 10.2 Runtime Guards

Reject undeclared routes

Reject malformed admission schemas

## 11. Governance Authority

This constitution is federal and authoritative.

All TI_ and TE_ artifacts MUST conform to this constitution without modification.

## 12. Versioning

This constitution is versioned and immutable.

Any change requires:

A new version

Explicit migration rationale

Backward-compatibility assessment

End of CONSTITUTION_TRANSPORT_V0
