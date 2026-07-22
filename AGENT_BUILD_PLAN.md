# Build Plan: RealEstate AI Sales OS

This file is the source of truth for building this repo. Read it fully before
writing any code. Work phase by phase, in order. Do not skip ahead to a later
phase before the current one meets its "Definition of Done." Do not build
anything listed under "Explicitly out of scope."

If something in this doc is ambiguous, make the simplest reasonable choice
and keep moving. Don't stall waiting for clarification on minor details.

---

## 1. What this project is

A stateful, multi-agent workflow platform that runs the real-estate sales
lifecycle end to end: lead intake, qualification, inventory search,
recommendation, follow-up/appointment/escalation/lost, CRM update.

It is not a chatbot. It is not a CRUD app with an LLM bolted on. The
LangGraph supervisor owns workflow state and routes to specialist agents,
which call tools through MCP servers, which are backed by mocked services
for now (CRM, calendar, messaging, inventory, knowledge).

## 2. Explicitly out of scope

Do not add, configure, or reference any of the following unless the user
asks for it directly in a later request:

- Docker / docker-compose
- Kubernetes
- CI/CD (GitHub Actions, etc.)
- Terraform or any IaC
- Cloud deployment (AWS/Vercel/Render/etc.)
- Prometheus / Grafana
- Packaging/distribution tooling

Local dev only: Python venv, local Postgres, local Redis.

## 3. Repo layout

```
real-estate-agent/
  app/
    api/
      routes/
        leads.py
        workflows.py
        webhooks.py
      deps.py
      main.py
    core/
      config.py
      security.py
      logging.py
    db/
      models/
      migrations/          # alembic
      session.py
    agents/
      state.py              # typed workflow state
      graph.py               # LangGraph StateGraph wiring
      supervisor.py
      qualification.py
      inventory.py
      recommendation.py
      followup.py
      crm.py
    mcp/
      client.py
      registry.py
      servers/
        crm_server.py
        inventory_server.py
        calendar_server.py
        messaging_server.py
        knowledge_server.py
    llm/
      gateway.py             # LiteLLM wrapper
      guardrails.py          # NeMo Guardrails config and hooks
    events/
      bus.py                 # Redis Streams producer/consumer
      schemas.py              # event payload models
    workers/
      celery_app.py
      tasks.py
    memory/
      workflow_state.py
      conversation.py
      semantic.py
    eval/
      deepeval_suite.py
    observability/
      tracing.py              # OpenTelemetry setup
      logging.py               # Structlog setup
  streamlit_app/
    Home.py
    pages/
      1_Dashboard.py
      2_Lead_Intake.py
      3_Live_Workflow_Monitor.py
      4_Graph_Visualizer.py
      5_Agent_Dashboard.py
      6_MCP_Explorer.py
      7_Workflow_Inspector.py
      8_Memory_Explorer.py
      9_Prompt_Studio.py
      10_LangSmith.py
      11_Evaluation_Center.py
      12_Knowledge_Base.py
      13_Conversation_Explorer.py
      14_Documentation.py
  prompts/
    supervisor.md
    qualification.md
    inventory.md
    recommendation.md
    followup.md
    crm.md
  data/
    seed/
      leads.json
      properties.json
      faqs.json
  tests/
    test_agents/
    test_mcp/
    test_api/
    test_workflow.py
  scripts/
    seed_db.py
    run_worker.sh
  docs/
    architecture.md
    agents.md
    mcp.md
    api.md
  alembic.ini
  pyproject.toml
  .env.example
  README.md
```

Keep files small. If an agent file, route file, or MCP server file goes past
~250 lines, split it. No god-files.

---

## 4. Build phases

### Phase 0: Scaffolding

Deliverables:
- `pyproject.toml` with dependencies (fastapi, uvicorn, sqlalchemy>=2,
  alembic, psycopg, redis, celery, pydantic>=2, langgraph, langchain-core,
  litellm, langsmith, deepeval, opentelemetry-sdk, structlog, streamlit)
- `.env.example` with every config var the app reads (DB url, Redis url,
  API keys as placeholders, LangSmith project, etc.)
- `app/core/config.py`: Pydantic Settings class reading from `.env`
- `app/core/logging.py`: Structlog config
- Empty `README.md` with just the project name and a one-paragraph
  description (expand later in Phase 9)

Definition of done: `uvicorn app.api.main:app` boots with a `/health`
endpoint returning 200. No agents, no DB models yet.

### Phase 1: Database and models

Deliverables:
- SQLAlchemy 2 models: `Lead`, `Customer`, `Property`, `Conversation`,
  `Message`, `WorkflowExecution`, `WorkflowCheckpoint`, `Event`,
  `AgentExecution`, `ToolInvocation`
- Alembic set up, first migration generated and applied
- `app/db/session.py` with a scoped session / dependency for FastAPI

Definition of done: `alembic upgrade head` runs clean against a local
Postgres instance; a throwaway script can insert and query a `Lead`.

### Phase 2: MCP servers (mocked)

