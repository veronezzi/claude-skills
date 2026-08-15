# Orquestrador de agentes (`/orchestrate`) — design

Data: 2026-08-14
Status: aprovado, pronto para plano de implementação

## Objetivo

Uma skill global, ativada por `/orchestrate`, que coordena múltiplos subagentes do
Claude Code (Agent tool) para tarefas que cruzam responsabilidades diferentes,
selecionando automaticamente o melhor agente para cada etapa e evitando que o
contexto da thread principal fique cheio.

## Por que isso funciona com o Agent tool

O Agent tool já isola contexto por natureza: cada subagente roda em contexto
próprio (carrega CLAUDE.md/skills do projeto, mas não o histórico da conversa
principal) e devolve só o relatório final. Isso resolve "não lotar o contexto"
de graça — a skill não precisa reinventar isolamento, só precisa decidir quem
chamar, quando, e o que fazer com a resposta.

Confirmado por pesquisa (ago/2026): scoping de agente por responsabilidade
reduz overhead de contexto de ~16.800 tokens para 3.000–4.300 tokens por
agente (MindStudio, "Sub-Agents Context Management"). O padrão de produção
dominante é "router barato + especialista caro": uma chamada de roteamento
(~200 tokens) seguida de uma chamada de especialista (~1.000 tokens) (Beam.ai,
"6 Multi-Agent Orchestration Patterns"). Claude Code também limita subagentes
a um nível — um subagente não pode chamar o Agent tool de novo (The Prompt
Shelf).

## Arquitetura

```
usuário → /orchestrate <pedido>
              │
              ▼
      [orquestrador = thread principal]
      1. TaskCreate: quebra o pedido em etapas de alto nível
      2. loop:
           a. router determinístico (regex/keywords) tenta casar
              a etapa atual com um agente do roster
           b. se ambíguo → decide com julgamento do próprio LLM
           c. se etapas independentes → fan-out paralelo (vários
              Agent calls no mesmo turno)
           d. despacha o(s) agente(s), aguarda relatório(s)
           e. registra a decisão no log de roteamento
           f. TaskUpdate na etapa; decide próxima etapa com base
              no relatório recebido (roteamento dinâmico)
      3. condição de parada: todas as etapas concluídas, ou
         limite de rodadas atingido, ou decisão que só o usuário
         pode tomar (AskUserQuestion)
      4. resume o resultado final pro usuário
```

O orquestrador **nunca faz o trabalho pesado ele mesmo** (não explora
codebase extensa, não escreve implementação longa) — isso é delegado. Ele só
mantém: a lista de tarefas (`TaskCreate`/`TaskUpdate`), o log de roteamento, e
os relatórios curtos que cada agente devolve.

## Roster de agentes

| Responsabilidade | Agente | Origem | Palavras-chave de roteamento determinístico |
|---|---|---|---|
| Explorar/localizar código | `Explore` | já existe | "onde está", "encontrar", "localizar" |
| Planejar implementação | `Plan` | já existe | "planejar", "como implementar" |
| Implementar código | `general-purpose` | já existe | (fallback de escrita quando nenhum specialist bate) |
| Revisão de código geral | `pr-review-toolkit:code-reviewer` | já existe | "revisar", "code review" |
| Simplificação/limpeza | `pr-review-toolkit:code-simplifier` | já existe | "simplificar", "limpar" |
| Caça a falhas silenciosas | `pr-review-toolkit:silent-failure-hunter` | já existe | "erro engolido", "catch vazio" |
| Cobertura de testes (PR) | `pr-review-toolkit:pr-test-analyzer` | já existe | "cobertura de teste", "faltou testar" |
| Arquitetura Android (Clean/MVVM) | **novo** `android-architect` | de `android-arch.md` | "arquitetura", "clean architecture", "mvvm", "mvi" |
| Gradle/build Android | **novo** `android-build` | de `android-gradle.md` | "gradle", "build.gradle", "dependência" |
| Debug Android | **novo** `android-debugger` | de `android-debug.md` | "crash", "stacktrace", "não funciona" |
| Compose/UI Android | **novo** `android-compose` | de `android-compose.md` | "compose", "composable", "recomposição" |
| Testes Android | **novo** `android-tester` | de `android-test.md` | "escrever teste", "unit test", "instrumented test" |

