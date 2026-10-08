---
description: Gera um desafio de código para a tecnologia e o nível informados
argument-hint: <tecnologia> [nível: Básico|Intermediário|Avançado]
---

A pessoa quer um desafio de código. Parâmetros: **$ARGUMENTS**

Interprete assim:
- O primeiro termo é a **tecnologia** (ex.: Python, Java, SQL, "IA Generativa").
- O último termo, se for Básico, Intermediário ou Avançado (com ou sem acento), é o **nível**. Se não houver nível, use **Intermediário**.

Leia `geo_explorer/data/desafios_geo.json`, vá em `desafios[tecnologia][nível]` e **sorteie um** dos desafios da lista. Se a pessoa pedir outro, sorteie de novo, preferindo um que ainda não tenha saído nesta conversa.

Use somente o conteúdo do arquivo e formate assim:

---

## 🧩 Desafio de Código — [tecnologia] ([nível])

### [titulo]

### 📋 Enunciado
[enunciado]

### 📥 Entrada
[entrada]

### 📤 Saída esperada
[saida]

### 💡 Dicas
- [cada item de dicas]

### ⚙️ Restrições
- [cada item de restricoes]

---

> 💬 Quando terminar, envie sua solução e eu faço a revisão!

Se a tecnologia ou o nível não existir no arquivo, diga isso e liste as opções disponíveis.
