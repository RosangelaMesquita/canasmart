# CanaSmart — Modo Local — v2

Projeto **CLI** para registrar colheitas de cana, calcular **perdas (%)**, **KPIs**, **detectar outliers** e **ATUALIZAR registros**.

## Novidades da v2
- Opção **[3] Detectar outliers** agora permite escolher **Z-score (configurável)** ou **IQR (boxplot)**.
- Opção **[4] Atualizar registro existente** com validações.


## Como executar (Windows)
1. Dê **duplo clique** em `run.bat` (cria venv, instala deps — não há libs externas — e roda).
2. Use o menu:
   1. Cadastrar registro
   2. Ver KPIs de perda
   3. Detectar outliers (**Z-score/IQR**)
   4. Atualizar registro existente
   5. Listar registros
   6. Sair

## Estruturas e Conteúdo Avaliativo
- **Subalgoritmos (funções)**: em `algorithms.py`, `services/validation.py`, `services/io_text_json.py`, `main.py`.
- **Estruturas de dados**: listas, dicionários, tuplas (e “tabela” como lista de dicts).
- **Manipulação de arquivos**: leitura/escrita **texto** (logs) e **JSON** (base).

