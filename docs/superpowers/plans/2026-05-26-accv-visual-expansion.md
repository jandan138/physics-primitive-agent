# ACCV Visual Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the ACCV submission candidate into a 13--14 page evidence-rich main paper using deterministic Phase 0 visualizations, collision-probe scene renders, outcome matrices, mechanism diagnostics, and Franka link-aware task visuals.

**Architecture:** Add one small reusable visualization module under `src/primitive_collision_compiler/paper/` plus one CLI wrapper under `scripts/paper/`. The module reads the recorded Phase 0 JSON report and ignored repo-local USD mirrors through explicit paths, emits compact publication PDFs under `paper/shared/figures/generated/`, and writes a small generated manifest. LaTeX then includes these figures and expands method/experiment/limitation prose without changing claim strength.

**Tech Stack:** Python 3.10, `json`, `pathlib`, `numpy`, `matplotlib`, existing `load_first_mesh()` USD loader, PyYAML for manifest validation, LaTeX/LNCS ACCV build.

---

### Task 1: Visualization Module And Tests

**Files:**
- Create: `src/primitive_collision_compiler/paper/__init__.py`
- Create: `src/primitive_collision_compiler/paper/accv_visuals.py`
- Create: `tests/test_accv_visuals.py`

- [x] **Step 1: Add pure helpers for report loading and primitive geometry.**

Implement functions that:

- load a Phase 0 report JSON;
- derive a compact case label from `asset_role` and `asset_id`;
- convert `box` and `convex_mesh` primitive dictionaries into point clouds;
- collect probe outcomes for a fixed set of probes: `contact_canary`, `body_state_drop_settle`, `stack_or_slide`, `sphere_rain`;
- summarize accepted, failed, fallback, and not-applicable outcomes.

The pure helpers must not require USD or matplotlib.

- [x] **Step 2: Add unit tests for the pure helpers.**

Use tiny in-memory report and primitive dictionaries. Verify:

- `box` half-extents produce eight vertices;
- `convex_mesh` vertices are passed through;
- unknown primitive kinds return an empty point array instead of crashing;
- outcome summary counts accept/failure/fallback/not-applicable values correctly.

Run:

```bash
python -m pytest tests/test_accv_visuals.py -q
```

Expected: all tests pass.

### Task 2: Figure Generation CLI

**Files:**
- Create: `scripts/paper/generate_accv_visuals.py`
- Modify: `src/primitive_collision_compiler/paper/accv_visuals.py`

- [x] **Step 1: Implement the CLI wrapper.**

The command must accept:

```bash
python scripts/paper/generate_accv_visuals.py \
  --report /path/to/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json \
  --asset-root /path/to/repo-with-ignored-assets \
  --output-dir paper/shared/figures/generated
```

It must create the output directory and generate five PDFs:

- `phase0_asset_package_overlays.pdf`
- `phase0_collision_probe_scenes.pdf`
- `phase0_outcome_matrix.pdf`
- `bed_franka_mechanism_diagnostic.pdf`
- `franka_link_aware_task_scene.pdf`

It must also write `accv_visuals_manifest.json` with report path, asset root, figure paths, and source record identifiers.

- [x] **Step 2: Implement deterministic figure functions.**

Use stable matplotlib settings, fixed figure sizes, fixed colors, fixed camera angles, and no random sampling. If a mesh is too large, cap with deterministic stride or existing `max_faces` loading.

Figure requirements:

- overlays: five asset rows with input mesh and package overlays for representative lanes;
- collision scenes: bowl, cup, and tray probe panels using recorded failure labels and final metrics;
- outcome matrix: all five rigid assets, selected lanes, and four probe types;
- mechanism diagnostic: capped bed versus Franka final speed and claim-boundary notes;
- Franka task scene: link-aware package coverage, link graph or ordered link schematic, and generated-package consumption metrics.

- [x] **Step 3: Run CLI against the current ignored evidence artifacts.**

Run from the worktree:

```bash
python scripts/paper/generate_accv_visuals.py \
  --report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json \
  --asset-root /cpfs/user/zhuzihou/dev/physics-primitive-agent \
  --output-dir paper/shared/figures/generated
```

Expected: five PDFs plus `accv_visuals_manifest.json` are created under `paper/shared/figures/generated/`.

### Task 3: Paper Integration

**Files:**
- Modify: `paper/shared/sections/method.tex`
- Modify: `paper/shared/sections/experiments.tex`
- Modify: `paper/shared/sections/discussion.tex`
- Modify: `paper/shared/sections/appendix.tex`
- Modify: `paper/shared/figures/sources.yaml`

- [x] **Step 1: Include the generated figures in the main text.**

Add figure environments with `\includegraphics[width=\textwidth]{figures/generated/<name>.pdf}`.
Each caption must state the evidence source and claim boundary in plain reviewer-facing language.

- [x] **Step 2: Expand method and experiment text around the figures.**

Add concise but substantive text covering:

- candidate package generation lanes;
- diagnostic probe semantics;
- why generated V-HACD packages can still fail body-state or support probes;
- collision-scene interpretation;
- Franka generated-package consumption scope.

- [x] **Step 3: Preserve limitations.**

Keep the discussion explicit that this is not broad benchmark superiority, whole-robot performance, formal verification, deployment readiness, real-world transfer, or safety certification.

### Task 4: Build, Page Count, And Preflight

**Files:**
- Modify only if checks expose a concrete issue.

- [x] **Step 1: Build the ACCV PDF.**

Run:

```bash
make -C paper accv
pdfinfo paper/venues/accv/build/main.pdf | rg '^Pages:'
```

Expected: build succeeds and page count is 13 or 14.

- [x] **Step 2: Run documentation and whitespace checks.**

Run:

```bash
python scripts/validate_docs.py
python - <<'PY'
import yaml
from pathlib import Path
yaml.safe_load(Path("paper/shared/figures/sources.yaml").read_text())
print("figure sources yaml ok")
PY
git diff --check
```

Expected: all commands exit 0.

- [x] **Step 3: Run focused tests.**

Run:

```bash
python -m pytest tests/test_accv_visuals.py -q
```

Expected: all tests pass.

### Task 5: Review, Commit, Push, And Clean Status

**Files:**
- No new implementation files beyond the planned set unless a verifier exposes a concrete need.

- [x] **Step 1: Review generated artifacts and diff.**

Check:

```bash
git status --short
git diff --stat
```

Confirm raw USD assets, large run directories, videos, and logs are not tracked.

- [ ] **Step 2: Commit and push the branch.**

Run:

```bash
git add docs/superpowers/plans/2026-05-26-accv-visual-expansion.md \
  src/primitive_collision_compiler/paper \
  tests/test_accv_visuals.py \
  scripts/paper/generate_accv_visuals.py \
  paper/shared/figures/generated \
  paper/shared/figures/sources.yaml \
  paper/shared/sections/method.tex \
  paper/shared/sections/experiments.tex \
  paper/shared/sections/discussion.tex \
  paper/shared/sections/appendix.tex
git commit -m "Expand ACCV paper with Phase 0 visuals"
git push -u origin accv-visual-expansion
```

- [ ] **Step 3: Report clean status.**

Run:

```bash
git status --short --branch
```

Expected: worktree branch is clean and tracks `origin/accv-visual-expansion`.
