# 2026-05-22 Bed-Aligned Box Primitive Contact-Throughput Microbenchmark

## Committee Summary

This microbenchmark isolates a concrete engine-facing advantage behind the Newton Primitive
Collision Compiler proposal: when an accepted collider package can stay in Newton-native primitive
form, contact generation can use primitive collision paths instead of generic convex-mesh paths.

In a bed-aligned collision-only pressure scene, the accepted 32-box bed primitive package delivered
2.21x higher generated-contact throughput than a same-count 64-vertex convex-mesh proxy baseline:
19.8k versus 9.0k generated contacts per second. Measured another way, the native primitive path
spent about 50.4 microseconds per generated contact, while the convex-mesh proxy path spent about
111.3 microseconds per generated contact.

This is a narrow but high-signal result. It is not a full simulation speedup claim. The end-to-end
collision-only wall time improved by about 5.3% in this CPU run because broadphase, contact sorting,
and fixed pipeline overhead remain in the measurement. The evidence supports a focused claim:
primitive-aware acceptance can expose an engine-level throughput advantage that is invisible if all
candidate colliders are collapsed into generic convex meshes.

## Scene

The scene reuses the current bed primitive package shape count and layout:

- asset package: recorded bed native primitive package, 32 accepted box primitives;
- primitive candidate: Newton-native `BOX` shapes;
- baseline: 32 generic convex-mesh proxies, approximately 64 vertices each, using the same
  oriented-box scales as the primitive package;
- probe load: 128 sphere probes placed near bed-aligned contact positions;
- runtime path: Newton collision pipeline only, repeated `pipeline.collide()` calls;
- device: CPU;
- repeats: 5 measured repeats after warmup;
- measured loop: 700 collision calls per repeat;
- reported statistic: median over repeats.

The baseline is intentionally a convex-mesh proxy stress baseline, not a collision-equivalent
quality reference. Its purpose is to test the cost difference between Newton-native primitive
collision paths and generic convex-mesh collision paths under a bed-aligned contact load.

## Result

| Metric | Native 32-box primitives | 32 convex64 mesh proxies | Primitive result |
|---|---:|---:|---:|
| Median collision-only time, 700 calls | 3.2483 s | 3.4293 s | 5.3% lower wall time |
| Median time per collide call | 4.640 ms | 4.899 ms | 5.3% lower wall time |
| Generated contacts per call | 92 | 44 | 2.09x more contacts generated |
| Contacted probes per call | 80 | 36 | 2.22x more probes contacted |
| Generated contacts per second | 19.8k | 9.0k | 2.21x higher throughput |
| Microseconds per generated contact | 50.4 us | 111.3 us | 2.21x lower contact cost |

## Interpretation

The result should be presented as a contact-throughput microbenchmark:

> In an early bed-aligned collision-only pressure test, Newton-native box primitives achieved
> 2.21x higher generated-contact throughput than same-count 64-vertex convex-mesh proxies,
> reaching 19.8k versus 9.0k generated contacts per second.

Why this matters for the DeepDive story:

- It turns "primitive colliders are simpler" into a measurable Newton runtime effect.
- It supports the compiler/checker framing: accepted primitive packages should remain primitives
  when the simulator can exploit primitive-specific collision paths.
- It gives the committee a first positive performance hook while the broader Phase 0 benchmark
  suite is still being built.
- It complements the cylinder/body-state evidence: the same checker must reject risky primitive
  packages and preserve high-throughput primitive packages when they pass diagnostics.

## Claim Boundary

Supported:

- one bed-aligned, CPU, collision-only generated-contact throughput result;
- native Newton boxes versus same-count convex64 mesh proxies in one pressure scene;
- a 2.21x generated-contact throughput ratio for this scene;
- a 5.3% collision-only wall-time reduction for this scene.

Not supported:

- full simulation step-time speedup;
- robot operation speedup;
- broad benchmark-suite superiority;
- collision-quality improvement;
- complete replacement of convex decomposition;
- safety, deployment, or real-world transfer conclusions.

## Environment

- date: 2026-05-22;
- repository: `physics-primitive-agent`;
- Newton source checkout: `/cpfs/user/zhuzihou/dev/newton`;
- Newton source commit: `96713fa965463b69c229a4d30582c733ff3526bb`;
- Python: 3.10.20 in `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`;
- Warp: `warp-lang==1.13.0`;
- NumPy: `numpy==2.2.6`;
- CPU: Intel Xeon Gold 6462C, 2 sockets, 32 cores per socket, 128 logical CPUs reported by
  `lscpu`;
- OS kernel: Linux 5.10.134-17.3.al8.x86_64.

## Follow-Up Needed

Before converting this into a broad benchmark claim, package the benchmark as a reproducible config
or CLI command, add more assets and baselines, and report paired full-simulation metrics alongside
collision-only throughput.