Build each server as a standalone module exposing tools over MCP. Back each
one with the seed JSON data (Phase 9 data, but stub in Phase 2 with a few
hardcoded records so this phase isn't blocked).

- `crm_server.py`: create_lead, update_stage, fetch_customer, add_note
- `inventory_server.py`: search_properties, property_details, availability
- `calendar_server.py`: available_slots, book_visit, cancel_visit
- `messaging_server.py`: send_message, send_reminder, conversation_history
- `knowledge_server.py`: faq_lookup, builder_policies, payment_plans

Deliverables:
- `app/mcp/registry.py`: central registry mapping server name to tool list
  to schema, so the dashboard's MCP Explorer can introspect it later
- `app/mcp/client.py`: thin client agents use to call any registered tool

Definition of done: a test script can list all tools in the registry and
successfully invoke one tool per server, get a well-typed response back.

### Phase 3: LiteLLM gateway and guardrails

Deliverables:
- `app/llm/gateway.py`: single entrypoint `call_model(role, messages, ...)`
  that routes qualification to GPT, recommendation to Claude, summary to
  Gemini (model names configurable via `.env`, not hardcoded)
- `app/llm/guardrails.py`: NeMo Guardrails config covering prompt
  injection, invalid tool call shape, unsafe output, schema violation

Definition of done: `call_model` returns a structured response for at least
one real provider call (use whichever API key is available in `.env`), and
a deliberately malformed input is caught by guardrails before reaching the
model.

### Phase 4: Agent state and LangGraph wiring

This is the core of the system. Take your time here.

Deliverables:
- `app/agents/state.py`: the typed `WorkflowState` (lead, customer,
  conversation, qualification, workflow_status, current_node,
  pending_tasks, tool_history, decision_history, memory, metadata,
  checkpoint_id, execution_id)
- One file per agent (`supervisor.py`, `qualification.py`, `inventory.py`,
  `recommendation.py`, `followup.py`, `crm.py`), each agent is a node
  function `(state) -> state`, calling `llm.gateway` and `mcp.client` as
  needed
- `app/agents/graph.py`: wires the StateGraph. Supervisor routes to each
  specialist, decision router branches to follow-up/appointment/escalate/
  lost, every node checkpoints via LangGraph's Postgres checkpointer
- Human review node: graph interrupt before CRM update when qualification
  confidence is low or the customer explicitly asks for a human

Definition of done: running the graph in-process against a seeded lead
produces a full trace from `LeadCreated` through to `WorkflowCompleted` (or
a pause at the human review node), with a checkpoint written after each
node.

### Phase 5: Events, Redis Streams, Celery

Deliverables:
- `app/events/schemas.py`: pydantic models for LeadCreated, LeadQualified,
  InventoryMatched, RecommendationGenerated, CustomerResponded,
  AppointmentBooked, FollowupScheduled, WorkflowPaused, WorkflowResumed,
  WorkflowCompleted
- `app/events/bus.py`: publish/consume against Redis Streams
- `app/workers/celery_app.py` plus `tasks.py`: a worker that consumes
  `LeadCreated` events and kicks off the graph execution

Definition of done: publishing a `LeadCreated` event via a script results
in a Celery worker picking it up and running the graph to completion,
visible in the DB as a `WorkflowExecution` row.

### Phase 6: FastAPI gateway

Deliverables:
- `POST /leads`: create a lead, publish `LeadCreated`
- `POST /webhooks/customer-reply`: simulate inbound customer message
- `GET /workflows/{id}`: workflow status and current node
- `GET /workflows/{id}/timeline`: full event/checkpoint history
- Basic auth (API key header is fine, this is not the focus)

Definition of done: the full loop works over HTTP. Create a lead via
curl/Postman, see it flow through the graph, query its status.

### Phase 7: Observability

Deliverables:
- `app/observability/tracing.py`: OpenTelemetry instrumentation across
  API, agents, tools, DB, queue
- LangSmith wired into the LLM gateway calls (traces, token usage, cost)
- DeepEval suite in `app/eval/deepeval_suite.py` covering hallucination,
  faithfulness, relevance, tool correctness, routing correctness

Definition of done: a workflow run produces a LangSmith trace and a
DeepEval report can be generated against a small eval dataset.

### Phase 8: Streamlit console

Build pages in this order, each one functional before moving to the next:
Dashboard, Lead Intake, Live Workflow Monitor, Graph Visualizer,
Agent Dashboard, MCP Explorer, Workflow Inspector, Memory Explorer,
Prompt Studio, LangSmith viewer, Evaluation Center, Knowledge Base,
Conversation Explorer, Documentation.

Definition of done: each page reads real data from Postgres/Redis/LangSmith,
with no hardcoded mock numbers in the final version of a page.

### Phase 9: Seed data, docs, polish

Deliverables:
- Realistic seed data: ~20 leads, ~40 properties, ~15 FAQs
- `docs/architecture.md`, `docs/agents.md`, `docs/mcp.md`, `docs/api.md`
- Full `README.md`: what it is, architecture diagram (ASCII is fine),
  setup instructions, how to run a sample workflow end to end

Definition of done: someone with no context can clone the repo, follow the
README, and watch a lead go through the full workflow.

---

## 5. Coding standards

- Python 3.11+, type hints everywhere, Pydantic v2 for all structured data
- No comment explaining what the code obviously does. Comment only the
  non-obvious "why," not the "what"
- No leftover TODOs. If something's a stub (like a mock MCP server), it
  should say so once at the top of the file, not scattered through it
- Repository pattern for DB access, service layer between routes and
  agents. Don't call the DB directly from a route handler
- Real tests for agents, MCP servers, and the workflow graph, not just API
  smoke tests
- Prefer explicit over clever. This needs to read like production code a
  team would maintain, not a demo
