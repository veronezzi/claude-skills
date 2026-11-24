# Application tracker (kanban)

## Formato (YAML)

```yaml
applications:
  - id: 1
    company: Empresa X
    role: Desenvolvedor Backend Pleno
    platform: LinkedIn
    applied_date: 2026-01-10
    status: Interview  # Applied | Screening | Interview | Offer | Rejected
    next_action: "Preparar entrevista técnica"
    notes: "Contato: Maria (recrutadora)"
```

## Colunas

- Applied: candidatura enviada.
- Screening: triagem/HR screen.
- Interview: entrevistas em andamento.
- Offer: oferta recebida.
- Rejected: rejeitado (manter para aprendizado).

## Uso

- Atualize o status a cada mudança.
- Registre next_action e data.
- Revise semanalmente: onde estão os gargalos?
- Mantenha em `~/.curriculo-vagas/tracker.yaml` ou no projeto.
