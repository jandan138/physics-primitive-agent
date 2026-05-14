# Newton 引擎中用大模型自动生成 Primitive 碰撞包替代 / 优先于 Convex 分解：公司预研级多角度评审报告

**版本**：v1.0  
**日期**：2026-05-14  
**适用对象**：公司预研、技术路线评审、论文选题论证、Newton / Isaac / USD 资产管线研发  
**核心问题**：是否值得把“用大模型在 Newton 引擎中自动生成 primitive collision package，以替代或优先于 convex decomposition”作为公司预研方向？  
**结论预览**：值得做，但应把命题从“完全替代 convex decomposition”改写为 **primitive-first / fallback-aware / simulation-verified collision asset compiler**。

---

## 0. Executive Summary

### 0.1 一句话结论

**有搞头，而且方向很对；但不要承诺“完全替代 convex decomposition”。**  
更好的公司预研命题是：

> **LLM/VLM-guided Primitive-First Collision Proxy Generation for Newton Physics：给定 mesh / USD / URDF / MJCF 资产和任务语义，自动生成可编辑、低成本、任务感知的 primitive collision package；用 Newton 仿真闭环验证，失败区域局部回退到 convex decomposition / convex mesh / SDF / hydroelastic。**

### 0.2 为什么“有搞头”

从工程、科研、产品三方面看，这个方向同时踩中了几个趋势：

1. **主流引擎都偏好 simple primitive colliders**  
   PhysX / Omniverse / Isaac / Unity / Newton 文档都反复强调：primitive 比 convex mesh、SDF mesh、triangle mesh 更便宜，且更稳定、可编辑性更高。

2. **自动 primitive collider 生成已经成为 2026 年明确研究热点**  
   2026 年的 *Convex Primitive Decomposition for Collision Detection* 已经直接提出用 boxes / spheres / capsules / cylinders / prisms 等 primitive 来替代传统 convex hull decomposition，并在 Sketchfab 数据集和刚体仿真 benchmark 上展示了比 V-HACD / CoACD 更低复杂度和更好 wall-clock performance 的趋势。

3. **Newton 正好是适合做这件事的平台**  
   Newton 支持 sphere、capsule、box、cylinder、cone、ellipsoid、mesh、convex mesh；支持 SDF 与 hydroelastic；支持 GPU collision pipeline；还支持 `approximate_meshes()` 用 convex hull、bounding box、bounding sphere、CoACD、V-HACD 替换 mesh collision。也就是说，Newton 已经有 fallback 基础，你可以在上层做一个 collision compiler。

4. **LLM/VLM 的价值不在“直接吐浮点数”，而在语义、任务、工具编排和失败修复**  
   纯几何 primitive fitting 已经有人做；你要有差异化，必须引入：
   - 语义 part decomposition；
   - task-aware collider budget；
   - Newton-in-the-loop verification；
   - 自动 repair / fallback；
   - collision contract 可解释输出。

### 0.3 最大风险

最大风险不是技术不可行，而是 **claim 写错**：

| Claim | 风险 | 建议 |
|---|---:|---|
| “primitive 完全替代 convex decomposition” | 高 | 不建议作为正式目标 |
| “LLM 自动输出所有 primitive 数值参数” | 高 | LLM 不应直接负责高精度数值拟合 |
| “自动 primitive fitting 比 CoACD/V-HACD 更快更好” | 中高 | 已有 2026 CPD 论文，需要差异化 |
| “primitive-first + Newton verifier + fallback” | 中 | 推荐 |
| “任务感知、仿真验证、可编辑 collision contract” | 低到中 | 最推荐，科研和产品价值都高 |

### 0.4 推荐立项名称

建议不要叫：

```text
LLM primitive fully replaces convex decomposition
```

建议叫：

```text
Primitive-First Collision Asset Compiler for Newton:
LLM-Guided, Simulation-Verified, and Fallback-Aware
```

或者中文：

```text
面向 Newton 的 Primitive-First 碰撞资产编译器：
大模型引导、仿真验证、局部回退的自动碰撞代理生成
```

---

## 1. 问题定义

### 1.1 你真正想解决的问题

物理引擎中的 render mesh / CAD mesh 往往不适合作为动态刚体 collision geometry。原因包括：

- render mesh 三角面太多；
- 非凸几何对 dynamic collision 支持差；
- 视觉细节和物理接触意图不一致；
- triangle mesh / SDF / hydroelastic 的精度高但代价高；
- convex decomposition 自动但会产生 hull soup，难编辑、难解释、shape 数可能很多；
- 人工做 primitive collision package 成本高，但效果通常更好。

因此公司真正的痛点是：

> 能不能自动、稳定、可控地把视觉资产转换为低成本、可编辑、任务适配的 collision proxy？

### 1.2 传统方案对比

| 方案 | 优点 | 缺点 | 典型用法 |
|---|---|---|---|
| 单 convex hull | 简单、快 | 凹陷、孔洞、内腔全被填平 | 非关键动态物体 |
| V-HACD / CoACD | 自动处理非凸，保留更多几何 | hull 多、参数敏感、难编辑、仍是 hull soup | 批量资产、复杂非凸物体 |
| 手工 primitive compound | 快、稳定、可编辑、语义清晰 | 人工成本高，批量不可扩 | 游戏、机器人 link、角色、道具 |
| triangle mesh | 几何准确 | 动态非凸支持受限，贵，接触点复杂 | 静态场景、地形 |
| SDF / hydroelastic | 高细节、适合接触丰富任务 | 内存/预处理/运行成本高，调参复杂 | 插入、装配、精密 manipulation |
| 自动 primitive-first | 潜在最优折中 | 目前仍是新方向，鲁棒性和语义尚未完全解决 | 本报告建议预研方向 |

### 1.3 本项目的核心假设

本预研方向可以压成四个可验证假设：

1. **H1：在大多数非精密接触资产上，primitive compound 可以用更少参数和更低运行成本达到 CoACD/V-HACD 级别的任务行为。**
2. **H2：任务语义可以显著降低 collider 数量，例如“只用于堆叠 / 碰撞阻挡 / 抓取 / 容器承载”对应不同 collision fidelity。**
3. **H3：LLM/VLM 对 part semantics、type prior、预算规划和失败修复有价值，但不应直接取代数值优化器。**
4. **H4：Newton-in-the-loop verifier 能把几何 proxy 评估从“看起来贴 mesh”提升到“仿真行为等价”。**

### 1.4 明确非目标

为了避免 scope 爆炸，建议第一阶段不要承诺：

- 不承诺所有资产 100% primitive；
- 不承诺精密插入 / 螺纹 / 齿轮 / 薄壁 CAD 全靠 primitive；
- 不承诺 LLM 直接生成所有浮点参数；
- 不承诺比 SDF/hydroelastic 更准确；
- 不承诺跨所有物理引擎行为一致。

---

## 2. 多 Agent 并行评审结论

下面模拟 9 个评审角色，从不同角度独立审阅该方向。

### 2.1 Agent A：几何算法研究员

**判断**：方向成立，但纯 primitive fitting 的 novelty 已被 2026 CPD 部分覆盖。  

**理由**：

- 近似凸分解本质上是覆盖问题，严格最优通常不可行。
- V-HACD / CoACD 走的是“分块 + convex hull”路线。
- 2026 CPD 已经明确从 convex hull 转向 convex primitive。
- ResFit / PrimitiveAnything / MeshLLM 表明 3D primitive abstraction 和结构化 mesh 表示正在成为热点。

**建议**：

- 不要把论文贡献放在“又一个 primitive decomposition”。
- 应把贡献放在：
  - task-aware；
  - physics behavior metric；
  - Newton closed-loop verification；
  - LLM-guided repair；
  - hybrid fallback。

**一票意见**：支持立项，但必须和 CPD 拉开差异。

---

### 2.2 Agent B：物理引擎工程师

**判断**：primitive-first 非常合理，因为它直接减少 narrow phase 成本和 contact complexity。  

**理由**：

- primitive 有解析 support function 或高度优化的窄相碰撞路径；
- convex mesh 需要 cooking，有顶点/面数限制，复杂 hull 会更贵；
- SDF / hydroelastic 在高精度场景有价值，但不应默认用于所有资产；
- 许多性能问题不是单个 shape 贵，而是 shape count、contact count、filter pairs、pair explosion 引发的。

**风险**：

- 如果自动 primitive 生成太多小 shape，broad phase 和 contact pair 反而变贵；
- 同一 body 上多个 shape 的 self-filter / parent-child filter 必须正确处理；
- primitive 过粗会改变接触 leverage 和摩擦行为；
- cylinder/cone 不是总比低顶点 convex mesh 便宜，某些引擎对 cylinder/cone 有额外 smooth contact 特殊路径。

