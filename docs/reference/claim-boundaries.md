# Claim Boundaries

This file is the source of truth for reviewer-facing claims. If a stronger claim becomes
necessary, add the evidence requirement here before using it in the DeepDive package.

## Current Strategic Framing

The current project direction is a simulation-checked primitive collider compiler for Newton
workflows. Primitive collider generation is candidate generation. Acceptance requires named
diagnostics over body state, contact behavior, and, for robots, articulation behavior.

CPD-style primitive decomposition is a related work item, possible candidate generator, and
baseline. It is not the novelty claim by itself.

## Allowed Current Claims

- The repository is a DeepDive-first proposal and bootstrap, not a completed compiler.
- The intended direction is simulation-checked, fallback-aware primitive collider generation for
  Newton workflows.
- Physics engines are treated as executable diagnostic layers under named assumptions, settings,
  versions, and tasks.
- Collision packages are safety-affecting artifacts that require review before use.
- The current executable surface includes config/reporting diagnostics, USD asset intake
  diagnostics, ignored local asset mirror materialization for current smoke assets, Newton source
  and environment-readiness diagnostics, CPD-like geometry smoke paths, contact canaries, and named
  Newton task smokes.
- The current capped bed/Franka cylinder mechanism question is answered for the recorded scope:
  the bed `not_settled` label is a full-compound package effect involving a large flat cylinder and
  COM/inertia body-state sensitivity; the recorded Franka cylinder packages are smaller and pass in
  their capped package context.
- The current opt-in package body-state guard task path can be described as a recorded diagnostic:
  it falls back only the flagged capped bed package while keeping the unflagged capped Franka
  cylinder package in the recorded Newton task smoke.
- A preliminary bed-aligned collision-only contact-throughput microbenchmark can be described as a
  narrow performance hook: native Newton boxes achieved 2.21x generated-contact throughput versus
  same-count convex64 mesh proxies in one pressure scene, with about 5.3% collision-only wall-time
  reduction.
- Current Franka evidence includes capped package/task-smoke evidence, one USD articulation smoke,
  one link-aware package generation and boundary-audit record, and one generated-package robot
  task smoke where all 12 generated package primitives are consumed by Newton. It is not
  whole-robot collider quality, manipulation, or broad articulated-dynamics evidence.
- "Simulation-checked" may be used only when a dated record links a generated package to a named
  Newton task, settings, asset, environment, and report.
- "Diagnostic checker" is preferred over formal-verification language.

## Required Wording Boundaries

- Prefer "simulation-checked" over stronger validation wording unless a verification standard is
  documented.
- Prefer "candidate generator" for primitive or CPD-style outputs before Newton diagnostics.
- Prefer "fallback-aware" rather than "primitive-only".
- Use "Franka articulation smoke" only for the recorded USD import/short-trajectory smoke.
  Use "generated-package Franka task smoke" only for the recorded run where the link-aware
  generated package is attached to Newton bodies and exercised by the short hold/trajectory probe.
  Do not shorten this to whole-robot quality or manipulation wording.
- Use "body-state risk guard" only for the opt-in diagnostic path unless calibrated threshold
  evidence exists.

## Unsupported Claims

Do not claim:

- finished compiler functionality before implementation and records exist;
- broad benchmark superiority, full-simulation speedup, or general primitive speed superiority
  before benchmark-suite evidence exists;
- complete replacement of convex decomposition;
- novelty in automatic primitive collider generation itself;
- full CPD paper reproduction;
- calibrated default selector or guard threshold;
- validated COM/inertia repair;
- broad cylinder stability;
- whole-robot Franka joint-performance or manipulation validity;
- do not claim deployment readiness, real-world transfer, safety certification, or a safety proof.

## Evidence Needed For Stronger Claims

### Default Selector Policy

Before claiming a default selector policy, record:

- calibrated thresholds or selection rules;
- held-out asset/task evidence;
- fallback behavior for failed packages;
- comparison against simple and CPD/CoACD/V-HACD-style baselines;
- failure analysis for accepted and rejected packages.

### Whole-Robot Articulation Evidence

Before claiming whole-robot Franka or broader robot-operation behavior, record:

- source robot asset, license/provenance, and hash;
- link/joint graph preservation;
- proof that primitive merges do not cross link boundaries;
- proof that generated packages are consumed by the robot task runtime;
- whether collision proxies affect dynamic inertial properties;
- Newton joint tree import;
- gravity hold;
- scripted joint trajectory;
- self-collision sanity;
- end-effector pose sanity;
- contact-operation smoke if task behavior is claimed.

### Benchmark Evidence

Before claiming benchmark results, record:

- fixed asset split and source/license metadata;
- Newton source/version, hardware, solver settings, seeds, and configs;
- paired asset-level metrics;
- baseline versions and parameters;
- artifact paths;
- failure and fallback examples;
- statistical treatment when making comparative claims.

### Safety Or Deployment Evidence

Simulator diagnostics can support safety-relevant review, but they do not support deployment,
real-world transfer, or certification claims without a separate verification standard, deployment
protocol, and external evidence record.
