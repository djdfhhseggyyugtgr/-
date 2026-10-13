# Claude Code as the orchestration backbone — research notes (2026-10-13)

Tags: [V] = verified against a primary source (official docs, Anthropic posts, installed CLI) · [C] = community opinion or report · [?] = uncertain or inferred
Raw fetched pages are in `research/agents_cc/` (F_*.json = page fetches, S_*.json = searches, yt/*.txt = transcripts, cli_help.txt = `claude --help` from this machine).

Facts verified locally: this cloud session runs **Claude Code 2.1.296** (`claude --version`). The bundled `claude-api` skill holds a model table cached 2026-10-06. [V]

---

## 0. Things that changed recently (read these first)

| Date | Change | Source |
|---|---|---|
| 2026-10-07 | **Claude Haiku 5.5** released ($0.10/$0.50 per MTok up to 100K prompt; 1M ctx). Sonnet 5.5 cache reads halved. Max/Team get **monthly API credits**. | https://www.anthropic.com/claude-haiku-5-5 [V] |
| 2026-10-07 | Agent SDK billing: Max/Team plans include monthly API credits (Max 5x $100, Max 20x $200, Team up to $500 pooled). The credits cover the Agent SDK, `claude -p`, the API and Managed Agents. **You can still run the Agent SDK, `claude -p` and third-party apps on subscription limits.** The credits do NOT cover interactive Claude Code. This policy has flip-flopped (announced June, paused June 15, revised Oct 6–7). | https://support.claude.com/en/articles/15036540 · https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers · HN https://news.ycombinator.com/item?id=49997654 [V] |
| 2026-09-28 | **Claude Sonnet 5.5** released (needs Claude Code ≥ v2.1.284) | https://www.anthropic.com/claude-sonnet-5-5 [V] |
| 2026-09-22 | **Claude Opus 5.5** released. It becomes `default` on Pro/Max/Team/Enterprise/API (needs ≥ v2.1.280). Default effort is **medium**. 5-hour limits were raised. | https://www.anthropic.com/claude-opus-5-5 · https://code.claude.com/docs/en/model-config [V] |
| 2026-09-14 | Claude Code weekly limits permanently +25%, after the temporary +50% ended (net −17% versus the promo) | https://usingclaude.com/en/pricing/plans/claude-code-weekly-limits-permanent-25-percent-faq [C, quoting @ClaudeDevs] |
| 2026-09-01 | **Claude Fable 5.1** released (needs ≥ v2.1.255–257). Pro plans pay usage credits; Max/premium seats can spend up to 50% of the weekly limit on it | https://support.claude.com/en/articles/15424964 [V] |
| v2.1.283 | **Auto mode** is now the default starting permission mode for interactive terminal and VS Code sessions | https://code.claude.com/docs/en/permission-modes [V] |
| Aug 2026 | Fork mode on by default, so subagents run in the background by default. Cross-session messaging shipped (native Windows ≥ v2.1.234). | https://code.claude.com/docs/en/whats-new/index [V] |
| May 28 2026 | **Dynamic workflows** (Workflow tool / `ultracode`) shipped. Now GA on all paid plans. | https://claude.com/blog/introducing-dynamic-workflows-in-claude-code [V] |

The what's-new digest index stops at Week 37 (Sep 7–11), so features from after that are known only from the changelog and the docs.

---

## 1. Model lineup usable in Claude Code (Oct 2026)

### 1.1 Models, IDs, price, context (first-party API) [V]
Sources: the bundled claude-api skill (cached 2026-10-06), https://code.claude.com/docs/en/model-config, the launch posts.

| Model | ID | Context / max out | $/MTok in/out | Notes |
|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 1M / 128K | 10 / 50 (cache read 0.25) | Most capable widely released model. Thinking is always on. Sustains long autonomous runs. Pro plans pay usage credits; Max can spend ≤50% of the weekly limit on it |
| Claude Fable 5 | `claude-fable-5` | 1M / 128K | 10 / 50 | Previous Fable |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M / 128K | 4 / 20 (cache read 0.20) | **Default model in Claude Code.** Default effort is medium. Launch post: performs "at the level of Fable 5.1 on most work" and costs 40% less than Opus 5. Output is >30% faster |
| Claude Opus 5 | `claude-opus-5` | 1M / 128K | 5 / 25 | |
| Claude Opus 4.8 / 4.7 / 4.6 | `claude-opus-4-8` … | 1M | 5 / 25 | |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M / 128K | 2 / 10 (cache read halved 2026-10-07; Claude Code now prices it at $0.10) | "Well-scoped everyday coding". 30% faster than Sonnet 5. Default effort is **medium in Claude Code** and high on the API |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | 2 / 10 | |
| Claude Haiku 5.5 | `claude-haiku-5-5` | 1M / 128K | 0.10 / 0.50 (≤100K prompt), 0.50 / 2.50 above | First Haiku with an effort setting. Positioned as "a subagent on coding work" |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K / 64K | 1 / 5 | |

Aliases in Claude Code on the Anthropic API: `opus`→Opus 5.5, `sonnet`→Sonnet 5.5, `haiku`→Haiku 5.5, `fable`→Fable 5.1. `best` means fable where available, otherwise opus. `opusplan` uses opus in plan mode and sonnet for execution. `[1m]` suffixes exist but don't matter for 5.x, which is natively 1M. Pin versions with full IDs or `ANTHROPIC_DEFAULT_OPUS_MODEL` and similar. [V] https://code.claude.com/docs/en/model-config

What `default` means: on Pro, Max, Team, Enterprise and the API it is now **Opus 5.5** (before v2.1.280 Pro got Sonnet 5). [V]

### 1.2 Effort
- Levels are low, medium, high, xhigh and max, plus `ultracode`, which is a setting rather than a level: it makes Claude orchestrate dynamic workflows for each substantive task. Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to **medium**. Opus 4.7 defaults to xhigh. The others default to high. [V] model-config
- Anthropic's own tests: "Opus 5.5 at medium matches or exceeds Opus 5 at high on coding and knowledge-work evaluations" [V]
- `ultrathink` in a prompt gives one turn of deeper reasoning. "think hard" and similar phrases are NOT keywords any more. [V]
- You can't turn thinking off on Opus 5.5, Sonnet 5.5, Haiku 5.5 or Fable. Lower the effort instead. [V] costs doc
- `maxEffortLevel` setting caps effort; CLAUDE_CODE_EFFORT_LEVEL env overrides everything. [V]

### 1.3 Anthropic guidance: which model for what
- Blog "Choosing a Claude model and effort level in Claude Code" (Jul 7 2026): "Fable is a specialist…, Opus is the expert, and Sonnet is a really good generalist." The heuristic: if Claude had the context, clearly tried, and still got it wrong, use a bigger model. If it skipped a file, didn't run the tests, or bailed partway, raise the effort. Start from the default effort. [V] https://claude.com/blog/claude-model-and-effort-level-in-claude-code
- Sonnet 5.5 guide: use Sonnet 5.5 for well-scoped everyday coding, high-volume development, documents and slides, and repeatable agent tasks (investigation, review, drafting). Use Opus 5.5 for long-horizon agentic coding, careful judgment and the hardest problems. Epic Games quote: Sonnet 5.5 handled "tens of thousands of lines of code for gameplay system architecture" and multi-hour tasks. [V] https://claude.dev/blog/building-with-claude-sonnet-5-5/
- Haiku 5.5: "pairs well with Opus 5.5 and Sonnet 5.5 as a subagent on coding work". [V]
- Fable: "Describe the outcome, not the steps… Skip the verification reminders… Size up larger tasks". Save it for work that needs it. [V] model-config
- Help Center: plan with Opus and execute with Sonnet; `/model opusplan` does this. [V] https://support.claude.com/en/articles/14552983
- Costs doc: use Sonnet for teammates, and `model: haiku` for simple subagents. [V] https://code.claude.com/docs/en/costs
- **Advisor tool** (experimental, Anthropic API only): run a cheaper main model and have it consult a stronger advisor at key moments, e.g. `/advisor opus`, the `advisorModel` setting, or `--advisor`. The advisor must rank at or above the main model. It suits long tasks where most turns are routine but plan quality matters. [V] https://code.claude.com/docs/en/advisor

### 1.4 Plans, limits, billing
- Subscription usage has a 5-hour session window plus a weekly limit. Subagents, workflows, cloud sessions and routines all draw from the **same** pool. [V] (cloud doc, routines doc)
- Fable: on Max and premium seats it may use up to 50% of the weekly limit. On Pro and Team standard it runs on usage credits from the first request. [V]
- Max/Team monthly API credits (new Oct 7): they cover the API, the Agent SDK, Managed Agents and `claude -p`. They do NOT cover interactive Claude Code. They don't roll over. Each linked Console org gets at least the Start tier. [V]
- Routines: 100 scheduled runs/hour per account; 30/hour per routine for run-now and API fires. They draw down subscription usage. [V] https://code.claude.com/docs/en/routines
- Enterprise averages about $13 per developer per active day (Anthropic's figure). [V] costs doc
- Third-party clients must not use claude.ai OAuth unless approved. Agent SDK apps should use API keys. [V] https://code.claude.com/docs/en/agent-sdk/overview

---

## 2. Claude Code multi-agent features (status, Oct 2026)

Overview page: Claude Code has "five ways to work on several tasks at once": **subagents, agent view, agent teams, projects, dynamic workflows**, plus worktrees, cross-session messaging and `/batch`. [V] https://code.claude.com/docs/en/agents

| Feature | Status | Who coordinates | Notes |
|---|---|---|---|
| Subagents | GA | Claude, turn by turn | Each has its own context and returns a summary. Background by default (fork mode). Nest up to 3 levels deep. Max 20 concurrent |
| Agent view (`claude agents`, `--bg`) | Research preview | You | Background sessions on your machine. Each one gets its own worktree before it edits |
| Agent teams | **Experimental, off by default** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) | A lead session | Shared task list and direct messaging between teammates. **Teammates are not isolated in worktrees.** Interactive only (not `-p` or SDK) |
| Projects (claude.ai/code) | Public beta on Pro/Max | Claude across days | Threads run in the cloud, or on your PC through Remote Control |
| Dynamic workflows (Workflow tool, `ultracode`) | GA on paid plans | A JS script | Dozens to hundreds of agents. Resumable. 16 concurrent agents by default, 1,000 agents per run max |
| Cross-session messaging | GA (macOS/Linux ≥ v2.1.224, native Windows ≥ v2.1.234) | Peers | ListAgents and SendMessage. Can reach other machines and the cloud only with a subscription login |
| Routines (`/schedule`) | Research preview | A schedule, API call or GitHub event | Run in the cloud, needs a subscription |
| `/loop`, `/goal` | GA | Session | /goal uses a separate evaluator model to check the completion condition after every turn |

### 2.1 Subagents (`.claude/agents/*.md`) [V] https://code.claude.com/docs/en/sub-agents
- Scope priority: managed > `--agents` CLI JSON > `.claude/agents/` (walks up from the cwd; nested directories allowed) > `~/.claude/agents/` > plugin `agents/`. Directories are scanned recursively, and identity comes from the `name` field. Edits are hot-reloaded without a restart.
- **Frontmatter fields** (only name and description are required; field names are camelCase; **unknown fields are silently ignored**): `name`, `description`, `tools`, `disallowedTools`, `model` (sonnet/opus/haiku/fable/full ID/inherit), `permissionMode`, `maxTurns`, `skills` (preloads full skill content), `mcpServers` (by name or inline), `hooks`, `memory` (user/project/local), `background`, `omitClaudeMd` (≥ 2.1.271), `effort`, `isolation: worktree`, `color`, `initialPrompt`, `experimental: {cacheTtl: 1h}`. The newest changelog also adds `autoCompactWindow`.
- Plugin subagents ignore `hooks`, `mcpServers` and `permissionMode`, for security.
- Model resolution: per-invocation param > frontmatter > `CLAUDE_CODE_SUBAGENT_MODEL` > main model. `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` forces one model onto every subagent, teammate and workflow agent. A newer variable, `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL`, puts all workflow agents on one model (changelog).
- Subagents inherit the main session's thinking setting. Built-in Explore and Plan skip CLAUDE.md. Override Explore with your own `Explore` that sets `model: haiku`.
- Nesting is limited by `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (default 3). The concurrency cap `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` defaults to 20.
- If the combined descriptions of custom subagents exceed 15K tokens, Claude Code warns at startup. Keep descriptions short and put detail in the body.
- Background subagents surface permission prompts in the main session. Granting "for session" applies to the whole session.
- Anthropic's own guidance: use the main conversation when phases share significant context (plan, implement, test). Use subagents for verbose output, tool restrictions, or self-contained work.
- Fork (`/subtask`, `/fork`) gives a subagent the full conversation context.

### 2.2 Agent teams [V] https://code.claude.com/docs/en/agent-teams
- Teammates load CLAUDE.md, MCP and skills but NOT the lead's history, so put specifics in the spawn prompt.
- Team size: "Start with 3-5 teammates", with "5-6 tasks per teammate". "Three focused teammates often outperform five scattered ones."
- Quality-gate hooks: `TeammateIdle`, `TaskCreated`, `TaskCompleted` (exit 2 blocks the action and sends feedback).
- Limitations: no `/resume` of in-process teammates; task status can lag; one team per session; no nested teams; the lead is fixed; permission modes are set at spawn; split panes need tmux or iTerm2 (**not supported in Windows Terminal, the VS Code terminal or Ghostty**). Teammates editing the same file overwrite each other.
- Costs: "approximately **7x more tokens** than standard sessions when teammates run in plan mode" [V] costs doc. Use Sonnet for teammates.
- [C] r/ClaudeCode (2026-09-02): message queueing confused leads into respawning teammates, so duplicate agents worked the same task for 30+ minutes. https://www.reddit.com/r/ClaudeCode/comments/1w5jjm1/
- Anthropic's C-compiler project used 16 parallel agents (a bare-bones `while true; claude -p` loop in Docker plus file locks in `current_tasks/`), about 2,000 sessions and $20k, producing a 100K-line compiler. Lessons: tests and an oracle (GCC) were needed so agents didn't all hit the same bug. [V] https://www.anthropic.com/engineering/building-c-compiler

### 2.3 Dynamic workflows (Workflow tool) [V] https://code.claude.com/docs/en/workflows · https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/
- Trigger: the `ultracode` keyword in a typed prompt, or asking for "a workflow". `/effort ultracode` makes Claude plan workflows automatically. The `ultracode` keyword does NOT trigger from `-p`, scheduled tasks or webhook payloads (≥ v2.1.210).
- The script is JS with top-level await: `agent(prompt, {schema, label, model?…})`, `parallel()`, `pipeline(list, fn)`, `phase()`, `log()`, `args`. Date.now and Math.random throw so runs are deterministic. There is no `import`, no direct filesystem access and no mid-run user input.
- Save with `s` in `/workflows`. Saved workflows go to `.claude/workflows/` (project) or `~/.claude/workflows/` and run as `/name`. They can be distributed in plugins. Load the `/workflow-authoring` skill before editing one.
- Limits: 16 concurrent agents (`CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS`, 1–256), ≤4,096 items per parallel or pipeline call, 1,000 agents per run. Agents with identical prefixes share the prompt cache (a 5 s stagger).
- Size guideline `workflowSizeGuideline`: small <5, medium <10 (the default; Pro defaults to small), large <50, or unrestricted. A "Large workflow" warning appears above 25 agents or 1.5M projected tokens.
- Turn off with `disableWorkflows: true` or `CLAUDE_CODE_DISABLE_WORKFLOWS=1`.
- Failure modes the blog says workflows address: **agentic laziness** (stopping at 35 of 50 items), **self-preferential bias** (favoring its own findings), **goal drift** (detail lost through compaction).
- Patterns from the blog: classify-and-act, fan-out-and-synthesize, adversarial verification, generate-and-filter, tournament, loop-until-done, and quarantine for untrusted input. "Most traditional coding tasks do not need a panel of 5 reviewers."
- [C] HN: "Tested on a 5x max plan… spun up 62 Opus 4.8 1M sub-agents… maxed out my ~5hr cap in 18 minutes." Another commenter found it "over tuned to use way more agents than I have ever found add value". https://news.ycombinator.com/item?id=48311705
- [C] Workflow agents don't reliably spawn nested subagents (r/ClaudeCode 2026-10-10). https://www.reddit.com/r/ClaudeCode/comments/1x2oana/

### 2.4 Hooks (33 events) [V] https://code.claude.com/docs/en/hooks
- Events: SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, MessageDisplay, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, SessionEnd.
- Handler types: `command`, `http`, `mcp_tool`, `prompt` (single-turn LLM decision), and `agent` (a subagent with tools that returns `{ok}`; experimental, 60 s default timeout). Matching hooks run in parallel. Fields include `if: "Bash(rm *)"`, `args: []` and `async: true` (command hooks only, non-blocking).
- Locations: user, project or local settings, managed settings, plugin `hooks/hooks.json`, skill frontmatter, subagent frontmatter. **Cloud sessions don't read the local `~/.claude/settings.json`**, so commit hooks to `.claude/settings.json`.
- Stop and SubagentStop: `{"decision":"block","reason":…}` or exit 2 keeps Claude working. Loop protection comes from `stop_hook_active` and an **8-consecutive-continuation cap**.
- The `$CLAUDE_CODE_REMOTE` env var is "true" in web or cloud sessions, so one hook script can branch between the cloud and the Windows PC.
- On Windows, command hooks run `powershell.exe` with `-NoProfile -ExecutionPolicy Bypass -File …`. The docs show separate handlers for the Bash and PowerShell tools.
- [C] HN (Agents Observe author): "hooks are blocking – performance degrades rapidly if you have a lot of plugins that use hooks"; switching to async hooks helped a lot. https://news.ycombinator.com/item?id=47602986

### 2.5 Skills, commands, plugins, mods, output styles [V]
- Skills live at `.claude/skills/<name>/SKILL.md`. Frontmatter: `name`, `description` (+`when_to_use`, truncated at 1,536 characters), `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context: fork` + `agent`, `background`, `hooks`, `paths` (glob-activated), `shell: powershell`, `arguments`. `.claude/commands/*.md` take the same fields. https://code.claude.com/docs/en/skills
- Skill with `context: fork` versus subagent with `skills:`: the first runs a task you wrote in the skill; the second uses skills as reference material.
- Plugins bundle skills, agents, hooks, MCP servers and mods. CLI: `claude plugin install|validate|eval|details`. `claude plugin eval` runs eval cases against a plugin. https://code.claude.com/docs/en/plugins/overview
- Mods (new): JS/TS handlers running inside Claude Code. Example events include `turn.step`, where a handler can "send it to a different model with `next({ ...e, model })`, or answer without calling the model", and `agent.spawn`, which can set a subagent's model. https://code.claude.com/docs/en/plugins/mods/events — [?] It's undocumented whether this can route to non-Anthropic providers.
- Output styles: built-ins such as Concise, Explanatory and Learning, plus custom ones.

### 2.6 Memory / CLAUDE.md [V] https://code.claude.com/docs/en/memory
- Load order: managed policy (`C:\Program Files\ClaudeCode\CLAUDE.md`) → `~/.claude/CLAUDE.md` → `./CLAUDE.md` or `./.claude/CLAUDE.md` → `./CLAUDE.local.md`. Subdirectory CLAUDE.md files load on demand. `@path` imports work.
- `.claude/rules/*.md` with `paths:` globs load only when matching files are touched. These suit per-domain rules such as `data/**/*.json` for datapacks or `kubejs/**` for KubeJS.
- **AGENTS.md** (≥ v2.1.277): read automatically when no CLAUDE.md exists. Setting `claude-md-and-agents-md` reads both. Or put `@AGENTS.md` in CLAUDE.md, which gives Codex and Claude one shared instruction file.
- Auto memory: Claude writes notes itself, per repository, shared across worktrees. The first 200 lines or 25KB load each session.
- Keep CLAUDE.md under about 200 lines and move procedures into skills. [V] costs doc and best practices.

### 2.7 Headless and SDK [V] https://code.claude.com/docs/en/headless · cli_help.txt
- `claude -p "…" --output-format json|stream-json --input-format stream-json --json-schema '{…}' --max-budget-usd N --allowedTools … --permission-mode auto|dontAsk --agents ./agents.json --append-subagent-system-prompt --forward-subagent-text --include-hook-events --bare --worktree --fallback-model a,b --effort high --model …`
- `--bare` skips hooks, skills, plugins, MCP, memory and CLAUDE.md, giving reproducible CI runs. It **requires ANTHROPIC_API_KEY**, not a subscription.
- `--permission-prompts none` denies anything that would prompt.
- Agent SDK: `@anthropic-ai/claude-agent-sdk` and `claude-agent-sdk`. It is the Claude Code binary as a library, with built-in tools, hooks, subagents, sessions and plugins. Agent teams do NOT spawn in `-p` or SDK sessions.
- Background sessions: `claude --bg`, `claude agents`, `attach`, `logs`, `stop`, `rm`, `respawn`.

### 2.8 Worktrees [V] https://code.claude.com/docs/en/worktrees
- `claude -w name` creates the worktree under `.claude/worktrees/<name>/` on branch `worktree-<name>`. Add that directory to .gitignore. `.worktreeinclude` copies gitignored files such as `.env`. `worktree.baseRef` chooses the base branch. Subagents can use `isolation: worktree`. `WorktreeCreate` and `WorktreeRemove` hooks support non-git VCS.
- Claude Code enforces isolation by blocking commands that escape to the main checkout.
- [C] Open Windows bugs: case-sensitive drive-letter comparison breaks worktree isolation (#91618, #85234).

### 2.9 Permissions and safety [V] https://code.claude.com/docs/en/permission-modes
- Modes: `default` (Manual), `acceptEdits`, `plan`, `auto` (a classifier that runs on Sonnet 5 by default; checks subagent spawns, actions and final reports), `dontAsk` (CI), `bypassPermissions` (isolated VMs only).
- Rules like `Agent(model:opus)` match tool parameters, e.g. to block Opus subagents.
- **The Bash sandbox doesn't work on native Windows; use WSL2.** https://code.claude.com/docs/en/sandboxing

### 2.10 Cloud, Remote Control, Projects, GitHub [V]
- Cloud sessions need Pro, Max, Team or Enterprise premium. They share rate limits. Setup scripts are cached when they finish in about 5 min. Repos must be on GitHub. `claude --cloud`, `--teleport`. https://code.claude.com/docs/en/claude-code-on-the-web
- Remote Control: drive a local session from a phone or browser. Needs a subscription. **It doesn't work when `ANTHROPIC_BASE_URL` points to a non-Anthropic host**, which matters if you route through Ollama or a gateway. https://code.claude.com/docs/en/remote-control
- Projects: one conversation that starts threads in the cloud, or on your PC through Remote Control. Public beta on Pro and Max, rolling out gradually. https://code.claude.com/docs/en/claude-projects
- GitHub Actions: `anthropics/claude-code-action@v1`, authenticated with `anthropic_api_key` or `claude_code_oauth_token` (from `claude setup-token`). Plugins and `claude_args` are supported. https://code.claude.com/docs/en/github-actions
- `claude ultrareview` / `/code-review ultra`: multi-agent bug hunting in the cloud.

---

## 3. Anthropic's published multi-agent guidance

1. **Building effective agents** (Dec 2024): prefer simple composable patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) and add agents only when needed. [V, URL] https://www.anthropic.com/engineering/building-effective-agents
2. **Multi-agent research system** (Jun 2025): Opus lead with Sonnet subagents beat single-agent Opus by **90.2%** on breadth-first research. Agents use about **4×** the tokens of chat, multi-agent systems about **15×**. Token usage alone explains 80% of performance variance. "Most coding tasks involve fewer truly parallelizable tasks than research." Embed effort-scaling rules (1 agent and 3–10 calls for simple tasks, and so on). [V] https://www.anthropic.com/engineering/multi-agent-research-system
3. **When to use multi-agent systems (and when not to)** (claude.com, ~early 2026): multi-agent setups use **3–10×** more tokens than single-agent. Use them only for (a) context protection, (b) parallelizable work, (c) specialization. **Decompose by context, not by problem type.** A planner/implementer/tester/reviewer split "spent more tokens on coordination than on actual work" (the "telephone game"). The **verification subagent** consistently works, but beware the **"early victory problem"**: verifiers declare a pass after one or two tests. "Start with the simplest approach that works." [V] https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
4. **Effective context engineering** (Sep 2025): context rot; compaction, structured note-taking, and subagents that return condensed summaries of 1–2K tokens. [V] https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
5. **Effective harnesses for long-running agents** (Nov 2025): an initializer agent sets up `init.sh`, `claude-progress.txt`, a **JSON feature list** ("less likely to inappropriately change… JSON compared to Markdown") and a first git commit. The coding agent then does **one feature at a time**, leaves a clean state, and tests end to end with browser automation. [V] https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
6. **Harness design for long-running apps** (Mar 2026): GAN-style planner, generator and evaluator, with the evaluator using Playwright and per-criterion hard thresholds. Generator and evaluator agree a "sprint contract" before building. Agents praise their own work, so use a separate evaluator. Solo run: 20 min, $9. Full harness: 6 hr, **$200**, with much better quality. **"Every component in a harness encodes an assumption… re-examine when a new model lands"**: Opus 4.5/4.6 let the author drop context resets and sprints. [V] https://www.anthropic.com/engineering/harness-design-long-running-apps
7. **Dynamic workflows** (Jun 2026): see 2.3. [V]
8. **Patterns and problems in multiagent systems** (Anthropic research, Aug 13 2026): swarms built a web-playable fantasy game over 12 hours with roles, a CEO hierarchy or neither. "In all three versions the resulting games were (perhaps predictably) bad… **Models have poor taste in this arena and currently require significant human direction.**" Newer models (Sonnet 5) merge PRs and share code much better than 4.6. [V] https://www.anthropic.com/research/multiagent-systems — **highly relevant to a quality-first game.**
9. **Claude Code best practices** (live doc): give Claude a check it can run, at four levels of gating (prompt → `/goal` → Stop hook → verification subagent or workflow). Explore, plan, code, commit. A Writer/Reviewer pair of sessions. An adversarial review subagent that flags only correctness gaps, to avoid over-engineering. `/clear` after two failed corrections. [V] https://code.claude.com/docs/en/best-practices

Token multipliers to plan with: chat ×1 → single agent ×4 → multi-agent ×15 (2025 research); multi-agent is 3–10× single agent (2026 blog); agent teams in plan mode are about 7× a session; a full harness cost about 20× a solo run.

---

## 4. Community patterns: what works and what's hype [C unless noted]

- **Parallel worktrees, 3–5 sessions**: the Claude Code team's #1 tip (Boris Cherny, Feb 2026, 50K likes). Also: plan first, have a second Claude review the plan "as a staff engineer", update CLAUDE.md after every correction, commit skills to git, ask Claude to "prove it works". https://x.com/bcherny/status/2017742741636321619 · summary https://ailearnedtoday.com/ref/boris-cherny-claude-code-tips
- **Session handoff and state files** (180-upvote r/ClaudeCode post, 2026-10-10): `/session-start` and `/handoff` commands, a lessons.md, a decisions file, and checking the notes against git and CI before trusting them. Commenters: "an unreadable check isn't a pass", and "keep the verbatim transcript; summaries drift". Others say "none of this is necessary any longer". https://www.reddit.com/r/ClaudeCode/comments/1x2os3k/
- **Cheap-worker armies are often a false economy**: YouTube test (4 days old, 186K views). Opus 5.5 solo beat Opus 5.5 managing Haiku 5.5 subagents **10–2**. The team saved 61% on decomposable code review but cost about 80% more and took an hour longer on integrated creative work (an animated film), plus 14 hallucinated bugs against 0 for solo Opus. https://www.youtube.com/watch?v=Ug3x37N6Z_E
- **Cross-model review** (Codex reviewing Claude's diffs) is widely reported to catch issues Claude misses (r/ClaudeCode threads Jul–Sep 2026). The official **openai/codex-plugin-cc** (31K stars) adds `/codex:review`, `/codex:adversarial-review` and `/codex:rescue` (delegate a task), plus background jobs. It uses ChatGPT or Codex limits. https://github.com/openai/codex-plugin-cc
- **Multi-provider subagents**: "sonata" runs a local proxy that routes `.claude/agents` model aliases to GPT, GLM or MiMo with fallbacks. The author reports $41 billed plus $177 covered by a ChatGPT subscription over 17 days, with 330 automatic fallbacks. Also claude-code-router (swaps the whole session's model). Both are third-party; treat as experimental. https://www.reddit.com/r/ClaudeCode/comments/1x4jkh8/
- **Ollama with the Claude Code harness** [V]: `ANTHROPIC_BASE_URL=https://ollama.com ANTHROPIC_AUTH_TOKEN=$OLLAMA_API_KEY ANTHROPIC_API_KEY="" claude --model <cloud-model>`, or `ollama launch claude --model X --yes -- -p "…"`. Tool-choice controls, deferred tools and hosted web search are "not fully supported". With a non-Anthropic base URL, Remote Control and server-managed settings turn off. https://docs.ollama.com/integrations/claude-code · https://docs.ollama.com/api/anthropic-compatibility
- **Ralph loop**: Anthropic ships a `ralph-wiggum` plugin (Nov 2025), and Anthropic's harness posts acknowledge the pattern. `/goal` and Stop hooks are now the official form of "keep going until a check passes". [V] https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum
- **Parallel-session managers** (Conductor, Claude Squad, Vibe Kanban, Crystal and others): mostly worktree plus tmux or GUI wrappers. Claude Code now ships agent view, `--bg`, `-w` and cross-session messaging natively, which reduces the need for them. Many of these tools are macOS-first. https://superterminal.dev/blog/multi-agent-coding-tools-compared.html
- **Spec-driven development** (Spec Kit, Kiro, a plain plan.md): field logs mostly settle on "plan mode plus a spec file plus gates you build yourself". Kiro builds the gates in. https://felipefontoura.com/articles/kiro-vs-claude-code/ · https://www.devmoment.dev/journal/spec-kit-vs-kiro-field-log-2026
- Skeptical voices (HN, dynamic workflows thread): "quality is the issue, not quantity", "build your own orchestration so you learn where you need to be in the loop", "agents ignore rules at implementation time", and mixed reports on rule-following.

---

## 5. Game dev / Minecraft specifics

- **Blockbench MCP** (jasonjgardner, 513★): a desktop plugin MCP over HTTP (`localhost:3000/bb-mcp`), plus a **headless `.bbmodel` stdio MCP** (`npx -y github:jasonjgardner/blockbench-mcp-plugin --root ./models`) that edits, validates, converts and renders bbmodels **without Blockbench running**. Several agents can run it in parallel, including in cloud sessions [?]. https://github.com/jasonjgardner/blockbench-mcp-plugin
- **@adhisang/minecraft-blockbench-mcp**: edits `java_block` and `geckolib_model` formats through a Blockbench plugin over a WebSocket, with undo entries. https://www.npmjs.com/package/@adhisang/minecraft-blockbench-mcp
- **adhi-jp/minecraft-modding-mcp**: 41 tools for decompiled MC source, Mojang/Yarn mappings, version diffs, NeoForge JAR analysis, and Mixin/AT validation. Self-described as "entirely vibe-coded". https://github.com/adhi-jp/minecraft-modding-mcp
- **MineCode MCP** (PyPI `minecode-mcp`): version-accurate datapack data. It detects the target version from `pack.mcmeta` and lists format breaks such as 1.21's singular folder names (`advancement/`), 1.20.5 item components and 1.21.2 dropping the `generic.` attribute prefix. Directly relevant to 1.21.1 datapacks. https://github.com/ancarsenat/minecode-mcp
- **NeoForge skills/plugins**: `chouzz/minecraft-mod-dev` (a marketplace plugin that fetches docs dynamically, covers JEI/AE2/Create), plus `neoforge-modding` skills on skill marketplaces. Many public NeoForge 1.21.1 repos ship a CLAUDE.md (e.g. nafre/ore_generator).
- [C] JASON13 video: Claude used outdated loader APIs until pointed at decompiled sources (`genSources` with Vineflower). That is, give it ground truth plus a compile and run check. https://www.youtube.com/watch?v=aAd--EO6gRM
- [V] Anthropic swarm research: agent-built games had "poor taste", so humans must own art and feel direction.
- [C] r/feedthebeast is strongly hostile to AI-generated mods and art (e.g. "AI generated mods should be banned", 1.7K upvotes, May 2026). Consider disclosure and keeping human-authored art if the map is published.
- **Windows and non-ASCII path risk** [V, GitHub issues]: Claude Code path-encoding bugs with Korean folder names. #70674 (non-Latin characters replaced by hyphens, causing session and memory directory collisions and data loss on purge) was closed 2026-10-12. **#84966 (Glob silently returns "No files found" when the path contains Hangul) is still open.** Move the repo to an ASCII path without spaces, e.g. `C:\dev\mc-soulslike`, which Gradle and Java also prefer. https://github.com/anthropics/claude-code/issues/84966 · /issues/70674

---

## 6. Design implications for the user's pipeline (synthesis)

1. **Default stack**: main or orchestrator session on Opus 5.5 at medium, raised to high or xhigh for hard systems work. Sonnet 5.5 for well-scoped implementation workers and teammates. Haiku 5.5 for Explore, log triage, JSON lint and lang files. Fable 5.1 only for rare architecture or root-cause calls; it is free within the plan only up to 50% of the weekly limit on Max. Or try `/advisor opus` with a Sonnet main model.
2. **Decompose by context boundary**, e.g. "Boss X: entity Java + GeckoLib geo + animations + loot + advancement" owned by one agent in one worktree. Don't split into writer, tester and reviewer roles. The exception is a **black-box verifier** (gradle build, game tests, datapack validation, screenshot diff) plus a cross-model **Codex adversarial review**.
3. **Deterministic gates over prompts**: a Stop hook or `/goal` that runs `gradlew build` plus validators. PostToolUse async validators for JSON and mcfunction. Path-scoped `.claude/rules/` per domain. Commit everything in `.claude/` so cloud and PC behave the same, branching on `$CLAUDE_CODE_REMOTE`.
4. **Where work runs**: cloud sessions and routines handle code, data and validation (headless). The Windows PC handles anything needing a GPU, client, Iris, Blockbench GUI, Blender or Animated Java, via Remote Control or a Projects thread. Cloud sessions can't render the client. [?] Whether the cloud network allows the Maven and NeoForge repos depends on the environment's network setting; test it.
5. **Budget controls**: `workflowSizeGuideline: small|medium`, `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL=sonnet`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, `maxEffortLevel`, the deny rule `Agent(model:fable)`, `--max-budget-usd` for `-p` runs, `/usage` (breaks usage down by subagent, skill, plugin and MCP).
6. **Re-evaluate the harness on each model release.** Anthropic's own lesson is to strip pieces that are no longer load-bearing.
