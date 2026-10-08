"""
certificado.py — gerador de certificados fictícios (comando /certificado).

O certificado só é emitido para trilhas que existem em trilhas_geo.json, e a
lista de "conteúdos dominados" vem dos módulos da própria trilha.
"""

import os
import random
import re
from datetime import date
from typing import Any, Dict, Optional, Tuple

from .dados import normalizar_nivel
from .trilhas import buscar_trilhas


def parsear_argumentos(args: str) -> Tuple[str, str, Optional[str]]:
    """Divide 'Nome | Trilha [| Nível]' em (nome, trilha, nivel).

    Levanta ValueError se faltar nome ou trilha.
    """
    partes = [p.strip() for p in args.split("|")]
    partes = [p for p in partes if p]
    if len(partes) < 2:
        raise ValueError("Use o formato: Nome | Trilha [| Nível]")
    nome, trilha = partes[0], partes[1]
    nivel = partes[2] if len(partes) > 2 else None
    return nome, trilha, nivel


def gerar_certificado(
    nome_usuario: str,
    nome_trilha: str,
    nivel: Optional[str] = None,
    seed: Optional[int] = None,
    hoje: Optional[date] = None,
) -> Dict[str, Any]:
    """Monta os dados do certificado.

    Levanta ValueError se a trilha não existir ou se o termo for ambíguo
    (por exemplo 'Python' sem nível, já que há três trilhas de Python).
    """
    nome_usuario = nome_usuario.strip()
    if not nome_usuario:
        raise ValueError("Informe o nome da pessoa.")

    achadas = buscar_trilhas(nome_trilha, nivel)
    if not achadas:
        raise ValueError(f"Nenhuma trilha encontrada para '{nome_trilha}'.")
    if len(achadas) > 1:
        opcoes = "; ".join(f"{t['nome']} ({t['nivel']})" for t in achadas)
        raise ValueError(
            f"'{nome_trilha}' corresponde a mais de uma trilha: {opcoes}. "
            "Informe o nível ou o nome completo."
        )

    trilha = achadas[0]
    hoje = hoje or date.today()
    codigo = f"GEO-{hoje.year}{random.Random(seed).randint(100000, 999999)}"
    return {
        "nome": nome_usuario,
        "trilha": trilha["nome"],
        "tecnologia": trilha["tecnologia"],
        "nivel": trilha["nivel"],
        "xp_total": trilha["xp_total"],
        "carga_horaria": trilha["carga_horaria"],
        "conteudos": list(trilha["modulos"]),
        "codigo": codigo,
        "data_emissao": hoje.strftime("%d/%m/%Y"),
    }


def formatar_certificado(c: Dict[str, Any]) -> str:
    primeiro_nome = c["nome"].split()[0]
    conteudos = "\n".join(f"- ✅ {m}" for m in c["conteudos"])
    return (
        "```\n"
        "╔══════════════════════════════════════════════════════════════╗\n"
        "║                                                              ║\n"
        "║              🌎  CERTIFICADO DE CONCLUSÃO  🌎                ║\n"
        "║                       GEO-EXPLORER                           ║\n"
        "║                                                              ║\n"
        "╚══════════════════════════════════════════════════════════════╝\n"
        "```\n\n"
        "**Certificamos que**\n\n"
        f"## {c['nome'].upper()}\n\n"
        "concluiu com êxito a trilha:\n\n"
        f"### 📚 {c['trilha']}\n\n"
        f"> *{c['tecnologia']} · Nível {c['nivel']} · {c['carga_horaria']}h · "
        f"{c['xp_total']} XP*\n\n"
        "---\n\n"
        "**Conteúdos dominados:**\n\n"
        f"{conteudos}\n\n"
        "---\n\n"
        "| | |\n|---|---|\n"
        f"| 📅 **Data de emissão** | {c['data_emissao']} |\n"
        f"| 🔖 **Código** | {c['codigo']} |\n"
        "| ✅ **Status** | Concluído com aprovação |\n\n"
        "---\n\n"
        f"🌟 **Parabéns, {primeiro_nome}! Continue explorando.** 🚀\n\n"
        "*Certificado fictício, gerado para fins educacionais. Sem validade oficial.*\n"
    )


def salvar_certificado(c: Dict[str, Any], pasta: str = "docs/certificados-emitidos") -> str:
    """Grava o certificado em Markdown e devolve o caminho do arquivo."""
    os.makedirs(pasta, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", c["nome"].lower()).strip("-") or "aluno"
    caminho = os.path.join(pasta, f"{c['codigo']}-{slug}.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(formatar_certificado(c))
    return caminho
