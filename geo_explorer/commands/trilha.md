---
description: Exibe o plano de estudos de uma trilha do Geo-Explorer pela tecnologia informada
argument-hint: <tecnologia> [nível: Básico|Intermediário|Avançado]
---

A pessoa quer consultar a trilha de estudos de: **$ARGUMENTS**

Leia o arquivo `geo_explorer/data/trilhas_geo.json` e localize as trilhas cuja propriedade `tecnologia` (ou `nome`) corresponda ao termo informado, sem diferenciar maiúsculas/minúsculas nem acentos. Se houver correspondência exata, use só ela (ex.: "java" não deve trazer "JavaScript"). Se um nível for informado, mostre apenas esse nível; senão, mostre os três.

Use **somente** os dados do arquivo. Não invente módulos, datas ou números.

Para cada trilha encontrada, formate a resposta assim:

---

## 📚 [nome]

| Informação | Detalhe |
|---|---|
| 🏷️ Tecnologia | [tecnologia] |
| 📊 Nível | [nivel] |
| ⏱️ Carga horária | [carga_horaria]h |
| 🏆 XP total | [xp_total] XP |
| 🪑 Vagas | [vagas_disponiveis] disponíveis |

### 🗂️ Módulos

Liste os itens de `modulos`, numerados a partir de 1.

### 📡 Lives agendadas

- **[titulo]** — [data] às [horario]

### 🎯 Promoção

Se `promocao.ativa` for true: "Desconto de [desconto_percentual]% válido até [validade]."
Se for false: "Nenhuma promoção ativa no momento."

---

Se nenhuma trilha for encontrada, informe isso e liste as tecnologias disponíveis no arquivo.
