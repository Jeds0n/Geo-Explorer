"""
cli.py — uso pelo terminal.

    python -m geo_explorer.src.cli listar
    python -m geo_explorer.src.cli trilha python [--nivel básico]
    python -m geo_explorer.src.cli desafio java avançado
    python -m geo_explorer.src.cli certificado "Ana Souza" python básico [--salvar]
"""

import argparse
import sys
from typing import List, Optional

from .certificado import formatar_certificado, gerar_certificado, salvar_certificado
from .dados import NIVEIS
from .desafio import formatar_desafio, obter_desafio
from .trilhas import buscar_trilhas, formatar_trilha, listar_tecnologias


def criar_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="geo-explorer", description="Geo-Explorer: trilhas, desafios e certificados.")
    sub = p.add_subparsers(dest="comando", required=True)

    sub.add_parser("listar", help="Lista as tecnologias disponíveis")

    t = sub.add_parser("trilha", help="Mostra o plano de estudos de uma tecnologia")
    t.add_argument("tecnologia")
    t.add_argument("--nivel", help=f"Filtra por nível ({', '.join(NIVEIS)})")

    d = sub.add_parser("desafio", help="Gera um desafio de código")
    d.add_argument("tecnologia")
    d.add_argument("nivel", nargs="?", default="Intermediário")

    c = sub.add_parser("certificado", help="Gera um certificado fictício")
    c.add_argument("nome")
    c.add_argument("trilha", help="Tecnologia ou nome da trilha")
    c.add_argument("nivel", nargs="?")
    c.add_argument("--salvar", action="store_true", help="Grava em docs/certificados-emitidos/")
    return p


def executar(argv: Optional[List[str]] = None) -> int:
    args = criar_parser().parse_args(argv)
    try:
        if args.comando == "listar":
            print("\n".join(f"- {t}" for t in listar_tecnologias()))
        elif args.comando == "trilha":
            achadas = buscar_trilhas(args.tecnologia, args.nivel)
            if not achadas:
                techs = ", ".join(listar_tecnologias())
                print(f"Nenhuma trilha encontrada para '{args.tecnologia}'. Disponíveis: {techs}.")
                return 1
            print("\n\n---\n\n".join(formatar_trilha(t) for t in achadas))
        elif args.comando == "desafio":
            print(formatar_desafio(obter_desafio(args.tecnologia, args.nivel)))
        else:
            cert = gerar_certificado(args.nome, args.trilha, args.nivel)
            print(formatar_certificado(cert))
            if args.salvar:
                print(f"Salvo em: {salvar_certificado(cert)}")
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    return 0


def main() -> None:
    sys.exit(executar())


if __name__ == "__main__":
    main()