**建议**：

- 输出时必须记录 shape count、pair count、contact count、narrowphase time；
- 建立 `primitive budget` 和 `fallback budget`；
- 对每个输出 shape 写入 metadata：part label、source region、confidence、fallback reason。

**一票意见**：强烈支持，但要严格用物理性能指标验收。

---

### 2.3 Agent C：机器人仿真 / Isaac / Newton 用户

**判断**：这是机器人 RL / manipulation 资产管线的真实痛点。  

**理由**：

- Isaac Lab 文档建议移除不重要区域的 collision geometry，只保留任务关键接触区域；
- 机器人训练中，过多复杂 collision 会显著降低吞吐；
- 对 locomotion、grasping、stacking，primitive 通常足够；
- 对 peg-in-hole、connector insertion、board placement，primitive 不够，需要 SDF/hydroelastic。

**建议**：

- 任务标签必须进入 pipeline：
  - `locomotion_obstacle`
  - `graspable_object`
  - `stackable_object`
  - `container`
  - `insertion_part`
  - `visual_only_detail`
- 不同任务选择不同 fidelity：
  - RL locomotion：低 fidelity、高吞吐；
  - grasp：接触面和手柄要高 fidelity；
  - insertion：优先 SDF/hydroelastic；
  - clutter / pile：避免过多 contact points。

**一票意见**：支持，但必须从任务驱动角度定义成功，而不是只用 Chamfer / Hausdorff。

---

### 2.4 Agent D：LLM / VLM 研究员

**判断**：LLM 应做 planner / critic / repair，不应做裸数值回归器。  

**理由**：

LLM 擅长：

- 识别物体类别；
- 理解“椅子腿、坐垫、靠背、杯子内腔、把手、机器人指尖”等部件；
- 根据任务描述选择哪些区域重要；
- 解释失败原因；
- 调用工具并迭代修复。

LLM 不擅长：

- 精确输出 3D 浮点参数；
- 保证 shape containment；
- 稳定处理 degenerate mesh；
- 保证几何约束满足。

**建议架构**：

```text
LLM/VLM: semantic plan + type priors + budget + repair proposal
Geometric optimizer: primitive fitting + constraints
Newton verifier: behavior score + failure logs
Repair agent: split/merge/shrink/expand/fallback
```

**一票意见**：支持，但 LLM 角色要设计正确。

---

### 2.5 Agent E：产品 / 公司预研负责人

**判断**：可以立项为 3～6 个月预研，前 4 周必须快速打出 non-LLM baseline。  

**商业价值**：

- 降低资产导入成本；
- 提升 Newton / Isaac / USD 管线易用性；
- 给 internal robotics / digital twin / RL 团队提供自动 collider 工具；
- 可输出论文、demo、SDK 工具、资产 QA 工具；
- 可作为后续“自然语言仿真资产编译器”的组件。

**里程碑建议**：

| 周期 | 目标 | 判断点 |
|---|---|---|
| 0～4 周 | CPD-like primitive baseline + Newton 输出 | 是否能跑通 20～50 个资产 |
| 4～8 周 | Newton verifier + 与 CoACD/V-HACD 对比 | 是否有稳定性能收益 |
| 8～12 周 | LLM/VLM planner + failure repair | LLM 是否带来可测收益 |
| 12～24 周 | hybrid fallback + paper/demo | 是否达到论文/产品化门槛 |

**一票意见**：值得做，但第一阶段不要过度依赖 LLM。

---

### 2.6 Agent F：怀疑型论文审稿人

**判断**：如果论文写成“LLM primitive 替代 convex decomposition”，我会质疑 novelty 和 rigor。  

**可能会被问的问题**：

1. 你和 CPD 2026 的区别是什么？
2. 你为什么需要 LLM？消融实验能证明吗？
3. LLM 是否只是增加成本，没有改善指标？
4. 你是否只在简单家具/道具上有效？
5. 对高频细节、内腔、孔洞、薄片、装配任务怎么办？
6. 你的 metric 是几何距离还是真实物理行为？
7. 你的结果是否 Newton-specific，换 PhysX/MuJoCo 是否失效？
8. 自动生成的 primitive 是否 guaranteed enclosing？是否允许 false negative penetration？
9. collision material、margin、gap、solver iteration 是否混淆了 collider 的贡献？

**建议回应方式**：

- 明确 baseline：CPD-like、CoACD、V-HACD、single hull、manual primitive、SDF oracle；
- 明确 LLM ablation：无 LLM / LLM planner / LLM repair / VLM semantics；
- 用 simulation behavior 作为主指标；
- 用 fallback coverage 和 failure taxonomy 证明系统工程价值；
- 不声称 universal replacement。

**一票意见**：只有改成 task-aware + simulation-verified 才有论文价值。

---

### 2.7 Agent G：数据与 Benchmark 工程师

**判断**：评估设计会决定这个方向成败。只看几何误差不够。  

**建议 benchmark 分层**：

1. 简单刚体：箱子、球、胶囊、瓶子；
2. 家具/道具：椅子、桌子、梯子、工具；
3. 容器/孔洞：杯子、篮子、碗、把手、槽；
4. 机器人/机械：机械臂 link、夹爪、轮子；
5. 高精度装配：peg-hole、connector、nut-bolt；
6. 失败集：薄片、高频雕刻、有内部非接触部件、非流形 mesh。

**建议指标**：

- geometry：Hausdorff、Chamfer、occupancy false positive/negative、excess volume；
- physics：step time、narrowphase time、contact count、penetration、jitter、contact normal distribution；
- task：stack success、grasp success、container success、hole traversal success；
- authoring：shape count、parameter count、semantic label accuracy、人类修改时间；
- fallback：fallback ratio、fallback region size、fallback reason。

**一票意见**：支持，但必须设计 benchmark harness。

---

### 2.8 Agent H：安全 / 可靠性 / QA

**判断**：必须把自动 collider 当成“会影响物理安全边界”的编译产物，而不是美术资产。  

**风险**：

- false negative：物体视觉上相交但 collider 漏了，会穿透；
- false positive：孔洞被堵住，会导致抓取/插入失败；
- margin/gap 设置不当造成提前接触；
- collision_group/filter pairs 错误引入自碰撞；
- mass/inertia 和 collision proxy 不一致导致动力学错误；
- 输出非确定性影响回归测试。

**建议**：

- 每次生成 collision package 都输出 report；
- 对每个资产保存 deterministic seed；
- 提供可视化 overlay；
- 记录 source mesh hash；
- 对 fallback 和人工修改保留 provenance；
- 建立 regression test suite。

**一票意见**：支持，但必须产品化为 compiler + verifier，而不是 one-shot generator。

---

### 2.9 Agent I：IP / 竞争态势

**判断**：纯 primitive decomposition 已经有强 prior art，不能作为唯一壁垒。  

**相关成果**：

- V-HACD：传统 ACD 工具；
- CoACD：collision-aware convex decomposition；
- CPD 2026：primitive decomposition for collision detection；
- VisACD 2026：GPU、visibility-based ACD；
- Learning Convex Decomposition via Feature Fields：learning-based open-world convex decomposition；
- PrimitiveAnything / ResFit / MeshLLM：primitive abstraction / mesh understanding / editable shape programs；
- LLMPhy / ChronoLLM / MCP-SIM：LLM + physics simulator + self-correction。

**建议 claim**：

不要 claim：

```text
first automatic primitive decomposition for collision detection
```

可以 claim：

```text
first task-aware, LLM-guided, Newton-in-the-loop primitive-first collision asset compiler with hybrid fallback and behavior-level verification
```

**一票意见**：方向可做，但 claim 要精准。

---

## 3. 最新科研与工程前沿综述

### 3.1 V-HACD：传统 voxelized approximate convex decomposition

V-HACD 的基本思想是：

```text
input mesh → voxelization → hierarchical split → near-convex clusters → convex hulls
```

它解决的是 exact convex decomposition 不实际的问题：严格最小凸分解通常计算困难，而且输出 cluster 数会很大。因此工程上放宽为 approximate convex decomposition。

**优点**：

- 工具链成熟；
- 很多引擎、DCC、机器人库都集成过；
- 对任意 mesh 相对鲁棒；
- 参数可控：resolution、concavity、max hulls、max vertices。

**缺点**：

- voxelization 可能损失孔洞、薄结构；
- 参数调优困难；
- 输出 hull soup，不容易人工编辑；
- hull 数和每 hull 顶点数可能高；
- 对 task-critical 区域没有语义理解。

