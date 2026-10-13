# Notes: multi-agent pipeline patterns + Minecraft/Blockbench agent tooling
Researched 2026-10-13 via Ollama web_search/web_fetch (+ Arctic Shift / YouTube helpers). Raw fetches in `research/agents_pat/`.
Tags: [V] verified from primary source fetched today; [C] corroborated by secondary source(s) / community; [?] uncertain, unverified, or extrapolated.

---------------------------------------------------------------------------------------------------
## PART A. Evidence on multi-agent design (2024-2026)

### A1. When multi-agent helps vs hurts (empirical)

**Google Research/MIT, "Towards a Science of Scaling Agent Systems" (arXiv 2512.08296, Dec 2025)** [V] https://arxiv.org/html/2512.08296
- 260 configs, 6 agentic benchmarks, 5 architectures (single, independent, centralized, decentralized, hybrid), 3 LLM families; standardized tools/prompts/compute.
- MAS relative to single agent ranges **+80.8% (decomposable financial reasoning, centralized)** to **-70% (sequential planning, independent)**.
- **Capability ceiling**: once single-agent accuracy > ~45%, adding agents gives negative returns (beta=-0.236, p=0.004).
- **Tool-coordination trade-off**: tool-heavy tasks (16-tool workflows) pay multi-agent overhead (beta=-0.096, p=0.002).
- **Error amplification**: independent (no central check) agents amplify trace-level errors **17.2x**; centralized coordination with a validation bottleneck contains it to **4.4x**.
- SWE-bench Verified: all MAS variants slightly worse than SAS (-15% to -2%). **PlanCraft (a Minecraft crafting-planning benchmark!) degraded under every MAS variant (-70% to -39%)** because of strong sequential dependencies.
- Predictive model picks best architecture for 87% of held-out configs.
- => Implication: parallelize only *decomposable, low-interdependence* work; keep sequential, stateful work (e.g., a datapack state machine, a boss fight script) in one agent; always put a central verifier before aggregation.

**Salesforce et al., "The Illusion of Multi-Agent Advantage"** [V] https://multi-agent-eval.github.io/
- Six automatic-MAS frameworks (DyLAN, MAS-Zero, ADAS, AFlow, MaAS, MAS-Orchestra) vs CoT + self-consistency on GPQA-Diamond, HLE-Math, SWE-Bench Lite, BrowseComp-Plus with GPT-4o/GPT-5/GPT-OSS-120B/Gemini-2.5-Pro.
- Automatic-MAS **consistently underperform CoT-SC at up to 10x the cost**; complex auto-generated graphs collapse into ensembling loops ("architectural bloat").
- Orchestration does **not** lift mid-tier models to frontier level; single GPT-5 with CoT-SC beat GPT-4o-based ADAS/AFlow using < half the tokens.
- **Expert-architected MAS** beat automatic-MAS when the task truly has decomposition/context separation/parallelism.
- => Hand-design the pipeline; don't use auto-generated agent graphs; cheap models don't become good via orchestration.

**Anthropic, "How we built our multi-agent research system" (Jun 13 2025)** [V] https://www.anthropic.com/engineering/multi-agent-research-system
- Opus 4 lead + Sonnet 4 subagents beat single Opus 4 by **90.2%** on internal research eval; wins on *breadth-first* parallel queries.
- Token usage alone explains **80%** of BrowseComp variance (tokens + tool calls + model = 95%). Multi-agent works largely by spending more tokens in separate context windows.
- Cost: agents ~**4x** tokens of chat; multi-agent ~**15x**. "Most coding tasks involve fewer truly parallelizable tasks than research."
- Eval lessons: start with ~20 real queries; a **single LLM-judge call with one rubric prompt (0.0-1.0 + pass/fail)** was more consistent than multiple judges; for stateful agents evaluate **end state**, broken into checkpoints; rainbow deployments; synchronous subagents are a bottleneck.

**Cognition (Devin), "Don't Build Multi-Agents" (Jun 12 2025)** [V] https://cognition.com/blog/dont-build-multi-agents and **"Multi-Agents: What's Actually Working" (Apr 22 2026)** [V] https://cognition.com/blog/multi-agents-working
- Principles: share full context; "actions carry implicit decisions" -> parallel *writers* conflict.
- 2026 update: what works is **"writes stay single-threaded; extra agents contribute intelligence, not actions."**
  1. Code-review loop: Devin Review finds ~2 bugs/PR on Devin-written PRs, ~58% severe. Works **best when reviewer shares NO context with the coder** (clean context avoids context rot; reviewer reasons backward from the diff). Need a filter step where the coder (with full user context) triages reviewer findings to avoid loops/scope creep.
  2. "Smart friend": cheap primary model consults an expensive model. Failed with a weak primary (SWE-1.5) - weak models don't know when to escalate; **worked across frontier models (Claude + GPT together in production)** as a *capability router* (some debug better, some do visual reasoning better, some write tests better). Share a fork of full context; ask broad questions.
  3. Manager Devin -> child Devins via internal MCP: managers over-prescribe; agents wrongly assume shared state; cross-agent messages don't happen by default. Practical shape = **map-reduce-and-manage**, not swarms.
- Notes that showcase swarm projects (200k-LOC browser, 100k-LOC C compiler) all had "a simple, verifiable success criterion"; real software needs scaled human taste.

