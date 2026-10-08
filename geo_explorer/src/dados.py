"""
dados.py — acesso aos arquivos JSON e utilitários de texto.

Fonte única de dados: tanto o código Python quanto o servidor MCP (TypeScript)
leem os mesmos arquivos em geo_explorer/data/.
"""

import json
import os
import unicodedata
from typing import Any, Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TRILHAS_PATH = os.path.join(DATA_DIR, "trilhas_geo.json")
DESAFIOS_PATH = os.path.join(DATA_DIR, "desafios_geo.json")

NIVEIS = ["Básico", "Intermediário", "Avançado"]


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos e sem espaços nas pontas (para comparações)."""
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return sem_acento.strip().lower()


def normalizar_nivel(nivel: str) -> str:
    """Converte 'basico', 'AVANÇADO' etc. para o nome oficial do nível.

    Levanta ValueError se o nível não existir.
    """
    chave = normalizar(nivel)
    for oficial in NIVEIS:
        if normalizar(oficial) == chave:
            return oficial
    raise ValueError(
        f"Nível inválido: '{nivel}'. Use um destes: {', '.join(NIVEIS)}."
    )


def carregar_trilhas(caminho: str = TRILHAS_PATH) -> List[Dict[str, Any]]:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)["trilhas"]


def carregar_desafios(caminho: str = DESAFIOS_PATH) -> Dict[str, Dict[str, list]]:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)["desafios"]
