# Agent Orchestrator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a global `/orchestrate` skill that routes multi-step requests to the right specialist subagent automatically, keeping the main thread's context small by delegating heavy work.

**Architecture:** One skill (`orchestrator`) holds the router/handoff logic and the agent roster table. Five new custom subagents (converted from the existing loose `.md` prompt files) give the roster real Android-specific specialists; everything else in the roster reuses subagents that already exist. No new code, no new dependencies — this is entirely markdown/frontmatter authoring plus manual verification.

**Tech Stack:** Claude Code skills (`SKILL.md` + frontmatter) and custom subagents (`.claude/agents/*.md` + frontmatter). No build system, no test runner — verification is manual invocation.

## Global Constraints

- All files live under `C:\Users\guigu\.claude\` (global scope), not inside the RiftTracker repo — per user decision during design.
- Agents with write access (`android-build`, `android-debugger`, `android-compose`) still follow Claude Code's existing risk-confirmation rules for destructive/risky actions — the skill must not grant an exception.
- Determinism first: the orchestrator must try keyword/regex match against the roster table before falling back to LLM judgment for routing (per design.md "Roteamento em camadas").
- No subagent may call the Agent tool itself — only the orchestrator (main thread) dispatches agents (Claude Code enforces this; the skill text must not instruct otherwise).
- Source spec: `C:\Users\guigu\.claude\skills\orchestrator\design.md` — every section of that file must map to a task below.

---

### Task 1: `android-architect` subagent

**Files:**
- Create: `C:\Users\guigu\.claude\agents\android-architect.md`
- Reference source: `C:\Users\guigu\.claude\skills\android-arch.md`

**Interfaces:**
- Produces: a subagent named `android-architect`, read-only, invoked by the orchestrator (Task 6) for keywords "arquitetura", "clean architecture", "mvvm", "mvi".

- [ ] **Step 1: Read the source prompt**

Read `C:\Users\guigu\.claude\skills\android-arch.md` in full — this becomes the body of the new agent's `description`/instructions, unchanged in substance (it already defines exactly what to check layer by layer).

- [ ] **Step 2: Write the agent definition**

Create `C:\Users\guigu\.claude\agents\android-architect.md`:

```markdown
---
name: android-architect
description: |
  Use this agent to review Android code for Clean Architecture + MVVM/MVI compliance — checking UI/ViewModel, Domain, and Data layer boundaries. Read-only: it reports violations and suggested refactors, it does not edit files. Invoke it when a task involves reviewing or auditing Android architecture, layering, or MVVM/MVI structure.

  Examples:

  <example>
  Context: The orchestrator routed a step tagged "arquitetura" from a user request to review a feature module.
  user: "revisa a arquitetura do módulo de login"
  assistant: "Vou usar o agente android-architect para revisar a conformidade com Clean Architecture."
  <commentary>
  Architecture review requests route to android-architect rather than general-purpose, since it applies a fixed per-layer checklist.
  </commentary>
  </example>
tools: Read, Grep, Glob
model: inherit
---

Analise o código Android fornecido e verifique a conformidade com Clean Architecture + MVVM/MVI.

**Camadas esperadas:**
- **UI (Presentation):** Activities, Fragments, Composables, ViewModels
- **Domain:** UseCases/Interactors, Models de domínio, interfaces de Repository
- **Data:** Implementações de Repository, DataSources (remote/local), DTOs, mapeadores

**Verificações por camada:**

**UI/ViewModel:**
- ViewModel não importa classes Android (Context, View) diretamente
- Estado da UI representado por uma sealed class / data class imutável
- Eventos únicos tratados com Channel ou SharedFlow
- ViewModel usa UseCases, não Repository diretamente

**Domain:**
- UseCases com responsabilidade única
- Entidades de domínio sem dependência de frameworks
- Interfaces de Repository definidas nesta camada

**Data:**
- Repository implementa interface do domain
- DTOs separados das entidades de domínio
- Mapeadores explícitos entre camadas
- Tratamento de erros com Result/sealed class

**Para cada violação encontrada:**
1. Identifique a camada e o arquivo
2. Explique qual princípio está sendo violado
3. Mostre como refatorar corretamente

**Ao terminar, devolva o relatório neste formato exato:**