**Berkeley, "Why Do Multi-Agent LLM Systems Fail?" MAST (NeurIPS 2025 D&B; arXiv 2503.13657)** [V] https://arxiv.org/html/2503.13657 ; code/data https://github.com/multi-agent-systems-failure-taxonomy/MAST
- 1,642 traces across 7 MAS frameworks; 14 failure modes in 3 categories; human IAA kappa=0.88; o1 few-shot LLM annotator accuracy 94%, kappa 0.77 (`pip install agentdash`).
- FC1 System design: disobey task spec 11.8%, disobey role 1.5%, **step repetition 15.7%**, context loss 2.8%, **unaware of termination 12.4%**.
- FC2 Inter-agent misalignment: conversation reset 2.2%, proceed on wrong assumptions instead of asking 6.8%, derailment 7.4%, withholding info 0.85%, ignoring other agents 1.9%, **reasoning-action mismatch 13.2%**.
- FC3 Task verification: premature termination 6.2%, **no/incomplete verification 8.2%, incorrect verification 9.1%**. Example: ChatDev chess program compiles but breaks rules -> superficial checks are not verification.
- A workflow fix (CEO gets final say) gave +9.4% on ChatDev.
- => Every agent needs explicit termination criteria, explicit role spec, "ask instead of assume" escalation, and *real* (behavioral, in-game) verification.