**对你项目的启示**：

V-HACD 是必须比较的 baseline，但不是你要跟随的路线。你要强调 primitive-first 更接近技术美术/仿真工程师手工 collision package 的 workflow。

---

### 3.2 CoACD：collision-aware convex decomposition

CoACD 是 2022 SIGGRAPH 工作，核心贡献包括：

1. **collision-aware concavity**：不只看边界到凸包的距离，也考虑内部，从而更能保留碰撞条件；
2. **直接用 3D planes 切 mesh**：避免 voxelization errors；
3. **tree search / multi-step planning**：避免 greedy 造成过多不必要切割。

它针对的是传统 ACD 会“填 toaster slots / 填孔洞”的问题。CoACD 在机器人交互和 articulated object 上更有意义。

**优点**：

- 比 V-HACD 更注重 collision condition；
- 对孔洞、槽、内腔等功能性几何更友好；
- 已有开源实现，仍是强 baseline。

**缺点**：

- 输出仍然是 convex hulls；
- 可编辑性弱；
- shape/hull complexity 不一定低；
- 不知道任务语义，只知道几何 concavity；
- 对运行时性能不一定优于 primitive package。

**对你项目的启示**：

CoACD 是你的主要竞争 baseline。你的方法必须回答：

> 在哪些任务和资产类别上，primitive-first 比 CoACD 更快、更可编辑，且任务行为不差？

---

### 3.3 Convex Primitive Decomposition for Collision Detection：最接近的直接竞争成果

2026 年 *Convex Primitive Decomposition for Collision Detection* 是最重要的直接竞品。它指出：

- 自动 ACD 主要生成 convex hulls；
- convex hulls 在游戏等 tight performance budget 场景中不如 manual primitives；
- convex hull 输出难以手工修改并保持凸性；
- primitive colliders 如 box、sphere、capsule 在物理引擎中通常更优化。

该论文提出 bottom-up primitive decomposition：

```text
mesh faces → per-face primitive candidates → greedy merge → minimize excess volume → output boxes/spheres/capsules/cylinders/prisms
```

其重要特征：

- 输出 primitive 而非 convex hull；
- 目标是 rigid body simulation；
- 保证 primitive 覆盖输入 surface；
- 用 Sketchfab 模型评估；
- 与 V-HACD / CoACD 比较几何距离、复杂度和仿真 wall-clock time。

**它对你项目的威胁**：

如果你只做：

```text
mesh → 自动 fitting boxes/spheres/capsules → Newton colliders
```

那么 novelty 很可能不够。

**它给你的机会**：

这篇论文也说明 primitive decomposition 是一个真实、重要、正在兴起的方向。你可以把它作为强 baseline，然后进一步做：

- task-aware；
- LLM/VLM semantic decomposition；
- Newton-specific verification；
- collision behavior equivalence；
- repair loop；
- hybrid fallback。

---

### 3.4 VisACD：2026 GPU / visibility-based ACD

VisACD 是 2026 年的另一个相关方向。它仍属于 approximate convex decomposition，但强调：

- visibility-based concavity；
- rotation-equivariant；
- intersection-free；
- GPU acceleration；
- fewer convex parts；
- 更高效率。

**对你项目的含义**：

Convex decomposition 并没有停止发展。2026 年仍有新 ACD 算法出现。因此“primitive 完全替代 convex decomposition”这个 claim 更危险。更稳的是：

```text
primitive-first where primitives are enough;
convex/SDF fallback where they are not.
```

---

### 3.5 Learning Convex Decomposition via Feature Fields：learning-based convex decomposition

2026 年 NVIDIA / UT Austin 的 *Learning Convex Decomposition via Feature Fields* 把 convex decomposition 表述为 feature learning：

- 用自监督几何损失学习 feature field；
- clustering feature 生成 approximate convex components；
- 支持 open-world shapes；
- 可从 mesh / point cloud / Gaussian splats 等不同输入模态推理；
- 推理速度快，支持多 granularity。

**对你项目的含义**：

learning-based decomposition 正在兴起。你的 LLM/VLM 方向不是孤立的，但要注意：

- 这类方法学习的是凸分解；
- 你可以学习 primitive type prior / part segmentation；
- 你也可以把 feature field / segmentation 结果作为 primitive fitting 的 region proposal。

---

### 3.6 Empart：交互式、区域约束的 convex decomposition

Empart 2025 关注 robotics 中的区域差异化简化：

- grasp contact 区域需要高 fidelity；
- 非关键区域可以更粗；
- uniform tolerance 会导致关键区域不够细或非关键区域过细；
- 通过交互指定 region-specific tolerance，在 pick-and-place 中降低 simulation time。

**对你项目的启示非常直接**：

你可以把人工交互换成 LLM/VLM 或 task prompt：

```text
“this object is used for grasping by a parallel gripper”
→ 高保真保留 side contact patches / handle / rim
→ 非接触装饰细节用粗 box 或 visual-only
```

这就是你的差异化核心之一：**task-aware region fidelity**。

---

### 3.7 PrimitiveAnything：人类风格 primitive assembly generation

PrimitiveAnything 2025 把 shape primitive abstraction 改写为 primitive assembly generation。它强调：

- 人类视觉认知倾向于把复杂形状分解成简单 primitive；
- 传统几何优化语义理解弱；
- 小规模类别特定数据泛化差；
- 使用 transformer 学习人类手工 primitive abstraction；
- 可生成更符合人类感知的 primitive assemblies。

**对你项目的含义**：

PrimitiveAnything 的输出不一定能直接作为 collision shape，因为 collision 需要 containment、contact correctness、Newton compatibility。但它可以作为：

- semantic part proposal；
- primitive type prior；
- human-like decomposition prior；
- editor-friendly primitive layout prior。

---

### 3.8 MeshLLM：LLM 理解和生成 3D mesh 的 primitive-mesh decomposition

MeshLLM 2025 的重点是让 LLM 处理 text-serialized 3D meshes。它引入 Primitive-Mesh decomposition，把 mesh 分成结构性子单元，从而构建大规模数据并改善 topology / spatial understanding。

**对你项目的含义**：

它说明 LLM + mesh structure 正在快速发展，但不意味着你应该让 LLM 直接处理完整高分辨率 mesh。更合理的是：

```text
mesh → geometry summary / part graph / candidate regions → LLM planner
```

而不是：

```text
完整 mesh 顶点序列 → LLM → primitive 参数
```

---

### 3.9 ResFit / SuperFrusta：可编辑、紧凑、可优化的 analytic primitive assembly

ResFit 2025 提出 SuperFrustum 这种表达力更强的 analytic primitive，并用 residual fitting 迭代拟合形状。其目标是：

- compact；
- editable；
- optimizable；
- high-fidelity primitive assemblies。

**对你项目的启示**：

传统 box/sphere/capsule/cylinder 可能不足以表达某些 curved / hollow / tapered / bent shapes。可以考虑两层策略：

1. Newton 原生 primitive：box/sphere/capsule/cylinder/cone/ellipsoid；
2. 高阶 analytic primitive：仅用于 proposal / segmentation / SDF fallback，或未来扩展。

短期不建议一开始就扩展 Newton primitive 类型，因为产品化复杂度高。先用 Newton 原生支持类型。

---

### 3.10 LLMPhy / ChronoLLM / MCP-SIM：LLM + physics simulator 闭环

这些工作共同说明：

- LLM 单次生成仿真代码或参数容易失败；
- 把 physics engine 作为 external tool / verifier 更可靠；
- 迭代 plan-act-reflect-revise 比 one-shot 更稳；
- LLM 可以通过 simulator feedback 修正 scene layout、physical parameters 或代码。

**对你项目的直接启示**：

应把 Newton 作为 verifier，而不是把 LLM 当成 oracle：

```text
LLM proposes strategy
optimizer fits colliders
Newton runs verification tests
metrics/logs returned to LLM/repair agent
system updates primitive package or fallback
```

---

## 4. Newton 工程现实：为什么它适合这个预研

### 4.1 Newton collision pipeline 的关键事实

Newton 的 collision pipeline 适合做这个方向，因为它清晰地区分了：

1. primitive / convex pairs；
2. mesh BVH queries；
3. precomputed SDF；
4. hydroelastic contacts。

简化理解：

```text
Broad Phase: AABB culling
    ↓
Pair triage:
    primitive / convex → MPR / GJK
    mesh without SDF   → BVH distance queries
    mesh with SDF      → O(1) SDF distance lookup
    hydroelastic pair  → distributed contact surface + contact reduction
```

Newton 支持的 shape 类型包括：