```
STATUS: concluído
ACHADOS: <bullet points, só o essencial>
PRÓXIMO PASSO SUGERIDO: <texto livre, opcional>
```
```

- [ ] **Step 3: Verify frontmatter is valid YAML**

Run:
```bash
python -c "import yaml,re; t=open(r'C:/Users/guigu/.claude/agents/android-architect.md',encoding='utf-8').read(); fm=t.split('---')[1]; yaml.safe_load(fm); print('OK')"
```
Expected: `OK` (no exception). If `python`/`yaml` isn't available, visually confirm the block between the two `---` lines parses as valid YAML (correct indentation under `description: |`, no stray colons).

- [ ] **Step 4: Commit**

This directory has no git repo (confirmed during design — `C:\Users\guigu\.claude` is not a git repository). Skip `git commit`; the file write itself is the persisted state. Move directly to Task 2.

---

### Task 2: `android-build` subagent

**Files:**
- Create: `C:\Users\guigu\.claude\agents\android-build.md`
- Reference source: `C:\Users\guigu\.claude\skills\android-gradle.md`

**Interfaces:**
- Produces: a subagent named `android-build`, read+write+bash, invoked by the orchestrator for keywords "gradle", "build.gradle", "dependência".

- [ ] **Step 1: Read the source prompt**

Read `C:\Users\guigu\.claude\skills\android-gradle.md` in full.

- [ ] **Step 2: Write the agent definition**

Create `C:\Users\guigu\.claude\agents\android-build.md` using the same structure as Task 1 Step 2, with these differences:
- `name: android-build`
- `description:` explains it handles Gradle/build-script issues (dependency conflicts, version catalogs, build variants, module wiring) and that it can edit `build.gradle(.kts)` files directly, not just report.
- `tools: Read, Grep, Glob, Edit, Write, Bash`
- Body: the full content of `android-gradle.md`, verbatim.
- End the body with the same `STATUS:`/`ACHADOS:`/`PRÓXIMO PASSO SUGERIDO:` report-format block as Task 1.

- [ ] **Step 3: Verify frontmatter is valid YAML**

Same check as Task 1 Step 3, pointed at `android-build.md`.

- [ ] **Step 4: Commit**

No git repo here — skip. Move to Task 3.

---

### Task 3: `android-debugger` subagent

**Files:**
- Create: `C:\Users\guigu\.claude\agents\android-debugger.md`
- Reference source: `C:\Users\guigu\.claude\skills\android-debug.md`

**Interfaces:**
- Produces: a subagent named `android-debugger`, read+write+bash, invoked by the orchestrator for keywords "crash", "stacktrace", "não funciona".

- [ ] **Step 1: Read the source prompt**

Read `C:\Users\guigu\.claude\skills\android-debug.md` in full.

- [ ] **Step 2: Write the agent definition**

Create `C:\Users\guigu\.claude\agents\android-debugger.md` following Task 1's structure:
- `name: android-debugger`
- `description:` explains it investigates crashes/stack traces/unexpected runtime behavior in Android code and can apply the fix directly.
- `tools: Read, Grep, Glob, Edit, Write, Bash`
- Body: the full content of `android-debug.md`, verbatim, ending with the same report-format block.

- [ ] **Step 3: Verify frontmatter is valid YAML**

Same check as Task 1 Step 3, pointed at `android-debugger.md`.

- [ ] **Step 4: Commit**

No git repo here — skip. Move to Task 4.

---

### Task 4: `android-compose` subagent

**Files:**
- Create: `C:\Users\guigu\.claude\agents\android-compose.md`
- Reference source: `C:\Users\guigu\.claude\skills\android-compose\` (check whether this is a file or directory before reading)

**Interfaces:**
- Produces: a subagent named `android-compose`, read+write+bash, invoked by the orchestrator for keywords "compose", "composable", "recomposição".

- [ ] **Step 1: Locate and read the source prompt**

Run `ls C:/Users/guigu/.claude/skills/ | grep -i compose` to confirm whether the source is `android-compose.md` (file, like the others) or a directory with its own `SKILL.md` (it appears in the skills listing as a directory, unlike the other `android-*.md` files — confirm before assuming). Read whatever file actually holds the content.

- [ ] **Step 2: Write the agent definition**

Create `C:\Users\guigu\.claude\agents\android-compose.md` following Task 1's structure:
- `name: android-compose`
- `description:` explains it reviews and fixes Jetpack Compose UI code — composable structure, state hoisting, recomposition performance, previews.
- `tools: Read, Grep, Glob, Edit, Write, Bash`
- Body: the content found in Step 1, verbatim, ending with the same report-format block. If the source file turns out to be generic Compose framework guidance rather than a reviewable checklist, keep it as-is — this task only relocates/wraps it, it doesn't rewrite it.

- [ ] **Step 3: Verify frontmatter is valid YAML**

Same check as Task 1 Step 3, pointed at `android-compose.md`.

- [ ] **Step 4: Commit**

No git repo here — skip. Move to Task 5.

---

### Task 5: `android-tester` subagent

**Files:**
- Create: `C:\Users\guigu\.claude\agents\android-tester.md`
- Reference source: `C:\Users\guigu\.claude\skills\android-test.md`

**Interfaces:**
- Produces: a subagent named `android-tester`, read-only, invoked by the orchestrator for keywords "escrever teste", "unit test", "instrumented test".

- [ ] **Step 1: Read the source prompt**

Read `C:\Users\guigu\.claude\skills\android-test.md` in full.

- [ ] **Step 2: Write the agent definition**

Create `C:\Users\guigu\.claude\agents\android-tester.md` following Task 1's structure:
- `name: android-tester`
- `description:` explains it evaluates unit/instrumented test coverage and quality for Android code and suggests missing test cases — read-only, like `android-architect`, per design.md's roster table.
- `tools: Read, Grep, Glob`
- Body: the full content of `android-test.md`, verbatim, ending with the same report-format block.

- [ ] **Step 3: Verify frontmatter is valid YAML**

Same check as Task 1 Step 3, pointed at `android-tester.md`.

- [ ] **Step 4: Commit**

No git repo here — skip. Move to Task 6.

---

### Task 6: `orchestrator` skill (router + roster + handoff logic)

**Files:**
- Create: `C:\Users\guigu\.claude\skills\orchestrator\SKILL.md`

**Interfaces:**
- Consumes: the five agents from Tasks 1–5 (`android-architect`, `android-build`, `android-debugger`, `android-compose`, `android-tester`), plus the pre-existing `Explore`, `Plan`, `general-purpose`, `pr-review-toolkit:code-reviewer`, `pr-review-toolkit:code-simplifier`, `pr-review-toolkit:silent-failure-hunter`, `pr-review-toolkit:pr-test-analyzer`.
- Produces: the `/orchestrate` slash command, invokable by the user.

- [ ] **Step 1: Write the skill file**

Create `C:\Users\guigu\.claude\skills\orchestrator\SKILL.md`:

```markdown
---
name: orchestrator
description: Coordinates multiple Claude Code subagents for requests that span more than one responsibility (e.g. "revisa a arquitetura e depois corrige o build"). Routes each step to the best-fit specialist agent automatically, using a deterministic keyword match first and LLM judgment as fallback, dispatches independent steps in parallel, and keeps the main thread's context small by delegating heavy work. Use when the user invokes /orchestrate, or explicitly asks to "orquestrar", "coordenar múltiplos agentes", or run a multi-step cross-responsibility task.
---