**Choi/Zhu/Li, "Debate or Vote" (NeurIPS 2025 spotlight; arXiv 2508.17536)** [V] https://arxiv.org/html/2508.17536
- Across 7 NLP benchmarks, **majority voting alone accounts for most of multi-agent-debate gains**; debate alone is a martingale (doesn't improve expected correctness) unless biased toward correction.
- => Prefer independent samples + vote/verify over chatty debate rounds.

### A2. Cross-model / heterogeneous review evidence

- **Vallecillos-Ruiz/Hort/Moonen (Simula), "Wisdom and Delusion of LLM Ensembles for Code Generation and Repair" (arXiv 2510.21513, 2026)** [V] https://arxiv.org/html/2510.21513 - 10 LLMs/5 families: ensemble *upper bound* up to **+83%** over best single model (Defects4J 112->205); **consensus selection falls into a "popularity trap"** (models fail the same way); **diversity-based selection** realizes up to 95% of potential, even with 2-model ensembles. Models from different families add more unique solutions.
- **Nogueira et al., "Evaluating Failure Independence in LLM-Generated Code" (arXiv 2607.02808, Jul 2026)** [V] https://www.emergentmind.com/papers/2607.02808 - 12 models, 224 problems, 5 languages: implementations from different models are more diverse but **still fail on the same tests far more than independence predicts**; 3- and 5-version majority voting realize only **0.43-0.44** of independent-failure gain, **<0.3 when same model**. Heterogeneous models help *partially*.
- **Z. Clement blog (Jun-Aug 2026)** [C] https://www.zacharyclement.com/posts/code_reviewing_performance/ - MBPP+: reviewer = same model as generator ("concordant") had significantly lower bug recall (coef -0.385, p=0.001); persona prompts had about half that effect. Overall reviewer recall only 12%; reviews rarely flipped working/broken; author says **test-driven development** matters more than model diversity. Small study, model names unverifiable [?].
- **"Council pattern" practitioner audit (cgaravito.dev, 2026)** [C] https://cgaravito.dev/en/blog/council-of-advisors-multi-model-code-auditing - 4 models (Opus 4.6, Sonnet 4.5, Gemini 3 Pro, Kimi K2.5) on 5k LOC: 84 findings -> 15 unique; each model 2-5 unique findings; cheapest (Kimi, $0.04) found a critical SSRF others missed; total $1.20. A 5th model deduped. Single anecdote.
- Cognition 2026: Claude+GPT cross-frontier "smart friend" worked in production as a capability router [V, above].
- **Synthesis**: heterogeneous review gives *real but partial* gains (errors are correlated). Use it as a cheap recall booster on reviews (union of findings, triaged by the owner agent), not as majority-vote correctness. Deterministic tests remain the strongest gate.

### A3. Long-horizon reliability (METR)

- **METR time horizons** [V] https://metr.org/time-horizons/ (page "no longer actively updated" as of Sep 8 2026); TH1.1 release Jan 29 2026 [V] https://metr.substack.com/p/2026-1-29-time-horizon-1-1 : 228 tasks (31 are 8h+, only 5 with human baselines); doubling ~196 days overall, **~131 days since 2023** under TH1.1.
- Data points (via tracker sites, [C]) https://exponentialtracker.com/curve/ai_metr , https://agitracker.io/blog/metr-time-horizons-2026/ : GPT-5 ~3.4h; Opus 4.5 ~4.9h; GPT-5.2 ~5.9h; **Opus 4.6 ~12h (Feb 2026)**; **Claude Mythos Preview ~17.4h at 50% (CI 8.5-55h), ~3h06m at 80% (Apr 2026)** - beyond what the suite measures reliably (>16h).
- Caveats from METR itself: tasks are clean, self-contained, auto-scored software tasks; **agents do worse on "messier" tasks**; at ~2h horizon a model reliably solves ~1/3 of 2h tasks, never ~1/3, sometimes ~1/3.
- **METR "Algorithmic vs Holistic Evaluation" (Aug 13 2025)** [V-search] https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/ - agents' functionally correct code often not usable as-is (tests, docs, quality).
- **METR "Many SWE-bench-passing PRs would not be merged" (Mar 10 2026)** [V] https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/ - ~half of test-passing PRs (mid-2024 to late-2025 agents) would be rejected by maintainers; maintainer merge rate ~24 pp below automated grader.
- **METR dev-productivity**: 2025 RCT found ~19-20% slowdown; Feb 24 2026 update says that finding is outdated, speedups now likely but design changed [V-search] https://metr.org/blog/2026-02-24-uplift-update/
- => Size each agent task well inside the **80%** horizon (minutes-to-few-hours of human-equivalent work), with explicit acceptance tests; "passes tests" != "acceptable" — keep a human/taste gate for content.

### A4. Harness patterns from Anthropic engineering (2024-2026)

- **Building effective agents (Dec 19 2024)** [V-search] https://www.anthropic.com/engineering/building-effective-agents - workflows: prompt chaining, routing, parallelization (sectioning/voting), **orchestrator-workers**, **evaluator-optimizer**; "find the simplest solution possible, only increase complexity when needed."
- **Effective harnesses for long-running agents (Nov 26 2025)** [V-search] https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents - initializer agent writes feature list (all failing) + progress file + init script; coding agent does **one feature per session**, commits to git, updates progress file; end-to-end testing (browser automation) before marking done.
- **Harness design for long-running application development (Mar 24 2026)** [V] https://www.anthropic.com/engineering/harness-design-long-running-apps
  - GAN-like **planner -> generator -> evaluator**. Self-evaluation is lenient ("confidently praising mediocre work"); **tuning a separate skeptical evaluator is far more tractable** than making the generator self-critical.
  - Subjective quality made gradable via **explicit rubric** (design quality, originality, craft, functionality) + **few-shot calibrated score examples**; evaluator uses **Playwright MCP to interact with the live app + screenshots** (analogue for us: drive the Minecraft client and screenshot).
  - **Sprint contracts**: before coding, generator proposes "what done means + how verified"; evaluator reviews; iterate until agreed. **Communication via files.** Hard thresholds per criterion -> sprint fails.
  - Out of the box "Claude is a poor QA agent" — it found issues then talked itself into approving; fix = read evaluator logs, find divergence from human judgement, update QA prompt, several rounds.
  - Costs: retro game maker solo 20 min/$9 vs full harness 6h/$200 (>20x) with far better result. Opus 4.6 version (DAW): 3h50m/$124.70; QA rounds only ~$3-4 each; builder dominated cost.
  - **"Every component in a harness encodes an assumption about what the model can't do"** — ablate one component at a time; re-simplify on each model upgrade. Evaluator worth its cost **only for tasks beyond what the model does reliably solo**.
  - Criteria wording steers outputs ("museum quality" caused convergence); sometimes a middle iteration was best -> keep all iterations, human picks.
- **anthropics/cwc-long-running-agents** (Code with Claude 2026 take-home; 668 stars; "not maintained") [V] https://github.com/anthropics/cwc-long-running-agents
  - Three primitives: **Default-FAIL contract** (`test-results.json` rows start false; PreToolUse hook denies writing it unless the agent has Read an evidence file: screenshot/log), **fresh-context evaluator** subagent with no Write/Edit returning PASS/NEEDS_WORK, **agent-maintained handoff** (PROGRESS.md + commit-on-stop hook). Built-in `/goal` command = generator/evaluator loop with fast model checking a completion condition.

### A5. LLM-as-judge / VLM-as-judge reliability (relevant for art & visual QA gates)

- General: position bias and self-preference bias are well documented — "Judging the Judges: Position Bias in LLM-as-a-Judge" (IJCNLP-AACL 2025) https://aclanthology.org/2025.ijcnlp-long.18.pdf ; "Beyond the Surface: Measuring Self-Preference in LLM Judgments" (EMNLP 2025) https://aclanthology.org/2025.emnlp-main.86.pdf ; "Do LLM Evaluators Prefer Themselves for a Reason?" https://arxiv.org/abs/2504.03846 ; survey https://arxiv.org/html/2411.15594v6 [C - search snippets only].
- **Cross-model VLM-judge protocol for 3D mesh quality (Transformer Lab, arXiv 2606.18451, Jun 2026)** [V] https://arxiv.org/html/2606.18451 - fixed **24-view headless render rig**, **two independent VLM judge families**, **mandatory position-bias correction (query both orders, keep only order-consistent verdicts)**; inter-family agreement kappa=0.66. Cheap proxies (render-CLIP) were at chance; geometry-validity only a weak, bimodal signal (catches visible geometric defects, not subtle quality).
- **3D-DefectBench (Roblox/Berkeley/Stanford, arXiv 2607.10826, Jul 2026)** [V] https://arxiv.org/html/2607.10826v1 - 9 binary defect types (geometry, texture, prompt adherence), 84 pipeline designs: **model choice dominates** agreement with humans; a **compact 6-view RGB** protocol is as good as denser views or depth/normal channels; **best of 12 VLMs still trails trained human labelers; texture-defect agreement drops sharply** on noisier labels.
- **Anthropic harness (Mar 2026)**: evaluator calibrated with few-shot scored examples + explicit rubric; still lenient by default; needs several prompt-tuning rounds against human judgement [V].
- **Anthropic research system**: single judge call with one rubric worked better than multiple judges [V].
- => For this project: VLM judges are fine as a **triage/regression filter** (e.g., "is the model's silhouette broken / texture missing / z-fighting / T-pose") using a fixed multi-view render rig and both-order comparisons across 2 model families, but **cannot be the final quality gate for pixel-art texture or animation feel** — a human art director owns that.

### A6. Spec-driven development and contracts

- **GitHub Spec Kit** (MIT, ~133k stars, created Aug 2025) [V-search] https://github.com/github/spec-kit ; docs https://github.github.com/spec-kit/ - `/speckit.constitution -> specify -> clarify -> plan -> tasks -> analyze -> implement`; spec has prioritized user stories each with an **independent acceptance test**, `FR-xxx` MUST/SHOULD requirements; tasks marked `[P]` are parallel-safe.
- Practitioner report (Duonary, Aug 21 2026) [C] https://duonary.com/blog/github-spec-kit-in-practice-spec-driven-development/ : review moved upstream (200-line spec > 40-file diff); `/clarify` caught two requirement bugs in 90s; `[P]` tasks let two agents in two worktrees merge without conflicts; **constitution is advisory — the model drifted from it in a long implement run; nothing enforces it mechanically** -> keep a human checklist item; ~30-45 min overhead per feature, pays off for anything >3 files; keep spec alive (update spec first, rerun plan/tasks).
- Anthropic "sprint contract" negotiated between generator and evaluator before work [V, A4].
- MAST: most failures are spec/role/termination/verification problems, i.e., contract problems [V, A1].
- Handoff/contract blog patterns (typed handoff artifacts, JSON schemas) [C, generic]: https://agentpatterns.ai/patterns/multi-agent/agent-handoff-protocols/ , https://www.pandastack.ai/blog/how-to-hand-off-work-between-ai-agents/

### A7. Game-dev specific agent research (2025-2026)

- **OpenGame (CUHK MMLab, arXiv 2604.18394, Apr 2026)** [V] https://arxiv.org/abs/2604.18394 - agentic web-game creation; frontier agents "stumble" on full games via (1) logical incoherence of global state, (2) broken event wiring, (3) **cross-file inconsistencies (mismatched asset keys, scene wiring, init order)**. Fixes: **Template Skill** (library of verified project skeletons) + **Debug Skill** (a *living protocol of verified fixes* updated from build/test/runtime outcomes); verification via headless browser build/test + **VLM judge** for visual usability + per-requirement intent verdicts (OpenGame-Bench: Build Health / Visual Usability / Intent Alignment).
  - => Directly transferable: keep a `debug_protocol.md` of verified Minecraft/NeoForge/KubeJS/GeckoLib fixes that agents must read and append to; keep template skeletons (entity + GeckoLib renderer + model + animation controller; datapack function layout; KubeJS event script).
- **AutoUE (ACL Findings 2026; arXiv 2603.07106)** [V] https://arxiv.org/html/2603.07106 - multi-agent UE game generation (model retrieval, scene, gameplay code, auto play-test); **RAG over engine tool docs to curb tool-use hallucination**; injecting design patterns raised PCG node/pin success from 79.6%/64.0% to 100%.
  - => Give agents version-pinned docs (NeoForge 1.21.1, GeckoLib 4.x, Epic Fight, KubeJS 2101) via retrieval/skills rather than relying on training memory.
- **TITAN (NetEase Fuxi/ZJU/SMU, arXiv 2509.22170)** [V] https://arxiv.org/pdf/2509.22170 - LLM MMORPG testing agent: state abstraction, action prioritization, trace memory + reflection, LLM bug oracles; 95% task completion vs 82% best baseline; 15 vs 9 bugs; 4 previously unknown bugs; deployed in 8 real QA pipelines. Reflection module mattered most.
- Others (search-level [C]): "Towards LLM-Based Automatic Playtest" (FSE 2025) https://arxiv.org/html/2507.09490v1 ; SAGE gray-box regression testing https://export.arxiv.org/pdf/2512.00560 ; "LLMs May Not Be Human-Level Players, But They Can Be Testers" (difficulty measurement, PACM HCI) https://dl.acm.org/doi/10.1145/3748634 ; RPGAgent (CHI 2026) story-to-play https://dl.acm.org/doi/10.1145/3772318.3790326
- Minecraft agent benchmarks: **MineAnyBuild** (NeurIPS 2025 D&B, spatial planning for building) https://mineanybuild.github.io/ ; **MineCollab/Mindcraft** (multi-agent embodied collaboration, Mineflayer-based; repo ~5.9k stars) https://mindcraft-minecollab.github.io/ , https://github.com/mindcraft-bots/mindcraft ; PlanCraft degraded under MAS (A1).
- Community reality check (r/MinecraftCommands 2026) [C]: LLMs still hallucinate version-specific command/NBT/component syntax and non-existent scoreboards/teams; "good for small packs with 4-5 functions, not to standard"; best results when the tool can inspect existing objectives/entities first. https://www.reddit.com/r/MinecraftCommands/comments/1wwdw7q/ , https://www.reddit.com/r/MinecraftCommands/comments/1ud7lin/

### A8. Ops: observability, budgets, recovery (generic)

- OpenTelemetry **GenAI semantic conventions** incl. agent spans — status **Development** (moved to its own repo) [V-search] https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md
- **Langfuse** (OSS, self-hostable via Docker) — "Tracing coding agents" guide; Claude Code observability plugin (May 2026) [V-search] https://langfuse.com/resources/engineering/coding-agent-tracing , https://docs.langfuse.com/self-hosting , https://github.com/langfuse/Claude-Observability-Plugin
- Budget guardrails: per-run token caps, step/tool-call/error limits, gateway budgets ("circuit breaker") [C, blog-level] https://ctxwire.com/articles/token-budgets-circuit-breakers-agents/ , https://www.agentnative.dev/patterns/cost-guardrail-pattern-for-agent-platforms
- Anthropic: rainbow deploys for long-running agents; resume from checkpoints rather than restart; git commits as recovery points [V, A1/A4].

---------------------------------------------------------------------------------------------------
## PART B. Domain tooling that lets agents build and verify Minecraft content

### B1. Blockbench agent tooling

**jasonjgardner/blockbench-mcp-plugin** — the de-facto Blockbench MCP. [V] https://github.com/jasonjgardner/blockbench-mcp-plugin ; API ref https://jasonjgardner.github.io/blockbench-mcp-plugin/ ; releases https://github.com/jasonjgardner/blockbench-mcp-plugin/releases
- GPL-3.0; ~513 stars; very active: v1.8.0 (Sep 20 2026: 109->140 tools, GeckoLib support, AI Scratchpad mode, AI-usage stamping, 839 tests, **requires Blockbench >= 5.0**), v1.9.0 (Sep 24 2026: **headless server**), v1.10.0 (**Oct 1 2026**: loopback-only + cross-site rejection hardening, many tool fixes).
- **Desktop plugin (HTTP, default `:3000/bb-mcp`)**: ~157 tools/resources/prompts in v1.10 reference, incl.:
  - Modeling: place/modify cube, knife cut, mesh tools (extrude, subdivide, loop cut...), groups/outline, armatures + vertex weights + IK, display transforms.
  - UV: `get_cube_uv`/`set_cube_uv` (**per-face rectangles, rotation, box-UV offset/mirror; "does not pack islands or repaint textures"**), mesh UV tools.
  - Texturing: brush/fill/gradient/eraser, layers, `create_texture`, PBR material (Bedrock MER-style texture sets; *not* LabPBR channel packing).
  - Animation: create_animation, keyframes, graph editor, timeline, batch keyframe ops, Molang vars.
  - **GeckoLib**: `geckolib_set_project_settings`, easing get/set/reverse, **`geckolib_validate_model`** (bone-name charset/duplicates, mod/object ID validity, armor template bones, texture size vs UV, animation loop/easing/length checks; "passing does not prove in-game correctness"), `geckolib_export_model/animations/display`.
  - Visual inspection: `create_offscreen_view` (up to 4, no AA option for crisp pixel art), `set_camera_angle`, `capture_screenshot`, `get_average_fps`.
  - Safety/recovery: `save_checkpoint` + undo stack; validator resources (errors/warnings); `risky_eval` (arbitrary JS — gate it), `emulate_clicks`, `fill_dialog`, `trigger_action` (can drive *other plugins' actions*, e.g., Animated Java export [?]).
  - Projects touched are stamped with Blockbench-native `ai_used`/`ai_agents` properties.
- **Headless `.bbmodel` MCP (stdio)**: `npx -y github:jasonjgardner/blockbench-mcp-plugin --root ./models` (or bunx); **each agent gets its own process -> parallel agents**; optimistic concurrency (`expected_revision`), atomic writes, lock files. [V] https://github.com/jasonjgardner/blockbench-mcp-plugin/blob/main/headless/README.md
  - Tools: info/outline/find/get_node/list textures/animations; **`bbmodel_sample_pose`** (evaluate an animation at time t -> bone positions/bounds); create/edit (batch atomic: groups, cubes, face UVs, textures incl. emissive render_mode, PBR, animations/keyframes, locators, particles); meshes (free format only); **`bbmodel_validate`** (broken outliner, slivers, block-size limits, floating parts, interpenetration, broken L/R symmetry, GeckoLib rules; `self_test` proves each check fires); **`bbmodel_validate_animations`** (parts sinking into ground, limbs detaching); export Bedrock geo, Java block/item JSON in/out, Modded Entity Java class; **`bbmodel_render` / `bbmodel_contact_sheet`** (WebGPU, needs Node >= 23.6 + GPU; optional full bb-render for video/path tracing); `blockbench_launch`.
  - Format rules enforced (java_block cubes in -16..32, allowed rotations, etc.). Limit: Blockbench doesn't hot-reload files changed on disk — don't edit the same file in app and headless simultaneously.
- Companion **skills repo** jasonjgardner/blockbench-mcp-project (Claude Code skills + Codex plugin marketplace: `codex plugin marketplace add jasonjgardner/blockbench-mcp-project --ref codex`) [V] https://github.com/jasonjgardner/blockbench-mcp-project
- Registration: `claude mcp add blockbench --transport http http://localhost:3000/bb-mcp` ; `codex mcp add blockbench --url http://localhost:3000/bb-mcp` ; headless via stdio.
- Animated Java: no dedicated AJ tools found; AJ uses its own `.ajblueprint` format inside Blockbench — agents could only drive it via generic `trigger_action`/`risky_eval` [?]. Treat AJ cutscenes as human-led.

Other Blockbench MCPs (smaller, newer) [V-search]:
- `@adhisang/minecraft-blockbench-mcp` v0.3.0 (Sep 28 2026; MIT) — stdio adapter + desktop plugin over loopback WS; Java block/item + **GeckoLib** formats; every op executed by Blockbench APIs with undo. https://www.npmjs.com/package/@adhisang/minecraft-blockbench-mcp
- Mishaadevv/blockbench-mcp (tested on BB 5.2.1; contact sheets, validation, export to many codecs, arbitrary JS) https://glama.ai/mcp/servers/Mishaadevv/blockbench-mcp
- RenasDemirbas/BlockBenchMCP (Oct 2026, BB 5.2) — r/Blockbench post got **strong community backlash** (top comments hostile) https://www.reddit.com/r/Blockbench/comments/1x1welt/
- enfp-dev-studio/blockbench-mcp (28 stars), sosadly, SwagRee, illia3 (0 stars) — not recommended.

Headless/CLI Blockbench:
- **No official headless CLI**. Issue #1764 (CLI conversion) open since 2023 https://github.com/JannisX11/blockbench/issues/1764 ; PR #2667 "Improved CLI" (`--hidden`, `--install-plugins`, terminal logging) **open, labeled stale** (updated Sep 2026) https://github.com/JannisX11/blockbench/pull/2667 [V]
- Programmatic `.bbmodel`: JSON format documented https://www.blockbench.net/wiki/docs/bbmodel/ ; community spec gist https://gist.github.com/mgerhardy/48adb8a9ccaa2079779ac38a4324fa8e ; `bbmodel-rs` (Rust serde) https://docs.rs/bbmodel-rs/latest/bbmodel_rs/ ; **the jasonjgardner headless server is the practical validator/renderer**.

AI 3D -> Blockbench:
- **BlockSmith** (gbusto, MIT, ~10 stars) text/image -> true-cube models; exports GLB/GLTF/**.bbmodel**/BlockJSON/Python DSL; `animate`, `link`, `convert` (GLB<->bbmodel) [V] https://github.com/gbusto/blocksmith
- Meshy "Minecraft model maker" — blocky low-poly meshes + PBR maps; explicitly notes meshes can't be saved as Java/Bedrock cuboid models directly (needs voxelize/rebuild) [V] https://www.meshy.ai/use-cases/free-game-assets/minecraft
- Tripo "Stylize: Minecraft/voxel", Hunyuan3D: generic mesh generators [C]. Voxify3D (CVPR 2026) noted by modeling agent.
- => Use as *concept/blockout reference only*; production cuboid models with clean per-face UV need a human modeler (agent helps with UV templates, mirroring, validation).

### B2. Minecraft runtime control / playtesting

Key constraint [V]: **Mineflayer cannot join a NeoForge server** ("You are trying to connect to a server that is running NeoForge..."; mineflayer issue #4097 open, Sep 2026; workaround = node-minecraft-protocol-forge PR, untested for 1.21.1+heavy mods) https://github.com/PrismarineJS/mineflayer/issues/4097 . Azalea-lab shows a Rust bot on NeoForge 1.21.1 only via **three server-side patches disabling NeoForge negotiation** — and a protocol bot still can't experience client-side mods (Epic Fight animations, GeckoLib rendering, Iris). https://github.com/TargetedEntropy/azalea-lab
=> Mineflayer-based MCPs (yuniko-software/minecraft-mcp-server ~780 stars, supports 1.21.11 only; Mindcraft) are **not suitable** for this modded map's QA. Use **in-client mod bridges** instead:

- **langyo/minecraft-mod-mcp** (Apache/MIT/CC0; ~41 stars; single maintainer; very active: v0.4.4 Oct 12 2026) — in-game mod + `npx minecraft-mod-mcp` stdio bridge; **46 tools**: screenshots with coordinate grids, click/type/scroll/drag/keys, run commands, player/world/screen info, SSE event stream; `launch_minecraft` can download+launch a client. **Release assets include `minecraft-mcp-1.21.1-neoforge-v0.4.4.jar`** [V]. Linux: works under Xvfb. https://github.com/langyo/minecraft-mod-mcp , https://github.com/langyo/minecraft-mod-mcp/blob/master/docs/guides/en/AI-TOOLS.md
- **mcdev-mcp** (use-ai-for-mc; ~16 stars) — static: decompiled MC source search/call graph (Vineflower; 1.14-1.21.x with Mojang mappings, 26.x) — useful for coding agents on 1.21.1 [V]; runtime half needs **DebugBridge, which is Fabric-only (1.19, 1.21.11, 26.1, 26.2)** -> not usable on NeoForge 1.21.1 [V]. Its tool design (snapshot, nearby entities, `mc_record_video` multi-frame contact sheet for animation glitches, glow markers, Groovy exec) is a good **spec for your own small NeoForge debug-bridge** [?]. https://github.com/use-ai-for-mc/mcdev-mcp , https://github.com/use-ai-for-mc/debugbridge
- ArclightPowered/minecraft-mcp (client mod JSON-RPC, 2 stars), chapmanjw Fabric MCP (8 stars) — minor.
- **minecraft-skills** (sya-ri; npm `@minecraft-skills/mcp`) — version-aware facts/command trees for agents, but covers Java **26.3/26.2/1.21.11** only, not 1.21.1 [V] https://github.com/sya-ri/minecraft-skills ; minecode-mcp (wiki/changelog lookup) https://github.com/AnCarsenat/minecode-mcp [C]
- Anthropic Code with Claude 2026 "Claude Plays Minecraft" workshop bot (mineflayer + HTTP seam, vanilla) [C, 404 on fetch] https://github.com/anthropics/cwc-workshops

### B3. Deterministic gates: build, tests, CI

- **NeoForge GameTest (1.21.1)** [V] https://docs.neoforged.net/docs/1.21.1/misc/gametest - `@GameTest` methods on structure templates; `succeed/succeedIf/succeedWhen/succeedOnTickWhen`, scheduling, assertions; `@GameTestGenerator`; `/test runall|runthese|runfailed`; **`gradlew runGameTestServer` returns exit code = number of failed required tests** (CI-friendly); NeoGradle needs `setForceExit false`; `neoforge.enabledGameTestNamespaces`. NeoForge also has a richer internal **TestFramework** https://github.com/neoforged/NeoForge/blob/11b0a67c/docs/TESTFRAMEWORK.md . Official MDK template: NeoForgeMDKs/MDK-1.21.1-ModDevGradle (CI build workflow) [C].
  - What to test: boss phase transitions, damage numbers, stamina/poise, loot tables, arena triggers, KubeJS-registered events (if callable), structure placement, entity spawns/despawns, cooldowns.
- **HeadlessMC + MC-Runtime-Test** (headlesshq; MIT) [V] https://github.com/headlesshq/mc-runtime-test , https://headlesshq.github.io/headlessmc/dev-ci-cd/ - GitHub Action runs the **real client** in CI under Xvfb (1.21-1.21.11 NeoForge supported), joins a SP world, waits for chunks, quits; runs `/test runall`; `-DMcRuntimeGameTestMinExpectedGameTests=N`; caveat: "Forge and NeoForge GameTest discovery may require additional setup/hacks". Catches client-only crashes (renderer, mixin conflicts, missing models/textures).
- **Datapacks**: 
  - Spyglass (Datapack Helper Plus) — VS Code language server; `spyglassmc.analyzeProject` lints whole project; npm `@spyglassmc/language-server` 0.4.69 (Sep 2026); **no official CLI** (only `@spyglassmc/mcdoc-cli`) [V]. https://spyglassmc.com/user/commands.html
  - **mecha / beet** (Python) CLI + GitHub Action `mcbeet/check-commands` — parses functions against version command trees (mecha updated to 1.21.10/1.21.11 Dec 2025, 26.1 Mar 2026, beet 26.2 Jun 2026; supports older versions via `minecraft:` input) [V]. Limitation: **doesn't know modded commands** (Epic Fight, KubeJS-registered) [?].
  - Ground truth: **boot a dedicated NeoForge 1.21.1 server with all mods + datapack and fail CI on any "Failed to load function / Couldn't parse / Unknown registry" log line** (real dispatcher incl. modded commands) [recommendation].
  - Packwright MCP (validates with real dispatcher + client capture) — **26.2 only**, so not usable, but a good design reference [V] https://github.com/rithwikbabu/packwright-mcp
- **KubeJS**: KubeJS NeoForge **2101.7.2-build.377** (CurseForge, Sep 9 2026) [V-search]. **ProbeJS v8** (default branch 1.21; CurseForge last update Jun 23 2026) dumps tsgo/TypeScript-native-compatible typings and explicitly targets "agents and LLMs ... generate 100% correct KubeJS code" [V] https://github.com/Prunoideae/ProbeJS/ -> gate: run TypeScript type-check over `kubejs/` scripts against the dump (exact setup to verify [?]), plus boot-log scan for KubeJS script errors.
- **Resource packs**: **MrKinau/ResourcePackValidator** (GPL-3; CLI + GitHub Action `MrKinau/ResourcePackValidator@v2` + Docker) — runs the vanilla-client load validations plus extras (missing textures, broken model refs, etc.) [V] https://github.com/MrKinau/ResourcePackValidator ; validator list https://github.com/MrKinau/ResourcePackValidator/blob/master/doc/VALIDATORS.md . Also LabPBR naming/channel checks are custom scripts (check `_n`/`_s` exist, sizes match albedo, alpha ranges) [recommendation].
- **Profiling**: **spark** — `/spark profiler start --timeout <s>`, `--only-ticks-over <ms>`, `--thread *`, `--alloc`; `/spark profiler stop --save-to-file` (no upload) ; `/spark health`, `/spark tps`, `/spark tickmonitor --threshold`; client side uses `/sparkc` [V] https://spark.lucko.me/docs/Command-Usage . Commands can be issued by an agent via RCON (server) or the in-client MCP mod (client).
- **Client FPS benchmarking**: FPS Benchmark | Performance Suite (Markdown+JSON reports, 1.21.1 **Fabric only, NeoForge "coming soon"**) https://www.curseforge.com/minecraft/mc-mods/fps-test-benchmark ; Valence Benchmark (10-min zero-alloc frametime capture, HTML/text report, Fabric) https://www.curseforge.com/minecraft/mc-mods/valence-benchmark [V]. => For NeoForge 1.21.1 + Iris, implement a ~100-line client command in your custom mod that flies a fixed camera path and logs frame times (avg, 1% low, p99) to JSON [recommendation].
- **Blender/Epic Fight**: Epic Fight Blender JSON exporter (Antikythera-Studios/blender-json-addon; also community fork for Blender 4.1) https://github.com/Antikythera-Studios/blender-json-addon ; **blender-mcp / mcp-for-blender** (ahujasid; MIT; ~30k stars; PyPI `mcp-for-blender` v2.1.0; pushed Oct 2026) lets agents drive Blender via Python [V-search] https://github.com/ahujasid/mcp-for-blender . Deterministic gate: `blender -b file.blend -P export_and_check.py` (bone names match EF armature, frame count, no NaN, keyframe timing for hit frames) [recommendation].

### B4. AI art / texture / animation generation (and policy)

- **Retro Diffusion** (Astropulse): pixel-art-specific models; Aseprite extension being phased out for own editor; credits-based; also on Scenario [C] https://retrodiffusion.ai/ , https://astropulse.itch.io/retrodiffusion . Licensing/training-data claims not verified [?].
- **PixelLab**: API v2 + **MCP server** (pixellab-mcp, 42 stars) for characters (4/8 directions), animations, tilesets, fonts; jobs async 2-5 min; reference sprites up to 256x256 [V] https://api.pixellab.ai/mcp/docs , https://github.com/pixellab-code/pixellab-mcp . Designed for 2D sprites — limited fit for 16-32 px *cuboid face* textures [?].
- Generic "AI Minecraft texture generators" (Spaleforce, PLAYTEX, Pixel GPT...) — marketing-level, unvetted [C].
- PBR from albedo: **DeepBump** (GPL-3, 1.4k stars, CLI + Blender add-on; normal + height from single image) https://github.com/HugoTini/DeepBump ; Depth-Anything-based albedo->normal tools; blockbench-mcp skills reference PyPBR/vgpu + Depth Anything for normal/height/MER [V-search]. For 16-32 px pixel textures these outputs generally need hand correction (see modeling notes: Bonemeal/Laigter/hand-fix) [C].
- Animation: Cascadeur 2026.1/2026.2 (AI inbetweening, AutoPhysics, ragdoll, additive layers, easing; GLB import; Mocap alpha) — strong fit for exaggerated combat keyframing before export to Blender/EF [V-search] https://cascadeur.com/blog/view/cascadeur-2026-2-animation-layers-easing-new-languages ; video mocap (Rokoko Video, etc.) covered in notes_animation.md.
- **Distribution policies (critical if the map is published)** [V]:
  - **Modrinth (since Aug 13 2026)**: mandatory "Contains AI-generated content" disclosure when substantial code is AI output, any asset is primarily/entirely AI output, or the design relies on gen-AI; **primarily AI-generated images banned from project pages (icon, gallery, description)**; **entirely/almost entirely AI-generated projects ("prompting and testing") cannot be listed publicly** (unlisted only). https://support.modrinth.com/en/articles/16551575-disclosure-and-usage-of-ai , https://modrinth.com/legal/rules
  - **Planet Minecraft (Apr 21 2026, edited Oct 10 2026)**: AI-generated content cannot replace/stand in for your original work — thumbnails, cover, gallery, or content where AI output replaces your creation; tools that assist workflow allowed "as long as the final result is your own work". https://www.planetminecraft.com/forums/pmc/news/ai-generated-content-shouldn-t-replace-your-work-or-images-706091/
  - CurseForge: no formal rule found; community idea threads request disclosure/filtering [C].
  - Community sentiment in r/Blockbench toward AI modeling MCPs is strongly negative (Oct 2026) [V].
  - Blockbench MCP stamps `ai_used`/`ai_agents` into .bbmodel; Sketchfab export uses `CreatedWithAI` tag [V].

### A9. Blackboard / shared-state and HITL guardrails (addendum to Part A)

- Blackboard MAS: Han & Zhang (arXiv 2507.01701) — agents read/write a shared blackboard, actors selected from blackboard content; competitive with SOTA static/dynamic MAS at fewer tokens on reasoning sets [V-abstract] https://arxiv.org/abs/2507.01701v1 . Salemi et al. (Google Cloud AI Research, arXiv 2510.01285) — central agent posts requests on a blackboard; sub-agents volunteer by capability; better scaling than rigid master-slave when the controller can't know sub-agent competencies [V-abstract] https://arxiv.org/html/2510.01285v2 .
  - => In a repo-based pipeline the "blackboard" is simply files: `docs/contracts/*.yaml`, `PROGRESS.md`, `test-results.json`, `debug_protocol.md`, issue tracker. Keep it append-only/structured; one owner per artifact.
- OpenAI Agents SDK guidance (2026): **input/output/tool guardrails** for automatic checks; **human-in-the-loop approvals** to pause before side effects (edits, shell commands, sensitive MCP actions); paused runs serializable via `RunState` [V] https://developers.openai.com/api/docs/guides/agents/guardrails-approvals , https://openai.github.io/openai-agents-python/human_in_the_loop/ ; OpenAI "A practical guide to building agents" (updated Jan 15 2026) https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ [V-search].
- Test-based selection beats consensus: CodeT-style generated tests (Microsoft, 2022) and ensemble "popularity trap" (A2) — prefer executable checks to voting [C].

---------------------------------------------------------------------------------------------------
## PART C. Synthesis: recommended agentic vs human-led split for THIS project (reasoned from A+B)

Principles (each tied to evidence):
1. **Single writer per artifact; other agents contribute review/intelligence** (Cognition 2026; MAST FC2; Google scaling: independent agents amplify errors 17.2x vs 4.4x with central verification).
2. **Parallelize only decomposable work** (separate assets, separate datapack modules); keep sequential stateful logic (boss state machine, cutscene timeline) in one agent (PlanCraft -39..-70% under MAS).
3. **Deterministic gates first, LLM/VLM judges second, humans last-but-mandatory for taste** (MAST FC3 verification failures 23.5% total; METR mergeability gap; VLM judges trail humans especially on textures).
4. **Fresh-context, different-family reviewer with no write tools** (Cognition clean-context; Clement concordance effect; ensemble diversity) — union findings, owner triages; don't majority-vote correctness (popularity trap; failure correlation 0.43).
5. **Task size well inside the 80% time horizon** (METR: frontier 50% horizon 12-17h but 80% ~3h on clean SW tasks; messier creative tasks lower) -> 30-120 min human-equivalent tickets with acceptance tests.
6. **Contracts as files + Default-FAIL evidence** (Anthropic sprint contracts; cwc-long-running-agents; Spec Kit; MAST spec failures).
7. **Version-pinned retrieval/skills for 1.21.1 APIs** (AutoUE RAG; OpenGame Template/Debug skills; community reports of version hallucination).
8. **Budget**: multi-agent ~15x chat tokens; a full planner/generator/evaluator harness ran 20x cost of solo; evaluators only where the task exceeds solo reliability; ablate components after model upgrades.

Stage split (A = agentic with gates, H = human-led with agent assist):
| Stage | Owner | Agent role | Gates |
|---|---|---|---|
| Design docs, boss move sheets, art bible, perf budget | H | draft from notes, clarify Qs, cross-model critique, convert to YAML contracts | schema validation; human sign-off |
| Custom NeoForge mod (Java) | A | planner->worker->fresh reviewer (other family) | gradle build, unit tests, `runGameTestServer` exit code, boot-log scan, HeadlessMC client boot |
| KubeJS scripts | A | worker + reviewer | ProbeJS v8 typings typecheck [?], boot-log KubeJS error scan, GameTests of resulting behavior |
| Datapacks (vanilla commands) | A | worker; generate from templates | mecha/check-commands (vanilla), dedicated-server load-log scan (modded), GameTests |
| Blockbench hero models (bosses, weapons) | H | blockout, UV templates, mirroring, naming, GeckoLib settings/export | bbmodel_validate + geckolib_validate_model + budget checks (bones/cubes/px density); 6-view contact sheet; VLM triage; art-director sign-off |
| Minor props/blocks | A->H review | headless bbmodel authoring | same + human pass |
| Pixel albedo textures | H | palette checks, tiling preview, atlas packing | human sign-off (quality + Modrinth/PMC policy) |
| LabPBR `_n`/`_s` | A draft -> H fix | generate normal/height drafts, pack channels per LabPBR 1.3 | channel-range/size/naming checker script; in-shader screenshot compare |
| Epic Fight combat anims (Blender) | H (Cascadeur optional) | headless Blender export + check script; registration JSON; hit-frame timing vs move sheet | bone/frame/NaN checks; in-game recording grid; human feel test |
| GeckoLib entity anims | H | keyframe chores, easing, loop flags | bbmodel_validate_animations, sample_pose clipping, geckolib validation |
| Animated Java cutscenes | H | trigger/camera/sound datapack glue | mecha + boot test + in-game screenshot sequence |
| World/level building | H | structure placement functions, spawners, triggers | GameTests for encounters |
| QA/playtest | A smoke + H feel | in-client MCP (langyo 1.21.1 NeoForge) routes, screenshots, recordings, spark | screenshot regression (VLM triage), spark profile, frame-time capture >=50 fps on target HW+shader; human playtest for difficulty |
| Release | H | changelog, AI-disclosure checklist | Modrinth/PMC policy check |
