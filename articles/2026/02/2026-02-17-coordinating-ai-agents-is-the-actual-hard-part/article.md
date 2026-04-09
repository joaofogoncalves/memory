---
title: "AI Can Write Code. Coordinating AI Agents Is the Actual Hard Part."
subtitle: "Building a full-stack SaaS platform with a 12-agent orchestration system using Claude Code custom agents."
date: 2026-02-17
tags: [ai, software-engineering, agents, claude-code]
medium_url: https://medium.com/@joaofogoncalves/ai-can-write-code-coordinating-ai-agents-is-the-actual-hard-part-9d692261e7d4
hero_image: media/hero-single-vs-orchestrated.webp
reading_time: 15
---

## 1. The Scene

I watched it happen on a Tuesday afternoon. A project manager agent read a feature spec, spawned three planning agents in parallel, and waited for all three to finish. A product manager reviewed their output and sent feedback. Then the system shifted gears: backend implementation, frontend picking up the generated types, optimization, simplification, tests, a quality checker running linting and type checks across the entire codebase, a code review, documentation updates. The system updated the draft PR to ready-for-review, and that was it.

No human keyboard input for over an hour, across 30+ files touching both backend and frontend. And the code was production-quality.

But getting here took six weeks of rebuilding everything I thought I knew about using AI for development.

Here's the thesis: most teams are optimizing single-agent prompting. The real productivity leap comes from solving orchestration: how multiple specialized agents coordinate, communicate, and quality-gate their own work. This is a systems design problem, and the principles for solving it transfer better than any specific prompt.

I built this system while developing a full-stack SaaS platform: Django on the backend, React on the frontend, the kind of multi-module application where features span models, schemas, endpoints, components, pages, and tests. What follows is the system, how it evolved, what worked, what didn't, and the principles that transfer regardless of stack or tooling.

## 2. The Problem: Why Single-Agent AI Hits a Ceiling

### The Copilot Plateau

AI-assisted coding has a productivity curve that flatlines faster than most teams expect. The first phase is magical: you ask for a function, it writes a function. You describe a bug, it suggests a fix. You paste an error, it explains it. For isolated tasks (write a utility, add a validation rule, refactor a method), the current generation of AI models is excellent.

The plateau hits when you move from tasks to features.

A feature isn't a function. It's a coordinated change across data models, API endpoints, frontend components, routing, state management, tests, and documentation. AI handles a CRUD endpoint beautifully. Ask it to build a cross-module feature, one that touches models, schemas, API contracts, components, and tests in coordinated sequence, and it starts losing coherence. Planning before implementation. Sequencing between layers. Verification after everything is wired together. A single agent holding all of that context doesn't get slower. It gets confused.

Engineering leaders have felt this gap intuitively. AI helped write a function, great. But who planned which function to write? Who verified it integrates with the existing system? Who checked it didn't break something three modules away?

### The Context Window Trap

A single AI session trying to hold a feature spec, the existing architecture, backend implementation decisions, frontend component patterns, test coverage requirements, and code review criteria simultaneously will lose coherence. This isn't a model intelligence problem. It's an information density problem. The more context you load, the less reliably the model attends to all of it.

You've experienced this as "the AI forgot what I told it earlier." At feature scale, it's more like "the AI is simultaneously trying to be an architect, a developer, a tester, and a reviewer, and doing none of them well."

### The Missing Middle

There's a gap between "AI writes a function" and "AI delivers a feature," and it's not bridged by better models or longer context windows. It's bridged by answering a set of questions that have nothing to do with the model's capabilities:

- Who plans what to build?
- Who builds it, and in what order?
- What inputs does each step need?
- What gates must pass before the next step begins?
- Who verifies the result?

These are orchestration questions. They're the same questions you'd answer when structuring a human engineering team. The missing middle isn't intelligence. It's organization.

## 3. The Insight: AI Agents Need What Human Teams Need

The breakthrough that changed my approach was obvious in hindsight: AI agents need the same organizational structures as human engineering teams.

A single brilliant engineer cannot replace a well-organized team. They can write excellent code, but they can't simultaneously hold the product vision, the system architecture, the implementation details, the test strategy, and the documentation plan with equal depth. We solved this in human organizations decades ago with specialization, workflow, and quality gates.

Single-agent AI has the same limitation. It's not that the model can't reason about architecture or testing or code review. It's that asking one agent to do all of these things in a single session produces the same result as asking one engineer to be the entire team: technically possible, practically mediocre.

