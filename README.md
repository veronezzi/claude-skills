# claude-skills

Coleção pessoal de [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview): pastas com instruções que o Claude carrega quando o contexto pede, para não repetir convenções toda sessão.

Mantido por **Guilherme** ([@veronezzi](https://github.com/veronezzi)).

## Índice

- [Skills](#skills)
- [Agents](#agents)
- [Prompts](#prompts)
- [Anatomia de uma skill](#anatomia-de-uma-skill)
- [Como usar](#como-usar)
- [Licença](#licença)

## Skills

| Skill | O que faz |
|---|---|
| [`orchestrator`](skills/orchestrator/) | `/orchestrator`: roteia um pedido multi-etapa pros subagentes certos (roster em [`agents/`](agents/)), com roteamento determinístico por palavra-chave, fan-out paralelo pra etapas independentes, e log de decisão. Tem uma opção `orchestrator-loop` (`/orchestrator orchestrator-loop <pedido>`) que reexecuta uma etapa até passar num critério de sucesso, com teto de tentativas. Design e plano completos em [`references/`](skills/orchestrator/references/) |
| [`apple-design`](skills/apple-design/) | Abordagem da Apple pra motion fluido e design de interface (gestos, springs, materiais translúcidos, tipografia), traduzida pra web. Importado de [emilkowalski/skills](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md) |
| [`loltracker-conventions`](skills/loltracker-conventions/) | Convenções e limites pedagógicos do rift-tracker: proíbe Jetpack Compose e impede o Claude de implementar features pelo Pedro |

### Exemplo: `orchestrator-loop`

Pra forçar o modo de retry até passar (em vez de depender de palavra-chave
no meio do pedido), passe `orchestrator-loop` como primeiro argumento:

```
/orchestrator orchestrator-loop corrige o build até o ./gradlew assembleDebug passar
```

O orchestrator pergunta o critério de sucesso se não estiver claro, avisa o
teto de tentativas (padrão 5 por etapa) antes de começar, e para sozinho se
o mesmo erro se repetir duas vezes seguidas, em vez de insistir às cegas.
Detalhes completos em [`skills/orchestrator/SKILL.md`](skills/orchestrator/SKILL.md#loop-até-funcionar-retry-até-passar).

## Agents

`agents/` guarda subagentes especializados que a skill `orchestrator` despacha via Agent tool, cada um com responsabilidade e tools restritas a um domínio.

| Agent | Responsabilidade | Tools |
|---|---|---|
| [`android-architect`](agents/android-architect.md) | Revisão de Clean Architecture + MVVM/MVI | somente leitura |
| [`android-build`](agents/android-build.md) | Diagnóstico e correção de Gradle/build | leitura + escrita |
| [`android-debugger`](agents/android-debugger.md) | Investigação e correção de crashes/ANRs | leitura + escrita |
| [`android-compose`](agents/android-compose.md) | Revisão e correção de UI Jetpack Compose | leitura + escrita |
| [`android-tester`](agents/android-tester.md) | Avaliação de cobertura de testes | somente leitura |

## Prompts

Prompts na raiz do repositório **geram** as skills daqui. A ideia é que cada skill seja reprodutível: se precisar ser refeita ou adaptada pra outro projeto, o prompt é o ponto de partida, não a memória de uma conversa perdida.

| Prompt | Gera |
|---|---|
| [`loltracker-conventions.prompt.md`](loltracker-conventions.prompt.md) | Convenções do repositório de estudo Android (XML/Views, sem Compose, DI manual) |

## Anatomia de uma skill

```
skills/nome-da-skill/
├── SKILL.md          # obrigatório: frontmatter (name, description) + instruções
├── references/       # docs carregadas sob demanda
├── scripts/          # código executável, quando fizer sentido
└── assets/           # templates, ícones, fontes
```

A `description` do frontmatter é o único mecanismo de disparo: é o que fica sempre no contexto do Claude. Ela precisa dizer o que a skill faz **e** em que situações usar, de forma explícita, já que skills tendem a não disparar quando deveriam.

## Como usar

**Claude Code**: clone e aponte o Claude pra pasta da skill, ou copie pro diretório de skills do projeto.

```bash
git clone https://github.com/veronezzi/claude-skills.git
cp -r claude-skills/skills/<nome> .claude/skills/
cp -r claude-skills/agents/<nome>.md .claude/agents/   # se a skill usar subagentes
```

**Claude.ai**: instale o arquivo `.skill` empacotado pelas configurações de skills.

## Licença

MIT, ver [LICENSE](LICENSE).
