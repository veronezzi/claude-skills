#!/usr/bin/env bash
# Cria o repositório PÚBLICO no GitHub e faz o primeiro push.
# Rode a partir da raiz deste diretório, com o gh CLI autenticado (gh auth status).
set -euo pipefail

REPO_NAME="${1:-claude-skills}"

command -v gh >/dev/null || { echo "gh CLI não encontrado: https://cli.github.com"; exit 1; }
gh auth status >/dev/null || { echo "Rode 'gh auth login' primeiro."; exit 1; }

if [ ! -d .git ]; then
  git init -b main
  git add -A
  git commit -m "chore: estrutura inicial do repositório de skills"
fi

# --public é intencional: este repo é para ser público. Revise o conteúdo antes.
gh repo create "$REPO_NAME" --public --source=. --remote=origin --push \
  --description "Coleção pessoal de Agent Skills para o Claude"

echo
echo "Pronto: $(gh repo view --json url -q .url)"
