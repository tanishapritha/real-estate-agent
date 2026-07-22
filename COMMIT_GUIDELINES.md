# Commit Guidelines

Read this before making commits in this repo. The goal is a history that
looks like one person built this steadily over time: small logical steps,
occasional fixes, a few "wait, that was wrong" corrections. Not one giant
commit, and not a suspiciously perfect linear list either.

## Format

```
<lowercase, imperative, short summary>

<optional body, only if the "why" isn't obvious from the diff>
```

- No prefix tags like `feat:`, `fix:`, `chore:`, just write what happened
- No emoji
- No "Generated with Claude" / "AI-assisted" / co-author trailers of any
  kind. This is your repo, your commit
- Keep the summary line under ~65 chars where possible
- Body text only when the reasoning matters (for example: "switched to a
  separate table for checkpoints instead of a JSON blob column, needed to
  query by execution_id"). Most commits don't need a body.

### Good examples

```
add lead and customer sqlalchemy models
wire up alembic, first migration
fix foreign key on conversation.lead_id
inventory mcp server: search + details tools
supervisor node: route to qualification first
handle missing customer email in qualification agent
add checkpoint write after every graph node

was losing state on worker restart because checkpoints only
wrote on completion, not per-node
add retry wrapper around litellm calls
streamlit: dashboard page, wire to real workflow counts
typo in event schema field name
tests for inventory ranking logic
```

### Bad examples (don't do this)

```
Implement comprehensive multi-agent orchestration system with full MCP integration
Add Files
final commit
WIP
Update README.md
Add supervisor agent
Refactor everything
```

## Granularity

One logical change per commit. A "logical change" is something you could
describe in one sentence without using "and" more than once.

Rough guide for what one commit should look like:
- One model plus its migration
- One MCP server tool (or a small group of related tools on the same
  server)
- One agent node
- One route
- One Streamlit page (or a meaningful chunk of a big page)
- One bug fix
- One test file

Don't bundle "add inventory agent, wire it into graph, add tests" into one
commit, that's three commits. Don't split "import statement" into its own
commit either, use judgment.

## Cadence and realism

Real solo projects aren't clean. Build the history so it includes:

- A few commits that fix something introduced two or three commits earlier
  ("fix null check in qualification agent" landing shortly after
  "qualification agent: extract structured preferences")
- At least one small revert-and-redo when an approach changes mid-phase
  (for example, moving from a JSON column to a proper table)
- Commits that are just plumbing: dependency bumps, config tweaks, a
  renamed field, not everything is a feature
- Not every commit needs a body. Most are a single line.

Don't manufacture fake typos or fake bugs for their own sake, just don't
polish the sequence into something that never has a correction. If you
build something correctly the first time, commit it correctly the first
time.

## Example sequence: Phase 1 (DB models)

```
add pyproject.toml with core deps
app skeleton: config, logging, health endpoint
add sqlalchemy base and session setup
add lead and customer models
set up alembic
first migration: leads, customers
add property model
add conversation and message models
fix message.conversation_id missing index
add workflow_execution and workflow_checkpoint models
add event and agent_execution models
migration for workflow and event tables
seed script: insert one test lead
```

Twelve commits for what could technically be one, that's the point. Each
one should leave the repo in a working state (migrations apply cleanly,
nothing half-imported).

## Branching

Solo project, keep it simple: commit to `main` directly unless you're
mid-way through something that would leave the app broken for more than a
commit or two, in that case use a short-lived branch and merge it back (no
need for PR review theater, just merge).

## What never goes in a commit message

- Anything referencing "the user asked" or "as requested"
- Anything referencing Claude, Anthropic, or AI assistance
- Overly formal changelog language ("This commit introduces...")