What do real engineering teams have that single-agent AI lacks? Specialization, for one. An architect thinks differently from a developer, who thinks differently from a QA engineer. Distinct roles produce distinct perspectives. Teams also have workflow: you plan before you build, build before you test, test before you ship. They have communication through artifacts. The architect produces a blueprint. The developer reads the blueprint. The tester reads the spec. They have quality gates, where work doesn't advance until it meets criteria. And they have state tracking, so everyone knows what phase the project is in.

The design principle that emerged: instead of asking one agent to do everything, build a team of specialists with clear interfaces between them. Define what each agent does, what it receives as input, what it produces as output, and what conditions must hold before the next agent begins.

## 4. The System: A 12-Agent Orchestrated Workflow

The implementation isn't a custom Python framework or a wrapper around an API. Each agent is a markdown file, a Claude Code custom agent definition that specifies the agent's role, constraints, inputs, outputs, and model. The project manager agent orchestrates the workflow by spawning these agents as sub-agents in the prescribed sequence. The entire system is configuration, not code. The tooling here is Claude Code, but the pattern (specialized agents with defined interfaces) applies to any agent framework.

### The Agent Roster

The key insight: constraints define roles more than capabilities. The architect's definition doesn't just say "you are an architect." It explicitly prohibits code generation: no Python classes, no TypeScript interfaces, no function signatures, no import statements, no executable code of any kind. The output must be field tables, relationship diagrams, and API operation descriptions. The boundary between "what to build" and "how to build it" is enforced by prohibition, not suggestion.

Similarly, the project manager is told it never implements code directly. It plans, delegates, tracks, and coordinates. Without this hard constraint, the agent reliably drifts into writing code itself instead of delegating to specialists.

### The 4-Phase Workflow

The system operates in four phases (plus initialization), each with explicit entry conditions, agent assignments, and gates:

**Phase 0: Initialization**
- Create branch, draft PR, state tracker on GitHub Issue
- Gate: infrastructure ready

**Phase 1: Planning (PARALLEL)**
- UI Designer -> design-plan.md
- Architect -> system-plan.md
- Test Writer -> test-plan.md
- Product Manager reviews all three
- Agents revise based on PM feedback
- Gate: all plans complete and reviewed

**Phase 2: Implementation (SEQUENTIAL)**
- Backend Developer -> commit + push
- Frontend Developer -> commit + push
- Code Optimizer -> commit + push
- Code Simplifier -> commit + push
- Gate: each step committed before next begins

**Phase 3: QA & Documentation (SEQUENTIAL)**
- Test Writer (implements tests) -> commit + push
- Quality Checker (ENTIRE codebase) -> commit + push
- Code Reviewer -> review report
- Documentation Expert -> commit + push
- Gate: all checks pass system-wide

**Phase 4: Ready for Review**
- Draft PR -> Ready for Review. Human enters the loop.

The parallel vs. sequential decision is intentional. Planning is embarrassingly parallel. Three agents creating independent perspectives on the same spec don't need to coordinate. The architect doesn't need the UI designer's output, and vice versa. But implementation is intentionally sequential: the frontend developer needs the backend's API types, the optimizer needs the code to exist before optimizing it, and the quality checker needs everything in place before running system-wide checks.

### The Communication Layer

Agents don't talk to each other directly. They communicate through named artifacts stored in defined locations: planning artifacts on the GitHub Issue, implementation artifacts on the Pull Request.

Each agent reads specific inputs and writes a specific output. The project manager orchestrates sequencing; communication is asynchronous and artifact-based. This makes the entire system debuggable. You can inspect any artifact to understand exactly what an agent received as input and what it produced.

## 5. Five Hard-Won Principles

### 5a. Constraints Over Capabilities

The most important word in every agent definition is "NOT."

The architect's definition doesn't just describe what an architect does. It explicitly enumerates what the architect must never produce: no Python class definitions, no Pydantic schema code, no TypeScript interfaces, no function signatures, no import statements, no executable code of any kind. The output format is prescribed as field tables, relationship diagrams, and API operation descriptions. Never implementation.

The project manager's core rule: "Never implements code directly — plans, delegates, tracks, coordinates."

Without these hard constraints, agents drift into each other's territory. The architect starts writing code. The project manager starts implementing instead of delegating. The boundaries blur and you end up back where you started.

Define what an agent cannot do more carefully than what it can do.

### 5b. Gates Over Trust

Every phase transition has an explicit gate. Planning doesn't advance to implementation until all three plans are complete and reviewed. Each implementation step must be committed before the next begins.

