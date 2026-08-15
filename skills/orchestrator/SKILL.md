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