- plane；
- heightfield；
- sphere；
- capsule；
- box；
- cylinder；
- cone；
- ellipsoid；
- mesh；
- convex mesh。

SDF 在 Newton 中不是独立 shape type，而是附着在 mesh 或 primitive 上的 collision data。

### 4.2 Newton 当前已有 mesh approximation API

Newton 的 `ModelBuilder.approximate_meshes()` 已经支持：

- `convex_hull`；
- `bounding_box`；
- `bounding_sphere`；
- `coacd`；
- `vhacd`。

这说明项目落地方式可以非常自然：

```python
builder.add_usd("robot_or_asset.usda")
# 当前：builder.approximate_meshes(method="coacd")
# 目标：builder.compile_collision_primitives(method="llm_primitive_first", task="grasping")
```

### 4.3 推荐 Newton 集成形态

建议新增或封装一个上层工具，而不是一开始改 Newton core：

```python
from primitive_compiler import compile_collision_package

builder = newton.ModelBuilder()
builder.add_usd("asset.usda")

report = compile_collision_package(
    builder,
    method="primitive_first",
    task="grasping",
    budget={"max_shapes": 16, "max_fallback_ratio": 0.15},
    verifier="newton",
    fallback=["convex_hull", "coacd", "sdf"],
    keep_visual_shapes=True,
)

model = builder.finalize()
```

输出 report：

```json
{
  "asset_id": "chair_042",
  "task": "stacking_and_grasping",
  "method": "llm_primitive_first",
  "num_primitives": 9,
  "num_fallback_convex": 1,
  "fallback_ratio_surface": 0.06,
  "estimated_speedup_vs_coacd": 1.8,
  "contact_stability_score": 0.91,
  "hole_preservation_score": 1.0,
  "warnings": [
    "thin decorative rods ignored as visual_only",
    "back_handle used local convex fallback"
  ]
}
```

### 4.4 Newton-specific 工程注意事项

必须严肃处理这些点：

1. **collision filtering**  
   同一 body 上多个 shapes 默认通常不应互相碰撞；articulation parent-child filter 也要保留。

2. **shape margin / gap**  
   margin 改变 contact point placement，gap 改变 contact generation distance。自动 primitive 过粗时，如果再叠加大 margin，会造成提前接触。

3. **mass / inertia**  
   collision proxy 和 mass/inertia 计算来源要明确。质量惯量可以来自原 mesh、primitive union 或用户指定。

4. **SDF / hydroelastic fallback**  
   对非凸、高细节、精密装配区域，可以局部 SDF；但 SDF 需要 watertight 优先，非 watertight 构建更慢或更不可靠。

5. **contact reduction**  
   mesh/SDF/hydroelastic 可能产生很多 raw contacts，需要 reduction；primitive direct path 通常 contact 更少。

6. **replicated RL worlds**  
   在大量并行环境中，shape 数和 contact pairs 会被放大，primitive-first 的价值更大，但错误 overlap 也更危险。

---

## 5. 工程前沿：主流引擎对 primitive / convex / mesh 的态度

### 5.1 Omniverse / PhysX / Isaac

Omniverse Physics 文档建议：

- primitive colliders 是首选，如果能足够近似物体；
- convex meshes 是 primitive 后的下一档；
- SDF mesh colliders 适合动态刚体需要高细节 triangle mesh collision 的场景，例如机器人装配；
- triangle mesh 更适合大型 static / kinematic 几何。

Isaac Sim / Isaac Lab 性能文档也强调：

- collision geometry 越简单，仿真越快；
- primitive colliders 最快；
- convex mesh 次之；
- SDF mesh 比 simple sphere 更贵；
- 高 aspect ratio convex hull 可能导致 GPU compatibility 问题和 CPU fallback。

**对本项目的启示**：

自动 primitive collision package 不只是学术方向，也和 Isaac / Omniverse 官方性能建议一致。

### 5.2 Unity

Unity 文档明确指出：

- Mesh collider 通常比 primitive collider 开销更高；
- concave mesh collider 有限制，通常 static / kinematic；
- 如果两个 concave mesh colliders 需要准确碰撞，应使用多个 convex colliders 的 compound collider；
- 对 runtime-changing mesh，通常更适合 primitive / compound approximation。

**对本项目的启示**：

游戏行业长期依赖手工 compound primitives。自动 primitive-first 本质上是在自动化技术美术工作流。

### 5.3 MuJoCo

MuJoCo 长期偏好明确建模的 geoms。近年来引入 SDF collision primitive，说明非凸高细节接触也是刚需，但这并不否定 primitive geoms 的主导地位。

**对本项目的启示**：

即使有 SDF，仿真管线仍然需要低成本 primitives；SDF 更像 fallback / high-fidelity mode。

### 5.4 PhysX convex mesh 限制

PhysX 5.4 文档显示，`PxConvexMesh` 是顶点/多边形面表示的凸多面体，顶点和面数量限制为 255，并且创建 convex mesh 需要 cooking。对于大量动态资产，convex cooking 和复杂 hull 都是成本因素。

**对本项目的启示**：

primitive package 有天然可编辑、低参数、低 cooking 负担的优势。

---

## 6. 核心技术方案

### 6.1 推荐系统名称

暂定：**NPC Compiler**，即：

```text
Newton Primitive Collision Compiler
```

注意 NPC 只是内部代号，避免和游戏 NPC 混淆。

### 6.2 输入输出定义

#### 输入

```yaml
asset:
  path: chair.usda
  type: USD | URDF | MJCF | OBJ | GLB | STL
  visual_mesh: true
  collision_mesh: optional

task:
  primary: grasping | stacking | locomotion_obstacle | insertion | container | generic
  critical_regions: optional
  allowed_fallback: [convex_hull, coacd, sdf]
  max_runtime_budget: optional
  max_shape_count: optional

engine:
  target: newton
  solver: mujoco_warp | xpbd | featherstone
  batch_worlds: 1024
  device: cuda
```

#### 输出

```yaml
collision_package:
  primitives:
    - type: box
      label: seat
      body: chair_body
      transform: [...]
      scale: [...]
      source_faces: [...]
      confidence: 0.96
    - type: capsule
      label: front_left_leg
      transform: [...]
      radius: 0.035
      half_height: 0.41
  fallback_shapes:
    - type: convex_mesh
      label: handle_inner_region
      reason: hole_preservation_failed_with_primitives
  config:
    collision_group: 1
    margin: 0.001
    gap: 0.005
  metrics:
    geometry:
      excess_volume: ...
      occupancy_false_positive: ...
      occupancy_false_negative: ...
    physics:
      median_step_time_ms: ...
      contact_jitter: ...
      task_success: ...
  provenance:
    source_mesh_hash: ...
    compiler_version: ...
    seed: 42
```

### 6.3 Pipeline 总览

```text
                ┌─────────────────────────┐
                │  Mesh / USD / URDF      │
                └───────────┬─────────────┘
                            ↓
                ┌─────────────────────────┐
                │ Geometry Preprocessor   │
                │ scale / normals / PCA   │
                │ connected components    │
                │ holes / thin features   │
                └───────────┬─────────────┘
                            ↓
                ┌─────────────────────────┐
                │ Semantic / Task Planner │
                │ LLM/VLM / part priors   │
                │ fidelity allocation     │
                └───────────┬─────────────┘
                            ↓
                ┌─────────────────────────┐
                │ Primitive Proposal Bank │
                │ box/sphere/capsule/...  │
                │ CPD-like merge          │
                └───────────┬─────────────┘
                            ↓
                ┌─────────────────────────┐
                │ Constrained Optimizer   │
                │ containment / volume    │
                │ contact patch preserve  │
                └───────────┬─────────────┘
                            ↓
                ┌─────────────────────────┐
                │ Newton Verifier         │
                │ drop/stack/grasp/slide  │
                │ container/hole tests    │
                └───────────┬─────────────┘
                            ↓
            pass ───────────┴─────────── fail
              ↓                            ↓
┌─────────────────────────┐    ┌─────────────────────────┐
│ Export Collision Package│    │ Repair / Split / Merge  │
│ Newton + USD metadata   │    │ or Local Fallback       │
└─────────────────────────┘    └───────────┬─────────────┘
                                           ↺
```

---

## 7. 各模块设计细化

### 7.1 Geometry Preprocessor

职责：把任意导入资产整理成可拟合、可评价的数据结构。

#### 输入处理

- normalize scale；
- compute AABB / OBB；
- connected component segmentation；
- remove isolated degenerate triangles；
- fix normals when possible；
- detect non-manifold / boundaries；
- sample surface points；
- compute curvature / thickness / local PCA；
- detect holes / tunnels / cavities；
- detect thin rods / plates；
- build adjacency graph；
- optional watertightness check。

