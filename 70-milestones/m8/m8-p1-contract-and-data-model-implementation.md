---
title: "M8-P1 Section 1.1 Contract And Data Model Implementation"
kind: note
created: "2026-08-10"
maturity: seed
tags:
  - milestone-08
  - phase-01
  - contract-and-data-model
  - evidence-manifests
  - profiles
  - runtime-matrices
aliases:
  - "M8-P1.1 Section 1.1 Contract And Data Model Implementation"
---

# M8-P1 Section 1.1 Contract And Data Model Implementation

## Purpose

This section establishes the contract and data model for evidence manifests, profiles, runtime matrices, and traceability. See [Section 1.2 Behavior And Integration](./m8-p1-behavior-and-integration-implementation.md) for the behavior and integration work that follows.

Complete the contract and data model for evidence manifests, profiles, runtime matrices, and traceability. This section turns the phase objective into explicit interfaces, invariants, implementation boundaries, and inspectable evidence.

## Design Decisions

### Subtask 1.1.1.1: Evidence Fields

The evidence manifest MUST capture the following fields for reproducible configuration:

```yaml
EvidenceManifest {
  source_revision: SourceRevision,
  artifact_digest: Digest,
  compiler: CompilerInfo,
  pdk: PDKInfo,
  optimizer: OptimizerInfo?,
  extism_sdk: ExtismSDKInfo,
  extism_kernel: ExtismKernelInfo,
  engine: EngineInfo,
  os: OSInfo,
  architecture: ArchitectureInfo,
  features: FeatureSet,
  host_protocol: HostProtocolInfo?,
  storage: StorageInfo?,
  policy: PolicyInfo?,
  limits: LimitsInfo?,
  seed: SeedInfo?,
  oracle: OracleInfo?
}

SourceRevision = {
  repository: string,
  revision: string,
  timestamp: ISO8601,
  author: string?,
  message: string?
}

Digest = {
  algorithm: HashAlgorithm,
  value: bytes
}

HashAlgorithm = "sha256" | "sha384" | "sha512" | "blake3"

CompilerInfo = {
  name: string,
  version: string,
  flags: string[]?
}

PDKInfo = {
  name: string,
  version: string,
  build_type: "release" | "debug"
}

OptimizerInfo = {
  name: string?,
  version: string?,
  flags: string[]?
}

ExtismSDKInfo = {
  version: string,
  git_revision: string?,
  features: string[]?
}

ExtismKernelInfo = {
  version: string,
  git_revision: string?,
  features: string[]?
}

EngineInfo = {
  name: string,
  version: string,
  git_revision: string?
}

OSInfo = {
  name: string,
  version: string,
  kernel: string?
}

ArchitectureInfo = {
  name: string,
  endianness: "little" | "big",
  word_size: 32 | 64,
  features: string[]?
}

FeatureSet = string[]

HostProtocolInfo = {
  name: string?,
  version: string?
}

StorageInfo = {
  type: "in-memory" | "filesystem" | "database" | "object-store",
  backend: string?
}

PolicyInfo = {
  engine: string?,
  version: string?
}

LimitsInfo = {
  memory_bytes: u64?,
  time_ms: u64?,
  calls: u64?
}

SeedInfo = {
  value: bytes?,
  source: string?
}

OracleInfo = {
  engine: string?,
  version: string?,
  model: string?,
  temperature: f64?,
  max_tokens: u32?
}
```

**Decision**: All fields are required except where marked optional. The manifest MUST be immutable once written. The digest covers the entire manifest excluding the `artifact_digest` field itself (to allow content-addressing).

### Subtask 1.1.1.2: Dispositions

The following dispositions are defined for evidence cells:

```
Disposition = "supported" | "experimental" | "excluded" | "skipped" |
              "expected-failure" | "quarantined" | "divergent" | "conforming"
```

**Disposition Definitions**:

| Disposition | Definition | Acceptance Criteria |
|-------------|------------|---------------------|
| **supported** | The configuration is fully tested and meets all normative requirements. | All tests pass, no divergences, no quarantines. |
| **experimental** | The configuration is under active development and may have known issues. | Tests pass with documented exceptions. |
| **excluded** | The configuration is explicitly excluded from testing (e.g., deprecated, unsupported). | No tests required. |
| **skipped** | The configuration was skipped due to external dependencies or resource constraints. | Must document reason. |
| **expected-failure** | The configuration is known to fail due to known issues. | Failure must be documented with issue reference. |
| **quarantined** | The configuration is failing and under investigation. | Must have investigation ticket. |
| **divergent** | The configuration produces different results across runtimes but all are correct. | Must document divergence and justification. |
| **conforming** | The configuration passes all tests and produces identical results across runtimes. | All tests pass, no divergences. |

**Decision**: Dispositions are organized along two dimensions:

1. **Correctness** - Whether all runtimes produce correct results:
   - **conforming**: All runtimes produce identical correct results (highest correctness)
   - **divergent**: All runtimes produce correct but different results
   - **expected-failure**: Known failures documented with issue references
   - **quarantined**: Failing and under investigation

