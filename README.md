# claude-skills

Coleção pessoal de [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) — pastas com instruções que o Claude carrega quando o contexto pede, para não ter que repetir convenções toda sessão.

Mantido por **Guilherme** ([@SEU_USUARIO](https://github.com/SEU_USUARIO)).

## Skills

| Skill | O que faz |
|---|---|
| [`loltracker-conventions`](skills/loltracker-conventions/) | Convenções e limites pedagógicos do rift-tracker: proíbe Jetpack Compose e impede o Claude de implementar features pelo Pedro |
| [`apple-design`](skills/apple-design/) | Abordagem da Apple pra motion fluido e design de interface (gestos, springs, materiais translúcidos, tipografia), traduzida pra web — importado de [emilkowalski/skills](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md) |
| [`orchestrator`](skills/orchestrator/) | `/orchestrate` — roteia um pedido multi-etapa pros subagentes especializados certos (roster em [`agents/`](agents/)), com roteamento determinístico por palavra-chave, fan-out paralelo pra etapas independentes e log de decisão. Design e plano completos em [`references/`](skills/orchestrator/references/) |

## Agents

`agents/` guarda subagentes especializados (`.claude/agents/*.md`) que a skill `orchestrator` despacha via Agent tool — cada um com responsabilidade e tools restritas a um domínio.

| Agent | Responsabilidade | Tools |
|---|---|---|
| [`android-architect`](agents/android-architect.md) | Revisão de Clean Architecture + MVVM/MVI | somente leitura |
| [`android-build`](agents/android-build.md) | Diagnóstico e correção de Gradle/build | leitura + escrita |
| [`android-debugger`](agents/android-debugger.md) | Investigação e correção de crashes/ANRs | leitura + escrita |
| [`android-compose`](agents/android-compose.md) | Revisão e correção de UI Jetpack Compose | leitura + escrita |
| [`android-tester`](agents/android-tester.md) | Avaliação de cobertura de testes | somente leitura |

## Prompts

`prompts/` guarda os prompts que **geram** as skills deste repo. A ideia é que a skill seja reprodutível: se ela precisar ser refeita ou adaptada para outro projeto, o prompt é o ponto de partida, não a memória de uma conversa perdida.

| Prompt | Gera |
|---|---|
| [`loltracker-conventions.prompt.md`](prompts/loltracker-conventions.prompt.md) | Convenções do repositório de estudo Android (XML/Views, sem Compose, DI manual) |

## Anatomia de uma skill

```
skills/nome-da-skill/
├── SKILL.md          # obrigatório: frontmatter (name, description) + instruções
├── references/       # docs carregadas sob demanda
├── scripts/          # código executável, quando fizer sentido
└── assets/           # templates, ícones, fontes
```

A `description` do frontmatter é o **único** mecanismo de disparo — é o que fica sempre no contexto do Claude. Ela precisa dizer o que a skill faz **e** em que situações usar, de forma explícita: skills tendem a não disparar quando deveriam.

## Como usar

**Claude Code** — clone e aponte o Claude para a pasta da skill, ou copie para o diretório de skills do projeto:

```bash
git clone https://github.com/SEU_USUARIO/claude-skills.git
cp -r claude-skills/skills/<nome> .claude/skills/
cp -r claude-skills/agents/<nome>.md .claude/agents/   # se a skill usar subagentes
```

**Claude.ai** — instale o arquivo `.skill` empacotado pelas configurações de skills.

## Licença

MIT — ver [LICENSE](LICENSE).
