<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width="30%" height="30%">
AI Project Document - Módulo 1 - FIAP
Nome do Grupo

CanaSmart

Nomes dos integrantes do grupo

[Rosangela Braga de Mesquita] — RM [568342]


Sumário

1. Introdução

2. Visão Geral do Projeto

3. Desenvolvimento do Projeto

4. Resultados e Avaliações

5. Conclusões e Trabalhos Futuros

6. Referências

Anexos

<a name="c1"></a>1. Introdução
1.1. Escopo do Projeto
1.1.1. Contexto da Inteligência Artificial

O agronegócio brasileiro é um dos pilares da economia nacional e demanda soluções digitais para monitorar produtividade, reduzir perdas e apoiar decisões operacionais. No contexto de IA e ciência de dados, técnicas de análise exploratória, detecção de outliers e indicadores (KPIs) permitem identificar desvios operacionais, orientar manutenção de equipamentos e direcionar boas práticas de colheita. Este projeto foca em análises estatísticas automatizadas e higienização de dados para apoiar a gestão da colheita de cana-de-açúcar em nível local (armazenamento em arquivo), com possibilidade de expansão.

1.1.2. Descrição da Solução Desenvolvida

CanaSmart (modo local) é um aplicativo CLI (linha de comando) que:

Registra colheitas (talhão, data, equipamento, massas pré/pós e tecnologia).

Calcula perda (%) automaticamente.

Gera KPIs (média, mediana, DP, Q1, Q3).

Detecta outliers por Z-score (configurável) e IQR (boxplot).

Atualiza registros existentes com validação e recalcula a perda.
Dados ficam em JSON e logs em texto; não há dependência de banco (sem Oracle) nesta entrega.

<a name="c2"></a>2. Visão Geral do Projeto
2.1. Objetivos do Projeto

Reduzir perdas na colheita pela identificação rápida de desvios.

Disponibilizar indicadores operacionais simples e claros.

Entregar uma base local (sem infraestrutura de banco) fácil de executar e avaliar.

Atender aos requisitos acadêmicos: subalgoritmos, estruturas de dados, manipulação de arquivos (texto/JSON) e usabilidade em prompt.

2.2. Público-Alvo

Técnicos e gerentes de campo que precisam de visão rápida de perdas.

Estudantes/analistas que desejam experimentar regras estatísticas de outliers antes de escalar para BI/IA.

2.3. Metodologia

Levantamento de requisitos: foco em perdas na colheita (massa pré x pós).

Modelagem de dados: registro de colheita (entidade simples).

Prototipação: CLI em Python, persistência local em JSON.

Análise estatística: KPIs, Z-score e IQR.

Validação: simulação com dados reais/realistas e cenários extremos para testar detecção.

Iteração: inclusão de atualização de registros e outliers configuráveis.

<a name="c3"></a>3. Desenvolvimento do Projeto
3.1. Tecnologias Utilizadas

Python 3.9+ (CLI)

Padrões de código: funções (subalgoritmos), dataclasses

Arquivos: JSON (base) e texto (logs)

Sem dependências externas (requirements vazio)

3.2. Modelagem e Algoritmos

Estruturas de dados

Dicionário/lista: registros em memória (tabela = lista de dicts).

Tupla: uso pontual em funções auxiliares.

Dataclass RegistroColheita (campos: talhão, data, equipamento, massa_pre, massa_pos, perda%, tecnologia).

Subalgoritmos (funções)

calc_perda_percentual(pre, pos): calcula e limita a perda a [0, 100].

kpis_perdas(registros): média, mediana, DP, Q1, Q3.

is_outlier_zscore(valor, media, dp, z): outlier por Z-score.

iqr_bounds(lista): Q1, Q3 e limites inferior/superior (1,5·IQR).

I/O: load_json, save_json, append_log, find_index_by_key.

Regras de outlier

Z-score (configurável no menu).

IQR (1,5·IQR), clássico para boxplot.

3.3. Treinamento e Teste

Não há modelo supervisionado nesta versão; o foco é estatística descritiva e regras de detecção.
Testes funcionais cobrem: cadastro, atualização, KPIs, outliers (com dados extremos) e persistência (JSON/log).

<a name="c4"></a>4. Resultados e Avaliações
4.1. Análise dos Resultados

Com uma base exemplo (incluindo um valor extremo), observou-se:

KPIs coerentes com a distribuição dos dados;

Z-score: com limiar Z=1.0–1.5, valores de 25% foram marcados; com Z=2.5–3.0, apenas perdas muito altas aparecem.

IQR: com Q1≈15% e Q3≈25%, o limite superior ≈ 40% — perdas maiores que isso aparecem como outlier; quando inseridos registros a 45–60%, foram corretamente destacados.

4.2. Feedback dos Usuários

CLI simples de operar;

Útil para “sanidade” dos dados antes de levar para planilhas/BI;

A atualização direta por chave (talhão+data) agiliza correções de digitação e recalcula a perda na hora.

<a name="c5"></a>5. Conclusões e Trabalhos Futuros

Conquistas

Entrega funcional sem dependências (JSON), atendendo aos requisitos acadêmicos.

KPIs e outliers auxiliam a priorizar investigações de campo.

Mecanismo de atualização garante qualidade dos dados.

Melhorias planejadas

Exportar CSV/XLSX e gráficos (histograma/boxplot) direto do CLI.

Dashboard web (Streamlit/Plotly) com filtros e séries temporais.

Forecast de perda com modelos simples (ex.: regressão, ARIMA) e, depois, ML supervisionado.

Opcional: integração Oracle e/ou APIs (Ceasas/Conab) para dados oficiais.

<a name="c6"></a>6. Referências

Conceitos de perdas e produtividade na colheita — literatura técnica setorial (Conab, Embrapa).

Estatística descritiva e detecção de outliers (Z-score e IQR) — referências acadêmicas clássicas.

Documentação Python (dataclasses, json, statistics).

Caso precise citar fontes específicas do seu levantamento (ex.: páginas da Conab/Embrapa que você usou), inclua-as aqui com título e link.

<a name="c7"></a>Anexos
A. Estrutura do Repositório
canasmart_local/
  main.py
  algorithms.py
  models.py
  services/
    io_text_json.py
    validation.py
  data/
    harvest_records.json   # base local (JSON)
    logs.txt               # log (texto)
  run.bat                  # executa no Windows (com venv)
  run_no_venv.bat          # execução simples
  README.md
  README_quickstart.md
  requirements.txt         # vazio (sem libs externas)

B. Guia de Execução (Windows)

Extraia o projeto.

Dê duplo clique em run.bat.

Use o menu:

[1] Cadastrar: cria um registro e calcula a perda.

[4] Atualizar: edita campos por talhão+data e recalcula a perda.

[2] KPIs e [3] Outliers: análises rápidas.

[5] Listar: visão rápida dos primeiros registros.

C. Exemplos para forçar outliers (IQR)

Perda 45%: pré=100, pós=55

Perda 60%: pré=100, pós=40

Perda 42%: pré=200, pós=116
Com Q1≈15% e Q3≈25%, o limite superior ≈40% — esses valores aparecem como outliers.