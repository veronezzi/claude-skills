---
description: Roda a skill orchestrator já no modo de retry até passar (loop até funcionar)
argument-hint: Descreva a tarefa e, se souber, o comando que define sucesso (ex. ./gradlew test)
---

# /orchestrator-loop

Atalho para `/orchestrator orchestrator-loop <pedido>`.

Invoque a skill `orchestrator` (ferramenta Skill, `skill: "orchestrator"`,
`args: "orchestrator-loop $ARGUMENTS"`). A skill já sabe interpretar o
primeiro argumento `orchestrator-loop` e força o modo de loop (retry até
passar num critério de sucesso, com teto de tentativas) descrito na seção
"Loop até funcionar" do `SKILL.md` dela para toda a execução, mesmo que o
texto do pedido não tenha nenhuma palavra-chave de loop.

Pedido do usuário: $ARGUMENTS
