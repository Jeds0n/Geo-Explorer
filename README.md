# 🌎 Geo-Explorer

Projeto de portfólio construído com apoio do **IBM Bob**: uma experiência de exploração de trilhas de aprendizagem, em que a pessoa pode **consultar uma trilha**, **receber um desafio de código** e **gerar um certificado fictício**.

Todos os dados (trilhas, módulos, lives, desafios) são **fictícios**, criados para este projeto.

## O que ele faz

| Comando | O que faz |
|---|---|
| `/trilha <tecnologia> [nível]` | Plano de estudos: módulos, carga horária, XP, lives e promoção |
| `/desafio <tecnologia> [nível]` | Sorteia um desafio de código com enunciado, entrada, saída, dicas e restrições |
| `/certificado <nome> \| <trilha> [\| nível]` | Gera um certificado fictício em Markdown |
| `/listar` | Lista tecnologias e níveis disponíveis |

**12 tecnologias**, cada uma com níveis Básico, Intermediário e Avançado: **36 trilhas** e **72 desafios**.

| Área | Tecnologias |
|---|---|
| Linguagens | Python, JavaScript, TypeScript, Java, SQL |
| Front-end | React |
| Dados e IA | Análise de Dados, IA Generativa |
| Infra e segurança | Cloud, DevOps, Segurança |
| Colaboração | Git e GitHub |

## Estrutura

```
geo-explorer/
├── geo_explorer/
│   ├── commands/        # comandos do Bob (/trilha, /desafio, /certificado, /listar)
│   ├── data/            # trilhas_geo.json e desafios_geo.json
│   ├── src/             # lógica em Python + CLI
│   └── mcp/             # servidor MCP em TypeScript
├── tests/               # testes automatizados
├── docs/                # arquitetura e decisões
├── requirements.txt
└── README.md
```

## Como executar

Requisitos: Python 3.10+ (o projeto não precisa de bibliotecas externas para rodar).

```bash
git clone https://github.com/Jeds0n/Geo-Explorer.git
cd geo-explorer
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # só para os testes
```

### Pelo terminal

```bash
python -m geo_explorer.src.cli listar
python -m geo_explorer.src.cli trilha python --nivel básico
python -m geo_explorer.src.cli desafio java avançado
python -m geo_explorer.src.cli certificado "Ana Souza" python básico --salvar
```

O nível aceita com ou sem acento (`basico`, `Básico`). Sem nível, `desafio` usa Intermediário.

### Pelo Bob

Abra o projeto no Bob e use os comandos:

```
/trilha python
/trilha sql avançado
/desafio "IA Generativa" intermediário
/certificado Ana Souza | Python | Básico
```

Se o Bob não listar os comandos, copie os arquivos de `geo_explorer/commands/` para a pasta de comandos personalizados do Bob (veja a documentação ou as aulas).

### Exemplo de saída (`trilha`)

```
## Python: Primeiros Passos
Tecnologia    : Python
Nível         : Básico
Carga horária : 20h
XP total      : 5000 XP

### Módulos
1. Variáveis e tipos de dados
2. Condicionais e laços
...
```

## Servidor MCP

O MCP expõe as mesmas funções como ferramentas para outros clientes (`buscar_trilha`, `listar_tecnologias`, `gerar_desafio`, `gerar_certificado`) e o recurso `trilhas://all`.

```bash
cd geo_explorer/mcp
npm install
npm run build
```

Depois registre o servidor no Bob usando `geo_explorer/mcp/mcp.example.json`. Detalhes em [`geo_explorer/mcp/README.md`](geo_explorer/mcp/README.md).

## Como executar os testes

```bash
pytest                                              # todos os testes
pytest --cov=geo_explorer --cov-report=term-missing # com cobertura
python -m unittest discover -s tests -t .           # sem instalar nada
```

São **65 testes** cobrindo a base de dados, busca de trilhas, sorteio de desafios, certificados e a CLI.

## Melhorias que fiz

- **Fonte única de dados:** Python e MCP leem os mesmos JSON.
- **Base ampliada:** 12 tecnologias × 3 níveis, com módulos, lives, promoções e desafios próprios de cada nível.
- **Novo comando `/listar`** e uma **CLI** para usar fora do Bob.
- **Certificado confiável:** só emite para trilhas reais, usa os módulos da trilha como conteúdos e pode ser salvo em arquivo (`--salvar`).
- **Busca tolerante:** ignora acentos e maiúsculas; correspondência exata antes da parcial.
- **Erros claros** para nível inválido, tecnologia inexistente e termo ambíguo.
- **Testes que validam os dados:** se uma tecnologia ficar sem desafio, ou uma trilha sem campo obrigatório, o teste falha. Há também um teste que emite certificado para cada uma das 36 trilhas.

## O que aprendi

- **Divisão em etapas pequenas:** pedir ao Bob uma coisa por vez (estrutura, dados, comando, teste, MCP) e revisar cada arquivo deu resultados melhores do que pedir o projeto inteiro.
- **Separar dados e código:** com trilhas e desafios em JSON, ampliei de 6 para 12 tecnologias sem mexer na lógica; só os testes de dados precisaram de atualização.
- **Testes encontram bugs:** a busca por "java" também retornava "JavaScript". Só percebi ao rodar os testes, e a correção (correspondência exata antes da parcial) virou teste permanente. Quando adicionei TypeScript, outro teste falhou e me mostrou um efeito colateral na busca parcial por "script".
- **Aleatoriedade testável:** usar `seed` no sorteio de desafios e no código do certificado permite testar sem depender do acaso.
- **MCP:** ele transforma funções locais em ferramentas que outros clientes usam. Aprendi que, em servidores stdio, `console.log` corrompe o protocolo, e que erros devem voltar como `isError` em vez de derrubar o servidor.
- **Revisar o que o agente gera:** conferi dados, mensagens de erro e arquivos antes de publicar, e verifiquei que não há segredos no repositório.

## Segurança

Nenhuma senha, token ou chave de API é usada. `.env`, `node_modules/` e certificados emitidos estão no `.gitignore`. Antes de publicar, rode `git status` e revise o que será enviado.

## Aviso

Projeto educacional. Os certificados são fictícios e não têm validade oficial.
