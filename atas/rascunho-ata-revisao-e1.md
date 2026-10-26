# Ata 01 – Reunião de revisão da Entrega 1 (RASCUNHO)

> **Rascunho preparado antes da reunião.** Preencham data, horário, presentes, resultado de cada votação e encaminhamentos **durante** a reunião. Depois, renomeiem o arquivo para `AAAA-MM-DD-ata-01.md`, apaguem este aviso e atualizem o índice em `docs/gestao/atas.md`.

| Campo | Valor |
|---|---|
| Data e horário | [AAAA-MM-DD, HHhMM–HHhMM] |
| Local | [Presencial / Online (ferramenta)] |
| Participantes | [ ] Bernardo Broetto Brun · [ ] Carlos Eduardo Deusdara Motta · [ ] João Pedro Sampaio Maciel · [ ] Maykon Junio dos Santos Soares · [ ] Pedro Goncalves Rocha |
| Ausentes | [ ] |
| Responsável pela ata | Carlos Eduardo Deusdara Motta |

## Pauta

1. Situação da Entrega 1 e migração do trabalho para o repositório da disciplina.
2. Validação das decisões da Fase 1.
3. Validação do plano GQM da Fase 2.
4. Gestão: sprints, custo da hora, registro de horas e PSM/CID.
5. Divisão de responsabilidades, tabela de contribuição e declaração de uso de IA.
6. Fechamento: release E1 e envio no Moodle.

## Decisões a votar

Marquem **Aprovada**, **Alterada** (descrever a alteração) ou **Rejeitada**.

| Nº | Decisão proposta | Justificativa | Resultado |
|---|---|---|---|
| D1 | Avaliar o **Moodle 5.3 LTS** (núcleo, tema Boost, sem plugins) em instalação local | Versão LTS lançada em 05/10/2026; cenário de atualização em IES | [ ] |
| D2 | Trocar **usabilidade** por **compatibilidade**; características finais: adequação funcional, compatibilidade e flexibilidade | A rubrica da Fase 1 (Critério 5) não aceita usabilidade; "funcionalidade" e "portabilidade" correspondem a adequação funcional e flexibilidade na ISO/IEC 25010:2023 | [ ] |
| D3 | Requisitante no cenário: **Coordenação de TI** da IES; ponto de vista dos objetivos GQM | Quem toma as decisões D1–D3 do propósito | [ ] |
| D4 | Notas R, K, V e A da matriz de priorização (Tabela 4 de [Seleção e priorização](../docs/fase-1/caracteristicas.md)) | Cada integrante confere as notas; mudanças exigem recalcular a matriz | [ ] |
| D5 | Catálogo de 12 tarefas essenciais (T01–T12) e ambientes de acesso A1–A4 | Recorte viável com os recursos da equipe | [ ] |
| D6 | Plano GQM com 3 objetivos, 11 questões, 11 hipóteses e 12 métricas | Ver [Fase 2](../docs/fase-2/index.md) | [ ] |
| D7 | Níveis de pontuação e regra de julgamento pelo pior caso | Ver [Níveis e julgamento](../docs/fase-2/niveis-e-julgamento.md) | [ ] |
| D8 | Limites de tempo de M3.4 (15/30/60 min) como candidatos, a calibrar no piloto da Fase 3 | Sem dados prévios da equipe | [ ] |
| D9 | Custo de referência de **R$ 15,00/h** e sprints de 13–19/10 e 20–26/10 | Usados nas medidas do PSM/CID | [ ] |
| D10 | Divisão de responsabilidades proposta em [Equipe e contribuição](../docs/sobre/equipe.md) | Um responsável e um revisor por característica | [ ] |

## Medições do PSM revisadas

Preencher depois de rodar `python3 scripts/psm_coleta.py --repo FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF`.

| Medida | Valor | Critério de decisão atingido? | Ação |
|---|---|---|---|
| Planejado vs. concluído (Sprint 2) | [ ] | [ ] | [ ] |
| Esforço realizado ÷ estimado (Sprint 2) | [ ] | [ ] | [ ] |
| Tempo de ciclo (mediana) e issues paradas | [ ] | [ ] | [ ] |

## Encaminhamentos

| Tarefa | Responsável | Prazo | Issue |
|---|---|---|---|
| Revisar propósito, partes interessadas e G1 | Bernardo Broetto Brun | 26/10/2026 | #1, #4 |
| Revisar produto, modelo, escopo e G2; registrar esta ata | Carlos Eduardo Deusdara Motta | 26/10/2026 | #2, #5, #12 |
| Revisar a priorização e G3 | Pedro Goncalves Rocha | 26/10/2026 | #3, #6 |
| Revisar ODS, abstraction sheets, diagrama GQM, rastreabilidade e GitPage | João Pedro Sampaio Maciel | 26/10/2026 | #3, #7, #13 |
| Revisar o artigo; consolidar horas e PSM; criar a release | Maykon Junio dos Santos Soares | 26/10/2026 | #8, #9, #11, #14 |
| Lançar as próprias horas e preencher a declaração de IA | Todos | 26/10/2026 | #10, #11 |
