# STRUCTURE_SECURITY_DOMAIN_UNCLASSIFIED_LOCAL_V0

## Machine

```yaml
artifact_code: STRUCTURE_SECURITY_DOMAIN_UNCLASSIFIED_LOCAL_V0
artifact_kind: STRUCTURE
version: V0
governed_by: fb.security_domain::CONSTITUTION_SECURITY_DOMAIN_V0
fqdn: fb.security_domain::STRUCTURE_SECURITY_DOMAIN_UNCLASSIFIED_LOCAL_V0
status: active

security_domain: UNCLASSIFIED_LOCAL
classification_level: UNCLASSIFIED
network_boundary: LOCAL
cross_domain_transfer_allowed: false

snapshot_scope:
  visibility: INTERNAL
```

---

## Purpose

Declares that this compiled snapshot operates in the UNCLASSIFIED_LOCAL security domain.
All data is unclassified. Execution is confined to the local network boundary.
No cross-domain data transfer is authorized.

This is the correct and complete description of V0 security domain posture.

## Active Declaration

This structure is the single active security domain declaration for V0. The compiler validates
its presence via `INVARIANT_SECURITY_DOMAIN_DECLARED_V0` and materializes:

```yaml
federation_profile:
  security_domain: UNCLASSIFIED_LOCAL
```

into every compiled snapshot. The `snapshot_scope.visibility: INTERNAL` field is
exclusively owned by this boundary — no other FB may declare visibility.
