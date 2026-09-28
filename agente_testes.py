"""
Agente de IA (LangChain + Azure OpenAI) que recebe um arquivo Python e gera
automaticamente um arquivo de testes unitários com pytest: test_<nome>.py

Uso:
    python agente_testes.py exemplos/calculadora.py
    python agente_testes.py exemplos/calculadora.py --saida outra_pasta/
"""

import argparse
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

PROMPT_SISTEMA = """\
Você é um engenheiro de software sênior especialista em testes com pytest.

Receberá o código de um módulo Python chamado `{modulo}`. Gere um arquivo de \
testes unitários seguindo ESTRITAMENTE estas regras:

1. A primeira linha do arquivo deve ser exatamente: import pytest
2. Importe as funções a serem testadas com: from {modulo} import ...
3. Para cada função, crie testes `def test_*` cobrindo casos de sucesso E \
casos de falha (use pytest.raises quando a função levantar exceção).
4. Use nomes de teste descritivos e, quando útil, @pytest.mark.parametrize.
5. Responda SOMENTE com código Python puro: sem markdown, sem cercas ```, \
sem explicações antes ou depois.
"""

PROMPT_USUARIO = "Código do módulo `{modulo}`:\n\n{codigo}"


def criar_llm() -> AzureChatOpenAI:
    """Cria o modelo a partir das variáveis de ambiente (.env)."""
    load_dotenv()
    obrigatorias = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT"]
    faltando = [v for v in obrigatorias if not os.getenv(v)]
    if faltando:
        sys.exit(f"Variáveis de ambiente ausentes: {', '.join(faltando)}. Veja o .env.example.")

    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        temperature=0,  # queremos código consistente, não criativo
    )


def limpar_saida(texto: str) -> str:
    """Remove cercas markdown e garante `import pytest` na primeira linha."""
    texto = re.sub(r"^```(?:python)?\s*\n|\n```\s*$", "", texto.strip())
    linhas = [ln for ln in texto.splitlines() if ln.strip() != "import pytest"]
    while linhas and not linhas[0].strip():
        linhas.pop(0)
    return "import pytest\n" + "\n".join(linhas) + "\n"


def gerar_testes(codigo: str, modulo: str, llm) -> str:
    """Cadeia LangChain: prompt -> modelo -> texto. Retorna o código do arquivo de testes."""
    prompt = ChatPromptTemplate.from_messages([("system", PROMPT_SISTEMA), ("human", PROMPT_USUARIO)])
    cadeia = prompt | llm | StrOutputParser()
    return limpar_saida(cadeia.invoke({"modulo": modulo, "codigo": codigo}))


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera testes pytest a partir de um arquivo Python.")
    ap.add_argument("arquivo", type=Path, help="Arquivo .py a ser testado")
    ap.add_argument("--saida", type=Path, default=None, help="Pasta de saída (padrão: mesma pasta do arquivo)")
    args = ap.parse_args()

    if not args.arquivo.is_file() or args.arquivo.suffix != ".py":
        sys.exit(f"Arquivo Python não encontrado: {args.arquivo}")

    modulo = args.arquivo.stem
    destino = (args.saida or args.arquivo.parent) / f"test_{modulo}.py"
    destino.parent.mkdir(parents=True, exist_ok=True)

    testes = gerar_testes(args.arquivo.read_text(encoding="utf-8"), modulo, criar_llm())
    destino.write_text(testes, encoding="utf-8")
    print(f"Testes gerados em {destino}. Rode: pytest")


if __name__ == "__main__":
    main()
