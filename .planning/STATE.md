# State: Model-Driven Framework (MDF)

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-05)

**Core value:** Engineers can verify the full structural design before typing `execute-phase` — no guessing, no mid-execution surprises.
**Current focus:** Milestone v1.0 — defining requirements and roadmap

## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: 2026-03-05 — Milestone v1.0 started

## Accumulated Context

- Full workflow design completed 2026-03-05 — see docs/plans/2026-03-05-mdf-development-workflow.md
- Research complete — see .planning/research/SUMMARY.md
- Build order confirmed: Schema Foundation → MCP Tools → Phase 0 Skills → Integration Validation
- Key stack: FastMCP 3.1.0, Pydantic v2, lxml, NetworkX, lark, ruamel.yaml
- Skills live at .claude/skills/mdf/; MCP server at mdf-server/
- GSD files never modified — integration via CLAUDE.md injection and config.json

## Decisions

| Decision | Outcome |
|----------|---------|
| Milestone v1.0 scope | Schemas + MCP server + Phase 0 skills |
| Research conducted | Yes — 4 parallel researchers + synthesizer |
| Skip research for future phases | Per-phase decision |

## Blockers

(None)
