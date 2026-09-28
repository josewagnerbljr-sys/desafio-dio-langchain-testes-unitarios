import pytest
from calculadora import divisao, soma, subtracao


def test_soma_numeros_positivos():
    assert soma(2, 3) == 5


def test_soma_com_negativos_e_zero():
    assert soma(-2, 2) == 0
    assert soma(0, 0) == 0


def test_subtracao_sucesso():
    assert subtracao(10, 4) == 6


def test_subtracao_resultado_negativo():
    assert subtracao(3, 5) == -2


def test_divisao_sucesso():
    assert divisao(10, 2) == 5


def test_divisao_com_decimais():
    assert divisao(1, 4) == 0.25


def test_divisao_por_zero_levanta_erro():
    with pytest.raises(ValueError):
        divisao(5, 0)
