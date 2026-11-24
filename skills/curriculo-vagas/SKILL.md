---
name: curriculo-vagas
description: Skill para buscar vagas de emprego em várias plataformas (LinkedIn, Indeed, Glassdoor, Gupy, Catho, Workday, Greenhouse, Lever, Ashby), adaptar o currículo do usuário para uma vaga desejada no padrão de recrutadores (ATS-friendly), gerar CV score 0-100, carta de apresentação, pesquisar empresas, mapear networking, preparar entrevistas, simular entrevistas, negociar salário, planejar a busca e rastrear candidaturas (kanban). Entrevista o usuário sobre experiência e skills, pede o currículo atual, reescreve o currículo com palavras-chave da vaga, gera DOCX + PDF, organiza o perfil do LinkedIn e indica vagas com links de busca filtrados. Adapta a orientação por estágio de carreira (júnior, pleno, sênior, executivo, fracionário). Use sempre que o usuário mencionar currículo, CV, vaga, emprego, candidatura, LinkedIn, recrutador, ATS, entrevista, salário, ou quiser adaptar perfil para uma vaga, mesmo que não peça explicitamente a skill.
---

# curriculo-vagas

Skill bilíngue (português/inglês) para caça de vagas e otimização de carreira.

## Módulos disponíveis

1. CV Optimisation (ATS) — reescreve o CV para a vaga.
2. CV Score — pontua o CV de 0 a 100 com dicas.
3. Cover Letter — carta de apresentação tailor-made.
4. Company Research — inteligência sobre a empresa.
5. Networking Intelligence — quem contatar, caminhos quentes.
6. Interview Prep — perguntas prováveis + respostas estruturadas.
7. Mock Interview — simulação com personas.
8. Post-Interview Coaching — diagnóstico após rejeição.
9. Salary Negotiation — pesquisa de mercado + scripts.
10. Offer Evaluation — matriz de decisão entre ofertas.
11. Job Search Plan — plano de 3 meses com metas semanais.
12. Application Tracker — kanban de candidaturas.
13. LinkedIn Optimisation — headline, about, skills.
14. LinkedIn Content Strategy — ritmo de posts.
15. Portfolio/Fractional Careers — carreiras fracionárias.
16. AI Readiness Assessment — lacunas de IA + roadmap.

Use apenas os módulos que o usuário precisa. Pergunte no início.

## Fluxo geral

### Fase 0 — Configuração (primeira vez)

Crie `~/.curriculo-vagas/config.yaml` (ou `perfil.json`) com: nome, área alvo, senioridade, modalidade, cidade, pretensão salarial, skills, idiomas, formação, experiências, links. Reutilize em sessões futuras. Pergunte se quer atualizar.

### Fase 1 — Entrevista e coleta

Siga `references/interview-script.md`. Uma pergunta por vez. Peça currículo atual (arquivo ou texto) e vaga alvo (URL ou texto). Se não tiver vaga, pule para busca (Fase 6).

### Fase 2 — Análise da vaga

Extraia: título, empresa, requisitos obrigatórios/desejáveis, responsabilidades, palavras-chave, senioridade, modalidade, localização. Liste "já tem" vs "falta". Seja honesto sobre lacunas e sugira mitigação.

### Fase 3 — CV Optimisation (ATS)

Reescreva o CV seguindo `references/ats-rules.md` e `references/cv-templates.md`. Estrutura: cabeçalho, resumo, experiência (bullets com verbo + métrica), formação, skills, idiomas, projetos. Não invente dados.

### Fase 4 — CV Score

Rode `scripts/ats_score.py` (CV vs job description) e complemente com análise qualitativa. Entregue score 0-100 + dicas priorizadas. Ver `references/scoring.md`.

### Fase 5 — Geração de arquivos

Gere DOCX com `scripts/build_cv.py` e PDF (LibreOffice/pandoc). Salve em `output/`. Nome: `Nome_Sobrenome_Cargo.docx`.

### Fase 6 — Busca de vagas

