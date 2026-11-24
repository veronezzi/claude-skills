#!/usr/bin/env python3
"""CLI para gerenciar o application tracker (kanban).

Uso:
  python tracker.py list [--file tracker.yaml]
  python tracker.py add "Empresa" "Cargo" "Plataforma"
  python tracker.py move <id> <status>
  python tracker.py note <id> "texto"
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_FILE = Path.home() / ".curriculo-vagas" / "tracker.yaml"
STATUSES = ["Applied", "Screening", "Interview", "Offer", "Rejected"]


def load(path):
    path = Path(path)
    if not path.exists():
        return {"applications": []}
    text = path.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text) or {"applications": []}
    # fallback JSON
    return json.loads(text)


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml:
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def next_id(data):
    ids = [a.get("id", 0) for a in data.get("applications", [])]
    return (max(ids) if ids else 0) + 1


def cmd_list(args):
    data = load(args.file)
    apps = data.get("applications", [])
    if not apps:
        print("Nenhuma candidatura registrada.")
        return
    for a in apps:
        print(f"[{a.get('id')}] {a.get('company')} | {a.get('role')} | {a.get('status')} | {a.get('platform')} | {a.get('applied_date')}")


def cmd_add(args):
    data = load(args.file)
    from datetime import date
    app = {
        "id": next_id(data),
        "company": args.company,
        "role": args.role,
        "platform": args.platform,
        "applied_date": str(date.today()),
        "status": "Applied",
        "next_action": "",
        "notes": "",
    }
    data.setdefault("applications", []).append(app)
    save(args.file, data)
    print(f"Adicionado: [{app['id']}] {app['company']} - {app['role']}")


def cmd_move(args):
    data = load(args.file)
    for a in data.get("applications", []):
        if a.get("id") == args.id:
            if args.status not in STATUSES:
                print(f"Status inválido. Use: {', '.join(STATUSES)}", file=sys.stderr)
                sys.exit(1)
            a["status"] = args.status
            save(args.file, data)
            print(f"[{a['id']}] -> {args.status}")
            return
    print(f"ID {args.id} não encontrado.", file=sys.stderr)
    sys.exit(1)


def cmd_note(args):
    data = load(args.file)
    for a in data.get("applications", []):
        if a.get("id") == args.id:
            a["notes"] = args.text
            save(args.file, data)
            print(f"Nota atualizada para [{a['id']}]")
            return
    print(f"ID {args.id} não encontrado.", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Application tracker CLI")
    parser.add_argument("--file", default=str(DEFAULT_FILE))
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="Listar candidaturas")
    p_list.set_defaults(func=cmd_list)

    p_add = sub.add_parser("add", help="Adicionar candidatura")
    p_add.add_argument("company")
    p_add.add_argument("role")
    p_add.add_argument("platform")
    p_add.set_defaults(func=cmd_add)

    p_move = sub.add_parser("move", help="Mover status")
    p_move.add_argument("id", type=int)
    p_move.add_argument("status")
    p_move.set_defaults(func=cmd_move)

    p_note = sub.add_parser("note", help="Adicionar nota")
    p_note.add_argument("id", type=int)
    p_note.add_argument("text")
    p_note.set_defaults(func=cmd_note)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
