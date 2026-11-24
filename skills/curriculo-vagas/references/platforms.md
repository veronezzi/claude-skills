# Padrões de busca de vagas por plataforma

Substitua os placeholders: `{cargo}` (URL-encoded), `{cidade}`, `{uf}`.

## LinkedIn

Busca de vagas:
```
https://www.linkedin.com/jobs/search/?keywords={cargo}&location={cidade}%2C%20{uf}&f_WT=2 (remoto) | f_WT=1 (presencial) | f_WT=3 (híbrido)
```
Filtros úteis: `f_E=2` (entry), `3` (mid), `4` (senior), `f_TPR=r86400` (últimas 24h), `f_TPR=r604800` (última semana).

## Indeed

```
https://br.indeed.com/jobs?q={cargo}&l={cidade}%2C+{uf}&remotejob=0379f-... (remoto)
```
Para remoto, adicione `&remotejob=0379f...` ou use o filtro "Remoto" na UI.

## Glassdoor

```
https://www.glassdoor.com.br/Vaga/{cidade}-{cargo}-vagas-SRCH_IL.0,{n}_IC... .htm
```
Mais simples: busque por `https://www.glassdoor.com.br/Vaga/{cargo}-vagas.htm?locT=C&locId=...`.

## Gupy

```
https://portal.gupy.io/job-search?jobName={cargo}&cityName={cidade}
```
Gupy também permite filtrar por modalidade na UI.

## Catho

```
https://www.catho.com.br/vagas/{cargo}/?cidade={cidade}
```

## Dicas gerais

- Sempre abra os links em nova aba e confirme se a busca retornou resultados.
- Ajuste o cargo para termos mais amplos se retornar poucos resultados (ex.: "Desenvolvedor" em vez de "Desenvolvedor Backend Pleno Node.js").
- Salve as buscas como alertas de e-mail nas plataformas.
- Candidate-se nos primeiros dias após a publicação.
- Use a rede: indique-se no LinkedIn com mensagem curta.
