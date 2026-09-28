"""Funções simples usadas como exemplo de entrada para o agente."""


def soma(a: float, b: float) -> float:
    return a + b


def subtracao(a: float, b: float) -> float:
    return a - b


def divisao(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisão por zero não é permitida.")
    return a / b
