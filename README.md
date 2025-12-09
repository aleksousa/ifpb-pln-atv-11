# ifpb-pln-atv-11
# 📄 Documentação do Projeto: Análise de Sumarização de Relatórios Financeiros

Este documento descreve a estrutura e os principais componentes do projeto focado na análise e comparação da performance de modelos de linguagem de grande porte (LLMs) na sumarização de textos complexos, como relatórios financeiros.

---

## 🏗️ Estrutura do Projeto

O projeto é organizado em módulos Python, garantindo modularidade para o gerenciamento de métricas, modelos e técnicas de *prompting*.

| Arquivo/Módulo | Descrição Principal |
| :--- | :--- |
| **`metrics.py`** | Centraliza as funções de cálculo de métricas de avaliação. |
| **`Qwen4.py`, `Qwen8.py`, `Qwen14.py`** | Implementações específicas para os modelos Transformer Qwen (4B, 8B e 14B). |
| **`prompts.py`** | Define e armazena as diferentes técnicas de *prompting* utilizadas. |
| **`corpus_orig.csv`** | Contém o *corpus* de textos originais extraídos de relatórios financeiros. |
| **`main.py`** | O orquestrador principal, responsável pela execução dos modelos e processamento dos resultados. |

---

## 📊 Módulos de Avaliação (`metrics.py`)

O módulo **`metrics.py`** é responsável por quantificar a qualidade e a similaridade dos resumos gerados.

### Funções de Métricas

| Métrica | Descrição |
| :--- | :--- |
| **Índice Flesch** | Calcula a **legibilidade** do resumo. Quanto mais alto o valor, mais fácil é a leitura, comparado ao texto original. |
| **BERTScore** | Avalia a **similaridade semântica** entre o resumo gerado e o texto original. Retorna uma pontuação F1 que indica o quão bem o significado foi preservado. |
| **Compression Ratio** | Mede a **taxa de compressão**, comparando o comprimento do resumo com o do texto original. |

---

## 🤖 Módulos de Modelos (Ex.: `Qwen4.py`, `Qwen8.py`, `Qwen14.py`)

Estes módulos contêm as classes ou funções que encapsulam a lógica de inferência para cada modelo específico da família **Qwen3** (4 Bilhões, 8 Bilhões e 14 Bilhões de parâmetros).

Cada módulo possui uma implementação que recebe um *prompt* e realiza a chamada ao *transformer* para gerar o texto de sumarização.

---

## 💬 Técnicas de Prompting (`prompts.py`)

O módulo **`prompts.py`** contém as definições das abordagens de *prompt* utilizadas no projeto para guiar o comportamento dos modelos.

| Técnica de Prompt | Descrição |
| :--- | :--- |
| **Zero-Shot** | Apenas a instrução da tarefa, sem exemplos. |
| **Zero-Shot with Instruction** | Instrução com diretrizes explícitas de formatação e tom. |
| **One-Shot** | A tarefa é demonstrada com um único par de exemplo (entrada/saída). |
| **Chain-of-Thought** | Solicita ao modelo que apresente a lógica de raciocínio antes de responder. |
| **Role-Playing** | Define um papel específico para o modelo (*e.g.*, "Aja como um analista financeiro..."). |

---

## 📑 Corpus de Dados (`corpus_orig.csv`)

Este arquivo CSV é a fonte de dados primária, contendo textos extraídos de relatórios financeiros públicos.

| Coluna | Conteúdo |
| :--- | :--- |
| `url` | URL de onde o PDF original foi baixado. |
| `type` | Categoria ou tipo do relatório financeiro. |
| `text` | O texto longo, integralmente extraído do relatório. |
| `flesch_original` | O Índice Flesch do texto original, servindo como a linha de base de complexidade. |

---

## ⚙️ Orquestrador Principal (`main.py`)

O módulo **`main.py`** coordena todas as etapas do experimento, desde a seleção dos modelos até o cálculo das métricas.

### Configuração e Fluxo

1.  **Configuração de LLMs:** O `main.py` utiliza um dicionário `llm_configs` para definir quais modelos serão executados, associando um nome de identificação à classe de análise correspondente.

    ```python
    llm_configs = {
        "qwen3-4B": Qwen3_4_Analyzer,
        "qwen3-8B": Qwen3_8_Analyzer,
        "qwen3-14B": Qwen3_14_Analyzer,
    }
    ```

2.  **Fluxo:** O *script* percorre o `corpus_orig.csv`, aplicando todas as técnicas de *prompt* (`prompts.py`) em cada modelo ativo (`llm_configs`). Após a geração do resumo, as métricas são calculadas e todos os resultados são persistidos em um arquivo de saída (e.g., `result_corpus_FINAL.csv`).
