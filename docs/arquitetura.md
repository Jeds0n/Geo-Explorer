# Arquitetura do Geo-Explorer

```
              ┌──────────────────────────────┐
              │ geo_explorer/data/*.json     │  ← fonte única de dados
              │  trilhas_geo.json            │
              │  desafios_geo.json           │
              └──────┬────────────┬──────────┘
                     │            │
        ┌────────────┘            └─────────────┐
        ▼                                       ▼
┌──────────────────┐                  ┌───────────────────┐
│ Python (src/)    │                  │ MCP (TypeScript)  │
│ trilhas.py       │                  │ mcp/src/index.ts  │
│ desafio.py       │                  │ 4 tools + 1 recurso│
│ certificado.py   │                  └─────────┬─────────┘
│ cli.py           │                            │
└───────┬──────────┘                            ▼
        │                              Bob / outros clientes MCP
        ▼
  terminal + testes (pytest)

Comandos do Bob (commands/*.md) leem os mesmos JSON via prompt.
```

## Decisões

1. **Dados em JSON, não no código.** Trilhas e desafios podem crescer sem mexer em Python ou TypeScript.
2. **Python e MCP leem os mesmos arquivos.** Evita duas versões da verdade.
3. **Erros explícitos.** Nível inválido, tecnologia inexistente e termo ambíguo geram mensagens claras (`ValueError` no Python, `isError` no MCP).
4. **Certificado só para trilha real.** Os "conteúdos dominados" vêm dos módulos da trilha, sem texto inventado.
5. **Sorteio reproduzível.** `obter_desafio(..., seed=n)` permite testar o aleatório.
6. **Busca exata antes de parcial.** "java" retorna só Java, não JavaScript (bug achado pelos testes).

## Base de dados

- 12 tecnologias × 3 níveis = 36 trilhas (dados fictícios).
- 72 desafios (2 por tecnologia e nível).
- Para adicionar uma tecnologia: inclua as 3 trilhas em `trilhas_geo.json` e os desafios em `desafios_geo.json`. O teste `test_todas_tecnologias_das_trilhas_tem_desafio` avisa se faltar algo.
