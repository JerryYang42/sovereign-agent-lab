"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No available venue matches 300 guests with vegan options (0 results)."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I changed The Albanach status in mcp_venue_server.py from available to full,
reran exercise4_mcp_client.py, then reverted it. Query 1 changed from two
matches to one match (only The Haymarket Vaults remained), but the final
recommended venue/address stayed The Haymarket Vaults. Query 2 stayed the
same semantically (no 300-person vegan venue). No client code changes were
required; only server data changed, proving MCP clients react to server-side
tool/data updates.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 10   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 49   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP gives a stable tool contract across multiple clients, not just file
separation. The same search_venues/get_venue_details tools were discovered
dynamically by the LangGraph client, and the architecture also allows Rasa
to consume the same server. When venue status changed server-side, client
logic did not change. This improves reuse, consistency, centralized updates,
and lowers integration risk as more tools are added in later weeks.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- Planner: decomposes ambiguous booking goals into ordered subgoals before execution; it lives in the autonomous-loop half.
- Executor ReAct agent: performs iterative tool-use (search, weather, cost, content generation) and resolves open-ended research; it lives in the autonomous-loop half.
- Structured confirmation agent (Rasa CALM): enforces deterministic, auditable business rules for deposits/commitments during calls; it lives in the structured-agent half.
- Shared MCP tool layer: exposes venue and later web/calendar/email capabilities through one contract both halves can discover; it lives in the shared layer.
- Handoff bridge + memory: routes tasks between autonomous and structured halves and stores state/context for continuity; it lives in the shared layer between both halves.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The research should be done by the autonomous LangGraph-style agent, and the
call/commitment should be handled by the structured Rasa-style agent. In the
Exercise 4 traces, the research flow needed iterative tool use and recovery
from argument-shape errors (multiple search_venues calls before a valid one),
which is a good fit for a flexible ReAct loop. For high-stakes confirmation,
that same improvisational behavior is risky: you want explicit flows,
deterministic checks, and auditable transitions. Swapping them feels wrong
because it would either over-constrain research or under-govern commitments.
"""