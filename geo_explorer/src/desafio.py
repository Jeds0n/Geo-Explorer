"""
desafio.py — gerador de desafios de código (comando /desafio).

Os enunciados ficam em data/desafios_geo.json; aqui só sorteamos e formatamos.
"""

import random
from typing import Any, Dict, Optional

from .dados import carregar_desafios, normalizar, normalizar_nivel


def obter_desafio(
    tecnologia: str,
    nivel: str = "Intermediário",
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """Sorteia um desafio para a tecnologia e o nível.

    ``seed`` torna o sorteio reproduzível (útil nos testes).
    Levanta ValueError se a tecnologia ou o nível não existirem.
    """
    nivel_ok = normalizar_nivel(nivel)
    catalogo = carregar_desafios()
    por_tecnologia = {normalizar(nome): (nome, niveis) for nome, niveis in catalogo.items()}

    chave = normalizar(tecnologia)
    if chave not in por_tecnologia:
        disponiveis = ", ".join(sorted(catalogo))
        raise ValueError(
            f"Tecnologia '{tecnologia}' não encontrada. Disponíveis: {disponiveis}."
        )

    nome_oficial, niveis = por_tecnologia[chave]
    desafio = random.Random(seed).choice(niveis[nivel_ok])
    return {"tecnologia": nome_oficial, "nivel": nivel_ok, **desafio}


def formatar_desafio(d: Dict[str, Any]) -> str:
    dicas = "\n".join(f"- {x}" for x in d["dicas"])
    restricoes = "\n".join(f"- {x}" for x in d["restricoes"])
    return (
        f"## Desafio de Código — {d['tecnologia']} ({d['nivel']})\n\n"
        f"### {d['titulo']}\n\n"
        f"**Enunciado:** {d['enunciado']}\n\n"
        f"**Entrada:** {d['entrada']}\n\n"
        f"**Saída esperada:** {d['saida']}\n\n"
        f"**Dicas:**\n{dicas}\n\n"
        f"**Restrições:**\n{restricoes}"
    )