# Orchestrator

You are acting as a router/coordinator, not an implementer. Delegate all
non-trivial work to subagents via the Agent tool — never do heavy
exploration, long implementation, or deep review yourself in this thread.
Keeping this thread's own context small is the point of this skill.

## Roster

Match each step of the user's request against this table. Try the keyword
column first (regex/substring match, case-insensitive, against the user's
own wording for that step). Only fall back to your own judgment when no
keyword matches.

| Responsibility | Agent (`subagent_type`) | Keywords | Access |
|---|---|---|---|
| Explorar/localizar código | `Explore` | "onde está", "encontrar", "localizar" | read-only |
| Planejar implementação | `Plan` | "planejar", "como implementar" | read-only |
| Implementar código (fallback) | `general-purpose` | (nenhum específico bate) | read+write |
| Revisão de código geral | `pr-review-toolkit:code-reviewer` | "revisar", "code review" | read-only |
| Simplificação/limpeza | `pr-review-toolkit:code-simplifier` | "simplificar", "limpar" | read+write |
| Caça a falhas silenciosas | `pr-review-toolkit:silent-failure-hunter` | "erro engolido", "catch vazio" | read-only |
| Cobertura de testes (PR) | `pr-review-toolkit:pr-test-analyzer` | "cobertura de teste", "faltou testar" | read-only |
| Arquitetura Android | `android-architect` | "arquitetura", "clean architecture", "mvvm", "mvi" | read-only |
| Gradle/build Android | `android-build` | "gradle", "build.gradle", "dependência" | read+write |
| Debug Android | `android-debugger` | "crash", "stacktrace", "não funciona" | read+write |
| Compose/UI Android | `android-compose` | "compose", "composable", "recomposição" | read+write |
| Testes Android | `android-tester` | "escrever teste", "unit test", "instrumented test" | read-only |

## Process

1. **Break down.** Use `TaskCreate` to turn the user's `/orchestrate` request
   into a short list of high-level steps. Keep each step scoped to one
   responsibility from the roster.
2. **Route each step.** For the current step: try the keyword match against
   the roster table. If nothing matches, decide yourself which existing
   agent fits best, or do the step inline only if it's trivial (a single
   file read, a one-line answer) — don't inline anything that the roster
   already covers.
