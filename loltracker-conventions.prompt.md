# Prompt: gerar a skill `loltracker-conventions`

**Onde usar:** Claude Code, com o diretório de trabalho na raiz deste repositório de skills.
**Por que Claude Code:** o `skill-creator` roda os scripts de empacotamento (`package_skill.py`) e o loop de teste; no Claude.ai parte disso é pulada.

---

## ⚠️ Preencher antes de colar

Substitua os valores entre `{{ }}` no prompt abaixo. São os únicos pontos variáveis.

| Parâmetro | Valor | Observação |
|---|---|---|
| `{{ORG}}` | | segmento do pacote: `com.{{ORG}}.loltracker` |
| `{{AGP}}` | `9.3` ou `8.x` | se AGP 9.x: Kotlin embutido (sem plugin `kotlin-android`) e Room via KSP (kapt é incompatível) |
| `{{REPO_APP}}` | | `owner/repo` do repositório do app tracker |

---

## Prompt (copiar daqui para baixo)

Use a skill `skill-creator` para criar uma skill nova chamada `loltracker-conventions`, e salve o resultado em `skills/loltracker-conventions/` neste repositório.

### Contexto — leia antes de escrever qualquer coisa

Existe um repositório Android (`{{REPO_APP}}`) que é um **projeto de estudo para um desenvolvedor iniciante chamado Pedro**. Eu sou o mentor: eu monto esqueleto, infraestrutura, documentação e board; **o Pedro escreve as features**. A skill existe para que qualquer sessão de Claude trabalhando nesse repositório respeite essas regras sem que eu precise repetir o contexto toda vez.

O risco número um que a skill precisa eliminar: alguém pedir "adiciona uma tela" e o Claude responder com **Jetpack Compose**, ou **implementar a feature inteira** — as duas coisas destroem o propósito pedagógico do repo.

### O que a skill deve fazer

Quando triggada, a skill precisa fazer o Claude:

1. **Nunca usar Jetpack Compose**, em nenhuma hipótese, nem como sugestão futura ou comentário do tipo "no futuro dá pra migrar pra Compose". A UI é XML + Android Views, e isso é uma decisão pedagógica deliberada, não uma limitação técnica a ser contornada. Se o Claude achar que Compose seria melhor, ele ignora e segue com XML.
2. **Nunca implementar features pelo Pedro.** Quando o pedido for "faça a tela X" ou "implemente o ViewModel Y", o comportamento correto é entregar esqueleto + `TODO` comentado explicando *o que* fazer ali e *por quê*, nunca o código pronto. Explicar conceito é sempre permitido; escrever a solução no lugar dele não é.
3. Respeitar as convenções técnicas e de nomenclatura do repo (detalhadas abaixo).
4. Escrever issues no formato exato que eu uso (detalhado abaixo).

### Quando a skill deve triggar (isso vai na `description`)

A `description` é o único mecanismo de disparo, então faça-a **explícita e um pouco insistente**. Ela deve disparar sempre que a sessão envolver:

- qualquer trabalho no repositório do tracker de LoL / projeto de estudo do Pedro
- criar, editar ou revisar tela, Fragment, ViewModel, Adapter, layout XML, navegação ou camada de rede/repositório desse app
- escrever ou revisar issues, PRs ou documentação desse repositório
- qualquer menção a "projeto do Pedro", "loltracker", "repo de estudo"

E deve deixar claro na própria description que o projeto **proíbe Jetpack Compose** e que o Claude **não implementa as features** — isso ajuda a disparar mesmo quando o pedido vem disfarçado ("cria um componente de card de partida").

### Convenções que a skill precisa carregar

**Stack fixa:** Kotlin; UI em XML + Android Views; ViewBinding obrigatório (`findViewById` proibido); Material Components com tema Material 3; ConstraintLayout como layout principal; RecyclerView com `ListAdapter` + `DiffUtil`; Single Activity + Fragments com Navigation Component e Safe Args; Retrofit + OkHttp + Kotlinx Serialization; Coroutines/Flow + ViewModel; Room (só a partir da sprint 4); Coil; JUnit + Turbine + MockK. Módulo único `:app`, version catalog em `libs.versions.toml`. AGP {{AGP}}, JDK 17.

