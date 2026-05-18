# STRUCTURE_CRYPTOGRAPHIC_TRUST_LOCAL_DEV_UNSIGNED_V0

## Machine

```yaml
artifact_code: STRUCTURE_CRYPTOGRAPHIC_TRUST_LOCAL_DEV_UNSIGNED_V0
artifact_kind: STRUCTURE
version: V0
governed_by: fb.cryptographic_trust::CONSTITUTION_CRYPTOGRAPHIC_TRUST_V0
fqdn: fb.cryptographic_trust::STRUCTURE_CRYPTOGRAPHIC_TRUST_LOCAL_DEV_UNSIGNED_V0
status: active

trust_mode: LOCAL_DEV_UNSIGNED
artifact_signing_required: false
payload_signing_required: false
trace_signing_required: false
trust_anchor: none
```

---

## Purpose

Declares that this compiled snapshot operates under LOCAL_DEV_UNSIGNED trust posture.
No cryptographic signing is required for artifacts, payloads, or traces. Trust is
implicit — appropriate for local development and single-operator environments.

This is the correct and complete description of V0 cryptographic trust posture.

## Active Declaration

This structure is the single active trust declaration for V0. The compiler validates
its presence via `INVARIANT_CRYPTOGRAPHIC_TRUST_DECLARED_V0` and materializes:

```yaml
federation_profile:
  cryptographic_trust: LOCAL_DEV_UNSIGNED
```

into every compiled snapshot.