3. **Fan out when independent.** If two or more pending steps don't depend
   on each other's output, dispatch them as multiple `Agent` tool calls in
   the same turn (parallel), not one after another.
4. **Dispatch and log.** Call the Agent tool with the chosen
   `subagent_type`. After it returns, append one line to the routing log
   (see below) before moving on.
5. **Handle the report.** Every agent in the roster returns:
   ```
   STATUS: concluído | bloqueado | precisa-decisão-do-usuário
   ACHADOS: <bullets>
   PRÓXIMO PASSO SUGERIDO: <texto livre, opcional>
   ```
   - `concluído` → `TaskUpdate` that step as completed, move to the next one.
   - `bloqueado` → try the agent's suggested next step, or re-route to a
     different agent if the roster has a better fit; don't retry the same
     agent on the same input more than once.
   - `precisa-decisão-do-usuário` → stop and use `AskUserQuestion`. Do not
     guess on the user's behalf.
6. **Stop conditions.** End the loop when: all `TaskCreate` steps are
   completed (summarize and report to the user), OR 15 agent dispatches
   have happened without completion (stop, explain the current state, ask
   the user how to proceed), OR a step returned
   `precisa-decisão-do-usuário` (per step 5).

## Routing log

Keep one line per dispatch in a scratch file for this session
(`<scratchpad>/orchestrator-log.md`), format:

```
[step] agent=<name> reason=<keyword:"<match>" | llm-judgment> result=<one-line summary of ACHADOS>
```

This is for your own debugging within the session — if a route turns out
wrong, you can point at why it was chosen. Not a formal audit trail.

## Safety

Agents with read+write access (`android-build`, `android-debugger`,
`android-compose`, `general-purpose`, `pr-review-toolkit:code-simplifier`)
still follow Claude Code's normal risk-confirmation rules for destructive
or risky actions (git push, deleting files, etc.). This skill does not
grant any exception — if a dispatched agent's work would normally require
user confirmation, that confirmation still happens.

No agent dispatched from here may call the Agent tool itself — only this
orchestrator thread dispatches agents.
```

- [ ] **Step 2: Verify frontmatter is valid YAML**

Run:
```bash
python -c "import yaml,re; t=open(r'C:/Users/guigu/.claude/skills/orchestrator/SKILL.md',encoding='utf-8').read(); fm=t.split('---')[1]; yaml.safe_load(fm); print('OK')"
```
Expected: `OK`.

- [ ] **Step 3: Confirm the skill is discoverable**

Start a fresh Claude Code session (or ask the current one) and check that
`orchestrator` appears in the available-skills listing (the same listing
this session's `<system-reminder>` shows for other skills). If it doesn't
appear, double check the file is at exactly
`C:\Users\guigu\.claude\skills\orchestrator\SKILL.md` (not nested one level
too deep) and that the frontmatter has both `name` and `description`.

- [ ] **Step 4: Commit**

No git repo here — skip.

---

### Task 7: End-to-end manual verification

**Files:** none created — this task only exercises Tasks 1–6.

**Interfaces:**
- Consumes: the `/orchestrate` skill and all six new agent definitions.

- [ ] **Step 1: Run a two-responsibility request**

In a Claude Code session (any project, since this is global), run:
```
/orchestrate revisa a arquitetura do módulo X e depois verifica se o build.gradle tem alguma dependência quebrada
```
(swap in a real small project/module you have handy, or point it at
RiftTracker's Android module).

- [ ] **Step 2: Check routing**

Confirm the orchestrator:
- Created at least two `TaskCreate` steps.
- Routed the architecture step to `android-architect` (keyword "arquitetura").
- Routed the build step to `android-build` (keyword "build.gradle").
- Wrote two lines to `<scratchpad>/orchestrator-log.md`.

- [ ] **Step 3: Check report handling**

Confirm each dispatched agent's `STATUS`/`ACHADOS` block was reflected in a
`TaskUpdate`, and the orchestrator's final summary to you references both
agents' findings (not just one).

- [ ] **Step 4: Check a trivial/ambiguous request doesn't over-delegate**

Run:
```
/orchestrate qual é a versão do Kotlin usada nesse projeto?
```
Confirm the orchestrator either answers inline (single file read, no
roster match) or routes to `Explore` — it should not spin up multiple
agents for a one-fact lookup.

- [ ] **Step 5: Record the outcome**

If any check in Steps 2–4 fails, fix the relevant agent/skill file (Tasks
1–6) and re-run Step 1. Once all checks pass, the plan is complete — no
commit needed (no git repo in scope).