#### 输出

```python
MeshSummary(
    components=[...],
    face_graph=...,
    sampled_points=...,
    normals=...,
    curvature=...,
    thickness=...,
    hole_candidates=...,
    thin_features=...,
    symmetry_axes=...,
)
```

### 7.2 Semantic / Task Planner

LLM/VLM 不直接输出最终 collider 参数，而是输出 strategy。

#### 输入

- mesh thumbnails / rendered views；
- geometry summary；
- part graph；
- task prompt；
- engine constraints；
- benchmark failure logs。

#### 输出示例

```json
{
  "object_class": "chair",
  "primary_task": "stacking_and_grasping",
  "part_plan": [
    {"name": "seat", "importance": "high", "preferred_primitives": ["box"]},
    {"name": "back", "importance": "medium", "preferred_primitives": ["box"]},
    {"name": "legs", "importance": "high", "preferred_primitives": ["capsule", "box"]},
    {"name": "small_decoration", "importance": "visual_only", "preferred_primitives": []}
  ],
  "budget": {
    "max_primitives": 12,
    "max_convex_fallbacks": 2,
    "preserve_holes": true
  },
  "verification_tests": ["drop", "stack", "side_push", "grasp"]
}
```

#### 为什么需要 LLM/VLM

纯几何算法不知道：

- 椅子的腿是否比装饰花纹重要；
- 杯子的内部空间是否必须保留；
- 机器人夹爪的指尖接触面是否必须高精度；
- 轮子的圆柱接触是否应该保持 smooth rolling；
- 哪些 visual details 可以删除 collision。

LLM/VLM 的价值是把物理任务映射到 fidelity allocation。

### 7.3 Primitive Proposal Bank

基础 primitive 类型建议先限制为 Newton 原生支持：

- box；
- sphere；
- capsule；
- cylinder；
- cone；
- ellipsoid；
- convex mesh fallback；
- mesh SDF fallback。

#### 拟合方法候选

1. **OBB fitting**  
   - PCA / minimum-volume OBB；
   - 适合 boxy parts；
   - 快，稳定。

2. **Capsule fitting**  
   - 主轴 PCA；
   - 对长条、肢体、管状、椅腿、机器人 link 有效；
   - 可用 line segment + max radial distance containment。

3. **Cylinder fitting**  
   - 轮子、圆柱轴、瓶身；
   - 注意在某些引擎中 cylinder smooth collision 比 low-poly convex 更贵。

4. **Sphere / ellipsoid fitting**  
   - 圆形物体、关节、球头；
   - ellipsoid 对有方向缩放的有机圆润形状有用。

5. **Cone fitting**  
   - 锥形零件、漏斗、尖端。

6. **CPD-like face merge**  
   - 从 face-level primitives 开始；
   - 贪心 merge；
   - 以 excess volume / containment / task score 为 cost。

7. **Part-region fitting**  
   - 根据 semantic segmentation 区域拟合；
   - 避免纯 topology merge 被非关键内部结构干扰。

### 7.4 Constrained Optimizer

目标函数建议不是单一 Chamfer，而是多目标：

```text
minimize:
  w1 * excess_volume
+ w2 * uncovered_surface_penalty
+ w3 * contact_patch_error
+ w4 * hole_blocking_penalty
+ w5 * primitive_count_penalty
+ w6 * pair_count_penalty
+ w7 * task_failure_penalty
```

#### 关键约束

- **containment constraint**：不能漏掉必须挡住的区域；
- **negative space constraint**：孔洞 / 内腔不能被错误堵住；
- **minimum feature preservation**：抓取面、支撑面、滚动面要保留；
- **shape count budget**；
- **Newton compatibility**；
- **scale / aspect ratio stability**。

### 7.5 Newton Verifier

Verifier 是项目核心差异化。它不只是跑一下 collision，而是形成自动评价矩阵。

#### 基础测试

1. **drop test**：物体落地，检查稳定性、穿透、反弹；
2. **sphere rain test**：大量小球落到物体上，检查孔洞/平台/容器行为；
3. **stack test**：堆叠稳定性；
4. **slide test**：接触面法线和摩擦行为；
5. **roll test**：轮子/圆柱 rolling behavior；
6. **push test**：侧推轨迹和接触力；
7. **grasp test**：夹爪接触成功率；
8. **container test**：小物体是否能进入容器；
9. **hole traversal test**：探针是否能穿过孔洞；
10. **insertion test**：插入任务是否需要 fallback。

#### 与 oracle 对比

可设置 oracle：

- high-resolution SDF / hydroelastic；
- original static triangle mesh；
- manual primitive collider；
- carefully tuned CoACD。

#### 输出指标

```yaml
physics_metrics:
  median_step_time_ms: 0.42
  p95_step_time_ms: 0.61
  narrowphase_time_ms: 0.11
  contact_count_mean: 12.3
  contact_count_p95: 24
  max_penetration_m: 0.003
  contact_normal_error_deg: 6.2
  jitter_score: 0.04
  task_success_rate: 0.93
```

### 7.6 Repair / Fallback Agent

当 verifier 失败时，不是直接丢弃，而是诊断：

| Failure | 可能原因 | Repair |
|---|---|---|
| 提前碰撞 | primitive 太大 / margin 过大 | shrink / split / reduce margin |
| 穿透 | false negative / primitive 漏覆盖 | expand / add primitive / local convex |
| 孔洞堵住 | box/capsule 跨越 negative space | split around hole / fallback CoACD/SDF |
| 抓取失败 | 接触面过粗 / handle 丢失 | preserve contact patch / local convex |
| jitter | 接触点过多或法线跳变 | merge / simplify / adjust gap |
| 速度慢 | primitives 过多 / cylinder/cone 太多 | merge / replace by box/capsule / reduce detail |
| CPU fallback | convex aspect ratio 问题 | replace by primitive / split / bounding cube |

Repair Agent 可以输出：

```json
{
  "diagnosis": "handle opening is blocked by single OBB",
  "repair": [
    "split handle region into two capsules",
    "add small box at upper bridge",
    "preserve inner clearance > 0.04m"
  ],
  "fallback_if_failed": "coacd on handle submesh only"
}
```

---

## 8. 研究问题与可发表贡献

### 8.1 推荐主研究问题

```text
Can task-aware primitive-first collision proxies, generated through LLM/VLM-guided planning and Newton simulation verification, match the behavior of convex/SDF collision proxies at lower computational and authoring cost?
```

中文：

```text
在 Newton 中，任务感知的 primitive-first 碰撞代理能否在更低运行和编辑成本下，达到 convex/SDF 碰撞代理相近的仿真行为？
```

### 8.2 可发表贡献点

#### Contribution 1：Task-aware primitive collision compiler

不是只做几何拟合，而是根据任务分配 fidelity：

```text
contact-critical regions → high fidelity primitives / local fallback
non-critical regions     → coarse primitive / visual-only
```

#### Contribution 2：LLM/VLM planner for collision semantics

LLM/VLM 不输出最终数值，而是输出：

- part labels；
- primitive type priors；
- importance weights；
- test selection；
- repair suggestions。

#### Contribution 3：Newton-in-the-loop behavior verification

主指标不是几何距离，而是：

- runtime；
- contact quality；
- task success；
- stability；
- fallback rate。

#### Contribution 4：Hybrid fallback with local convex/SDF

失败不全局回退，而是局部回退：

```text
90% surface primitive
10% task-critical hole/handle local CoACD or SDF
```

#### Contribution 5：Editable collision contract

输出可读、可编辑、可调参：

```yaml
box: seat_support
capsule: front_left_leg
fallback_convex: handle_inner_clearance
visual_only: decorative_screws
```

这比 hull soup 更适合产品化。

---

## 9. Baseline 设计

### 9.1 必须比较的 baseline

| Baseline | 作用 |
|---|---|
| single convex hull | 最简单凸近似 |
| bounding box / bounding sphere | primitive lower baseline |
| V-HACD | 传统 ACD baseline |
| CoACD | collision-aware ACD 强 baseline |
| CPD-like primitive decomposition | 最重要直接竞品 |
| manual primitive colliders | 人工 upper bound |
| SDF / hydroelastic | 高精度 oracle 或 fallback baseline |
| original triangle mesh static | 几何 oracle，仅部分任务可用 |

### 9.2 消融实验

