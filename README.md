# 🧪 Agente de Testes Unitários — LangChain + Azure OpenAI

Agente de IA que recebe um arquivo Python e gera automaticamente um arquivo de testes com **pytest** (`test_<nome>.py`), usando **LangChain** e **Azure OpenAI**.

## 📌 Descrição

O agente lê o código de entrada, monta um prompt com regras estritas e envia ao modelo (Azure ChatGPT) por meio de uma cadeia LangChain (`prompt | modelo | parser`). A resposta é limpa e salva como arquivo de testes contendo:

- `import pytest` na **primeira linha** (garantido por pós-processamento, mesmo que o modelo erre);
- funções `def test_*` para casos de **sucesso e de falha** (`pytest.raises`).

## 🗂️ Estrutura

```
├── agente_testes.py            # o agente (LangChain + Azure OpenAI)
├── exemplos/
│   ├── calculadora.py          # funções de exemplo: soma, subtracao, divisao
│   └── test_calculadora.py     # testes correspondentes
├── .env.example                # variáveis do Azure OpenAI
├── requirements.txt
└── README.md
```

## ⚙️ Configuração

```bash
git clone https://github.com/josewagnerbljr-sys/desafio-dio-langchain-testes-unitarios.git
cd desafio-dio-langchain-testes-unitarios
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
```

Preencha o `.env` com os dados do seu recurso Azure OpenAI:

| Variável | Descrição |
|---|---|
| `AZURE_OPENAI_ENDPOINT` | Endpoint do recurso (`https://SEU-RECURSO.openai.azure.com/`) |
| `AZURE_OPENAI_API_KEY` | Chave do recurso (Portal Azure → Chaves e Ponto de Extremidade) |
| `AZURE_OPENAI_DEPLOYMENT` | Nome do deployment do modelo de chat (ex.: `gpt-4o`) |
| `AZURE_OPENAI_API_VERSION` | Versão da API (padrão: `2024-08-01-preview`) |

## ▶️ Como rodar o agente

```bash
python agente_testes.py exemplos/calculadora.py
```

Isso gera `exemplos/test_calculadora.py`. Para escolher outra pasta de saída: `--saida pasta/`.

Depois, rode os testes:

```bash
pytest
```

## 💡 Exemplos de uso

`exemplos/calculadora.py` contém três funções simples criadas para o desafio: `soma`, `subtracao` e `divisao` (esta levanta `ValueError` na divisão por zero). Os testes em `exemplos/test_calculadora.py` cobrem sucesso, valores negativos/decimais e o caso de falha, e passam com `pytest`.

> **Transparência:** o `test_calculadora.py` incluído no repositório foi escrito manualmente no formato que o agente produz, pois a geração real depende de credenciais Azure OpenAI. A cadeia LangChain e o pós-processamento foram validados com um modelo simulado. Ao rodar o agente com suas credenciais, o arquivo será sobrescrito pela versão gerada pelo modelo.

## 🧠 Como funciona

1. `criar_llm()` lê o `.env` e cria o `AzureChatOpenAI` (temperatura 0, para código consistente).
2. `gerar_testes()` monta a cadeia LangChain `ChatPromptTemplate | modelo | StrOutputParser`.
3. `limpar_saida()` remove cercas markdown e garante `import pytest` na primeira linha.
4. O resultado é gravado em `test_<nome>.py`, ao lado do arquivo de origem, para que o `import` do módulo funcione no `pytest`.

## 📚 Contexto

Desafio da DIO: gerar testes unitários com LangChain e Azure ChatGPT.

## 📄 Licença

MIT
