---
name: orchestrator
description: Coordinates multiple Claude Code subagents for requests that span more than one responsibility (e.g. "revisa a arquitetura e depois corrige o build"). Routes each step to the best-fit specialist agent automatically, using a deterministic keyword match first and LLM judgment as fallback, dispatches independent steps in parallel, and keeps the main thread's context small by delegating heavy work. Has an "orchestrator-loop" option (`/orchestrator orchestrator-loop <pedido>`) that keeps re-attempting a step against a verification command until it passes, with a capped iteration count, also auto-triggered by phrases like "roda até funcionar"/"insiste até passar". Use when the user invokes /orchestrate, or explicitly asks to "orquestrar", "coordenar múltiplos agentes", or run a multi-step cross-responsibility task.
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
   responsibility from the roster. If the first argument is
   `orchestrator-loop`, strip it from the request text and mark every step
   as loop mode (see "Loop até funcionar" below) before dispatching.
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

## Loop até funcionar (retry até passar)

Gatilho, qualquer um dos dois:

- **Opção explícita `orchestrator-loop`.** O usuário invoca
  `/orchestrator orchestrator-loop <pedido>` (o primeiro argumento é
  literalmente `orchestrator-loop`). Ativa o modo de loop pra toda a
  execução, sem depender de palavra-chave no resto do texto.
- **Palavra-chave no pedido.** Mesmo sem o argumento explícito, frases como
  "roda até funcionar", "insiste até passar", "continua tentando até dar
  certo", "loop até funcionar" ativam o modo de loop pra aquela etapa
  específica.

Isso é um modificador de controle sobre uma etapa já roteada pela tabela de
roster, não uma entrada nova nela: primeiro escolha o agente normal pra
etapa (`android-build`, `android-debugger`, etc.), depois envolva o
despacho nesse loop.

Antes de começar:

1. **Cravar o critério de sucesso.** Pergunte ao usuário, ou use o que já
   estiver claro no pedido, qual comando ou condição define "funcionou":
   `./gradlew test`, `./gradlew assembleDebug`, uma classe de teste
   específica, "app abre sem crash". Sem um critério objetivo e verificável,
   use `AskUserQuestion` em vez de adivinhar.
2. **Definir o teto de tentativas.** Padrão: 5 ciclos por etapa. Avise o
   usuário desse teto antes de começar; ele conta para o limite geral de 15
   dispatches do passo 6 acima, não é um orçamento à parte.

Corpo do loop, repetir até parar:

1. Despachar o agente do roster pra essa etapa, anexando a saída da falha
   anterior se não for a primeira tentativa.
2. Rodar o critério de sucesso (Bash/PowerShell), ou pedir pro próprio
   agente rodar como última ação e reportar a saída bruta, sem resumir.
3. Avaliar o resultado:
   - **Passou** → para o loop, marca a etapa como concluída (`TaskUpdate`),
     segue pra próxima.
   - **Falhou com erro novo** → soma uma tentativa, loga (ver abaixo), volta
     ao passo 1 anexando a nova falha.
   - **Falhou com o mesmo erro duas vezes seguidas** → para de tentar às
     cegas; erro repetido é sinal de que o fix não ataca a causa raiz.
     Reroteia (ex: `Explore` pra achar a causa real antes de tentar de novo)
     ou cai em `precisa-decisão-do-usuário`.
   - **Bateu o teto de tentativas** → para, reporta o que foi tentado e a
     última falha, pergunta ao usuário como seguir. Não segue sozinho além
     do teto combinado.

O critério de sucesso é um comando real (teste, build, lint) e não a opinião
de outro LLM lendo o código: por isso este loop usa só um agente "maker" se
reatacando, sem um "checker" separado por trás.

## Routing log

Keep one line per dispatch in a scratch file for this session
(`<scratchpad>/orchestrator-log.md`), format:

```
[step] agent=<name> reason=<keyword:"<match>" | llm-judgment> result=<one-line summary of ACHADOS>
```

Em loops de retry, acrescente `iter=<n>/<teto>` ao final da linha.

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