| Variant | 目的 |
|---|---|
| no LLM, pure geometry | 验证几何 baseline |
| LLM planner only | 验证语义 part / type prior |
| LLM repair only | 验证失败诊断 |
| VLM part segmentation only | 验证视觉语义 |
| no Newton verifier | 验证仿真闭环价值 |
| no fallback | 验证 hybrid fallback 必要性 |
| geometry metrics only | 证明几何误差不等于物理行为 |
| task-aware vs generic | 验证任务语义价值 |

### 9.3 推荐成功指标

第一阶段可以设定：

```yaml
success_criteria_v0:
  assets: >= 50
  supported_tasks: [drop, stack, slide, grasp_proxy]
  median_step_time_vs_coacd: <= 0.75
  task_success_vs_coacd: >= 0.95
  primitive_count_median: <= 16
  fallback_surface_ratio_median: <= 0.15
  generation_success_rate: >= 0.85
  deterministic_regression: true
```

第二阶段可以设定：

```yaml
success_criteria_v1:
  assets: >= 300
  supported_tasks: [drop, stack, slide, roll, grasp, container, hole]
  median_step_time_vs_coacd: <= 0.60
  task_success_vs_sdf_or_manual: >= 0.90
  human_edit_time_reduction: >= 50%
  LLM_ablation_gain_task_success: >= 5%
  LLM_ablation_shape_reduction: >= 10%
```

---

## 10. Benchmark 资产集建议

### 10.1 资产类型矩阵

| 类别 | 示例 | 重点测试 |
|---|---|---|
| Primitive-like | box、ball、capsule、cylinder | 不应过拟合，输出应极简 |
| Furniture | chair、table、shelf | 多部件、支撑面、腿部 |
| Tools | hammer、wrench、drill | 抓取、长条、孔洞 |
| Containers | cup、bowl、basket、bin | 内腔、孔洞、放入小物体 |
| Robots | links、gripper、wheel | 接触面、关节附近 filter |
| Mechanical parts | bracket、gear-like、connector | fallback 判断 |
| Organic | animal statue、plant | high-frequency / curved failure |
| Thin structures | ladder、wireframe、fence | primitive 数量爆炸风险 |
| Non-manifold | scanned assets、Sketchfab messy mesh | robustness |

### 10.2 任务集

| 任务 | 评价目标 |
|---|---|
| Drop | 基础稳定性和穿透 |
| Stack | 支撑面和法线质量 |
| Slide | 摩擦接触行为 |
| Roll | 圆柱/轮子行为 |
| Push | 接触力矩和 leverage |
| Grasp | 抓取接触面 |
| Container Fill | 内腔保留 |
| Hole Probe | 孔洞不堵塞 |
| Insertion | 判断是否应 fallback SDF |
| RL Batch | 大规模并行性能 |

---

## 11. 指标体系

### 11.1 几何指标

| 指标 | 说明 |
|---|---|
| one-way Hausdorff collider→mesh | collider 表面到 mesh 的最大距离 |
| Chamfer distance | 平均几何贴合 |
| excess volume | primitive union 多包了多少体积 |
| uncovered surface | 必须覆盖区域是否漏掉 |
| occupancy false positive | 空腔/孔洞被误填 |
| occupancy false negative | 实体区域漏覆盖 |
| hole clearance | 孔洞最小可通过半径 |
| contact patch preservation | 任务关键接触面是否保留 |

### 11.2 物理指标

| 指标 | 说明 |
|---|---|
| Newton step time | 总步进时间 |
| narrowphase time | 碰撞窄相时间 |
| broadphase pair count | 候选 shape pair 数 |
| contact count mean/p95 | 接触点数量 |
| penetration depth | 穿透深度分布 |
| contact normal error | 与 oracle 的法线差 |
| jitter score | 静态接触抖动 |
| energy drift | 非物理能量变化 |
| solver iterations to converge | 求解代价 |

### 11.3 任务指标

| 任务 | 指标 |
|---|---|
| stack | 稳定秒数、倒塌率 |
| grasp | 成功率、滑落率、夹爪力 |
| container | 小物体进入率、误碰率 |
| hole | probe pass/fail、clearance error |
| insertion | 成功率、卡死率、接触力峰值 |
| locomotion obstacle | policy reward / collision stability |

### 11.4 可编辑性指标

| 指标 | 说明 |
|---|---|
| shape count | primitive 数 |
| parameter count | 可编辑参数量 |
| semantic label accuracy | part label 是否正确 |
| human edit time | 人工修正时间 |
| DCC compatibility | Blender/USD/Isaac 可视编辑 |
| reproducibility | seed/hash 是否复现 |

---

## 12. 为什么不能承诺“完全替代 convex decomposition”

### 12.1 高频细节

雕刻、有机模型、复杂曲面若完全用 primitives 表达，primitive 数可能爆炸。此时低顶点 convex hull 或 SDF 可能更合适。

### 12.2 内腔、孔洞、拓扑

Primitive fitting 容易跨越 negative space，把孔堵住。虽然可以 split，但复杂孔洞可能需要很多 primitives 或 fallback。

### 12.3 精密装配

对于 connector insertion、peg-in-hole、nut-bolt 等 tight tolerance 任务，primitive 的接触法线、间隙和真实几何差异会直接改变任务结果。这里 SDF/hydroelastic 更合理。

### 12.4 复杂 CAD / 非流形 mesh

工业 CAD 可能包含内部组件、薄壁、重叠面、非流形结构。primitive fitting 容易被内部或不可见几何干扰。

### 12.5 convex decomposition 仍在进化

CoACD、VisACD、learning-based convex decomposition 都说明 ACD 仍是活跃方向。primitive-first 是强补充，不是通吃替代。

---

## 13. 推荐产品形态

### 13.1 CLI 工具

```bash
newton-collision-compile \
  --input assets/chair.usda \
  --task grasping,stacking \
  --method primitive-first \
  --max-primitives 16 \
  --fallback coacd,sdf \
  --verify drop,stack,grasp \
  --output assets/chair_collision.usda \
  --report reports/chair_collision_report.html
```

### 13.2 Python API

```python
from npc_compiler import CollisionCompiler, CompileConfig

compiler = CollisionCompiler(engine="newton")
config = CompileConfig(
    method="primitive_first",
    task="grasping",
    max_primitives=16,
    fallback=["coacd", "sdf"],
    verify=["drop", "grasp", "side_push"],
    keep_visual=True,
)

result = compiler.compile("asset.usda", config)
result.export_usd("asset_collision.usda")
result.report.save("asset_report.md")
```

### 13.3 Isaac / USD UI 插件

UI 功能：

- visualize visual mesh vs collision package；
- display primitive labels；
- show heatmap of approximation error；
- mark false positive negative space；
- run Newton verifier；
- one-click repair；
- local fallback selection；
- export to USD custom attributes。

### 13.4 Asset QA dashboard

每个资产给一个状态：

```text
PASS: primitive-first, 8 shapes, no fallback
WARN: 12 primitives + local convex fallback on handle
FAIL: insertion task requires SDF, primitive package rejected
```

---

## 14. 技术路线图

### 14.1 Phase 0：调研与 baseline 复现（1～2 周）

目标：确认 API 和 benchmark harness。

任务：

- 整理 Newton shape API；
- 测试 `approximate_meshes()` 的 CoACD/V-HACD/bounding_box；
- 准备 20 个资产；
- 写 drop / sphere rain / stack benchmark；
- 输出 step time/contact count/report。

交付：

- baseline comparison notebook；
- Newton collision visualization；
- 初版 report schema。

### 14.2 Phase 1：Non-LLM primitive baseline（2～4 周）

目标：先不引入 LLM，做 CPD-like primitive fitting baseline。

任务：

- connected components；
- OBB/capsule/sphere/cylinder fitting；
- greedy merge by excess volume；
- max primitive budget；
- export Newton primitive shapes；
- 与 CoACD/V-HACD 对比。

交付：

- `primitive_first_baseline.py`；
- 50 个资产实验；
- speed/quality table。

通过标准：

- 至少 70% 资产能生成可运行 collision；
- median step time 优于 CoACD；
- 失败原因可分类。

### 14.3 Phase 2：Newton verifier + repair loop（4～8 周）

目标：把仿真行为纳入自动闭环。

任务：

- drop / stack / slide / sphere rain；
- contact metrics；
- failure taxonomy；
- repair operators：split、merge、shrink、expand、change primitive type；
- local convex fallback。

交付：

- verifier harness；
- automatic repair demo；
- failure gallery。

通过标准：

- repair 后 task success 明显提升；
- local fallback 比 full fallback 更便宜；
- report 能解释失败和修复。

### 14.4 Phase 3：LLM/VLM planner（8～12 周）

目标：证明 LLM/VLM 带来可测收益。

