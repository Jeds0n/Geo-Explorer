#!/usr/bin/env node
/**
 * Geo-Explorer — Servidor MCP (stdio)
 *
 * Ferramentas:
 *   • listar_tecnologias — tecnologias disponíveis        (/listar)
 *   • buscar_trilha      — plano de estudos               (/trilha)
 *   • gerar_desafio      — desafio de código sorteado     (/desafio)
 *   • gerar_certificado  — certificado fictício           (/certificado)
 *
 * Recurso:
 *   • trilhas://all — JSON completo da base de trilhas
 *
 * Os dados vêm de geo_explorer/data/*.json, os mesmos arquivos usados pelo Python.
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// ── Tipos ──────────────────────────────────────────────────────────────────
interface Live { titulo: string; data: string; horario: string }
interface Trilha {
  id: number;
  nome: string;
  tecnologia: string;
  nivel: string;
  carga_horaria: number;
  xp_total: number;
  vagas_disponiveis: number;
  modulos: string[];
  lives: Live[];
  promocao: { ativa: boolean; desconto_percentual: number; validade: string | null };
}
interface Desafio {
  titulo: string; enunciado: string; entrada: string; saida: string;
  dicas: string[]; restricoes: string[];
}
type Catalogo = Record<string, Record<string, Desafio[]>>;

// ── Dados (build/index.js → ../../data) ────────────────────────────────────
const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, "..", "..", "data");
const NIVEIS = ["Básico", "Intermediário", "Avançado"];

function carregarTrilhas(): Trilha[] {
  return JSON.parse(readFileSync(join(DATA_DIR, "trilhas_geo.json"), "utf-8")).trilhas;
}
function carregarDesafios(): Catalogo {
  return JSON.parse(readFileSync(join(DATA_DIR, "desafios_geo.json"), "utf-8")).desafios;
}

// ── Utilitários ────────────────────────────────────────────────────────────
/** minúsculas, sem acentos, sem espaços nas pontas */
function normalizar(texto: string): string {
  return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim().toLowerCase();
}

function normalizarNivel(nivel: string): string {
  const chave = normalizar(nivel);
  const oficial = NIVEIS.find((n) => normalizar(n) === chave);
  if (!oficial) throw new Error(`Nível inválido: '${nivel}'. Use: ${NIVEIS.join(", ")}.`);
  return oficial;
}

function listarTecnologias(trilhas = carregarTrilhas()): string[] {
  return [...new Set(trilhas.map((t) => t.tecnologia))].sort((a, b) => a.localeCompare(b, "pt-BR"));
}

function buscarTrilhas(termo: string, nivel?: string): Trilha[] {
  const trilhas = carregarTrilhas();
  const q = normalizar(termo);
  if (!q) return [];
  // Correspondência exata tem prioridade ("java" não traz "JavaScript")
  let achadas = trilhas.filter((t) => [normalizar(t.tecnologia), normalizar(t.nome)].includes(q));
  if (achadas.length === 0) {
    achadas = trilhas.filter(
      (t) => normalizar(t.tecnologia).includes(q) || normalizar(t.nome).includes(q)
    );
  }
  if (nivel) {
    const n = normalizarNivel(nivel);
    achadas = achadas.filter((t) => t.nivel === n);
  }
  return achadas;
}

// ── Formatação ─────────────────────────────────────────────────────────────
function formatarTrilha(t: Trilha): string {
  const promo = t.promocao.ativa
    ? `Desconto de ${t.promocao.desconto_percentual}% válido até ${t.promocao.validade}.`
    : "Nenhuma promoção ativa no momento.";
  return [
    `## ${t.nome}`,
    `Tecnologia    : ${t.tecnologia}`,
    `Nível         : ${t.nivel}`,
    `Carga horária : ${t.carga_horaria}h`,
    `XP total      : ${t.xp_total} XP`,
    `Vagas         : ${t.vagas_disponiveis} disponíveis`,
    "",
    "### Módulos",
    ...t.modulos.map((m, i) => `${i + 1}. ${m}`),
    "",
    "### Lives agendadas",
    ...t.lives.map((l) => `- ${l.titulo} — ${l.data} às ${l.horario}`),
    "",
    "### Promoção",
    promo,
  ].join("\n");
}

function sortearDesafio(tecnologia: string, nivel: string): string {
  const catalogo = carregarDesafios();
  const nomeOficial = Object.keys(catalogo).find((k) => normalizar(k) === normalizar(tecnologia));
  if (!nomeOficial) {
    throw new Error(
      `Tecnologia '${tecnologia}' não encontrada. Disponíveis: ${Object.keys(catalogo).sort().join(", ")}.`
    );
  }
  const nivelOk = normalizarNivel(nivel);
  const lista = catalogo[nomeOficial][nivelOk];
  const d = lista[Math.floor(Math.random() * lista.length)];
  return [
    `## Desafio de Código — ${nomeOficial} (${nivelOk})`,
    "",
    `### ${d.titulo}`,
    "",
    `**Enunciado:** ${d.enunciado}`,
    "",
    `**Entrada:** ${d.entrada}`,
    "",
    `**Saída esperada:** ${d.saida}`,
    "",
    "**Dicas:**",
    ...d.dicas.map((x) => `- ${x}`),
    "",
    "**Restrições:**",
    ...d.restricoes.map((x) => `- ${x}`),
  ].join("\n");
}