2. **Test Coverage** - Whether the configuration has been tested:
   - **supported**: Fully tested and meets all normative requirements
   - **experimental**: Under active development, may have known issues
   - **skipped**: Skipped due to external dependencies or resource constraints
   - **excluded**: Explicitly excluded from testing

A configuration with a "divergent" disposition MUST document the divergence and justification. The two dimensions are combined to produce the final disposition (e.g., "conforming" implies both highest correctness and full test coverage).

### Subtask 1.1.1.3: Initial Matrix

The initial runtime matrix covers:

| Engine | Version | OS | Architecture | Features | Status |
|--------|---------|-----|--------------|----------|--------|
| Extism/Wasmtime | 0.6.x | Linux | x86_64, aarch64 | WASI, memory, gas | supported |
| Extism/Wasmtime | 0.6.x | macOS | x86_64, aarch64 | WASI, memory, gas | supported |
| Extism/Wasmtime | 0.6.x | Windows | x86_64 | WASI, memory, gas | experimental |
| Extism/Wazero | 1.7.x | Linux | x86_64, aarch64 | WASI, memory | supported |
| Extism/Wazero | 1.7.x | macOS | x86_64, aarch64 | WASI, memory | supported |
| Extism/Wazero | 1.7.x | Windows | x86_64 | WASI, memory | experimental |

**Decision**: The matrix is defined as a YAML file in `20-notes/m8-p1-runtime-matrix.yaml`. The matrix is updated when new configurations are tested or existing configurations change status. The matrix MUST be committed alongside the evidence manifests it describes.

## Implementation Notes

### File Structure

The following files are created:

```
20-notes/
  m8-p1-contract-and-data-model-implementation.md  (this file)
  m8-p1-runtime-matrix.yaml
```

### Key Invariants

1. **Immutability**: Evidence manifests are immutable once written. To update, a new manifest MUST be created with a new digest.
2. **Content-addressing**: The manifest digest is computed over the manifest content excluding the `artifact_digest` field.
3. **Completeness**: All required fields MUST be populated. Missing fields are reported as validation errors.
4. **Traceability**: Each manifest MUST link to the source revision, artifact, and evidence files.

### Validation Rules

The validator MUST check:

1. All required fields are present and non-null.
2. The `artifact_digest` matches the actual artifact.
3. The manifest digest (computed over the manifest content) is consistent.
4. All referenced artifacts and evidence files exist and are accessible.
5. Dispositions are valid and properly assigned.

## Planned Tests

The following tests are planned for validation once the validator implementation is complete.

### Test 1.1.1: Manifest Validation

**Setup**: Create a valid evidence manifest with all required fields populated.

**Steps**:
1. Create `EvidenceManifest` with all required fields.
2. Compute manifest digest.
3. Write manifest to disk.
4. Run validator on the manifest.

**Expected Result**: Validator reports "conforming" status. Manifest digest matches computed value.

### Test 1.1.2: Missing Required Fields

**Setup**: Create an evidence manifest with missing required fields.

**Steps**:
1. Create `EvidenceManifest` with missing `compiler` field.
2. Run validator on the manifest.

**Expected Result**: Validator reports "missing-field" error for `compiler`.

### Test 1.1.3: Invalid Disposition

**Setup**: Create an evidence manifest with an invalid disposition.

**Steps**:
1. Create `EvidenceManifest` with disposition "invalid".
2. Run validator on the manifest.

**Expected Result**: Validator reports "invalid-disposition" error.

### Test 1.1.4: Divergent Disposition Without Documentation

**Setup**: Create an evidence manifest with "divergent" disposition but no documentation.

**Steps**:
1. Create `EvidenceManifest` with disposition "divergent" and empty `divergence_documentation` field.
2. Run validator on the manifest.

**Expected Result**: Validator reports "missing-divergence-documentation" error.

## Operational Notes

### Implementation-Defined Choices

1. **Hash Algorithm**: SHA-256 is the default hash algorithm for manifest digests. Other algorithms are supported but must be explicitly specified.
2. **Optional Fields**: Fields marked optional are included in the manifest only when relevant. For example, `optimizer` is only included when an optimizer was used.
3. **Feature Set**: The `features` field is a list of strings. Common features include "wasi", "memory", "gas", "http", "logging". Custom features are allowed but must be documented.

### Deferred Work

1. **Performance**: The validator is not yet optimized for large manifests (>1000 configurations).
2. **Caching**: Manifest digests are not cached. Each validation recomputes the digest.
3. **Parallelism**: Validation is sequential. Parallel validation is not yet supported.

### Earlier Milestone Assumptions

No earlier milestone assumptions are invalidated by this phase. The evidence manifests are orthogonal to the runtime contracts defined in earlier milestones.

## Checklist

- [x] 1.1.1.1 Subtask - Specify evidence fields for source revision, artifact digest, compiler, PDK, optimizer, Extism SDK/kernel, engine, OS, architecture, features, host protocol, storage, policy, limits, seed, and oracle.
- [x] 1.1.1.2 Subtask - Define supported, experimental, excluded, skipped, expected-failure, quarantined, divergent, and conforming dispositions.
- [x] 1.1.1.3 Subtask - Define the initial matrix for Extism/Wasmtime and Extism/Wazero across supported host platforms and guest toolchains.
