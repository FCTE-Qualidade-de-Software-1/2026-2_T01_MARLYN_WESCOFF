# Avaliação da qualidade do Moodle 5.3 LTS

**FGA0315 Qualidade de Software 1 · UnB/FCTE · 2026/2 · Turma 01 · Grupo Marlyn Wescoff**

[![Publicar GitPage](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/actions/workflows/deploy.yml/badge.svg)](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/actions/workflows/deploy.yml)
[![Compilar artigo](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/actions/workflows/artigo.yml/badge.svg)](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/actions/workflows/artigo.yml)

Avaliação da qualidade de produto do **Moodle 5.3 LTS**, sistema de gestão da aprendizagem de código aberto, seguindo o processo de avaliação da série SQuaRE (ISO/IEC 25040), o modelo de qualidade da ISO/IEC 25010:2023 e o método GQM. A gestão do projeto é acompanhada com métricas do PSM/CID.

| | |
|---|---|
| **GitPage** | <https://fcte-qualidade-de-software-1.github.io/2026-2_T01_MARLYN_WESCOFF/> |
| **Artigo da Entrega 1 (PDF)** | [`docs/artigo/artigo-e1.pdf`](docs/artigo/artigo-e1.pdf) · [na GitPage](https://fcte-qualidade-de-software-1.github.io/2026-2_T01_MARLYN_WESCOFF/artigo/artigo-e1.pdf) |
| **Releases** | [Releases do repositório](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/releases) |
| **Docente** | Profa. Cristiane Soares Ramos |

## O que está sendo avaliado

Uma instituição de ensino superior que mantém um Moodle precisa decidir se atualiza para a versão 5.3 LTS. A avaliação responde a três perguntas, uma por característica priorizada:

| Objetivo | Característica (ISO/IEC 25010:2023) | Pergunta | Decisão apoiada |
|---|---|---|---|
| G1 | Adequação funcional | O núcleo cobre e calcula corretamente as tarefas acadêmicas essenciais? | D1 – adotar só o núcleo ou prever plugins |
| G2 | Compatibilidade | O Moodle troca dados com os sistemas vizinhos sem perdas e convive com outras aplicações no servidor? | D2 – manter ou adaptar as integrações |
| G3 | Flexibilidade | A instalação e a atualização 4.5 → 5.3 funcionam pela documentação e os fluxos rodam nos ambientes de acesso? | D3 – procedimento de migração e ambientes suportados |

Capacidade de interação (usabilidade) está fora do escopo por regra da disciplina. O plano GQM tem **3 objetivos, 11 questões com hipóteses e 12 métricas**, todas com níveis de pontuação e critérios de julgamento.

## Situação das entregas

| Entrega | Fases | Situação |
|---|---|---|
| E1 · 26/10/2026 | Fase 1 (requisitos) e Fase 2 (especificação) | Em revisão pela equipe |
| E2 | Fase 3 (plano) e Fase 4 (execução e ação de melhoria) | Não iniciada |

## Estrutura do repositório

```text
.
├── docs/                  # Conteúdo da GitPage (MkDocs Material)
│   ├── fase-1/            # Propósito, partes interessadas, produto, modelo, priorização, escopo, ODS
│   ├── fase-2/            # Abstraction sheets, GQM, métricas, níveis e julgamento, rastreabilidade
│   ├── gestao/            # Plano de medição PSM/CID, registro de medições, atas
│   ├── sobre/             # Equipe e contribuição, uso de IA, referências, entregas
│   ├── artigo/            # PDF publicado do artigo
│   ├── javascripts/       # Interações da GitPage (explorador GQM, animações)
│   └── stylesheets/       # Identidade visual
├── overrides/             # Templates do tema (página inicial personalizada)
├── includes/              # Glossário de siglas (tooltips da GitPage)
├── artigo/                # Código-fonte LaTeX do artigo (modelo SBC)
├── dados/
│   ├── gestao/            # Registro de horas e retratos do PSM/CID
│   └── avaliacao/         # Dados brutos das medições (Fase 4)
├── atas/                  # Atas de reunião
├── scripts/               # Coleta automática das métricas do PSM/CID
└── .github/               # Workflows, modelos de issue e de pull request
```

## Como executar localmente

### GitPage

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

O site fica em <http://127.0.0.1:8000/2026-2_T01_MARLYN_WESCOFF/> e recarrega a cada alteração. Antes de abrir um pull request, rode `mkdocs build --strict`.

### Artigo

```bash
cd artigo
latexmk -pdf main.tex      # ou: tectonic main.tex
cp main.pdf ../docs/artigo/artigo-e1.pdf
```

O workflow `artigo.yml` também compila o artigo a cada alteração em `artigo/` e disponibiliza o PDF como artefato da execução.

### Métricas do PSM/CID

```bash
python3 scripts/psm_coleta.py --repo FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF
```

Lê as issues e milestones pela API do GitHub e o arquivo `dados/gestao/horas.csv`, imprime o resumo das três medidas e grava um retrato em `dados/gestao/psm-AAAA-MM-DD.csv`.

## Como contribuir

1. Abra uma issue com o modelo **Tarefa** (com estimativa de horas) e associe ao milestone da sprint.
2. Crie um branch, por exemplo `docs/fase-2-compatibilidade`.
3. Abra um pull request e peça revisão a outro integrante.
4. Ao terminar, registre as horas em `dados/gestao/horas.csv` e, se usou IA, em `docs/sobre/uso-de-ia.md`.

Regras de estilo da disciplina: figuras e tabelas numeradas, com legenda e fonte; referências cruzadas; sem emojis, figurinhas ou ícones no relatório e na GitPage.

## Equipe

| Integrante | GitHub |
|---|---|
| Bernardo Broetto Brun | — |
| Cadu Motta | — |
| João Pedro Maciel | — |
| Maykson Soares | — |
| Pedro Rocha | — |

## Referências principais

- ISO/IEC 25010:2023, 25023 e 25040 (série SQuaRE).
- BASILI, V. R.; CALDIERA, G.; ROMBACH, H. D. The Goal Question Metric approach, 1994.
- PSM. *Continuous Iterative Development Measurement Framework*, v2.1, 2021.
- MOODLE. [Moodle 5.3 (LTS)](https://moodledev.io/general/releases/5.3), 2026.

A lista completa está em [`docs/sobre/referencias.md`](docs/sobre/referencias.md).

---

Projeto acadêmico em homenagem a Marlyn Wescoff, uma das programadoras originais do ENIAC. Sem vínculo ou endosso da Moodle HQ.
