---
title: "GitHub Artifact Attestations"
kind: source
created: "2026-08-10"
authors:
  - "GitHub"
published: null
citation_key: "github2026artifactattestations"
container: "actions/attest Documentation"
edition: "actions/attest v4"
isbn: null
doi: null
url: "https://github.com/actions/attest"
accessed: "2026-08-10"
tags:
  - deployment
  - security
aliases:
  - "actions attest"
---

# GitHub Artifact Attestations

## Reference

GitHub. *actions/attest: Action for generating attestations for workflow
artifacts*. Version 4 documentation.
[Source and documentation](https://github.com/actions/attest), accessed
10 August 2026.

## Contribution

The action generates signed attestations for files and OCI images from GitHub
Actions, including default SLSA build provenance and optional SBOM or custom
predicates.

## Method

This note inspected the current action inputs, permissions, outputs, container
example, attestation format, and registry publication behavior.

## Findings

For an OCI image, the action accepts a fully qualified `subject-name` without a
tag and the `sha256:` digest returned by the image build. With
`push-to-registry: true`, it publishes the attestation for that digest. Default
mode creates SLSA build provenance, and generated attestations are stored as
Sigstore bundles.

The workflow needs read access to repository contents plus write permissions
for the OIDC token and attestations; registry publication also needs the
appropriate package permission and login. The action can attest a file path,
an explicit digest, a checksum file, an SBOM, or a custom predicate, subject to
its documented mutual-exclusion and size rules.

## Relevance

Agent WASM can bind the multi-architecture product digest to its Git revision
and GitHub workflow identity after the image build has passed the target Port
and release smoke tests. That is stronger release evidence than publishing an
unbound checksum alone.

## Limits

An attestation establishes a signed statement about a subject; it does not
prove that the build was correct, dependencies were benign, targets were
tested, or consumers enforced the statement. Workflow actions and builder
images must themselves be pinned and reviewed, and deployment policy must
verify the expected repository, workflow, signer, and digest.

## Derived work

- [Elixir/OTP Port packaging and release pipeline](../20-notes/elixir-otp-port-finished-product-packaging-and-release-pipeline.md)
