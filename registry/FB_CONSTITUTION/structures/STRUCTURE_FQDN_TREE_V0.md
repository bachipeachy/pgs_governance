# STRUCTURE_FQDN_TREE_V0

## Header
- Artifact Code: STRUCTURE_FQDN_TREE_V0
- Tier: Sovereign Authority
- Artifact Kind: structure
- Governed By: fb.constitution::CONSTITUTION_GOVERNANCE_V0
- Version: v0
- Status: active
- Supersedes: NONE
- Dependencies: []

---

## 1. Purpose

Declare the authoritative logical package (FQDN) tree for OmniBachi.

This document is the single source of truth for:
- Build ordering
- Registry discovery
- Dependency resolution
- Package authority levels

No implicit filesystem derivation is permitted.

---

## 2. Global Rules

- Only packages declared here participate in build.
- Build order is explicit and deterministic.
- Dependencies must be acyclic and forward-only.
- Physical directory layout is mapped, not inferred.
- Undeclared packages or registries are build errors.
- Runtime bindings, where declared, MUST be domain-scoped and SHALL NOT appear in shared registries.

---

## 3. Package Roles

| Role | Description |
|------|-------------|
| `core` | Protocol infrastructure (pgs_runtime package) |
| `capability_pack` | Reusable capability implementations (atoms, molecules) |
| `domain_pack` | Domain-specific workflows, contracts, intents |

### 3.1 Domain Isolation Invariant

Domain artifacts SHALL NOT appear in platform infrastructure packages.
The platform TLD is reserved for protocol substrate only.

- `core` packages may contain only platform artifacts (governance, schemas, transport constructs, and platform-level workflows/contracts/bindings for infrastructure concerns).
- `capability_pack` packages may contain only reusable CT/CS artifacts.
- `domain_pack` packages may contain domain artifacts (intents, events, actors, workflows, contracts, bindings, and domain-scoped CT/CS).
- Any artifact type discovered outside its role-allowed set is a build violation.

This rule is machine-enforced at build time via `role_artifact_rules` in the Machine block.
Enforcement severity: WARNING during rollout, promoted to ERROR once stable.

---

## 4. Authority Levels

| Authority | Description |
|-----------|-------------|
| `sovereign` | Root authority, defines protocol semantics |
| `delegated` | Authority derived from sovereign, must comply with core |

---

## 5. Build Contract

Builder MUST:
- Load this document first
- Validate schema and dependency order
- Resolve physical paths explicitly
- Iterate packages strictly by build_order
- Load only declared registries
- Respect `artifact_patterns` for file discovery

Builder MUST NOT:
- Scan directories implicitly
- Infer semantics from folder names
- Include undeclared artifacts

---

## 6. Determinism & Trace Binding

- This document is hashed as part of build manifest.
- Trace metadata MUST reference the FQDN tree hash.
- Any change to this file constitutes a governance-visible change.

---

## 7. Versioning

- Changes require a new version (e.g., GOVERNANCE_FQDN_TREE_V1).
- Backward compatibility is not assumed.

---

## Machine

