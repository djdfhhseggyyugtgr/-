---
name: blockbench-setup
description: Install and verify this project's Blockbench plugins through the Blockbench MCP server. Use when the user asks to install, update or check Blockbench plugins, or to set up Blockbench for this project.
---

# Blockbench plugin setup

This installs the project's Blockbench plugin set into the user's running Blockbench desktop app through the `blockbench` MCP server (the jasonjgardner Blockbench MCP plugin, HTTP at `http://localhost:3000/bb-mcp`, configured in `.mcp.json`).

It only works in a session running on the user's own computer (Claude Code in the repository folder, or `claude remote-control`). In a cloud session the `blockbench` server is not reachable; say so and stop.

## Preconditions

1. Blockbench 5.2 or newer is running on the user's PC.
2. The Blockbench MCP plugin is installed in it. It is not in the official plugin store (the store does not allow AI features), so the user installs it once by hand: File > Plugins > Load Plugin from URL > `https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js`.
3. Settings > General keeps the defaults: MCP Server Port `3000`, MCP Server Endpoint `bb-mcp`, and the risky eval toggle on.
4. The `blockbench` server shows as connected in `/mcp`.

If any of these fail, tell the user which step to do (the Korean guide is `docs/setup/blockbench-mcp.md`) and stop.

## Steps

1. Call `get_capabilities` on the `blockbench` server. Confirm the Blockbench version is 5.1.4 or newer (Animated Java needs 5.1.4).
2. Read `tools/blockbench/install-plugins.js` and pass its whole content, unchanged, as the `code` argument of `risky_eval`. The tool rejects code that contains `console.`, `//` or `/* */`, so never add comments or URLs to it.
3. Blockbench may open a message box (for a deprecated plugin, or after 12 installs in one session). If the call seems to hang, ask the user to look at Blockbench and click the dialog.
4. Read `tools/blockbench/list-plugins.js` and run it through `risky_eval` to confirm what is installed.
5. Report a table to the user: plugin id, result, version.

## Optional plugins

Install these only when the user asks. Use the same code as `install-plugins.js` with a different `ids` list:

| id | use |
| --- | --- |
| `palette_swap` | Swap colour families in a texture |
| `baked_ambient_occlusion` | Bake AO into mesh textures (meshes only) |
| `mesh_tools`, `uv_locker` | Mesh modelling tools |
| `cem_template_loader`, `emf_animation_addon` | Vanilla mob re-models for EMF/ETF |
| `structure_importer`, `structure_to_model` | Bring map structures into Blockbench for scale reference |
| `resourcepack_packager` | Package Java models and textures into a resource pack |

## Do not install

| id | reason |
| --- | --- |
| `free_rotation` | Needs Minecraft 1.21.4+ item models; the project is on 1.21.1 |
| `pbr_preview` (PBR Tools) | Supports Blockbench up to 4.11.9 only |
| `animation_utils` | Deprecated; replaced by `geckolib` |
| `ambient_occlusion` | Deprecated |
