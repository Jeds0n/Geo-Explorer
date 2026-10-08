# Geo-Explorer — Servidor MCP

Permite que o Bob (ou qualquer cliente MCP) use o Geo-Explorer como ferramentas.
Transporte: **stdio**. Os dados vêm de `geo_explorer/data/*.json`, os mesmos arquivos do Python.

## Ferramentas

| Tool | Equivale a | Parâmetros |
|---|---|---|
| `listar_tecnologias` | `/listar` | — |
| `buscar_trilha` | `/trilha` | `tecnologia`, `nivel` (opcional) |
| `gerar_desafio` | `/desafio` | `tecnologia`, `nivel` (padrão: Intermediário) |
| `gerar_certificado` | `/certificado` | `nome_usuario`, `trilha`, `nivel` (opcional) |

**Recurso:** `trilhas://all` — JSON completo da base de trilhas.

## Instalação

Requer Node.js 18+.

```bash
cd geo_explorer/mcp
npm install
npm run build
```

## Registrar no Bob

Copie `mcp.example.json` para a configuração de MCP do Bob (por exemplo `.bob/mcp.json`),
troque `CAMINHO-ABSOLUTO` pelo caminho real do projeto e reinicie o Bob.

## Exemplos de chamadas

```
buscar_trilha      { "tecnologia": "Java", "nivel": "Básico" }
gerar_desafio      { "tecnologia": "SQL", "nivel": "Avançado" }
gerar_certificado  { "nome_usuario": "Ana Souza", "trilha": "Python", "nivel": "Básico" }
```

## Observações

- Em stdio nunca use `console.log` no código: ele corrompe o protocolo. Logs vão para `stderr`.
- Se a tecnologia tiver vários níveis, `gerar_certificado` pede o nível em vez de adivinhar.
