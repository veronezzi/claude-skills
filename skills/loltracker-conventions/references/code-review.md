# Revisão de código — rift-tracker

Ao revisar um Fragment, ViewModel, Adapter ou PR deste repo, cheque explicitamente cada item abaixo que se aplique ao código em questão. Aponte o problema e explique o mecanismo (por que aquilo quebra), não só o "conserte X" — o Pedro precisa entender, não decorar a correção.

## Armadilhas conhecidas

- **`_binding` não zerado no `onDestroyView`.** O padrão de ViewBinding em Fragment guarda a binding em uma propriedade nullable (`_binding`) e expõe um getter não-nulo (`binding`). Se `_binding = null` não roda em `onDestroyView`, o Fragment continua segurando a view depois que ela morreu — vazamento de memória em toda navegação.

- **Coleta de `StateFlow`/`Flow` no `lifecycleScope` do Fragment em vez de `viewLifecycleOwner.lifecycleScope` + `repeatOnLifecycle`.** O `lifecycleScope` da Activity/Fragment vive mais que a view. Coletar ali continua rodando (e pode crashar tentando tocar em views destruídas) depois que `onDestroyView` já rodou. O padrão correto é `viewLifecycleOwner.lifecycleScope.launch { repeatOnLifecycle(Lifecycle.State.STARTED) { ... } }`.

- **`notifyDataSetChanged()` em vez de `submitList()`.** Com `ListAdapter` + `DiffUtil`, `notifyDataSetChanged` joga fora o cálculo de diff (perde animação de item e é mais caro). Se o adapter é `ListAdapter`, a atualização de lista é sempre via `submitList`.

- **Adapter recriado a cada emissão do Flow** em vez de instanciado uma vez e atualizado via `submitList`. Recriar joga fora estado de scroll e é desperdício.

- **Estado perdido na rotação.** UI state que devia sobreviver a mudança de configuração (texto de busca, item selecionado, resultado carregado) precisa estar no ViewModel, não em variável do Fragment/Activity.

- **URLs do Data Dragon montadas sem buscar `versions.json` primeiro.** A versão do Data Dragon usada na URL dos assets (ícones de campeão, splash art) muda com frequência; hardcodar uma versão quebra silenciosamente quando a Riot atualiza. Sempre buscar `versions.json` e usar a versão retornada.

- **Chave da Riot expirada (403) tratada como erro genérico.** A Riot Developer Key expira a cada 24h. Um 403 da API da Riot é quase sempre chave expirada, não "erro de rede" — tratar como caso genérico esconde a causa real e confunde o Pedro na hora de debugar.

## Fora de escopo pra revisão de convenção

Bugs de lógica de negócio pontuais e ajustes de UI que não tocam nas regras acima são revisão normal — as armadilhas aqui são especificamente sobre os erros recorrentes desse projeto, não uma lista geral de code review.
