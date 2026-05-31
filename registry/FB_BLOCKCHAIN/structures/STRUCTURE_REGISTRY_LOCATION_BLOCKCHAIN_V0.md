# STRUCTURE_REGISTRY_LOCATION_BLOCKCHAIN_V0

**Artifact Type**: STRUCTURE
**Version**: V0
**Status**: CANONICAL
**Governed By**: fb.constitution::CONSTITUTION_STRUCTURE_V0

---

## Purpose

Defines registry module location and discovery pattern for the BLOCKCHAIN layer. Establishes hierarchical subdomain structure (identity, transaction, wallet) for blockchain domain artifacts.

---

## Machine

```yaml
structure_code: STRUCTURE_REGISTRY_LOCATION_BLOCKCHAIN_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  layer_code: BLOCKCHAIN
  registry_module: pgs_blockchain.registry
  module_path_pattern: "{registry_module}.{subdomain}"

  description: >
    Blockchain domain artifacts with hierarchical subdomain structure:
    identity, transaction, wallet, consensus_pos.

  subdomains:
    - identity
    - transaction
    - wallet
    - consensus_pos

invariants:
  - no_cross_subdomain_imports: true
  - subdomain_name_required: true

output_configuration:
  artifacts_path:
    layer: BLOCKCHAIN
    subpath: compiled/artifacts

  conformance_path:
    layer: BLOCKCHAIN
    subpath: compiled/conformance
```

---

## Subdomain Structure

### Identity Subdomain
- **FQDN Pattern**: `blockchain.identity::ARTIFACT_CODE`
- **Registry Module**: `pgs_blockchain.registry.identity`
- **Responsibilities**: Actor verification, identity management

### Transaction Subdomain
- **FQDN Pattern**: `blockchain.transaction::ARTIFACT_CODE`
- **Registry Module**: `pgs_blockchain.registry.transaction`
- **Responsibilities**: Transaction submission, validation, recording

### Wallet Subdomain
- **FQDN Pattern**: `blockchain.wallet::ARTIFACT_CODE`
- **Registry Module**: `pgs_blockchain.registry.wallet`
- **Responsibilities**: Wallet creation, key management

### Consensus PoS Subdomain
- **FQDN Pattern**: `blockchain.consensus_pos::ARTIFACT_CODE`
- **Registry Module**: `pgs_blockchain.registry.consensus_pos`
- **Responsibilities**: Proof-of-Stake validator registration, lifecycle management

---

## Version History

- **V0**: Initial blockchain layer registry location definition (2026-04-23)
