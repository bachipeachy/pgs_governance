# STRUCTURE_IDENTITY_V0

**Artifact Type**: STRUCTURE
**Version**: V0
**Status**: CANONICAL
**Authority**: CONSTITUTIONAL

---

## Purpose

Single source of truth for artifact identity. Defines FQDN composition, normalization rules from short names to fully qualified IDs, and identity uniqueness constraints.

---

## Machine

```yaml
structure_code: STRUCTURE_IDENTITY_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  summary: Consolidated artifact identity and FQDN configuration
  description: >
    Defines the canonical identity system for all protocol artifacts.
    Namespace identity is federation-boundary-scoped under the fb.* scheme.

identity:
  fqdn:
    format: "{namespace}::{artifact_code}"
    
    namespace:
      derivation:
        method: module_path
        rules:
          # Federation boundary namespaces — one canonical namespace per boundary
          # More specific paths must precede less specific paths
          - match: "pgs_governance.registry.FB_CONSTITUTION"
            namespace: "fb.constitution"
          - match: "pgs_governance.registry.FB_TOPOLOGY"
            namespace: "fb.topology"
          - match: "pgs_governance.registry.FB_TRANSPORT"
            namespace: "fb.transport"
          - match: "pgs_governance.registry.FB_AUTHORITY"
            namespace: "fb.authority"
          - match: "pgs_governance.registry.FB_VOCABULARY"
            namespace: "fb.vocabulary"
          - match: "pgs_governance.registry.FB_CONFORMANCE"
            namespace: "fb.conformance"
          - match: "pgs_governance.registry.FB_IDENTITY"
            namespace: "fb.identity"
          - match: "pgs_governance.registry.FB_BLOCKCHAIN"
            namespace: "fb.blockchain"
          - match: "pgs_governance.registry.FB_AI_GOVERNANCE"
            namespace: "fb.ai_governance"
          - match: "pgs_governance.registry.FB_EXECUTION_PLACEMENT"
            namespace: "fb.execution_placement"
          - match: "pgs_governance.registry.FB_EXECUTION_SCHEDULING"
            namespace: "fb.execution_scheduling"
          - match: "pgs_governance.registry.FB_SECURITY_DOMAIN"
            namespace: "fb.security_domain"
          - match: "pgs_governance.registry.FB_CRYPTOGRAPHIC_TRUST"
            namespace: "fb.cryptographic_trust"
          - match: "pgs_governance.registry.FB_CHANGE_MGMT"
            namespace: "fb.change_mgmt"

          # Reusable layers
          - match: "pgs_transforms"
            namespace: "capability_transforms"
          - match: "pgs_side_effects"
            namespace: "capability_side_effects"
          - match: "pgs_capabilities"
            namespace_template: "{module_path}"

          # Domain layers (federated)
          - match: "pgs_blockchain.registry"
            namespace: "blockchain"
          - match: "pgs_ai_governance"
            namespace: "ai_governance"

          # Other platform layers
          - match: "pgs_structure"
            namespace: "structure"
          - match: "pgs_execution"
            namespace: "execution"
          - match: "pgs_compiler"
            namespace: "compiler"
          - match: "pgs_ingress"
            namespace: "ingress_gateway"

    uniqueness:
      scope: global
      constraint: no_duplicate_fqdn

normalization:
  # How to resolve short names (e.g. CT_FOO_V0) to FQDNs
  short_name_resolution:
    allowed: true
    resolution_phase: compile_time
    rules:
      - local_scope_first
      - global_search
    on_ambiguity: FAIL
```
