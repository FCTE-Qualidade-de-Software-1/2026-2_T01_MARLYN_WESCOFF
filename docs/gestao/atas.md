# Atas de reunião

As atas ficam na pasta [`atas/`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/tree/main/atas) do repositório, uma por reunião, com o nome `AAAA-MM-DD-ata-NN.md`, a partir do [modelo](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/modelo-ata.md).

| Nº | Data | Pauta principal | Arquivo |
|---|---|---|---|
| 01 | 11/10/2026 (aproximada) | Definição do projeto final: escolha do Moodle e características iniciais | [2026-10-11-ata-01.md](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/2026-10-11-ata-01.md) |
| Retrospectiva | 28/10/2026 | Retrospectiva da E1 (facilitador: Bernardo; relator: João Pedro): tópicos priorizados C2 "ausência de liderança" e C3 "pouca atenção aos prazos". As decisões decorrentes estão no [Registro de decisões de gestão](../metricas/03-registro-de-decisoes.md) (DG-06 e DG-07); transcrição em [Retrospectiva da E1](retrospectiva-e1.md) | [2026-10-28-retrospectiva-e1.pdf](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/2026-10-28-retrospectiva-e1.pdf) |
| 02 | 14/11/2026 | Aprovação do plano de avaliação da Fase 3: cronograma de 16 a 22/11, um servidor por integrante, manutenção das 6 execuções de M3.3 a M3.5 e responsáveis das issues #52 a #78 | [2026-11-14-ata-02.md](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/atas/2026-11-14-ata-02.md) |

<p class="legenda">Tabela 1. Índice das atas. Fonte: pasta `atas/`.</p>

## Registro de decisões

Decisões tomadas fora de reunião formal, durante a elaboração e a revisão das Entregas 1 e 2.

| Data | Decisão | Justificativa | Onde está |
|---|---|---|---|
| 11/10/2026 | Avaliar o Moodle | Ata 01 | [Produto avaliado](../fase-1/produto.md) |
| 25/10/2026 | Fixar a versão-alvo no **Moodle 5.3 LTS**, com atualização a partir da 4.5 LTS | Versão LTS lançada em 05/10/2026, com mudanças de requisitos que motivam a avaliação | [Propósito](../fase-1/proposito.md) |
| 25/10/2026 | Trocar **usabilidade** por **compatibilidade**; características finais: adequação funcional, compatibilidade e flexibilidade | O Critério 5 da Fase 1 não aceita usabilidade; "funcionalidade" e "portabilidade" correspondem a adequação funcional e flexibilidade na ISO/IEC 25010:2023 | [Seleção e priorização](../fase-1/caracteristicas.md) |
| 25/10/2026 | Migrar a documentação para o repositório da disciplina e para a GitPage em MkDocs | Repositório oficial exigido pela premissa 4 | [Metodologia](../metodologia.md) |
| 26/10/2026 | Dividir o esforço da E1 igualmente entre os cinco integrantes (20% cada) | Trabalho distribuído e revisado por todos | [Equipe e contribuição](../sobre/equipe.md) |
| 26/10/2026 | Na E2, abrir as issues no planejamento da sprint e lançar as horas ao fechar cada uma | Resultado da primeira medição do PSM/CID | [Registro de medições](registro-medicoes.md) |
| 23/11/2026 | Corrigir o instrumento de M2.2 (`scripts/compara_registros.py`): a célula numérica de XLSX passa a ser comparada como número (10.0 = 10.00), e a resposta numérica de GIFT, por peso, valor, tolerância e feedback (`#144` = `=%100%144:0`). O critério de M2.2 não muda: só espaços em branco são normalizados, e acentos, maiúsculas, casas decimais em texto e datas continuam contando como divergência | Na coleta de 22/11 (PR #133), o instrumento marcou como divergentes os 30 registros de F3 e 5 de F4 por diferença de representação, e não de dado: o XLSX guarda o número, e o Moodle exporta o GIFT numérico na forma estendida. Com a correção, F3 = 30/30 e F4 = 15/15 nos mesmos arquivos | [`compara_registros.py`](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARLYN_WESCOFF/blob/main/scripts/compara_registros.py), issue #65 |
| 23/11/2026 | Adotar o prazo novo da Entrega 2, **24/11/2026, até 23h59**, e refazer o cronograma da Fase 4 com o previsto, o realizado e o restante | O prazo da E2 mudou depois do PC2. A coleta, prevista para 18 a 20/11, ocorreu entre 15 e 23/11, e o julgamento e a consolidação passaram para 23 e 24/11 | [Plano de execução da Fase 4](../fase-4/plano-de-execucao.md#sequencia-ate-a-entrega-2), Tabelas 2 e 3; milestone E2 |

<p class="legenda">Tabela 2. Registro de decisões das Entregas 1 e 2. Fonte: elaboração própria.</p>

Cada ata registra data, participantes, pauta, decisões e encaminhamentos e, quando houver, a decisão de gestão tomada a partir das [medições do PSM](registro-medicoes.md).
