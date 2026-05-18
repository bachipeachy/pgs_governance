# CONSTITUTION_CRYPTOGRAPHIC_TRUST_V0

## Machine

```yaml
constitution_code: CONSTITUTION_CRYPTOGRAPHIC_TRUST_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.constitution::CONSTITUTION_GOVERNANCE_V0
fqdn: fb.cryptographic_trust::CONSTITUTION_CRYPTOGRAPHIC_TRUST_V0

core:
  summary: Governs snapshot signing, payload sealing, runtime attestation, encrypted transport, and trust admissibility
  description: |
    Declares the cryptographic trust regime active for a compiled snapshot.
    Governs whether snapshots must be signed, payloads sealed, runtimes attested,
    and transport encrypted. Trust mode is a compile-time declaration — runtimes
    execute under the declared trust posture rather than negotiating it.

    In V0, the trust mode is LOCAL_DEV_UNSIGNED: no cryptographic verification
    is required. This seeds the governance axis for future signed, sealed, and
    attested execution without any protocol redesign.
  scope: system
  enforcement_model: compiler_enforced

rules:
  - rule_id: TRUST_MODE_MUST_BE_DECLARED
    applies_to: compiled_snapshot
    constraint: >
      Every compiled snapshot MUST declare exactly one active trust contract.
      A snapshot with no trust declaration is a compiler validation failure.
    enforced_by: compiler_validation

  - rule_id: TRUST_MODES_ARE_ADDITIVE
    applies_to: compiled_snapshot
    constraint: >
      Trust modes are cumulative. SIGNED_SNAPSHOT requires signing but not
      payload encryption. SEALED_PAYLOAD requires both signing and payload
      encryption. ATTESTED_RUNTIME additionally requires runtime attestation.
      Each mode is a superset of the previous.
    enforced_by: process_enforced

  - rule_id: UNSIGNED_SNAPSHOTS_LOCAL_ONLY
    applies_to: compiled_snapshot
    constraint: >
      Snapshots compiled with LOCAL_DEV_UNSIGNED trust mode MUST NOT be deployed
      to non-local execution substrates. This is enforced by governance process
      at V0; future compiler validation will assert this mechanically.
    enforced_by: process_enforced

  - rule_id: TRUST_IS_NOT_TRANSPORT
    applies_to: federation_boundary
    constraint: >
      FB_CRYPTOGRAPHIC_TRUST governs cryptographic trust posture only.
      It MUST NOT govern transport protocols, network routing, or TLS configuration.
      Transport security is an infrastructure concern; trust posture is a
      governance concern.
    enforced_by: process_enforced

  - rule_id: RUNTIME_READS_TRUST_PASSIVELY
    applies_to: runtime
    constraint: >
      Runtime MAY read the active trust contract for trace metadata emission.
      Runtime MUST NOT branch on trust mode or perform signature verification,
      payload decryption, or attestation checks. In V0, all such checks are absent.
      Future trust enforcement is a runtime evolution concern (V3+).
    enforced_by: process_enforced
```

---

## Purpose

This constitution governs the cryptographic trust posture under which PGS execution is
authorized. It answers: *what cryptographic guarantees are required for this snapshot to
be considered trustworthy and legally executable?*

Trust posture is a governance declaration, not a runtime configuration. The compiler
validates the declared trust mode; runtimes execute under it passively. This ensures
that moving from unsigned local development to signed, attested, or encrypted deployment
is a governance change, not a code change.

## §1. V0 Trust Mode

The only authorized trust mode in V0 is `LOCAL_DEV_UNSIGNED`.

This means:
- Snapshots are not required to carry cryptographic signatures
- Payloads are not encrypted or sealed
- Runtime processes are not attested
- Transport channels are not required to be encrypted

This is the correct posture for local development and single-node execution.
It is explicitly declared — not assumed — which is the important distinction.

## §2. What "Trust" Means in PGS

Cryptographic trust governs confidence in the integrity and provenance of execution
artifacts: the snapshot, the payload, the runtime process, and the transport channel.
It does not govern identity trust (FB_IDENTITY) or authority delegation (FB_AUTHORITY).

| Concern | Governed By |
|---------|-------------|
| Snapshot integrity | FB_CRYPTOGRAPHIC_TRUST |
| Payload confidentiality | FB_CRYPTOGRAPHIC_TRUST |
| Runtime process attestation | FB_CRYPTOGRAPHIC_TRUST |
| Transport channel security | FB_CRYPTOGRAPHIC_TRUST |
| Identity legality | FB_IDENTITY |
| Authority delegation | FB_AUTHORITY |

## §3. Compiler Behavior

The compiler MUST:
- Discover the active trust contract in this boundary
- Validate that exactly one contract is active
- Materialize trust mode into the snapshot federation profile under:

```yaml
federation_profile:
  cryptographic_trust: LOCAL_DEV_UNSIGNED
```

## §4. Runtime Behavior

The runtime MUST:
- Record `federation_profile.cryptographic_trust` in trace metadata
- NOT perform signature verification, decryption, or attestation in V0
- NOT branch on trust mode values

## §5. Future Expansion Path

```
LOCAL_DEV_UNSIGNED
  → SIGNED_SNAPSHOT        (snapshot carries verifiable signature)
  → SEALED_PAYLOAD         (payload encrypted; signing required)
  → ATTESTED_RUNTIME       (runtime process attested; sealing required)
  → ENCRYPTED_TUNNEL       (transport encrypted; attestation required)
```

Each step requires a new trust contract. Runtime enforcement capability arrives
with Runtime V3+.

## §6. Versioning

Changes to trust semantics require a new constitution version and migration rationale.
