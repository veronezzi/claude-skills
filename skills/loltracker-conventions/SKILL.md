---
name: loltracker-conventions
description: 'Convenções e limites pedagógicos do rift-tracker (veronezzi/rift-tracker), um app Android de estudo para um iniciante chamado Pedro que está aprendendo Android puro (XML/Views), sem Jetpack Compose. Use esta skill sempre que a sessão tocar nesse repositório: criar, editar ou revisar telas, Fragments, ViewModels, Adapters, layouts XML, navegação, camadas de rede/repositório, issues, PRs ou documentação, mesmo quando o pedido não menciona o projeto pelo nome explicitamente (ex: cria um componente de card de partida, adiciona uma tela de busca). Duas regras não negociáveis regem tudo aqui: Jetpack Compose é proibido neste projeto (mesmo como sugestão futura), e o Claude nunca implementa a feature pelo Pedro, o Pedro escreve o código, o Claude entrega esqueleto, TODOs explicativos e explicações de conceito. Dispare esta skill também para projeto do Pedro, loltracker ou repo de estudo.'
---

# Convenções do rift-tracker

O rift-tracker é um projeto de estudo Android. Pedro (iniciante) escreve as features; o mentor (usuário desta sessão) monta esqueleto, infraestrutura, documentação e board. Cada regra abaixo existe para proteger esse propósito pedagógico — otimizar contra elas (ex. "Compose seria mais rápido de implementar aqui") quebra o motivo de o projeto existir.

## As duas regras que nunca cedem

**1. Zero Jetpack Compose.** Nenhuma dependência de Compose no `libs.versions.toml`, `buildFeatures { compose = false; viewBinding = true }` sempre, nenhum `ComposeView` em XML. Não sugerir Compose nem como "melhoria futura" ou comentário. A UI é XML + Android Views porque é isso que o Pedro está aprendendo — não é uma limitação técnica a contornar.

**2. Nunca implementar a feature pelo Pedro.** Pedido como "faz a tela X" ou "implementa o ViewModel Y" → entregar esqueleto (classe, layout, assinaturas de método) + comentários `TODO(Pedro):` explicando *o quê* fazer e *por quê* ali, nunca a lógica pronta. Explicar o conceito por trás é sempre bem-vindo; escrever a solução no lugar dele não. Isso vale para código em respostas de chat e em arquivos — não só em PRs.

Se o pedido for ambíguo sobre isso (ex. "corrige esse bug"), corrigir bugs pontuais é OK — o limite é sobre *features novas*, não sobre manutenção do que já existe.

## Stack fixa

Kotlin · UI em XML + Views · ViewBinding obrigatório (nunca `findViewById`) · Material Components (tema Material 3) · ConstraintLayout como layout principal · RecyclerView com `ListAdapter` + `DiffUtil` · Single Activity + Fragments (Navigation Component + Safe Args) · Retrofit + OkHttp + Kotlinx Serialization · Coroutines/Flow + ViewModel · Room (só a partir da sprint 4) · Coil · JUnit + Turbine + MockK. Módulo único `:app`, version catalog em `libs.versions.toml`. AGP 9.x, JDK 17.

Detalhes de versões e particularidades do AGP 9.x: leia `references/stack.md`.

## Proibições duras (além do Compose)

- **`findViewById`** — sempre ViewBinding.
- **Hilt ou qualquer framework de DI** — a DI aqui é manual: um `AppContainer` simples + uma `ViewModelProvider.Factory` comentada. É proposital: o Pedro precisa sentir a dor do acoplamento manual antes de a ferramenta que resolve isso fazer sentido pra ele.
- **kapt** — o projeto está em AGP 9.x, que embute o Kotlin e não é compatível com kapt. Room usa KSP.
- **Commitar a chave da Riot** — ela vive em `local.properties` (fora do git), exposta via `BuildConfig`. Nunca hardcoded, nunca em texto de PR/issue.

## Estrutura de pacotes

Base: `com.rifttracker.loltracker`

```
core/network, core/util
data/remote/api, data/remote/dto, data/local, data/mapper, data/repository
domain/model, domain/repository
ui/ (MainActivity + search/, profile/, matchdetail/, common/)
di/
```

Arquivo novo vai no pacote da sua camada — nunca DTO em `domain/`, nunca model de domínio em `data/remote/dto/`.

## Nomenclatura de layout

`fragment_*.xml` (tela) · `item_*.xml` (item de RecyclerView) · `view_*.xml` (componente reutilizável).

## Revisão de código / PR

Ao revisar qualquer Fragment, ViewModel, Adapter ou PR deste repo, leia `references/code-review.md` e cheque a lista de armadilhas de lá antes de responder.

## Escrever issues

Toda issue segue um template fixo, em português, tom de mentor. Leia `references/issue-template.md` antes de escrever ou revisar uma issue.

## Fluxo de trabalho

Branch `feat/<numero>-<slug>` · Conventional Commits · PR pequeno · nunca commit direto na `main` · CI verde obrigatório.
