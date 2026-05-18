# STRUCTURE_REGISTRY_LOCATION_AI_GOVERNANCE_V0

**Artifact Type**: STRUCTURE
**Version**: V0
**Status**: CANONICAL
**Governed By**: fb.constitution::CONSTITUTION_STRUCTURE_V0

---

## Purpose

Defines registry module location and discovery pattern for the AI_GOVERNANCE layer. Establishes flat structure combining ai_licensing and agent_governance domains.

---

## Machine

```yaml
structure_code: STRUCTURE_REGISTRY_LOCATION_AI_GOVERNANCE_V0
version: V0
governed_by: fb.constitution::CONSTITUTION_STRUCTURE_V0

core:
  layer_code: AI_GOVERNANCE
  registry_module: pgs_ai_governance
  module_path_pattern: "{registry_module}.{domain}.registry"

  description: >
    AI Governance domain artifacts (subdomain structure).
    Combines ai_licensing and agent_governance.

  domains:
    - ai_licensing
    - agent_governance

invariants:
  - no_cross_domain_imports: true

output_configuration:
  artifacts_path:
    layer: AI_GOVERNANCE
    subpath: compiled/artifacts

  conformance_path:
    layer: AI_GOVERNANCE
    subpath: compiled/conformance
```

---

## Domain Structure

### AI Licensing Subdomain
- **FQDN Pattern**: `ai_governance::ARTIFACT_CODE`
- **Registry Module**: `pgs_ai_governance.ai_licensing.registry`
- **Responsibilities**: AI licensing and provisioning workflows

### Agent Governance Subdomain
- **FQDN Pattern**: `ai_governance::ARTIFACT_CODE`
- **Registry Module**: `pgs_ai_governance.agent_governance.registry`
- **Responsibilities**: Agent action governance workflows

### Combined Layer
This layer combines two previously separate domains under a single FQDN namespace:
- **ai_licensing**: AI licensing and provisioning workflows
- **agent_governance**: Agent action governance workflows

Both use the same `ai_governance::` FQDN prefix despite being in separate subdirectories.

---

## Version History

- **V0**: Initial AI governance layer registry location definition (2026-04-23)