But the most important gate is in Phase 3. The quality checker must run six checks (linting, formatting, type checking, and tests for both backend and frontend) across the entire codebase, not just the files changed in this feature. A new feature cannot silently break existing functionality.

Without gates, agents optimistically advance and quality degrades silently. They'll report "looks good" when it isn't, because the default behavior of a language model is to be helpful and move forward, not to block progress.

Don't trust agents to self-assess quality. Build external verification into the workflow.

### 5c. Artifacts Over Conversation

Agents communicate through named artifacts: design-plan.md, system-plan.md, backend-implementation.md. Each agent has defined inputs and outputs. The architect reads pm-spec.md and produces system-plan.md. The backend developer reads pm-spec.md and system-plan.md and produces backend-implementation.md.

This matters because of debuggability. When something goes wrong (and it will), you can inspect any artifact to understand what an agent saw, what it produced, and where the chain broke down. Conversational context is ephemeral. Artifacts persist, and you can version them and inspect them after the fact.

Treat agent outputs as contracts. Name them, store them, make them inspectable.

### 5d. Scoped Changes, Global Verification

The code optimizer and code simplifier are scoped to "only files modified in this feature." They don't touch the rest of the codebase. But the quality checker runs on the entire codebase. Every lint rule, every type annotation, every test, across all modules.

This is an intentional asymmetry. Agents that change things should be scoped tightly. You don't want an optimizer "improving" code in unrelated modules. But agents that verify things should run broadly, because you need to know that your changes didn't break something elsewhere.

Scope changes narrowly. Verify broadly.

### 5e. Model Selection Is a Lever

Not every agent needs the most powerful model. The architect uses the most capable model because its job is structural reasoning about system boundaries and data flows. The project manager uses a faster model because it follows a defined workflow and updates state. That's coordination, not cognition.

Match model capability to task complexity. Over-powering coordination agents wastes tokens and adds latency.

## 6. The Evolution: How the System Grew

### Week 1: The Starting Six

The system began with six agents: a feature orchestrator, a backend implementer, a frontend implementer, a code optimizer, a code reviewer, and a test writer. The orchestrator tried to do too much: planning, coordinating, and making product decisions all at once.

The names reflected implementation thinking. "Backend implementer" sounds like a function call. "Feature orchestrator" sounds like middleware. These weren't just labels. They shaped how the agents behaved.

### Week 2: The Communication Crisis

The original system stored state in files on disk. Planning artifacts lived in a local directory. State tracking was a markdown file that agents read and updated. This worked for a single feature in isolation. It broke the moment anything went wrong. A failed step, a context window limit, a session restart.

The turning point was realizing that GitHub Issues and Pull Requests are already a communication layer designed for multi-person coordination. They have comments, labels, project boards, state tracking, and an API for programmatic updates.

I shifted all artifacts to Issue and PR comments. State tracking moved to a single updatable comment via the GitHub API. Planning artifacts posted to the Issue. Implementation artifacts posted to the PR.

This was the single biggest improvement in the system's reliability. Not because GitHub is a better file system, but because it's a communication layer that already handles persistence, visibility, linking artifacts to context, and surviving session restarts.

### Week 3: The Specialization Expansion

The system grew from 6 to 12 agents. The most important additions were the architect and the product manager.

The architect was the breakthrough. Before it existed, the backend developer was simultaneously deciding what to build and how to build it. Separating architectural decisions from implementation eliminated an entire class of coherence problems. The architect reasons about data models, API contracts, and system boundaries. The developer reads that blueprint and implements it. Each does one thing well.

The product manager created a similar separation: what the user needs vs. what the system needs. The PM reviews all plans through a user-centric lens. Without it, technical elegance sometimes won over user value.

### Week 4: The Naming Revelation

I renamed "feature-orchestrator" to "project-manager" and "backend-implementer" to "backend-developer."

This sounds trivial. It wasn't.

Names shape behavior. "Implementer" tries to implement. It's a verb, an action, a narrow mandate. "Developer" thinks about development more holistically. The same agent definition with a name change produced noticeably different outputs. The "backend-developer" more naturally considered edge cases and integration points that the "backend-implementer" had ignored.

Similarly, "feature-orchestrator" sounded like infrastructure. "Project-manager" sounded like a role with judgment and responsibility. The agent started making better sequencing decisions.

### Weeks 5-6: Quality Layers and Hardening