**Proibições duras (a skill deve listar e justificar cada uma):**
- Jetpack Compose — nenhuma dependência no `libs.versions.toml`, `buildFeatures { compose = false; viewBinding = true }`, nenhum `ComposeView` dentro de XML
- `findViewField`/`findViewById` — sempre ViewBinding
- Hilt e qualquer framework de DI — a DI é **manual**, via um `AppContainer` simples mais uma `ViewModelProvider.Factory` comentada. Isso é proposital: o Pedro precisa sentir o problema antes de ver a solução
- kapt (se AGP 9.x) — Room vai de KSP
- Commitar a chave da Riot: ela mora em `local.properties`, é exposta via `BuildConfig`, e `local.properties` está no `.gitignore`

**Estrutura de pacotes** (`com.{{ORG}}.loltracker`): `core/network`, `core/util`, `data/remote/api`, `data/remote/dto`, `data/local`, `data/mapper`, `data/repository`, `domain/model`, `domain/repository`, `ui/` (MainActivity + `search/`, `profile/`, `matchdetail/`, `common/`), `di/`. Arquivo novo vai no pacote da camada dele — nada de DTO em `domain/`, nada de model de domínio em `data/remote/dto/`.

**Nomenclatura de layout:** `fragment_*.xml` para tela, `item_*.xml` para item de RecyclerView, `view_*.xml` para componente reutilizável.

**Armadilhas que a skill deve mandar o Claude checar em toda revisão de código ou PR:**
- `_binding` não zerado no `onDestroyView` (vazamento de memória)
- coleta de `StateFlow` no `lifecycleScope` errado em vez de `viewLifecycleOwner.lifecycleScope` + `repeatOnLifecycle`
- `notifyDataSetChanged` em vez de `submitList`
- Adapter recriado a cada emissão em vez de ter a lista atualizada
- estado perdido na rotação
- URLs do Data Dragon montadas sem buscar o `versions.json` primeiro
- chave da Riot expirada (403) tratada como erro genérico

**Fluxo de trabalho:** branch `feat/<numero>-<slug>`, Conventional Commits, PR pequeno, nunca commit direto na `main`, CI verde obrigatório.

**Formato obrigatório de issue** (a skill deve trazer isso como template literal, em português, tom de mentor — direto, sem entregar a resposta, mas sem deixar o Pedro travado sem pista):

```
## Contexto
Por que essa task existe e onde ela encaixa no app.

## Objetivo
Uma frase do resultado esperado.

## Conceito Android novo
O conceito que a task ensina, em 3 a 5 linhas.

## Passo a passo sugerido
Passos, sem código pronto.

## Arquivos provavelmente tocados
Incluindo os XML de res/layout.

## Critérios de aceite
- [ ] checklist verificável

## Armadilhas comuns
As que se aplicam a esta task.

## Dificuldade
N/5 — estimativa: Xh

## Links de estudo
developer.android.com, sempre a versão de Views/XML, nunca a de Compose.
```

Labels de toda issue: sprint, área (`ui`/`data`/`infra`) e dificuldade.

### Estrutura sugerida da skill

Mantenha o `SKILL.md` enxuto (as regras que valem para toda interação) e empurre o resto para `references/`, que o Claude lê só quando precisa. Sugestão, mas ajuste se fizer mais sentido:

- `SKILL.md` — proibições duras, regra de não implementar feature, mapa de pacotes, nomenclatura, e ponteiros claros de quando ler cada reference
- `references/code-review.md` — checklist de revisão de PR e as armadilhas
- `references/issue-template.md` — o formato de issue e o tom de mentor
- `references/stack.md` — versões, `libs.versions.toml`, particularidades do AGP {{AGP}}

Prefira imperativo e explique **por que** cada regra existe — o motivo pedagógico é o que impede o Claude de "otimizar" contra a regra.

### Testes

Antes de empacotar, rode 3 casos de teste e me mostre a saída de cada um. Sugestões — troque se achar que cobrem mal:

1. "Adiciona a tela de detalhe da partida nesse projeto" → esperado: esqueleto + TODOs em XML/Views, **zero** código de feature pronto, **zero** menção a Compose
2. "Escreve a issue da sprint 3 sobre RecyclerView com ListAdapter e DiffUtil" → esperado: issue no formato exato, em português, tom de mentor, sem código da solução, com links de Views/XML
3. "Revisa esse Fragment" (cole um Fragment com `_binding` não zerado no `onDestroyView` e coleta de Flow no `lifecycleScope` errado) → esperado: as duas armadilhas apontadas explicitamente

Depois dos testes e do meu OK: empacote com `package_skill.py`, deixe a pasta em `skills/loltracker-conventions/`, atualize a tabela de skills do `README.md` na raiz do repo, e faça um commit `feat(skills): adiciona loltracker-conventions`. **Não faça push** — eu reviso antes.
