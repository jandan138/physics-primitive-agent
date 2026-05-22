# 2026-05-22 Bed-Aligned Box Primitive Contact-Throughput Microbenchmark

## Date

2026-05-22

## Status

Complete for a preliminary single-scene collision-only contact-throughput record. Not complete as a
broad benchmark suite, full simulation speedup result, collision-quality validation, robot-operation
result, or safety evidence.

## Purpose

Record the first positive performance evidence for preserving accepted primitive packages as
Newton-native primitives instead of converting every candidate to generic convex meshes.

The question was narrow: in a bed-aligned pressure scene, does the accepted 32-box bed primitive
package show a measurable engine-level advantage over a same-count convex-mesh proxy baseline?

## Setup

- asset package: recorded bed native primitive package with 32 accepted box primitives;
- primitive path: Newton-native `BOX` shapes;
- baseline path: 32 generic convex-mesh proxies, approximately 64 vertices each, using the same
  oriented-box scales as the primitive package;
- probe load: 128 sphere probes near bed-aligned contact positions;
- runtime path: repeated Newton `pipeline.collide()` calls only;
- measured loop: 700 collision calls per repeat;
- repeats: 5 measured repeats after warmup;
- reported statistic: median over repeats;
- device: CPU.

Environment:

- Newton source commit: `96713fa965463b69c229a4d30582c733ff3526bb`;
- Python: 3.10.20 in `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`;
- Warp: `warp-lang==1.13.0`;
- NumPy: `numpy==2.2.6`;
- CPU: Intel Xeon Gold 6462C, 2 sockets, 32 cores per socket, 128 logical CPUs reported by
  `lscpu`.

## Results

| Metric | Native 32-box primitives | 32 convex64 mesh proxies |
|---|---:|---:|
| Median collision-only time, 700 calls | 3.2482579667 s | 3.4293470718 s |
| Seconds per collide call | 0.0046403685 s | 0.0048990672 s |
| Generated contacts per call | 92 | 44 |
| Contacted probes per call | 80 | 36 |
| Generated contacts per second | 19826.0116 | 8981.3015 |
| Microseconds per generated contact | 50.4388 | 111.3424 |

Derived ratios:

- native generated-contact throughput over convex64 proxy: 2.2075x;
- convex64 microseconds per generated contact over native: 2.2075x;
- native collision-only wall-time reduction versus convex64 proxy: 5.2806%.

## Interpretation

This is a contact-throughput microbenchmark, not a full simulation benchmark. The most useful
committee-facing sentence is:

> In an early bed-aligned collision-only pressure test, Newton-native box primitives achieved
> 2.21x higher generated-contact throughput than same-count 64-vertex convex-mesh proxies,
> reaching 19.8k versus 9.0k generated contacts per second.

This result supports the DeepDive story because it shows that accepted primitive packages are not
only smaller or more inspectable; they can also preserve access to Newton-native primitive collision
paths. That is exactly why the proposed compiler should be both primitive-aware and
simulation-checked: preserve primitive speed when diagnostics pass, and fall back when body-state,
contact, or robot-operation diagnostics fail.

## Claim Impact

Allowed wording:

- "preliminary bed-aligned collision-only contact-throughput evidence";
- "2.21x generated-contact throughput for native boxes versus convex64 mesh proxies in one
  bed-aligned pressure scene";
- "5.3% collision-only wall-time reduction in the same scene";
- "a first performance hook motivating primitive-aware acceptance."

Forbidden wording:

- full simulation speedup;
- full Newton step-time speedup;
- robot manipulation or articulated-dynamics speedup;
- broad benchmark superiority;
- collision-quality improvement;
- replacement of convex decomposition;
- safety, deployment, certification, or real-world transfer conclusions.

## Artifacts

- Reviewer-facing report:
  [reports/2026-05-22-bed-aligned-contact-throughput-microbenchmark.md](../../reports/2026-05-22-bed-aligned-contact-throughput-microbenchmark.md)

No large raw logs or generated run directories are committed. Follow-up work should package this
microbenchmark as a reproducible config or CLI command before using it as part of a broad benchmark
suite.

## Next Action

Promote this from preliminary evidence to benchmark-suite evidence only after adding a reproducible
command/config, more assets, more baselines, paired full-simulation metrics, and statistical
treatment across scenes.