The final evolution added the code simplifier and the quality checker, and introduced system-wide quality checks, where verification must run on the entire codebase, not just changed files. Early versions also tried to parallelize implementation (backend and frontend simultaneously), which failed because the frontend depends on backend types. Understanding which steps are truly independent took weeks of trial and error. By week six, features started shipping end-to-end.

Key lesson: You cannot design a multi-agent system from scratch. You grow it. Start with minimum viable orchestration and add complexity only when you hit a specific failure mode.

## 7. What Didn't Work (And Still Doesn't)

Honest assessment.

**Token costs are significant.** A 12-agent workflow for a single feature uses substantially more tokens than a single-session implementation. The economics work for complex features that span multiple modules. They don't make sense for small changes, bug fixes, or isolated tasks. Knowing when to use the pipeline vs. a single session is itself a skill.

**The orchestrator is a bottleneck.** The project manager runs sequentially by design. It can't delegate Phase 2 work until Phase 1 completes. On long workflows, it sometimes loses track of state across extended sessions. Context limits are real. When the orchestrator gets confused, the whole pipeline stalls.

**Parallel planning isn't truly parallel.** The sub-agent system has coordination overhead. Three agents spawned "in parallel" are faster than running sequentially, but not 3x faster. There's setup cost, context loading, and result collection.

**Error recovery is manual.** When an agent fails (a test it can't fix, a type error it doesn't understand), the project manager doesn't always recover gracefully. Human intervention remains the escape hatch. The system is semi-automated with a human on call.

**Agents produce plausible-but-wrong output more often than you'd expect.** The architect occasionally designs data models that look reasonable but miss an existing pattern in the codebase. The backend developer sometimes generates an API contract that doesn't match what the frontend needs. These aren't hallucinations in the obvious sense. They're coherent, well-structured, and wrong. The quality gates catch most of it, but human review at the PR stage catches the rest. The system reduces human effort; it doesn't eliminate human judgment.

**Agent definitions are tightly coupled to the project.** They reference specific file patterns, naming conventions, import paths, and quality check commands. This isn't a portable framework. It's a bespoke system for a specific codebase. Porting to another project means rebuilding most of the definitions. The principles transfer; the definitions don't.

## 8. Where This Is Heading: From Manual Orchestration to Native Agent Teams

Everything described so far is manual orchestration. Agent definitions written by hand. Workflow encoded in markdown. Sequencing managed by a project manager agent following instructions. It works, but it's held together by carefully crafted prompts, not by infrastructure.

Claude Code recently shipped an experimental feature called Agent Teams that provides native infrastructure for exactly this pattern. What Agent Teams adds beyond what I built manually:

- Native split-pane display for monitoring all agents at once
- File locking to prevent write conflicts during parallel work
- Plan approval workflows where teammates plan in read-only mode until the lead approves
- Automatic task dependency resolution, so completed tasks unblock downstream work without manual intervention

What this suggests: the pattern of specialized agents with structured workflows is not a hack or a workaround. It's the direction the tooling is moving. Claude Code is building Agent Teams. CrewAI, LangGraph, and AutoGen are converging on similar primitives: role specialization, task dependencies, quality gates, scoped delegation. The specifics differ, but the shape is the same.

Teams that learn orchestration patterns now will be ready to adopt native tooling as it matures. The hard part was never the tooling. It's understanding which workflows benefit from parallelism, where gates should go, how to scope agent responsibilities, and how to design the artifact interfaces between them. That understanding transfers regardless of whether you're wiring agents together with markdown prompts or with a native team coordination layer.

## 9. The Orchestration Imperative

AI agent orchestration, not single-agent prompting, is the productivity lever engineering teams should invest in learning.

The gap between "AI writes code" and "AI delivers features" is a systems design problem. The models are capable enough. What's missing is the organizational layer: who does what, in what order, with what inputs, through what gates, producing what outputs.

You don't need 12 agents to start. Start with 3: a planner, a builder, and a reviewer. Add specialization when you hit a specific failure mode. When the planner is simultaneously making product decisions and architectural decisions, split it into two agents. When quality keeps slipping, add a dedicated checker. When the builder is deciding what to build while building it, add an architect. Grow the system; don't design it from scratch.

The principles transfer across any tooling. Constraints over capabilities. Gates over trust. Artifacts over conversation. Scoped changes with global verification. Model selection as a lever, not an afterthought.

The next time you watch an AI agent generate code, ask yourself: who reviews this? What happens next? Where does it go? If you don't have answers, you have an orchestration problem.