```yaml
structure_code: STRUCTURE_FQDN_TREE_V0
fqdn_tree_code: STRUCTURE_FQDN_TREE_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

# Compatibility shim: structure_tree.py expects fields at root
# Compiler expects core block. Including both for transition.

core:
  summary: Authoritative logical package (FQDN) tree configuration
  description: >
    Defines the logical package structure, roles, and build order for the platform and domains.

  machine:
    id: omnibachi-machine-v0
    role: protocol_executor
    authority: layers
    responsibilities:
      - protocol_loading
      - registry_federation
      - compilation
      - execution
      - conformance
      - observability
      - trace_sealing
    execution_model:
      determinism: strict
      replay: required
      side_effects: capability_guarded
      concurrency: explicit_only
    trace:
      required: true
      format: jsonl
      schema: STRUCTURE_TRACE_SCHEMA_V0
      hash_chain: enabled
      seal_on_complete: true
    security:
      tamper_evidence: required
      registry_snapshot_hash: required
      trace_hash_chain: required
    failure_policy:
      on_violation: fail_build
      on_runtime_violation: abort_execution
    forbidden:
      - implicit_filesystem_discovery
      - dynamic_registry_mutation
      - undeclared_capability_execution

# Fields for structure_tree.py (mandatory)
packages:

  - package: structure
    role: core
    authority: foundational
    build_order: 0
    physical_root: ./pgs_structure
    module_root: structure
    contains:
      - discovery
      - loading
      - resolution
    registries: []
    depends_on: []

  - package: governance
    role: core
    authority: federal
    build_order: 1
    physical_root: ./pgs_governance
    module_root: registry
    contains:
      - registry
      - schemas
      - vocabulary
      - conformance
      - constitution_validator
    registries:
      - path: registry/FB_CONSTITUTION
        artifact_types:
          - registry
          - constitutions
          - structures
        notes: "Constitutional federation boundary — sovereign authority artifacts"
      - path: registry/FB_TOPOLOGY
        artifact_types:
          - constitutions
          - invariants
        notes: "Topology federation boundary"
      - path: registry/FB_TRANSPORT
        artifact_types:
          - constitutions
          - invariants
        notes: "Transport federation boundary"
      - path: registry/FB_AUTHORITY
        artifact_types:
          - constitutions
          - invariants
        notes: "Authority federation boundary"
      - path: registry/FB_VOCABULARY
        artifact_types:
          - constitutions
          - invariants
        notes: "Vocabulary federation boundary"
      - path: registry/FB_CONFORMANCE
        artifact_types:
          - constitutions
          - assertions
          - invariants
        notes: "Conformance federation boundary"
      - path: registry/FB_IDENTITY
        artifact_types:
          - constitutions
          - invariants
        notes: "Identity federation boundary"
    namespace_mappings:
      constitution: registry/FB_CONSTITUTION
      topology: registry/FB_TOPOLOGY
      transport: registry/FB_TRANSPORT
      authority: registry/FB_AUTHORITY
      vocabulary: registry/FB_VOCABULARY
      conformance: registry/FB_CONFORMANCE
      identity: registry/FB_IDENTITY
    depends_on: []

  - package: execution
    role: core
    authority: delegated
    build_order: 2
    physical_root: ./pgs_execution
    module_root: execution
    contains:
      - machine
      - host
    registries: []
    depends_on:
      - governance

  - package: transforms
    role: capability_pack
    authority: delegated
    build_order: 3
    physical_root: ./pgs_transforms
    module_root: transforms
    contains:
      - atoms
      - molecules
    registries:
      - path: registry/registry
        artifact_types:
          - capability_transforms
    depends_on:
      - governance
      - execution

  - package: side_effects
    role: capability_pack
    authority: delegated
    build_order: 4
    physical_root: ./pgs_side_effects
    module_root: side_effects
    contains:
      - persistent
      - volatile
    registries:
      - path: registry/registry
        artifact_types:
          - capability_side_effects
    depends_on:
      - governance
      - execution

  - package: blockchain
    role: domain_pack
    authority: delegated
    build_order: 5
    physical_root: ./pgs_domains/domains/blockchain
    module_root: pgs_domains.domains.blockchain
    contains:
      - registry
      - protocol
      - test_payloads
      - capability_transforms
    registries:
      - path: domains/blockchain/registry/identity
        artifact_types:
          - capability_contracts
          - intents
          - workflows
          - events
          - actors
      - path: domains/blockchain/registry/wallet
        artifact_types:
          - capability_contracts
          - capability_transforms
          - intents
          - workflows
          - events
          - runtime_bindings
      - path: domains/blockchain/registry/transaction
        artifact_types:
          - capability_contracts
          - capability_transforms
          - intents
          - workflows
          - events
    depends_on:
      - governance
      - transforms
      - side_effects

  - package: ai_licensing
    role: domain_pack
    authority: delegated
    build_order: 6
    physical_root: ./pgs_domains/domains/ai_licensing
    module_root: pgs_domains.domains.ai_licensing
    contains:
      - registry
      - protocol
      - test_payloads
      - capability_transforms
    registries:
      - path: domains/ai_licensing/registry
        artifact_types:
          - capability_contracts
          - capability_transforms
          - intents
          - workflows
          - events
          - actors
          - runtime_bindings
    depends_on:
      - governance
      - transforms
      - side_effects

  - package: agent_governance
    role: domain_pack
    authority: delegated
    build_order: 7
    physical_root: ./pgs_domains/domains/agent_governance
    module_root: domains.agent_governance
    contains:
      - registry
      - protocol
      - testbed
    registries:
      - path: domains/agent_governance/registry
        artifact_types:
          - capability_contracts
          - intents
          - workflows
          - events
          - actors
          - runtime_bindings
    depends_on:
      - governance
      - transforms
      - side_effects

  - package: tooling
    role: core
    authority: delegated
    build_order: 8
    physical_root: ./pgs_tooling
    module_root: tooling
    contains:
      - builder
      - artifact_validation
      - protocol_validation
      - trace_examiner
      - visualization
      - experimental
    registries: []
    depends_on:
      - governance
      - execution

  - package: transport
    role: core
    authority: delegated
    build_order: 9
    physical_root: ./pgs_transport
    module_root: transport
    conformance_generation: false
    contains:
      - registry
      - gateway
      - command_line
      - http_rest
    registries:
      - path: registry/registry/http_gateway
        artifact_types:
          - transport_intents
          - transport_egress
          - workflows
          - capability_contracts
          - runtime_bindings
    depends_on:
      - governance
      - execution

role_artifact_rules:
  core:
    - constitutions
    - registry
    - schemas
    - capability_transforms
    - capability_side_effects
    - transport_intents
    - transport_egress
    - workflows
    - capability_contracts
    - runtime_bindings
  capability_pack:
    - capability_transforms
    - capability_side_effects
  domain_pack:
    - capability_contracts
    - capability_transforms
    - capability_side_effects
    - intents
    - workflows
    - events
    - actors
    - runtime_bindings

artifact_patterns:

  constitutions:
    file_pattern: "CONSTITUTION_*.md"
    code_key: constitution_id

  governance:
    file_pattern: "*_V0.md"
    code_key: artifact_code

  schemas:
    file_pattern: "SCHEMA_*.json"
    code_key: "$id"

  capability_transforms:
    file_pattern: "CT_*.md"
    code_key: ct_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  capability_side_effects:
    file_pattern: "CS_*.md"
    code_key: cs_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  capability_contracts:
    file_pattern: "CC_*.md"
    code_key: cc_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  intents:
    file_pattern: "IN_*.md"
    code_key: in_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  workflows:
    file_pattern: "WF_*.md"
    code_key: wf_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  events:
    file_pattern: "EV_*.md"
    code_key: ev_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  actors:
    file_pattern: "AC_*.md"
    code_key: ac_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  runtime_bindings:
    file_pattern: "RB_*.md"
    code_key: rb_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  transport_intents:
    file_pattern: "TI_*.md"
    code_key: ti_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

  transport_egress:
    file_pattern: "TE_*.md"
    code_key: te_code
    exclude_patterns:
      - "CONSTITUTION_*.md"

output_configuration:
  _type: metadata  # This artifact defines metadata, not output paths
```
