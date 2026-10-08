---
description: Gera um certificado fictício de conclusão de trilha
argument-hint: <nome> | <tecnologia ou trilha> [| nível]
---

A pessoa quer um certificado fictício. Parâmetros: **$ARGUMENTS**

Interprete assim, separando por `|`:
1. **Nome** da pessoa.
2. **Trilha**: tecnologia ou nome da trilha.
3. **Nível** (opcional): Básico, Intermediário ou Avançado.

Procure a trilha em `geo_explorer/data/trilhas_geo.json` (sem diferenciar maiúsculas/minúsculas nem acentos).
- Se não existir, **não emita** o certificado: informe e liste as tecnologias disponíveis.
- Se houver mais de uma (ex.: "Python" tem três níveis), pergunte qual nível, mostrando as opções.

Quando houver exatamente uma trilha, use `nome`, `tecnologia`, `nivel`, `carga_horaria`, `xp_total` e a lista `modulos` do arquivo, e gere:

---

```
╔══════════════════════════════════════════════════════════════╗
║              🌎  CERTIFICADO DE CONCLUSÃO  🌎                ║
║                       GEO-EXPLORER                           ║
╚══════════════════════════════════════════════════════════════╝
```

**Certificamos que**

## [NOME EM MAIÚSCULAS]

concluiu com êxito a trilha:

### 📚 [nome da trilha]

> *[tecnologia] · Nível [nivel] · [carga_horaria]h · [xp_total] XP*

**Conteúdos dominados:** liste cada item de `modulos` com "✅".

| | |
|---|---|
| 📅 **Data de emissão** | [data atual, DD/MM/AAAA] |
| 🔖 **Código** | GEO-[ano][6 dígitos aleatórios] |
| ✅ **Status** | Concluído com aprovação |

🌟 **Parabéns, [primeiro nome]! Continue explorando.** 🚀

*Certificado fictício, gerado para fins educacionais. Sem validade oficial.*

---
