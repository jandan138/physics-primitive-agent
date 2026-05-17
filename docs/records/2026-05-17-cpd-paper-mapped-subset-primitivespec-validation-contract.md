# CPD Paper Mapped-Subset PrimitiveSpec Validation Contract

## Date

2026-05-17

## Status

Complete

## Decision

Implement `paper_mapped_subset_primitivespec_validation_contract` as a command-only offline
validation contract after the PrimitiveSpec dry-run contract.

## What Changed

- The CPD paper offline report now records PrimitiveSpec validation requirement rows for six paper
  primitive families.
- The report now records 16 current no-op validation rows for unmapped trapezoidal-prism rows.
- The validation checks the dry-run field list, mapped future shape labels, row counts, source
  traceability, zero current candidates, zero generated PrimitiveSpecs, and false
  runtime/evaluation triggers.
- The validation now also checks exact six-family semantics, non-empty source ids, aligned
  future mapping-candidate labels, and separate blocked-versus-no-op requirement counts.
- The report advances the next gate to
  `paper_mapped_subset_primitivespec_generation_preflight_contract`.

## Boundary

This is not PrimitiveSpec generation, CollisionPackage generation, package readiness, runtime
admissibility, Newton support, real-USD evidence, benchmark evidence, collision-quality evidence,
deployment readiness, or safety certification. Current unmapped rows remain offline/no-op.

## Verification

The implementation is covered by focused CPD paper offline and CLI tests, plus the repository doc
claim validators in this development slice.