Os `.md` soltos em `~/.claude/skills/` viram definições reais de subagente em
`~/.claude/agents/*.md` (frontmatter `name`, `description`, `tools`), com
tools restritas ao necessário: `android-architect` e `android-tester` somente
leitura (Read/Grep/Glob), `android-build`/`android-debugger`/`android-compose`
com Edit/Write/Bash liberados por precisarem corrigir código.

## Roteamento em camadas

1. **Determinístico primeiro**: regex/keyword contra a coluna "palavras-chave"
   da tabela acima. Rápido, previsível, sem custo de LLM extra.
2. **LLM como fallback**: só quando a etapa não casa com nenhuma keyword, o
   orquestrador usa julgamento próprio para escolher o agente (ou decide que
   nenhum agente do roster serve e faz a etapa inline, se for trivial).
3. **Fan-out paralelo**: etapas sem dependência entre si (ex: revisão de
   arquitetura + revisão de cobertura de teste no mesmo diff) são despachadas
   no mesmo turno em chamadas paralelas do Agent tool, não em sequência.

## Log de roteamento

Arquivo de estado por sessão (scratchpad), formato simples, uma linha por
decisão:

```
[etapa] agente escolhido | motivo (keyword casada / julgamento LLM) | resumo do relatório recebido
```

Existe para debug quando o roteamento erra o agente — não é auditoria
formal, é o orquestrador conseguir explicar "por que chamei X e não Y" se
perguntado, e você conseguir olhar depois o histórico de uma sessão longa.

## Protocolo de handoff

Todo agente do roster devolve relatório em formato curto e fixo:

```
STATUS: concluído | bloqueado | precisa-decisão-do-usuário
ACHADOS: <bullet points, só o essencial>
PRÓXIMO PASSO SUGERIDO: <texto livre, opcional>
```

O orquestrador usa `STATUS` para decidir se avança, para e pergunta ao
usuário, ou tenta outro agente. `PRÓXIMO PASSO SUGERIDO` é uma dica, não uma
ordem — o roteamento determinístico/LLM do orquestrador ainda decide o
próximo agente real.

## Condição de parada

- Todas as tarefas do `TaskCreate` marcadas concluídas → resume e encerra.
- Limite de rodadas (ex: 15 chamadas de agente) atingido sem conclusão →
  para, explica o estado atual, pergunta ao usuário como prosseguir.
- Um agente devolve `STATUS: precisa-decisão-do-usuário` → orquestrador usa
  `AskUserQuestion`, não decide sozinho.

## Regras de segurança (herdadas, não redefinidas)

Agentes com poder de escrita (`android-build`, `android-debugger`,
`general-purpose`) continuam sob as mesmas regras de ações arriscadas já
válidas pro Claude Code (confirmação antes de ação destrutiva, push, etc.) —
a skill não cria uma via alternativa que pule essas confirmações.

## Fora de escopo (YAGNI)

- Não cria um "agent registry" dinâmico com embeddings/scoring — o roster é
  uma tabela estática editada à mão. Adiciona quando o número de agentes
  passar de ~20 e a tabela ficar difícil de manter.
- Não implementa telemetria de custo/tokens por rota — o log de roteamento é
  só texto, sem dashboard.
- Não permite subagentes chamarem outros subagentes (Claude Code já limita a
  um nível; a skill não tenta contornar isso).

## Arquivos a criar

- `~/.claude/skills/orchestrator/SKILL.md` — a skill em si (lógica do
  orquestrador, roster, protocolo).
- `~/.claude/agents/android-architect.md`
- `~/.claude/agents/android-build.md`
- `~/.claude/agents/android-debugger.md`
- `~/.claude/agents/android-compose.md`
- `~/.claude/agents/android-tester.md`
