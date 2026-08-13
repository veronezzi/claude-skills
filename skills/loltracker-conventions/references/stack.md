# Stack — rift-tracker

## Versões-base

- Kotlin, AGP 9.x (Kotlin embutido no AGP — não adicionar o plugin `kotlin-android` separado, ele já vem junto e duplicar gera conflito).
- JDK 17.
- Módulo único `:app`. Sem multi-módulo — não é o objetivo pedagógico atual, não sugerir split de módulos.
- Dependências centralizadas em `gradle/libs.versions.toml` (version catalog). Nova dependência entra ali, não como string solta no `build.gradle.kts`.

## Particularidades do AGP 9.x

- **kapt não funciona.** AGP 9.x não é compatível com o plugin `kotlin-kapt`. Qualquer processamento de anotação (Room incluso) usa **KSP**, não kapt.
- **Room só entra na sprint 4.** Antes disso não adicionar a dependência nem sugerir persistência local — o app trabalha só com dados remotos até lá.

## UI

- XML + Android Views, `buildFeatures { compose = false; viewBinding = true }`.
- Material Components, tema Material 3.
- ConstraintLayout como layout principal de tela.
- RecyclerView sempre com `ListAdapter` + `DiffUtil` (nunca `RecyclerView.Adapter` puro com `notifyDataSetChanged`).
- Single Activity + Fragments, navegação via Navigation Component, argumentos via Safe Args (nunca `Bundle` manual entre fragments).

## Rede e dados

- Retrofit + OkHttp + `kotlinx.serialization` para parsing (não Gson, não Moshi).
- Coroutines + `Flow` para assincronia, exposto ao Fragment via `ViewModel` (`StateFlow`/`SharedFlow`).
- Coil para carregar imagens (ícones de campeão, splash art) — não Glide, não Picasso.

## DI

Manual: um `AppContainer` (classe simples que instancia e expõe as dependências) + uma `ViewModelProvider.Factory` comentada explicando o papel dela. Sem Hilt, Koin ou qualquer framework de injeção — é proposital, ver `SKILL.md`.

## Testes

JUnit para testes unitários, Turbine para testar `Flow`/`StateFlow`, MockK para mocks (não Mockito).

## Segredos

A Riot Developer Key expira a cada 24h. Fica em `local.properties` (fora do git, no `.gitignore`), exposta ao código via `BuildConfig` (`BuildConfig.RIOT_API_KEY`). Nunca hardcoded, nunca em texto de commit/PR/issue.

## Data Dragon

Os assets estáticos da Riot (ícones, splash arts) são versionados por um `versions.json` que muda com frequência. Sempre buscar essa versão antes de montar qualquer URL de asset — nunca hardcodar uma versão de Data Dragon no código.