Monte links filtrados por plataforma (ver `references/platforms.md`): LinkedIn, Indeed, Glassdoor, Gupy, Catho, Workday, Greenhouse, Lever, Ashby. Forneça 3-5 vagas de exemplo se pesquisar via browser.

### Fase 7 — Cover Letter

Gere carta de apresentação tailor-made (ver `references/cover-letter.md`): 3-4 parágrafos, gancho, valor, fecho com CTA.

### Fase 8 — Perfil LinkedIn

Gere headline (≤220 chars), about, experiências, skills (top 5 pinadas), recomendações de foto/banner/URL. Ver `references/linkedin.md`.

### Fase 9 — Company Research

Pesquise empresa: financeiro, estratégia, liderança, cultura, notícias. Cite fontes. Ver `references/company-research.md`.

### Fase 10 — Networking Intelligence

Mapeie hiring managers, recrutadores internos, advocates, caminhos quentes. Ver `references/networking.md`.

### Fase 11 — Interview Prep e Mock

Gere perguntas prováveis por cargo, respostas STAR baseadas na experiência real, explique o que o entrevistador avalia. Simule com personas. Ver `references/interview.md`.

### Fase 12 — Post-Interview Coaching

Diagnóstico após rejeição: skill gap vs signal gap vs fit. Ver `references/post-interview.md`.

### Fase 13 — Salary Negotiation e Offer Evaluation

Pesquisa salarial por mercado (BR/US/EU/APAC), scripts de contra-oferta, análise de compensação total, matriz de decisão. Ver `references/salary.md`.

### Fase 14 — Job Search Plan

Plano de 3 meses com metas semanais e ritmo diário. Inclua bem-estar. Ver `references/plan.md`.

### Fase 15 — Application Tracker

Kanban em YAML/JSON: Applied, Screening, Interview, Offer, Rejected. Ver `references/tracker.md`.

### Fase 16 — LinkedIn Content Strategy

Ritmo de posts sustentável baseado em expertise real. Ver `references/content.md`.

### Fase 17 — Portfolio/Fractional Careers

Rate setting, estruturas legais (IR35, LLC/S-Corp), aquisição de clientes, posicionamento. Ver `references/fractional.md`.

### Fase 18 — AI Readiness Assessment

Análise de lacunas de IA + roadmap de upskilling. Ver `references/ai-readiness.md`.

### Fase 19 — Entrega

Entregue: arquivos DOCX/PDF, carta, perfil LinkedIn, links de vagas, checklist de candidatura, tracker atualizado.

## Adaptação por estágio de carreira

Ver `references/career-stages.md`. Ajuste verbos, foco e extensão do CV:
- Júnior: 1 pág, foco em formação, projetos, potencial.
- Pleno: 1-2 pág, resultados, ownership.
- Sênior: 2-3 pág, liderança, arquitetura, impacto no negócio.
- Executivo: 2-3 pág, visão, P&L, transformação.
- Fracionário: portfolio de engajamentos, taxas, disponibilidade.

## Referências

- `references/ats-rules.md`
- `references/cv-templates.md`
- `references/platforms.md`
- `references/interview-script.md`
- `references/scoring.md`
- `references/cover-letter.md`
- `references/linkedin.md`
- `references/company-research.md`
- `references/networking.md`
- `references/interview.md`
- `references/post-interview.md`
- `references/salary.md`
- `references/plan.md`
- `references/tracker.md`
- `references/content.md`
- `references/fractional.md`
- `references/ai-readiness.md`
- `references/career-stages.md`

## Scripts

- `scripts/build_cv.py` — gera DOCX.
- `scripts/ats_score.py` — score ATS por keyword match.

## Observações

- Sempre pergunte antes de inventar dados.
- Entregue arquivos em `output/`.
- Idioma: pergunte se CV em PT ou EN (ou bilíngue). Vagas no exterior = inglês.
- Trate o usuário com respeito; busca de emprego é estressante. Seja direto e sem julgamento.
- Cite fontes em pesquisas de empresa.