function emitirCertificado(nome: string, termo: string, nivel?: string): string {
  const nomeLimpo = nome.trim();
  if (!nomeLimpo) throw new Error("Informe o nome da pessoa.");
  const achadas = buscarTrilhas(termo, nivel);
  if (achadas.length === 0) throw new Error(`Nenhuma trilha encontrada para '${termo}'.`);
  if (achadas.length > 1) {
    const opcoes = achadas.map((t) => `${t.nome} (${t.nivel})`).join("; ");
    throw new Error(`'${termo}' corresponde a mais de uma trilha: ${opcoes}. Informe o nível.`);
  }
  const t = achadas[0];
  const hoje = new Date();
  const data = hoje.toLocaleDateString("pt-BR");
  const codigo = `GEO-${hoje.getFullYear()}${Math.floor(100000 + Math.random() * 900000)}`;
  return [
    "```",
    "╔══════════════════════════════════════════════════════════════╗",
    "║              🌎  CERTIFICADO DE CONCLUSÃO  🌎                ║",
    "║                       GEO-EXPLORER                           ║",
    "╚══════════════════════════════════════════════════════════════╝",
    "```",
    "",
    "**Certificamos que**",
    "",
    `## ${nomeLimpo.toUpperCase()}`,
    "",
    "concluiu com êxito a trilha:",
    "",
    `### 📚 ${t.nome}`,
    "",
    `> *${t.tecnologia} · Nível ${t.nivel} · ${t.carga_horaria}h · ${t.xp_total} XP*`,
    "",
    "**Conteúdos dominados:**",
    "",
    ...t.modulos.map((m) => `- ✅ ${m}`),
    "",
    "| | |",
    "|---|---|",
    `| 📅 **Data de emissão** | ${data} |`,
    `| 🔖 **Código** | ${codigo} |`,
    "| ✅ **Status** | Concluído com aprovação |",
    "",
    `🌟 **Parabéns, ${nomeLimpo.split(/\s+/)[0]}! Continue explorando.** 🚀`,
    "",
    "*Certificado fictício, gerado para fins educacionais. Sem validade oficial.*",
  ].join("\n");
}

// ── Servidor ───────────────────────────────────────────────────────────────
const texto = (t: string) => ({ content: [{ type: "text" as const, text: t }] });
const erro = (e: unknown) => ({
  content: [{ type: "text" as const, text: `Erro: ${e instanceof Error ? e.message : String(e)}` }],
  isError: true,
});

const server = new McpServer({ name: "geo-explorer", version: "1.0.0" });

server.registerTool(
  "listar_tecnologias",
  { description: "Lista as tecnologias com trilhas disponíveis no Geo-Explorer.", inputSchema: {} },
  async () => texto(listarTecnologias().map((t) => `- ${t}`).join("\n"))
);

server.registerTool(
  "buscar_trilha",
  {
    description:
      "Consulta o plano de estudos (módulos, carga horária, XP, lives e promoção) de uma tecnologia. Equivale ao comando /trilha.",
    inputSchema: {
      tecnologia: z.string().describe('Tecnologia ou nome da trilha, ex.: "Python", "SQL"'),
      nivel: z.string().optional().describe("Básico, Intermediário ou Avançado (opcional)"),
    },
  },
  async ({ tecnologia, nivel }) => {
    try {
      const achadas = buscarTrilhas(tecnologia, nivel);
      if (achadas.length === 0) {
        return texto(
          `Nenhuma trilha encontrada para "${tecnologia}".\n\nDisponíveis: ${listarTecnologias().join(", ")}`
        );
      }
      return texto(achadas.map(formatarTrilha).join("\n\n---\n\n"));
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "gerar_desafio",
  {
    description: "Sorteia um desafio de código para a tecnologia e o nível. Equivale ao comando /desafio.",
    inputSchema: {
      tecnologia: z.string().describe('Ex.: "Python", "Java", "IA Generativa"'),
      nivel: z.string().default("Intermediário").describe("Básico, Intermediário ou Avançado"),
    },
  },
  async ({ tecnologia, nivel }) => {
    try {
      return texto(sortearDesafio(tecnologia, nivel));
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerTool(
  "gerar_certificado",
  {
    description:
      "Gera um certificado fictício para uma trilha existente. Equivale ao comando /certificado.",
    inputSchema: {
      nome_usuario: z.string().describe("Nome da pessoa que concluiu a trilha"),
      trilha: z.string().describe('Tecnologia ou nome da trilha, ex.: "Python: Dados e APIs"'),
      nivel: z.string().optional().describe("Obrigatório quando a tecnologia tem vários níveis"),
    },
  },
  async ({ nome_usuario, trilha, nivel }) => {
    try {
      return texto(emitirCertificado(nome_usuario, trilha, nivel));
    } catch (e) {
      return erro(e);
    }
  }
);

server.registerResource(
  "trilhas-all",
  "trilhas://all",
  { description: "Base completa de trilhas em JSON", mimeType: "application/json" },
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify({ trilhas: carregarTrilhas() }, null, 2),
      },
    ],
  })
);

const transport = new StdioServerTransport();
await server.connect(transport);
// Em stdio, nunca use console.log (corrompe o protocolo). Logs vão para stderr.
console.error("Geo-Explorer MCP rodando em stdio");
