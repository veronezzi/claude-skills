# Changelog

Todas as mudanças notáveis deste repositório são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Unreleased]

### Added
- Skill `curriculo-vagas`: caça de vagas + otimização de currículo (ATS-friendly).
  - Entrevista o usuário (área, senioridade, skills, experiência, pretensão salarial).
  - Analisa vaga alvo e lista "já tem" vs "falta".
  - Reescreve CV com verbos de ação, métricas e palavras-chave da vaga.
  - Gera DOCX (build_cv.py) e PDF.
  - CV Score 0-100 com breakdown e top 5 melhorias (ats_score.py).
  - Carta de apresentação tailor-made.
  - Optimização de perfil LinkedIn (headline, about, skills).
  - Pesquisa de empresa com fontes.
  - Networking intelligence (hiring managers, advocates, caminhos quentes).
  - Prep de entrevista (perguntas STAR, mock com personas).
  - Post-interview coaching (skill gap vs signal gap vs fit).
  - Negociação salarial e avaliação de ofertas (BR/US/EU/APAC).
  - Plano de busca de 3 meses com metas semanais.
  - Application tracker (kanban em YAML).
  - LinkedIn content strategy.
  - Carreiras fracionárias/portfolio.
  - AI readiness assessment.
  - Adaptação por estágio de carreira (júnior, pleno, sênior, executivo, fracionário).
  - Plataformas: LinkedIn, Indeed, Glassdoor, Gupy, Catho, Workday, Greenhouse, Lever, Ashby.
- 19 referências em `skills/curriculo-vagas/references/`.
- Scripts `build_cv.py` e `ats_score.py`.

### Changed
- README.md: tabela de skills atualizada com `curriculo-vagas`.

## [1.0.0] - 2026-01-01

### Added
- Skill `orchestrator` com roteamento determinístico e modo orchestrator-loop.
- Skill `apple-design`.
- Skill `loltracker-conventions`.
- Agents Android especializados.
- Comando `/orchestrator-loop`.
