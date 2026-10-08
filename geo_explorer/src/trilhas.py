"""
trilhas.py — consulta de trilhas de estudo (comando /trilha e /listar).
"""

from typing import Any, Dict, List, Optional

from .dados import carregar_trilhas, normalizar, normalizar_nivel


def buscar_trilhas(
    tecnologia: str,
    nivel: Optional[str] = None,
    trilhas: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Trilhas da tecnologia ou nome informado (sem acento, sem caixa).

    Usa correspondência exata quando existe; senão, busca parcial.

    Se ``nivel`` for informado, filtra também pelo nível.
    """
    if trilhas is None:
        trilhas = carregar_trilhas()
    termo = normalizar(tecnologia)
    if not termo:
        return []
    # Correspondência exata tem prioridade: "java" não deve trazer "JavaScript".
    achadas = [
        t for t in trilhas
        if termo in (normalizar(t["tecnologia"]), normalizar(t["nome"]))
    ]
    if not achadas:
        achadas = [
            t for t in trilhas
            if termo in normalizar(t["tecnologia"]) or termo in normalizar(t["nome"])
        ]
    if nivel:
        nivel_ok = normalizar_nivel(nivel)
        achadas = [t for t in achadas if t["nivel"] == nivel_ok]
    return achadas


def listar_tecnologias(trilhas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
    """Tecnologias disponíveis, em ordem alfabética, sem repetição."""
    if trilhas is None:
        trilhas = carregar_trilhas()
    return sorted({t["tecnologia"] for t in trilhas})


def formatar_promocao(trilha: Dict[str, Any]) -> str:
    promo = trilha.get("promocao", {})
    if promo.get("ativa"):
        return f"Desconto de {promo['desconto_percentual']}% válido até {promo['validade']}."
    return "Nenhuma promoção ativa no momento."


def formatar_lives(trilha: Dict[str, Any]) -> List[str]:
    return [
        f"{live['titulo']} — {live['data']} às {live['horario']}"
        for live in trilha.get("lives", [])
    ]


def formatar_trilha(trilha: Dict[str, Any]) -> str:
    linhas = [
        f"## {trilha['nome']}",
        f"Tecnologia    : {trilha['tecnologia']}",
        f"Nível         : {trilha['nivel']}",
        f"Carga horária : {trilha['carga_horaria']}h",
        f"XP total      : {trilha['xp_total']} XP",
        f"Vagas         : {trilha['vagas_disponiveis']} disponíveis",
        "",
        "### Módulos",
    ]
    for i, titulo in enumerate(trilha["modulos"], start=1):
        linhas.append(f"{i}. {titulo}")
    linhas += ["", "### Lives agendadas"]
    linhas += [f"- {live}" for live in formatar_lives(trilha)]
    linhas += ["", "### Promoção", formatar_promocao(trilha)]
    return "\n".join(linhas)
