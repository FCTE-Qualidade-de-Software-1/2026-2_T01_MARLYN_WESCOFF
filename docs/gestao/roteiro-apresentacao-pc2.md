# Roteiro da apresentação do PC2

A apresentação de **18/11/2026** dura **15 minutos** e é feita pela GitPage, sem slides. Cada integrante apresenta uma parte de cerca de 3 minutos, na ordem do menu do site. A tabela abaixo é a ordem de navegação; as seções seguintes dizem o que mostrar e o que falar em cada parte.

| Ordem | Parte | Quem apresenta | Tempo | Páginas |
|---|---|---|---|---|
| 1 | Abertura e Fase 1 | Bernardo | 3 min | Início, Propósito, Seleção e priorização |
| 2 | Fase 2 | Maykon | 3 min | Objetivos, questões e hipóteses; Níveis de pontuação e julgamento; Diagrama GQM |
| 3 | Fase 3 | João Pedro | 3 min | Plano de avaliação |
| 4 | Fase 4 | Carlos | 2 min 30 s | Plano de execução |
| 5 | Gestão do projeto (PSM/CID) | Pedro | 3 min | Indicadores e dashboard; Decisões de gestão |
| 6 | Encerramento | Bernardo | 30 s | Início |
| | **Total** | | **15 min** | |

<p class="legenda">Tabela 1. Ordem, apresentador e tempo de cada parte. A divisão é uma proposta, a confirmar pela equipe até 17/11. Fonte: elaboração própria.</p>

Endereço do site: <https://fcte-qualidade-de-software-1.github.io/2026-2_T01_MARLYN_WESCOFF/>. Os caminhos abaixo são relativos a ele.

## 1. Abertura e Fase 1 (Bernardo, 3 min)

- **Mostrar:** `/` (Início) → `fase-1/proposito/` (seção "Decisões apoiadas") → `fase-1/caracteristicas/` (seção "Resultado").
- **Falar:**
    - Quem somos e o produto: Moodle 5.3 LTS, avaliado para uma instituição que decide se atualiza.
    - As decisões que a avaliação apoia: D1 a D3, mais a ação de melhoria D4.
    - Por que adequação funcional, compatibilidade e flexibilidade: o método de priorização com pesos. Usabilidade ficou fora por regra da disciplina.

## 2. Fase 2 (Maykon, 3 min)

- **Mostrar:** `fase-2/objetivos-questoes-hipoteses/` → `fase-2/niveis-e-julgamento/` (Tabela 2 e "Da questão para o objetivo") → `fase-2/diagrama-gqm/`.
- **Falar:**
    - 3 objetivos GQM, 11 questões, cada uma com hipótese, e 12 métricas.
    - Cada métrica tem níveis de 1 a 4, definidos **antes** da coleta.
    - O objetivo é julgado pelo pior caso: uma nota errada não é compensada por outra tarefa que funciona.

## 3. Fase 3 (João Pedro, 3 min)

- **Mostrar:** `fase-3/plano-de-avaliacao/`: seção 1 (método e regras R1 a R8), seção 2 (servidor, massa de dados e oráculo) e seção 4 (piloto e congelamento).
- **Falar:**
    - Avaliação caixa-preta, orientada a tarefas, com oráculo calculado à mão.
    - Regras para que dois avaliadores obtenham a mesma medida: critério antes da coleta, sessão limpa, só a documentação oficial e registro de toda falha.
    - O plano foi aprovado em 14/11 (ata 02).

## 4. Fase 4 (Carlos, 2 min 30 s)

- **Mostrar:** `fase-4/plano-de-execucao/`: Tabela 1 (métricas e responsáveis), Tabela 3 (sequência) e "Do dado ao julgamento".
- **Falar:**
    - Coleta de 18 a 20/11, em paralelo, cada integrante no próprio servidor, montado pelo mesmo script.
    - A preparação de que cada métrica depende fica pronta até 17/11.
    - Em 21/11, os valores viram notas e julgamento pelas regras da Fase 2. Os resultados com nota 1 ou 2 são candidatos à ação de melhoria.

## 5. Gestão do projeto (Pedro, 3 min)

- **Mostrar:** `metricas/dashboard/` (Tabela 1, com as medidas dentro e fora do limiar, e um ou dois gráficos) → `metricas/03-registro-de-decisoes/` (tabela de resumo).
- **Falar:**
    - As três categorias do PSM/CID, com 11 medidas, e dados gerados por script, sem edição manual.
    - Uma medida fora do limiar pede uma decisão. Exemplos: a DG-04 (as tarefas da E2 divididas em blocos) e a DG-09 (o custo da hora com fonte).
    - Mostrar o [quadro de tarefas](https://github.com/users/cadumotta/projects/1) se sobrar tempo.

## 6. Encerramento (Bernardo, 30 s)

- **Mostrar:** `/` (Início).
- **Falar:** o próximo marco é a Entrega 2, em 22/11, com os resultados da Fase 4 e a ação de melhoria. Abrir para perguntas.

## Antes da apresentação

- [ ] Divisão das partes confirmada pela equipe até 17/11
- [ ] Site publicado conferido em 17/11, depois dos merges do PC2, com todas as páginas acima abrindo
- [ ] Cada integrante ensaia a própria parte cronometrada
- [ ] No dia, as páginas ficam abertas em abas, na ordem da Tabela 1, e uma pessoa controla o tempo