任务：

- 输入多视图渲染 + geometry summary；
- 生成 part plan / type prior / task fidelity；
- 与 pure geometry 比较；
- LLM repair suggestion；
- structured output validation。

交付：

- LLM planner prompts；
- ablation results；
- task-aware demo。

通过标准：

- LLM 版本在 task success 或 primitive count 上有统计收益；
- 输出稳定，失败可回退；
- LLM 不直接生成未经验证的最终 collider。

### 14.5 Phase 4：Hybrid fallback + product prototype（12～24 周）

目标：做成公司内部可用工具。

任务：

- local CoACD/SDF fallback；
- USD metadata export；
- Isaac/Newton viewer overlay；
- regression test；
- batch asset compiler；
- documentation。

交付：

- CLI + Python API；
- 300+ assets benchmark；
- internal demo；
- paper draft or tech report。

---

## 15. 论文路线建议

### 15.1 推荐标题

```text
Primitive-First Collision Asset Compilation for Newton Physics
with Language-Guided Task Semantics and Simulation Verification
```

或：

```text
Task-Aware Editable Primitive Colliders for Contact-Rich Simulation
```

### 15.2 摘要雏形

```text
Collision geometry authoring remains a bottleneck in physical simulation pipelines.
Approximate convex decomposition can automate mesh-to-collider conversion, but often
produces hull soups that are difficult to edit and may be inefficient for large-scale
robot learning. We present a primitive-first collision asset compiler for Newton Physics.
Given a visual mesh and task specification, our system proposes editable primitive
collision packages, verifies their behavior in Newton, and locally falls back to convex
or SDF representations when primitives fail. A language/vision model is used not as a
numeric regressor, but as a semantic planner and repair critic, allocating fidelity to
task-critical regions. Experiments across object interaction tasks show that our method
reduces collision complexity and simulation time compared with convex decomposition
baselines while preserving task-level behavior on non-precision tasks, and identifies
when high-fidelity fallback is necessary.
```

### 15.3 论文贡献表述

不要写：

```text
We replace convex decomposition.
```

写：

```text
We introduce a primitive-first, fallback-aware compiler that automatically chooses the
simplest collision representation sufficient for a given task.
```

不要写：

```text
LLM generates accurate primitive colliders.
```

写：

```text
LLM/VLM provides semantic priors and repair decisions; all numeric geometry is optimized
and verified by deterministic tools and Newton simulation.
```

---

## 16. 风险清单与缓解策略

### 16.1 Novelty 风险

**风险**：CPD 2026 已经做 primitive decomposition。  
**缓解**：以 CPD-like 为 baseline，贡献放在 task-aware、Newton verifier、LLM repair、hybrid fallback。

### 16.2 LLM 无效风险

**风险**：LLM 带不来 measurable gain。  
**缓解**：先做 non-LLM baseline；LLM 只在语义和 repair 上引入；必须做 ablation。

### 16.3 性能反噬风险

**风险**：primitive 太多导致 pair/contact count 上升，反而更慢。  
**缓解**：shape budget、pair count penalty、merge step、runtime verifier。

### 16.4 物理行为错误风险

**风险**：几何看似合理，但接触行为错误。  
**缓解**：Newton-in-the-loop，以 task metrics 为主。

### 16.5 精密任务失败风险

**风险**：插入/装配 primitive 不够精确。  
**缓解**：明确 fallback 到 SDF/hydroelastic，不承诺 primitive-only。

### 16.6 资产鲁棒性风险

**风险**：非流形、破面、内部几何干扰 fitting。  
**缓解**：preprocessor + failure classification + user override。

### 16.7 工程维护风险

**风险**：Newton API 变化，SDF/hydroelastic 配置变化。  
**缓解**：通过 adapter 层隔离，引擎版本记录。

---

## 17. Go / No-Go 决策标准

### 17.1 建议 Go 条件

满足以下任意 4 条即可继续：

- 在 50 个资产上自动生成成功率 ≥ 80%；
- primitive-first median step time 比 CoACD 快 ≥ 25%；
- task success 不低于 CoACD 的 95%；
- local fallback ratio median ≤ 15%；
- LLM planner 相比 non-LLM 在 shape count 或 task success 上有 ≥ 5% 改善；
- 人工编辑时间预计减少 ≥ 50%；
- 能生成可读 report 和 USD metadata。

### 17.2 建议 No-Go 条件

出现以下任意 3 条，应调整方向：

- 纯几何 baseline 已经达到 LLM 版本同等效果，LLM 无增益；
- 大多数资产都 fallback 到 CoACD/SDF，primitive-first 覆盖率低；
- primitive count 经常超过 CoACD hull count，性能无优势；
- Newton verifier 结果高度不稳定；
- 精密任务被误纳入 primitive-only，导致严重失败；
- 资产修复需要大量人工，不具备自动化价值。

---

## 18. 推荐最终立项方案

### 18.1 项目定位

```text
不是：自动 primitive 完全替代 convex decomposition
而是：为 Newton 选择“足够好且最便宜”的 collision representation
```

### 18.2 技术命题

```text
Given an asset and task, generate the simplest editable primitive-first collision package
that passes Newton simulation verification; use local fallback when primitive representation
is insufficient.
```

中文：

```text
给定资产和任务，自动生成能够通过 Newton 仿真验证的最简单、可编辑 primitive-first 碰撞包；当 primitive 不足时进行局部 convex/SDF 回退。
```

### 18.3 最小可行产品

MVP 功能：

- 输入 USD/OBJ mesh；
- 输出 Newton primitive shapes；
- 支持 box/sphere/capsule/cylinder/ellipsoid；
- 支持 CoACD fallback；
- 运行 drop / sphere rain / stack verifier；
- 输出 markdown/html report；
- 可视化 overlay。

MVP 不做：

- 精密插入；
- 自定义 primitive 类型；
- 端到端训练；
- 复杂 UI；
- 全自动修复所有失败。

---

## 19. 最终判断

### 19.1 投资价值

**高**。因为它同时具备：

- 真实工程痛点；
- 明确性能收益路径；
- 可产品化；
- 可论文产出；
- 与 Newton / Isaac / OpenUSD 生态契合；
- 与 LLM 工具编排趋势契合。

### 19.2 技术可行性

**中高**。non-LLM primitive baseline 可较快做出；难点在：

- robust segmentation；
- negative space preservation；
- task-aware metrics；
- LLM 增益证明；
- fallback 策略。

### 19.3 科研新颖性

**中到高，取决于 claim**。

- 纯 primitive decomposition：新颖性中等偏低，因为 CPD 已经做了；
- task-aware + Newton verifier + LLM repair + hybrid fallback：新颖性高；
- behavior-level collision proxy compilation：有较好论文空间。

### 19.4 推荐决策

**建议立项，但重命名、重构目标。**

最终推荐：

```text
立项：YES
方向：Primitive-first collision asset compiler for Newton
策略：LLM/VLM-guided + geometry optimization + Newton verification + local fallback
不建议：primitive-only / fully replace convex decomposition
```

---

## 20. 可直接带去评审会的 5 页提纲

### Slide 1：Problem

- 真实资产 mesh 不适合作为 dynamic collision；
- CoACD/V-HACD 自动但产生 hull soup；
- 手工 primitive 好但贵；
- Newton/Isaac/RL 需要低成本、可编辑、可验证 collider。

### Slide 2：Opportunity

- 2026 CPD 证明 primitive decomposition 是前沿；
- 但纯几何 primitive fitting 不懂任务；
- LLM/VLM 可以提供语义和任务规划；
- Newton 可以提供真实仿真 verifier。

### Slide 3：System

```text
Mesh + task → LLM/VLM planner → primitive fitter → Newton verifier → repair/fallback → USD/Newton package
```

### Slide 4：Evaluation

- Baselines：single hull、bounding box、V-HACD、CoACD、CPD-like、SDF、manual；
- Metrics：step time、contact count、task success、jitter、hole clearance、human edit time；
- Tasks：drop、stack、slide、grasp、container、hole、insertion。

### Slide 5：Decision

- Go：3-month prototype；
- No-go：if LLM no gain and primitive baseline not better than CoACD；
- Best claim：primitive-first, fallback-aware, simulation-verified；
- Avoid claim：fully replace convex decomposition。

---

## 21. 参考资料与来源

> 下面列出本报告使用的主要公开资料。建议后续正式论文/白皮书改为 BibTeX 格式。

1. Newton Physics Engine, NVIDIA Developer.  
   https://developer.nvidia.com/newton-physics

