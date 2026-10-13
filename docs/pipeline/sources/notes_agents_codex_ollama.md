# Notes: OpenAI Codex + Ollama Cloud + wiring them with Claude Code (as of 2026-10-13)

Tags: [V] verified from official docs/pages or my own test call today; [C] community report / third-party source; [?] uncertain, inferred, or untested.
Raw fetched pages: `research/agents_cx/` (F_*.json = fetched pages, S_*.json = searches, ollama_tags.json / ollama_show.json = live API output).

---------------------------------------------------------------------
## 0. Things that changed recently (read first)

| Date | Change | Source |
|---|---|---|
| 2026-08-24 / 09-05 | `codex mcp-server` deprecated in Codex CLI 0.149.1, then **removed** (commit #42993, 2026-09-05). Docs: "The `codex mcp-server` command and standalone `codex-mcp-server` binary have been removed. Use the Codex app server instead." Every 2025-era guide saying `claude mcp add codex -- codex mcp-server` is now broken. [V] | https://developers.openai.com/codex/cli/reference.md , https://developers.openai.com/codex/sdk.md , https://upd.dev/openai/codex/commit/531f3836a1e38ea61eaaba3dccda6711eb6c0dca.patch |
| 2026-08-31 | Ollama replaced GPU-time / 5-hour / weekly limits with **per-token pricing + monthly credit pool** (Pro $20 = $60 credits, Max $100 = $300, Team $500 = $1,000). Legacy plans keep old terms until changed. [V] | https://ollama.com/blog/transparent-pricing |
| 2026-08-31 | gpt-5.4 / gpt-5.4-mini retired from ChatGPT-auth Codex. [V] | https://developers.openai.com/codex/models |
| 2026-09-03 | GPT-6 Astra launched; 2026-09-29 GPT-6.1 Sol (DevDay) replaced GPT-6 Sol as the recommended model; Codex 0.161.0 (2026-10-07) makes `gpt-6.1-sol` the default. [V] | https://openai.com/index/introducing-gpt-6-1-sol/ , https://github.com/openai/codex/releases/tag/rust-v0.161.0 |
| 2026-09-14 | GPT-5.3-Codex-Spark retired from Codex. [V] | codex/models |
| 2026-09-18 | **Claude Code 2.1.277 reads AGENTS.md natively** (when no CLAUDE.md / CLAUDE.local.md exists; configurable). [V] | https://code.claude.com/docs/en/memory |
| **2026-10-14 (tomorrow)** | **GPT-5.5 retires from ChatGPT-auth Codex** (stays on API). Any config/script pinning `gpt-5.5` must switch to `gpt-6-sol`/`gpt-6.1-sol` (paid) or `gpt-6-luna` (Free/Go). [V] | https://developers.openai.com/codex/models |
| ongoing | `approval_policy = "untrusted"` retired and "can prevent either client from starting"; `codex exec --full-auto` deprecated (use `--sandbox workspace-write`). [V] | https://developers.openai.com/codex/agent-approvals-security.md , https://developers.openai.com/codex/noninteractive.md |
| ongoing | Codex custom providers must speak the **Responses API**; `wire_api = "chat"` no longer supported. [V] | codex/models |

---------------------------------------------------------------------
## 1. OpenAI Codex (Oct 2026)

### 1.1 Surfaces [V]
- **Codex CLI** (Rust; `npm i -g @openai/codex`, signed PowerShell installer for Windows since 0.162.0). Latest stable 0.162.1 (2026-10-09); 0.163 alphas daily. https://github.com/openai/codex/releases
- **IDE extension** (VS Code etc.), **ChatGPT desktop app** (Codex lives inside it now, alongside "ChatGPT Work"), **Codex Cloud** (web/mobile; cloud environments w/ setup scripts; tasks run on OpenAI VMs; VM state recoverable 7 days). https://help.openai.com/en/articles/20001545-using-codex-cloud
- **GitHub integration**: `@codex review` on a PR, automatic reviews, `@codex security review` (Pro/Business/Enterprise; not Plus). Posts only P0/P1 findings. Reads `## Code Review Rules` sections in the nearest AGENTS.md. Requires ChatGPT sign-in (not API key). https://learn.chatgpt.com/docs/third-party/github.md
- **`codex exec`** (headless, alias `codex e`): default read-only sandbox; progress to stderr, final message to stdout; `--json` JSONL events (`thread.started`, `turn.*`, `item.*`); `--output-schema schema.json -o out.json` for schema-conformant final output; `--ephemeral`; `codex exec resume --last "..."`; `--ignore-user-config`, `--ignore-rules`; `--skip-git-repo-check`; MCP server with `required=true` fails the run if it can't start. https://developers.openai.com/codex/noninteractive.md
- **`codex review`** non-interactive review: `--uncommitted` | `--base <branch>` | `--commit <sha>` | custom prompt. [V] cli/reference
- **Codex SDK**: TypeScript `@openai/codex-sdk` (`new Codex().startThread().run(...)`, resumeThread) and Python `pip install openai-codex` (stable; `Codex().thread_start(model="gpt-6.1-sol", sandbox=Sandbox.workspace_write)`; drives the local **app-server** over JSON-RPC). https://developers.openai.com/codex/sdk.md
- **App server** (`codex app-server`, JSON-RPC 2.0; stdio/unix socket/experimental websocket) = the official deep-integration surface replacing mcp-server. https://developers.openai.com/codex/app-server.md
- **Codex as MCP client**: `codex mcp add NAME -- cmd args`, or `[mcp_servers.NAME]` in `~/.codex/config.toml` or project `.codex/config.toml` (trusted projects only). STDIO + streamable HTTP (bearer, OAuth/CIMD/DCR). Per-tool `approval_mode`, `enabled_tools`, `tool_timeout_sec` (default 60), `startup_timeout_sec` (10). https://developers.openai.com/codex/mcp.md
- **Subagents / custom agents**: built-ins `default`, `worker`, `explorer`; custom TOML files in `~/.codex/agents/` or `.codex/agents/` with `name`, `description`, `developer_instructions`, optional `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`… `[agents]` defaults incl. `default_subagent_model`, `max_concurrent_threads_per_session`. "Ultra" effort = max reasoning + proactive subagent delegation. https://learn.chatgpt.com/docs/agent-configuration/subagents
- **Skills**: `.agents/skills/<name>/SKILL.md` scanned from CWD up to repo root, plus user/admin/system locations. Plugins = distributable bundles of skills/apps/MCP. https://developers.openai.com/codex/skills.md
- **Managed worktrees** (0.162.0: create/list managed worktrees from trusted projects; `codex --worktree` puts them in `~/.codex/worktrees/` on a detached HEAD [C: data-dynamics.io]).
- Image generation (GPT-Image-2) inside Codex; consumes limits 3-5x faster. [V pricing]. Useful for concept art / reference images — Claude cannot generate images (Reddit users call Codex from Claude Code for this [C]).

### 1.2 Sandbox / approvals [V]
- `--sandbox read-only | workspace-write | danger-full-access`; `--ask-for-approval on-request | never` (+ `approval_policy = { granular = {...} }`). `untrusted` policy retired; use `[projects."/path"] trust_level="untrusted"` instead.
- Network off by default in workspace-write; enable `[sandbox_workspace_write] network_access = true` or permission profiles (`default_permissions`, `[permissions.X] extends=":workspace"`, domain allowlist with `features.network_proxy = true`).
- `approvals_reviewer = "auto_review"` routes escalations to a reviewer agent (extra usage).
- **Windows**: native PowerShell sandbox. Three implementations: `mxc` (recommended; Windows 11 24H2 build 26100.9278+ / 25H2 26200.9278+, no admin), `elevated` (admin-approved setup; preferred legacy fallback), `unelevated` (weaker network isolation). `[features] prefer_mxc = true` or `[windows] sandbox="elevated"`. Test: `codex -c windows.sandbox=mxc sandbox --include-managed-config --permission-profile :workspace -- cmd.exe /d /c echo MXC_OK`. WSL2 remains an alternative. https://developers.openai.com/codex/windows.md
- 0.162.0 preserves CRLF line endings in apply_patch (relevant for Windows repos). [V]

### 1.3 Models (Codex, Oct 2026) [V unless noted]
API page data: https://developers.openai.com/api/docs/models/gpt-6.1-sol , /gpt-6-astra , /gpt-6-luna

| Model id | Positioning | Context / max out | API $/1M in·cached·out | Codex credits/1M (in·cached·out) | Plus local msgs per 5h (est.) | Notes |
|---|---|---|---|---|---|---|
| `gpt-6-astra` | Most capable; hardest end-to-end work | 1.05M / 128K (922K max input) | 10 · 1 · 50 | 250 · 25 · 1250 | 5–45 | effort low…max; >272K input = 2x in, 1.5x out |
| `gpt-6.1-sol` (default since 0.161) | "Near-Astra at 1/5 price"; repeated long-running work | 1.05M / 128K | 2 · 0.10 · 10 | 50 · 2.5 · 250 | 15–160 | effort low/medium(default)/high/xhigh/max (+Ultra in Codex); no `none`/`minimal`; tool calls need Responses API |
| `gpt-6-sol` | previous Sol | 1.05M | – | 50 · 5 · 250 | 15–150 | replacement for gpt-5.5 per OpenAI |
| `gpt-6-luna` | cheapest; extraction, classification, transformation, structured summaries | 1.05M / 128K | 0.10 · 0.01 · 0.50 | 2.5 · 0.25 · 12.5 | 350–3,000 | effort none…max (no Ultra); Free/Go get Luna |
| `gpt-5.6-sol/terra/luna` | still available during rollout | – | – | 100·10·500 / 50·5·300 / 5·0.5·30 | – | 5.6 Sol promo pricing through ≥ 2026-11-21 |
| `gpt-5.5` | **retires from ChatGPT-auth Codex 2026-10-14** | – | API only after | 125·12.5·750 | – | |

All GPT-6 models: text+image input, text output, function calling, structured outputs, web_search, apply_patch, hosted_shell, computer_use, MCP, tool_search, prompt caching. Fast mode = 2x price (2.5x of included limits); Ultrafast (Astra/6.1 Sol) = 6x price, Pro $500 only.

Vendor benchmarks (treat as directional) [V vendor / C aggregator]:
- OpenAI: GPT-6.1 Sol matches Astra on DeepSWE v1.1 at ~1/5 cost; beats Opus 5.5 on GDP.pdf and AutomationBench (+2.2pp at medium). https://openai.com/index/introducing-gpt-6-1-sol/
- AgentAtlas compile of vendor numbers: Opus 5.5 vs GPT-6 Astra — Terminal-Bench 4.0 66.4 vs 57.9, OSWorld 2.1 81.8 vs 72.6, DeepSWE 1.1 74.2 vs 74.1 (tie), Astra leads AutomationBench and Terminal-Bench-Science. Opus 5.5 API $4/$20. https://agentatlas.org/models/compare/claude-opus-5-5-vs-gpt-6-astra/ [C]
- HN Pac-Man bake-off: Opus 5.5 99 ($2.00), GPT-6.1 Sol 91 ($0.51), Astra 87 ($2.42). https://news.ycombinator.com/item?id=49896586 [C]

### 1.4 Plans / limits [V] (https://developers.openai.com/codex/pricing)
- Free $0 / Go $8: GPT-6 Luna in desktop app (rollout).
- **Plus $20**: Codex web/CLI/IDE/iOS, cloud integrations (auto code review, Slack), GPT-6.1 Sol + Luna; 5-hour windows + weekly limits; buy credits to extend.
- **Pro $100 / $200 / $500**: "Pro plans currently have no five-hour limit" (weekly limits still apply); Ultrafast only on $500.
- **API key**: CLI/SDK/IDE only, no cloud features (no GitHub review/Slack), pay API rates. Recommended for CI.
- Image gen and MCP servers eat limits; docs recommend fewer MCP servers and smaller AGENTS.md.
- [C] Usage volatility: reports of GPT-6.1 Sol draining a Plus 5-hour window in 11 min, Sol Ultra in 2–3 min (codex issue #53046), Astra ~7x Sol consumption (HN), "banked resets" giving reduced allowance, "model at capacity" errors on Windows desktop (issue #53594). https://codexinsider.ai/articles/codex-user-says-gpt-6-1-sol-drained-a-chatgpt-plus-5-hour-allowance-in-1-b8dec1/ , https://github.com/openai/codex/issues/53046

### 1.5 AGENTS.md conventions [V] (https://developers.openai.com/codex/guides/agents-md.md)
- Chain: `~/.codex/AGENTS.override.md` or `AGENTS.md` → repo root → … → CWD (one file per dir: `AGENTS.override.md` > `AGENTS.md` > `project_doc_fallback_filenames`). Concatenated root→leaf; **32 KiB cap** (`project_doc_max_bytes`).
- To make Codex also read CLAUDE.md: `project_doc_fallback_filenames = ["CLAUDE.md"]`.
- `## Code Review Rules` section drives GitHub reviews.

### 1.6 Auth [V] (https://developers.openai.com/codex/auth.md)
- ChatGPT sign-in (subscription) or API key (`printenv OPENAI_API_KEY | codex login --with-api-key`; or `CODEX_API_KEY=... codex exec`).
- Headless: `codex login --device-auth` (beta; must enable device-code login in ChatGPT security settings).
- `cli_auth_credentials_store = file|keyring|auto|ephemeral`. `~/.codex/auth.json` = password-equivalent; don't use ChatGPT-auth CI on public repos.

---------------------------------------------------------------------
## 2. Ollama Cloud (Oct 2026)

### 2.1 Live model list (my API call to `https://ollama.com/api/tags` + `/api/show`, 2026-10-13) [V]
Prices from https://ollama.com/pricing (per 1M tokens: input / cached / output). Context = `model_info.*context_length`.

| Model (API name) | Size / type | Context | Caps (from /api/show) | $ in / cached / out | Notes |
|---|---|---|---|---|---|
| `kimi-k3` | 2.8T MoE, MXFP4 | 1M | tools, thinking, vision | 3.00 / 0.30 / 15.00 | strongest open model on the list; billed "extra usage"; AA index ~43.8 |
| `glm-5.3` | 753B FP8 | 1M | tools, thinking | 1.40 / 0.26 / 4.40 | "most capable open-weights coding model"; AA ~44.8 |
| `glm-5.2` | 756B | 1M | tools, thinking | 1.40 / 0.26 / 4.40 | previous flagship |
| `glm-5.3-flash` | 321B (18B active) FP8 | 1M | tools, thinking, **vision** | 0.15 / 0.03 / 0.50 | cheap workhorse; AA ~41.8; very popular; reasoning-stall complaints |
| `deepseek-v4-pro:0813` | 1.65T FP8 | 1M | tools, thinking | 1.32 / 0.044 / 3.96 (off-peak half) | three reasoning modes |
| `deepseek-v4.1-flash` | 763B FP8 | 1M | tools, thinking, vision | 0.30 / 0.006 / 1.20 (off-peak 0.15/0.60) | cheapest cache reads; good bulk/long-context |
| `kimi-k2.7-code` | 1.04T INT4 | 256K | tools, thinking, vision | 0.95 / 0.19 / 4.00 | coding-tuned K2.6, ~30% fewer thinking tokens |
| `kimi-k2.6` | 1.04T INT4 | 256K | tools, thinking, vision | 0.95 / 0.16 / 4.00 | |
| `minimax-m3` | ? | 512K (page says 1M) | tools, thinking, vision | 0.60 / 0.12 / 2.40 | coding/agentic |
| `minimax-m2.7` | 229B | 192K | tools, thinking | 0.30 / 0.06 / 1.20 | |
| `mistral-large-4` | 1.05T (52B active) | 1M | tools, thinking, vision | 0.68 / 0.07 / 2.09 | added 2026-10-06; [C] beats Kimi K3 on Terminal-Bench |
| `mistral-large-3:675b` | 675B FP8 | 256K | tools, vision (no thinking) | 0.50 / – / 1.50 | |
| `nemotron-3-ultra` | 550B | 256K | tools, thinking | 0.10 / 0.10 / 3.00 | |
| `nemotron-3-super` | 120B (12B active) NVFP4 | 256K | tools, thinking | 0.015 / 0.015 / 0.60 | near-free input → good for huge-input summarization |
| `nemotron-3-nano:30b` | 32B FP8 | 256K | tools, thinking | 0.06 / – / 0.24 | fastest (~250–300 tok/s [C]) |
| `gemma4:31b` | 32.7B BF16 | 256K | tools, thinking, **vision** (+audio per site) | 0.14 / 0.05 / 0.40 | fast (~216–299 tok/s [C]), terse, good cheap vision |
| `gpt-oss:120b` | 117B MXFP4 | 128K | tools, thinking | 0.15 / 0.014 / 0.60 | fast (~170–257 tok/s [C]) |
| `gpt-oss:20b` | 21B | 128K | tools, thinking | 0.07 / 0.035 / 0.30 | |

- **No embedding or reranker models on Ollama Cloud** (open feature request https://github.com/ollama/ollama/issues/17129). Use local Ollama (e.g., `embeddinggemma`) on the PC or OpenAI embeddings. [V list / C issue]
- Retired June 2026: kimi-k2-thinking, kimi-k2:1t, minimax-m2, glm-4.6, qwen3-next, qwen3-vl:235b, cogito-2.1 (replacements listed). Note: **no Qwen models currently on Ollama Cloud** although Qwen3.8 Max/Flash exist elsewhere. [V list; C ollamatps.com/limits]
- [C] r/ollama 2026-09-29: users note new-model velocity slowed after the pricing change.

### 2.2 Plans / limits [V] (https://ollama.com/pricing , https://ollama.com/blog/transparent-pricing)
- Free $0: starter credits on starter models, 1 concurrent request; can buy credits to unlock all models.
- **Pro $20/mo ($200/yr)**: $60 usage credits/mo, 3 concurrent.
- **Max $100/mo**: $300 credits/mo, 10 concurrent, early access.
- Team $500/mo: $1,000 shared credits, unlimited users.
- No 5h/weekly windows on new plans; credits reset monthly, no rollover; overage at same per-token rate; email at 90%.
- **Peak pricing**: "Off-peak pricing applies outside 12:00–18:00 UTC on weekdays and all day weekends" (currently DeepSeek rows). For Korea (UTC+9): peak = **21:00–03:00 KST weekdays**.
- No published RPM/TPM; queue beyond concurrency then reject. [C ollamatps.com/limits]
- Web search API: `POST https://ollama.com/api/web_search {query, max_results≤10}`, `POST /api/web_fetch {url}`; free account required; counts against cloud usage; known bug: returns 200 with empty body when usage exhausted (issue #16045). https://docs.ollama.com/capabilities/web-search

### 2.3 APIs / compatibility [V]
- Native: `https://ollama.com/api/chat` (Bearer `$OLLAMA_API_KEY`). Model names as returned by `/api/tags` (e.g., `gemma4:31b`); via local Ollama app use `<name>:cloud`.
- OpenAI-compatible: `https://ollama.com/v1` — chat/completions and **stateless** Responses. "The cloud API does not support stateful Responses, built-in web search through /v1/responses, or custom/freeform tool-call replay." https://docs.ollama.com/api/openai-compatibility
- Anthropic-compatible: `https://ollama.com/v1/messages` — messages, streaming, function calling; needs `Authorization: Bearer` (x-api-key alone rejected); tool-choice controls, deferred tools, hosted web search not fully supported. https://docs.ollama.com/api/anthropic-compatibility
- **Structured outputs NOT supported on Ollama Cloud** ("Ollama's Cloud currently does not support structured outputs." https://docs.ollama.com/capabilities/structured-outputs). **My test today**: `format` JSON schema ignored by gpt-oss:20b and glm-5.3-flash (prose returned). Workaround that worked: Anthropic `/v1/messages` with a tool whose `input_schema` is the target schema → glm-5.3-flash returned `stop_reason: tool_use` with JSON input in 0.6 s. Schema still not *enforced* → always validate.
- **My tests today** [V]:
  - `/v1/messages` + tool → glm-5.3-flash tool_use OK (0.6 s).
  - `/v1/responses` stateless → gpt-oss:20b `completed` (0.8 s).
  - Vision (32×32 red/blue PNG via `/api/chat` `images`): gemma4:31b correct, terse (0.6 s); kimi-k2.7-code correct (1.0 s); glm-5.3-flash correct but with `think:false` it leaked its reasoning into `content`.
  - **Codex CLI 0.162.1 → Ollama Cloud directly works** with config below, BUT first attempt failed: `the web_search tool is not supported` → must set `web_search = "disabled"`. Also warns "Model metadata for `glm-5.3-flash` not found. Defaulting to fallback metadata" (ollama launch codex generates a `model_catalog_json` to fix this). Trivial task cost 8.5K input tokens (Codex system prompt overhead). `codex exec` also blocks on "Reading additional input from stdin..." unless stdin is closed (`< /dev/null`).
- Data handling: "We do not use them to train models"; "Prompt or response data is never logged or trained on"; hosted primarily US, may route to Europe; partners (NVIDIA Cloud Providers) under no-logging/ZDR. [V pricing FAQ, docs.ollama.com/cloud]
- Latency/throughput [C, https://ollamatps.com/ 2026-10-12]: TTFT ~0.3–1.4 s; gpt-oss:120b 170–257 tok/s, gemma4:31b 160–299, glm-5.3-flash ~148, deepseek-v4.1-flash ~170, glm-5.3 ~110, kimi-k3 ~100, kimi-k2.7-code ~122, minimax-m2.7 ~33, nemotron-3-ultra ~31–40.
- Reliability [C]: Sept–Oct 2026 r/ollama threads "Cloud becoming increasingly unusable" (https://www.reddit.com/r/ollama/comments/1wsp4bp/), "How is anyone getting anything done" (1–5 tok/s episodes; https://www.reddit.com/r/ollama/comments/1wmbv4u/), outage 2026-10-05 (https://www.reddit.com/r/ollama/comments/1wy6cdk/). GLM-5.3-Flash "stops during long reasoning" traced partly to client max-output caps (opencode 32K) + max thinking (https://www.reddit.com/r/ollama/comments/1wpupjl/). Others report no issues. → Treat Ollama Cloud as a cheap, best-effort lane with retries/timeouts, not a critical path.

### 2.4 Running Claude Code / Codex on Ollama models [V]
- `ollama launch claude [--model glm-5.3:cloud] [--yes] [-- <claude args>]`; `ollama launch codex`; `ollama launch opencode|hermes|openclaw|codex-app`. `--yes` for CI/scripts (requires `--model`).
- `ollama launch claude` sets (source cmd/launch/claude.go): `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY=`, `ANTHROPIC_AUTH_TOKEN=ollama`, `ANTHROPIC_DEFAULT_OPUS_MODEL=ANTHROPIC_DEFAULT_SONNET_MODEL=ANTHROPIC_DEFAULT_HAIKU_MODEL=CLAUDE_CODE_SUBAGENT_MODEL=<model>`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS=<ctx>`, `CLAUDE_CODE_AUTO_MODE_SERVER=0`, `ENABLE_CLAUDEAI_MCP_SERVERS=false`, telemetry/feedback off. https://github.com/ollama/ollama/blob/main/cmd/launch/claude.go
- Direct cloud (no local Ollama): `ANTHROPIC_BASE_URL=https://ollama.com ANTHROPIC_AUTH_TOKEN="$OLLAMA_API_KEY" ANTHROPIC_API_KEY="" claude --model glm-5.3-flash`. Hosted WebSearch and advanced tool controls not fully supported. https://docs.ollama.com/integrations/claude-code
- Claude Code's base URL is **global per process**: no native per-subagent provider routing (open FRs https://github.com/anthropics/claude-code/issues/38698 , #74073). ToolSearch was disabled behind custom base URLs (issue #32378, closed). Anthropic does not support non-Claude models behind gateways ([C] baltor.ai summary of Claude Code docs).
- Codex: `codex --oss -m gpt-oss:120b` (local Ollama), `ollama launch codex` (profile `~/.codex/ollama-launch.config.toml`, `wire_api="responses"`, base_url `http://localhost:11434/v1/`), or direct cloud provider (tested config in §4).
- [C] Ollama's `/v1/responses` silently ignores `previous_response_id` (0.34.0 bug) → stateful clients lose context; send full history. https://mangodeveloper.com/articles/ollamas-responses-api-silently-drops-conversation-context-while-returning-200-ok

---------------------------------------------------------------------
## 3. Integration patterns Claude Code ⇄ Codex ⇄ Ollama

### 3.1 Claude Code → Codex
1. **Official `openai/codex-plugin-cc`** (34k★, created 2026-03-30; wraps the Codex app server; uses your global `codex` + its auth/config) [V README https://github.com/openai/codex-plugin-cc]:
   ```
   /plugin marketplace add openai/codex-plugin-cc
   /plugin install codex@openai-codex
   /reload-plugins
   /codex:setup
   ```
   Commands: `/codex:review [--base main] [--background|--wait]` (read-only, not steerable), `/codex:adversarial-review [--base main] <focus text>` (steerable, read-only), `/codex:rescue [--model ..] [--effort ..] [--resume|--fresh] <task>` (delegates to `codex:codex-rescue` subagent; can write), `/codex:transfer` (moves current Claude session into a Codex thread → `codex resume <id>`), `/codex:status`, `/codex:result`, `/codex:cancel`. Optional **review gate**: `/codex:setup --enable-review-gate` → Stop hook runs Codex review and blocks Claude from stopping until issues are fixed ("can create a long-running Claude/Codex loop and may drain usage limits quickly").
   - Pitfall: README examples still mention `gpt-5.4-mini` and `spark` (both retired from ChatGPT-auth Codex) — set `model = "gpt-6.1-sol"`/`"gpt-6-luna"` in `.codex/config.toml`. [V]
   - [C] Windows: hang at "Initializing…" when spawning app-server (issue #236, Apr 2026, plugin 1.0.3) — check current status.
2. **Plain `codex exec` from a Claude skill / Bash** (most deterministic; no plugin):
   `codex exec -m gpt-6.1-sol -c model_reasoning_effort="high" --sandbox read-only --ephemeral --output-schema .ai/schemas/review.json -o .ai/out/codex_review.json "Review the diff vs main for correctness…" < /dev/null`
   or `codex review --base main`. Community skills doing this: shaharsha/claude-skills codex-review ("fresh context, no write access, adjudicate every finding"), cathrynlavery/codex-skill, dwgx/claude-codex-subagent. [C]
3. Third-party MCP wrappers (tuannvm/codex-mcp-server 628★ `claude mcp add codex-cli -- npx -y codex-mcp-server`, cexll/codex-mcp-server) — they wrap the CLI, so they survive the mcp-server removal, but are unofficial. [C]
4. **PAL MCP (formerly Zen MCP, BeehiveInnovations/pal-mcp-server, ~11.8k★)**: multi-provider (OpenAI, Gemini, OpenRouter, Ollama, custom OpenAI-compatible) tools `chat`, `consensus`, `codereview`, `precommit`, `planner`, plus `clink` (spawn Codex/Claude/Gemini CLIs as isolated subagents). README model recommendations are stale (Sonnet 4.5 / GPT-5.2). Windows requires WSL2. [V README / C freshness]

### 3.2 Codex → Claude Code
- `claude mcp serve` exposes **Claude Code's tools** (Read/Edit/Bash…) over stdio MCP — not a Claude reasoning agent; the client must implement confirmations. Add to Codex: `codex mcp add claude-code -- claude mcp serve`. https://code.claude.com/docs/en/mcp [V]
- For "ask Claude" from Codex: a Codex skill that shells out to `claude -p "<prompt>" --output-format json` (headless) in read-only permission mode. [?] (standard Claude Code headless usage; not tested here)

### 3.3 Ollama in the mix
- Claude Code main session stays on Anthropic; cheap Ollama workers run as **separate processes**: `ANTHROPIC_BASE_URL=https://ollama.com ANTHROPIC_AUTH_TOKEN=$OLLAMA_API_KEY ANTHROPIC_API_KEY= claude -p --model glm-5.3 "…"` or plain Python/`curl` to `ollama.com/api/chat` (cheapest, no harness overhead), or via PAL MCP.
- Codex: second provider in config.toml + profile (`codex --profile ollama` / `-c model_provider=ollama-cloud`). [V tested]. Codex custom agent TOML may set `model_provider` for a cheap subagent [?] (docs say custom agent files accept the same keys as config.toml; untested).
- Proxies: **LiteLLM** (docs for both Claude Code and Codex client setup; can front Anthropic/OpenAI/Ollama with budgets & logging) https://docs.litellm.ai/docs/proxy/client_setup/codex_cli.md ; **claude-code-router** (musistudio, ~36.6k★; route Claude Code requests by task type to other providers incl. Ollama). [C] Adds a moving part; only worth it if you want per-request routing inside one Claude session.

### 3.4 Shared instructions
- **AGENTS.md as canonical**; Claude Code ≥2.1.277 loads AGENTS.md only if there is **no** CLAUDE.md / CLAUDE.local.md in CWD or above; otherwise use `CLAUDE.md` containing `@AGENTS.md`, or `/config` → Project instructions = `claude-md-and-agents-md`. Claude Code does **not** read `AGENTS.override.md`, `AGENTS.local.md`, or anything under `.agents/`. [V https://code.claude.com/docs/en/memory]
- Codex reads AGENTS.md chain (32 KiB cap); can read CLAUDE.md via `project_doc_fallback_filenames`.
- Skills drift: Claude `.claude/skills/` vs Codex `.agents/skills/` — two copies; on **Windows avoid symlinks** (need Developer Mode/admin; Git checks them out as text unless `core.symlinks=true`) → keep one source dir and a sync script, or pointer files. [C r/codex 1x2wkid]
- Community consensus: one shared file, tool-specific lines prefixed ("Claude only:" / "Codex only:"); a shared session journal / work-order backlog; "never use both at the same time on the same files" or use worktrees. [C https://www.reddit.com/r/codex/comments/1x2wkid/]

### 3.5 Worktrees / parallelism pitfalls [C: https://www.data-dynamics.io/en/blog/git-worktree-claude-codex-parallel , https://dev.to/offrun/running-claude-code-and-codex-in-parallel-on-one-repo-git-worktree-gotchas-and-cross-review-41eg]
- `claude -w <name>` → `<repo>/.claude/worktrees/<name>`, branch `worktree-<name>` (add `.claude/worktrees/` to .gitignore); `codex --worktree` → `~/.codex/worktrees/…` detached HEAD (create a branch before keeping work).
- Git refuses same branch in two worktrees (good). **Stash is shared** across worktrees (agents' `git stash pop` can grab another's stash). `.env`, `node_modules` (for us: `run/`, `.gradle`, `build/`, local libs) aren't copied.
- [?] NeoForge-specific inference: each worktree needs its own Gradle build and `run/` dir; parallel `runClient`/`runServer`/GameTest runs collide on ports (25565) and on the shared Gradle daemon/cache locks — serialize game launches.

### 3.6 CI
- **openai/codex-action@v1** (installs CLI, starts Responses API proxy so the key isn't in job env; `prompt`/`prompt-file`, `model`, `effort`, `sandbox`, `codex-args` e.g. `["--output-schema","schema.json"]`, `output-file`, `safety-strategy: drop-sudo` default; Windows runners need `safety-strategy: unsafe`). Pattern: Codex job with `contents: read` → patch artifact → separate job with write perms opens PR. https://developers.openai.com/codex/github-action.md [V]
- Codex GitHub app reviews (`@codex review`, auto-review) — ChatGPT plan usage, not API. [V]
- **anthropics/claude-code-action@v1** for `@claude` mentions / automation (other agent likely covers details). https://code.claude.com/docs/en/github-actions
- Ollama in CI: plain `curl https://ollama.com/api/chat -H "Authorization: Bearer $OLLAMA_API_KEY"` from a step, or `ollama launch claude --model X --yes -- -p "…"`. Budget via Ollama credits; set timeouts/retries (reliability).
- Never put `OPENAI_API_KEY`/`CODEX_API_KEY` as job-level env in jobs running repo code. [V]

### 3.7 Claude Code cloud sessions (this environment type)
- Network is allowlisted per environment; to call `api.openai.com` / `chatgpt.com` (Codex) or `ollama.com` (Ollama) from a cloud session, add them under the environment's Network access → Allowed domains, and store keys as environment secrets/variables (not in chat). https://code.claude.com/docs/en/cloud-environments#network-access [V product docs]
- In ephemeral containers prefer API-key auth for Codex (`CODEX_API_KEY` / `codex login --with-api-key` in a SessionStart hook); ChatGPT device-auth tokens won't persist. [?]

---------------------------------------------------------------------
## 4. Tested / ready config snippets

`~/.codex/config.toml` (Windows: `%USERPROFILE%\.codex\config.toml`)
```toml
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"          # high/xhigh for reviews
project_doc_fallback_filenames = ["CLAUDE.md"]
# approval_policy = "untrusted"  # DO NOT USE - retired

[profiles.ollama]                           # codex --profile ollama
model = "glm-5.3"
model_provider = "ollama-cloud"
web_search = "disabled"                     # REQUIRED: Ollama rejects hosted web_search (tested)

[model_providers.ollama-cloud]
name = "Ollama Cloud"
base_url = "https://ollama.com/v1"
env_key = "OLLAMA_API_KEY"
wire_api = "responses"

[mcp_servers.claude-code]                   # Claude Code tools inside Codex (tools only)
command = "claude"
args = ["mcp", "serve"]
```
(Tested 2026-10-13 with codex-cli 0.162.1 + glm-5.3-flash: shell tool call + answer OK.)

Codex custom agent `.codex/agents/reviewer.toml`:
```toml
name = "reviewer"
description = "Read-only adversarial reviewer for diffs"
developer_instructions = "Review only. Report P0/P1 issues with file:line and a failing scenario. No edits."
model = "gpt-6.1-sol"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
```

Claude Code → cheap Ollama worker (PowerShell):
```powershell
$env:ANTHROPIC_BASE_URL="https://ollama.com"; $env:ANTHROPIC_AUTH_TOKEN=$env:OLLAMA_API_KEY; $env:ANTHROPIC_API_KEY=""
claude -p --model glm-5.3-flash "Summarize docs/research/*.md into a 1-page brief"
```

JSON via Ollama (since `format` is ignored): use tool-as-schema on `/v1/messages`, then validate (jsonschema + Minecraft `/reload` / datapack validator) and retry on failure. For strict JSON prefer `gpt-6-luna` (API structured outputs, $0.10/$0.50) or `codex exec --output-schema`.

---------------------------------------------------------------------
## 5. Community evidence: who is best at what (late Sept – mid Oct 2026) [C]
Sources: r/codex 1x2jf2g (split work), 1x2ojgq (favor GPT), 1x2rqfh (back to Claude, 197↑), 1x2wkid (instruction sync); r/ClaudeCode 1x3sasx ("mass migration from Codex to Claude because Opus 5.5…"); HN 49896586; claudefluent guide.
- **Opus 5.5 (Claude Code)**: fastest to working code, better UI/UX and wording, orchestration, long unattended "vibe" runs; criticized for verbosity, assumptions, missing edge cases. Many Codex users moved to Claude in Oct 2026.
- **GPT-6.1 Sol / Astra (Codex)**: thorough, careful, strong at **code review, edge cases, debugging, verification**, computer use, automations/scheduled tasks, image generation; criticized for slowness, over-engineering ("27,000 lines vs 650"), usage-limit drains. Astra ≈ 7x Sol usage.
- **Most repeated multi-model pattern**: *Claude implements → Codex (Sol high/xhigh) reviews cold diff → Claude adjudicates*; "never let the same model grade its own homework"; reviewer read-only; tests as referee; swap roles when stuck. Several say "much better results running them together". Counter-view: "what's powerful is having *another* agent review, not GPT specifically."
- Open models: GLM-5.3-Flash praised for speed/capability on large codebases (r/LocalLLaMA 1wyuqha, 163↑), GLM-5.3 strong; but Ollama Cloud service quality complaints.
- Handoff is the unsolved part: use a repo file (plan.md / work order / journal) as the contract between agents.

---------------------------------------------------------------------
## 6. Recommended task→model mapping for this project (synthesis) [?]
| Task | First choice | Cheap/bulk lane | Why |
|---|---|---|---|
| Architecture, mod Java code, KubeJS, refactors | Claude Opus 5.5 (Claude Code) | — | community + vendor coding benchmarks |
| Independent code review of every PR/diff | Codex GPT-6.1 Sol high (`/codex:review`, `codex review --base`) | glm-5.3 / kimi-k2.7-code via Ollama as pre-filter | cross-model review is the most-endorsed pattern |
| Hard bug hunts (crashes, mixin/registry issues) | Codex Sol xhigh / Astra (rescue) + Claude | — | Codex thoroughness |
| Bulk web research / doc summarization | Ollama deepseek-v4.1-flash (1M ctx, off-peak) / glm-5.3-flash / gpt-oss:120b | nemotron-3-super (input $0.015) | price + speed |
| Vision QA of screenshots / textures | gemma4:31b (cheap, fast) → kimi-k2.7-code/kimi-k3 or Claude for 2nd opinion | — | tested vision; LLM vision unreliable for pixel-exact checks → pair with scripts (size, palette, alpha, LabPBR channel ranges) |
| JSON/datapack/loot/advancement generation | GPT-6 Luna via API with structured outputs, or `codex exec --output-schema` | Ollama glm-5.3-flash with tool-as-schema + validator | Ollama Cloud ignores JSON schema |
| Concept/reference images | Codex image gen (GPT-Image-2) | — | Claude has no image gen |
| Embeddings (asset/doc search) | local Ollama embeddinggemma / OpenAI embeddings | — | none on Ollama Cloud |
