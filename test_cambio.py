"""Solicitud de cambio (A + F) mod 3 = 0  ->  zona insular (San Andrés).
Escritas ANTES de implementar el cambio (TDD): fallan en v2.0.0 y pasan en v2.1.0.
R4: recargo insular +70 %.  R9: los envíos insulares no aceptan cupón.
"""
import importlib
import os

import pytest

calc = importlib.import_module(os.environ.get("ENVIOS_MODULE", "envios_refactorizado")).calc
ERROR = "ERROR"

CASOS_CAMBIO = [
    # TC37  R2,R4
    (2, 'insular', 'normal', 1, None, 10200),
    # TC38  R9
    (2, 'insular', 'normal', 1, 'ENVIO10', ERROR),
    # TC39  R9
    (2, 'insular', 'normal', 1, 'FALSO', ERROR),
    # TC40  R4,R5,R6,R9
    (4, 'insular', 'vip', 7, None, 15800),
]
IDS_CAMBIO = ["TC37", "TC38", "TC39", "TC40"]


@pytest.mark.parametrize("peso,zona,cliente,dia,cupon,esperado", CASOS_CAMBIO, ids=IDS_CAMBIO)
def test_zona_insular(peso, zona, cliente, dia, cupon, esperado):
    if esperado == ERROR:
        # R9: el error debe ser por el cupón, no por "zona inválida"
        with pytest.raises(ValueError, match="cupón"):
            calc(peso, zona, cliente, dia, cupon)
    else:
        assert calc(peso, zona, cliente, dia, cupon) == esperado