2. Newton Adds Contact-Rich Manipulation and Locomotion Capabilities for Industrial Robotics, NVIDIA Technical Blog, 2026-03-16.  
   https://developer.nvidia.com/blog/newton-adds-contact-rich-manipulation-and-locomotion-capabilities-for-industrial-robotics/

3. Newton Physics Documentation, Collisions and Contacts.  
   https://newton-physics.github.io/newton/stable/concepts/collisions.html

4. Newton ModelBuilder API / approximate_meshes documentation.  
   https://newton-physics.github.io/newton/stable/api/_generated/newton.ModelBuilder.html

5. Convex Primitive Decomposition for Collision Detection, Julian Knodt and Xifeng Gao, arXiv:2602.07369, 2026.  
   https://arxiv.org/abs/2602.07369

6. Approximate Convex Decomposition for 3D Meshes with Collision-Aware Concavity and Tree Search, Wei et al., SIGGRAPH 2022, arXiv:2205.02961.  
   https://arxiv.org/abs/2205.02961

7. CoACD project page.  
   https://colin97.github.io/CoACD/

8. CoACD GitHub repository.  
   https://github.com/SarahWeiii/CoACD

9. V-HACD / Unity-Technologies repository.  
   https://github.com/Unity-Technologies/VHACD

10. V-HACD archived original repository.  
    https://github.com/kmammou/v-hacd

11. VisACD: Visibility-Based GPU-Accelerated Approximate Convex Decomposition, arXiv:2604.04244, 2026.  
    https://arxiv.org/abs/2604.04244

12. Learning Convex Decomposition via Feature Fields, arXiv:2603.09285, 2026.  
    https://arxiv.org/abs/2603.09285

13. Empart: Interactive Convex Decomposition for Converting Meshes to Parts, arXiv:2509.22847, 2025.  
    https://arxiv.org/abs/2509.22847

14. PrimitiveAnything: Human-Crafted 3D Primitive Assembly Generation with Auto-Regressive Transformer, arXiv:2505.04622 / SIGGRAPH 2025.  
    https://arxiv.org/abs/2505.04622

15. PrimitiveAnything project page.  
    https://primitiveanything.github.io/

16. MeshLLM: Empowering Large Language Models to Progressively Understand and Generate 3D Mesh, arXiv:2508.01242 / ICCV 2025.  
    https://arxiv.org/abs/2508.01242

17. Residual Primitive Fitting of 3D Shapes with SuperFrusta, arXiv:2512.09201, 2025.  
    https://arxiv.org/abs/2512.09201

18. LLMPhy: Parameter-Identifiable Physical Reasoning Combining Large Language Models and Physics Engines, arXiv:2411.08027v3, 2026.  
    https://arxiv.org/abs/2411.08027

19. ChronoLLM: customizing language models for physics-based simulation code generation, Multibody System Dynamics, 2026.  
    https://link.springer.com/article/10.1007/s11044-026-10152-x

20. MCP-SIM: A self-correcting multi-agent LLM framework for language-based physics simulation and explanation, npj Artificial Intelligence, 2026.  
    https://www.nature.com/articles/s44387-025-00057-z

21. Creation, evaluation and self-validation of simulation models with large language models, Neurocomputing, 2025.  
    https://www.sciencedirect.com/science/article/pii/S092523122502702X

22. Omni Physics Colliders documentation.  
    https://docs.omniverse.nvidia.com/kit/docs/omni_physics/latest/dev_guide/rigid_bodies_articulations/collision.html

23. Omni Physics Simulation Performance Guide.  
    https://docs.omniverse.nvidia.com/kit/docs/omni_physics/latest/dev_guide/guides/physics-performance.html

24. Isaac Lab Simulation Performance and Tuning.  
    https://isaac-sim.github.io/IsaacLab/main/source/how-to/simulation_performance.html

25. Isaac Sim Performance Optimization Handbook.  
    https://docs.isaacsim.omniverse.nvidia.com/6.0.0/reference_material/sim_performance_optimization_handbook.html

26. Unity Manual: Introduction to Mesh Colliders.  
    https://docs.unity3d.com/6000.4/Documentation/Manual/mesh-colliders-introduction.html

27. MuJoCo Changelog: SDF collision primitive.  
    https://mujoco.readthedocs.io/en/stable/changelog.html

28. PhysX 5.4 Geometry Documentation.  
    https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/Geometry.html

---

## 22. 附录 A：建议 Prompt / Contract Schema

### 22.1 LLM Planner Prompt 草案

```text
You are a collision asset planning agent for Newton Physics.
Given a mesh summary, rendered views, and a task description, produce a collision planning contract.
Do not output exact floating point primitive parameters.
Output semantic parts, primitive type priors, fidelity priorities, verification tests, and fallback policy.
Prefer primitive colliders when sufficient; request local convex/SDF fallback when primitives would block holes,
lose contact-critical surfaces, or require too many shapes.
```

### 22.2 JSON Schema 草案

```json
{
  "object_class": "string",
  "task_intent": "string",
  "global_strategy": "primitive_first | convex_first | sdf_first | hybrid",
  "parts": [
    {
      "name": "string",
      "importance": "high | medium | low | visual_only",
      "preferred_primitives": ["box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"],
      "avoid": ["string"],
      "requires_negative_space_preservation": true,
      "expected_contact_role": "support | grasp | rolling | blocking | container | none"
    }
  ],
  "budget": {
    "max_primitives": 16,
    "max_fallback_components": 2,
    "max_fallback_surface_ratio": 0.15
  },
  "verification_tests": ["drop", "stack", "grasp"],
  "fallback_policy": {
    "allowed": ["convex_hull", "coacd", "sdf"],
    "prefer_local_fallback": true
  }
}
```

---

## 23. 附录 B：Failure Taxonomy

| Code | Name | Description | Auto Repair |
|---|---|---|---|
| F01 | HoleBlocked | primitive union blocks a required opening | split / shrink / local fallback |
| F02 | UnderCovered | collision proxy misses solid region | add primitive / expand |
| F03 | OverCovered | too much excess volume | split / change type |
| F04 | TooManyShapes | primitive count exceeds budget | merge / coarsen / fallback convex |
| F05 | SlowNarrowPhase | runtime worse than baseline | simplify / remove cylinders / merge |
| F06 | ContactJitter | unstable contact normals/counts | smooth primitive choice / reduce contacts |
| F07 | GraspFail | gripper cannot establish stable contact | refine contact surfaces |
| F08 | StackFail | support plane inaccurate | add/resize support primitive |
| F09 | InsertionFail | primitive cannot represent tolerance | SDF/hydroelastic fallback |
| F10 | FilterError | self-collision or parent-child issue | repair collision filters |
| F11 | InertiaMismatch | collision proxy changes inertia assumptions | recompute or separate mass source |
| F12 | NonDeterministic | repeated generation differs too much | seed / deterministic optimizer |

---

## 24. 附录 C：最小实验表格模板

```markdown
| Asset | Task | Method | #Shapes | #Fallback | Step ms | Contacts p95 | Task Success | FP Occ | FN Occ | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| chair_01 | stack | CoACD | 28 | 0 | 1.20 | 64 | 0.96 | 0.08 | 0.01 | baseline |
| chair_01 | stack | Primitive-first | 9 | 0 | 0.58 | 18 | 0.95 | 0.10 | 0.02 | good |
| mug_04 | container | CoACD | 18 | 0 | 0.88 | 44 | 0.91 | 0.04 | 0.02 | ok |
| mug_04 | container | Primitive-first | 7 | 1 SDF | 0.73 | 31 | 0.93 | 0.03 | 0.01 | local fallback |
```

---

## 25. 附录 D：给管理层的最终建议

### 建议投入

- **短期投入**：2 人 × 4 周，做 non-LLM baseline + Newton verifier；
- **中期投入**：3～4 人 × 12 周，做 LLM/VLM planner + repair + fallback；
- **长期投入**：5～6 人 × 6 个月，做产品化和论文。

### 人员配置

| 角色 | 人数 | 任务 |
|---|---:|---|
| Geometry engineer | 1 | primitive fitting / mesh preprocessing |
| Newton/physics engineer | 1 | verifier / performance / API integration |
| ML/LLM engineer | 1 | planner / repair / ablation |
| Robotics benchmark engineer | 0.5～1 | tasks / datasets / metrics |
| Product/UX engineer | 0.5 | visualization / report / USD export |

### 最推荐的第一步

不要先训练模型。先做：

```text
CPD-like primitive baseline + Newton benchmark harness + CoACD/V-HACD comparison
```

一旦确认 primitive-first 在 Newton 上确实有稳定收益，再引入 LLM/VLM 做语义规划和 repair。

---

