# Como contribuir

Guia rápido para os integrantes do Grupo Marlyn Wescoff.

## Fluxo de trabalho

1. **Abra uma issue** com o modelo *Tarefa*: descrição, fase, estimativa em horas e critério de pronto. Associe-a ao milestone da sprint e atribua a você.
2. **Crie um branch** a partir da `main`, com prefixo e assunto: `docs/fase-3-ambiente`, `artigo/resultados`, `fix/link-quebrado`.
3. **Faça commits pequenos**, com mensagem no imperativo e em português, por exemplo "Adiciona as fichas das métricas de G2".
4. **Abra um pull request** com o modelo do repositório, cite a issue (`Fecha #N`) e peça revisão a outro integrante.
5. **Depois do merge**, registre as horas em `dados/gestao/horas.csv` e, se usou IA, em `docs/sobre/uso-de-ia.md`.

## Antes de abrir o pull request

```bash
pip install -r requirements.txt
mkdocs build --strict          # o site precisa gerar sem avisos
cd artigo && latexmk -pdf main.tex   # se alterou o artigo
cp artigo/main.pdf docs/artigo/artigo-e1.pdf
```

## Padrões de escrita

- Português formal e direto; termos da ISO/IEC 25010:2023 em português (adequação funcional, compatibilidade, flexibilidade).
- Toda figura e tabela tem número, legenda e fonte, e é citada no texto.
- Toda afirmação sobre o Moodle cita a fonte oficial em `docs/sobre/referencias.md`.
- Sem emojis, figurinhas ou ícones no relatório e na GitPage.
- Dados brutos ficam em `dados/`, com o identificador da métrica no nome da pasta (por exemplo, `dados/avaliacao/M2.1/`).

## Atas e decisões

Cada reunião gera uma ata em `atas/AAAA-MM-DD-ata-NN.md` (modelo em `atas/modelo-ata.md`). Decisões tomadas fora de reunião entram no registro de decisões em `docs/gestao/atas.md`.
