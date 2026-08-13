# Formato de issue — rift-tracker

Toda issue escrita ou revisada neste repositório segue o template abaixo, em português, tom de mentor: direto, sem entregar a resposta pronta, mas sem deixar o Pedro travado sem nenhuma pista. Pense em como um mentor escreveria uma task pra alguém aprender fazendo — contexto suficiente pra saber por onde começar, não um passo a passo que vira "copia e cola".

## Template (usar exatamente esta estrutura)

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

## Regras de conteúdo

- **"Passo a passo sugerido"** descreve a sequência de decisões (ex. "crie o ViewHolder", "conecte o `submitList` no coletor do Flow"), nunca o código da solução.
- **"Armadilhas comuns"** puxa apenas as armadilhas do `references/code-review.md` que se aplicam a essa task específica — não colar a lista inteira em toda issue.
- **"Links de estudo"** aponta sempre para a documentação de Views/XML do developer.android.com. Nunca linkar a versão Compose de um artigo, mesmo que seja o resultado mais direto.
- **Labels obrigatórias em toda issue:** sprint, área (`ui`, `data` ou `infra`) e dificuldade.
- Dificuldade e estimativa de horas são um chute honesto pra uma pessoa iniciante, não pra quem já conhece Android.
