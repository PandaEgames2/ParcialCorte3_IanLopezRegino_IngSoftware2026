"""Suite de pruebas - Parcial 3 (Ingeniería de Software I)
Estudiante: Ian de Jesús López Regino - Código 0182310059
Parámetros: A=3 B=1 C=0 D=0 E=5 F=9 -> PMAX=45, L1=3, L2=10, RR=15 %, RN=40 %, V=10 %, S=$2.000

Contra el código heredado:      pytest -v
Contra el código refactorizado: ENVIOS_MODULE=envios_refactorizado pytest -v
(Windows PowerShell:  $env:ENVIOS_MODULE="envios_refactorizado"; pytest -v)
"""
import importlib
import inspect
import os

import pytest

calc = importlib.import_module(os.environ.get("ENVIOS_MODULE", "envios")).calc
ERROR = "ERROR"   # se espera ValueError


def _verificar(esperado, *args):
    if esperado == ERROR:
        with pytest.raises(ValueError):
            calc(*args)
    else:
        assert calc(*args) == esperado


# ------------------------------------------------------------------ caja negra
# (peso, zona, cliente, día, cupón, esperado)
CASOS_CAJA_NEGRA = [
    # TC01  R1  VL
    (0, 'urbana', 'normal', 1, None, ERROR),
    # TC02  R1,R3  VL
    (0.1, 'urbana', 'normal', 1, None, 6000),
    # TC03  R3  VL
    (3, 'urbana', 'normal', 1, None, 6000),
    # TC04  R3  VL
    (3.1, 'urbana', 'normal', 1, None, 9000),
    # TC05  R3  VL
    (10, 'urbana', 'normal', 1, None, 9000),
    # TC06  R3,R8  VL
    (10.1, 'urbana', 'normal', 1, None, 9100),
    # TC07  R1,R3  VL
    (45, 'urbana', 'normal', 1, None, 37000),
    # TC08  R1  VL
    (45.1, 'urbana', 'normal', 1, None, ERROR),
    # TC09  R1  PE
    (-5, 'urbana', 'normal', 1, None, ERROR),
    # TC10  R1  PE
    (0, 'urbana', 'normal', 1, None, ERROR),
    # TC11  R2  PE
    (2, 'aerea', 'normal', 1, None, ERROR),
    # TC12  R2  VL
    (2, 'urbana', 'normal', 0, None, ERROR),
    # TC13  R2  VL
    (2, 'urbana', 'normal', 8, None, ERROR),
    # TC14  R3  PE
    (12, 'urbana', 'normal', 1, None, 10600),
    # TC15  R4  PE
    (2, 'rural', 'normal', 1, None, 6900),
    # TC16  R4  PE
    (2, 'nacional', 'normal', 1, None, 8400),
    # TC17  R5  VL
    (2, 'urbana', 'normal', 5, None, 6000),
    # TC18  R5  VL
    (2, 'urbana', 'normal', 6, None, 8000),
    # TC19  R5  VL
    (2, 'urbana', 'normal', 7, None, 8000),
    # TC20  R6,R8  PE
    (1, 'urbana', 'vip', 1, 'ENVIO10', 5000),
    # TC21  R8  VL
    (10.0625, 'urbana', 'normal', 1, None, 9100),
    # TC22  R6  TD
    (4, 'urbana', 'normal', 1, None, 9000),
    # TC23  R5  TD
    (4, 'urbana', 'normal', 6, None, 11000),
    # TC24  R6  TD
    (4, 'urbana', 'normal', 1, 'ENVIO10', 8100),
    # TC25  R5,R6  TD
    (4, 'urbana', 'normal', 7, 'ENVIO10', 10100),
    # TC26  R6,R8  TD
    (4, 'urbana', 'frecuente', 1, None, 8600),
    # TC27  R5,R6,R8  TD
    (4, 'urbana', 'frecuente', 6, None, 10600),
    # TC28  R6,R8  TD
    (4, 'urbana', 'frecuente', 1, 'ENVIO10', 7700),
    # TC29  R5,R6,R8  TD
    (4, 'urbana', 'frecuente', 7, 'ENVIO10', 9700),
    # TC30  R6  TD
    (4, 'urbana', 'vip', 1, None, 8100),
    # TC31  R5,R6  TD
    (4, 'urbana', 'vip', 6, None, 10100),
    # TC32  R6,R8  TD
    (4, 'urbana', 'vip', 1, 'ENVIO10', 7300),
    # TC33  R5,R6,R8  TD
    (4, 'urbana', 'vip', 7, 'ENVIO10', 9300),
    # TC34  R7  TD
    (4, 'urbana', 'normal', 1, 'FALSO', ERROR),
    # TC35  R3,R4,R5,R6,R8  Sistema
    (10, 'nacional', 'vip', 6, 'ENVIO10', 12200),
    # TC36  R3,R4,R5,R6,R8  Sistema
    (12, 'rural', 'frecuente', 7, 'ENVIO10', 12400),
] 
IDS_CAJA_NEGRA = ["TC01", "TC02", "TC03", "TC04", "TC05", "TC06", "TC07", "TC08", "TC09", "TC10", "TC11", "TC12", "TC13", "TC14", "TC15", "TC16", "TC17", "TC18", "TC19", "TC20", "TC21", "TC22", "TC23", "TC24", "TC25", "TC26", "TC27", "TC28", "TC29", "TC30", "TC31", "TC32", "TC33", "TC34", "TC35", "TC36"]


@pytest.mark.parametrize("peso,zona,cliente,dia,cupon,esperado", CASOS_CAJA_NEGRA, ids=IDS_CAJA_NEGRA)
def test_caja_negra(peso, zona, cliente, dia, cupon, esperado):
    _verificar(esperado, peso, zona, cliente, dia, cupon)


def test_tc10_mensaje_peso_invalido():
    """R1: el mensaje del error debe ser exactamente 'peso inválido'."""
    with pytest.raises(ValueError, match="peso inválido"):
        calc(0, "urbana", "normal", 1, None)


# ------------------------------------------------------------------ caja blanca
# un caso por camino independiente P1..P14
CASOS_CAJA_BLANCA = [
    # CB01  camino P1: Camino base: T1, urbana, día hábil, normal, sin cupón, sin mínimo
    (2, 'urbana', 'normal', 1, None, 6000),
    # CB02  camino P2: Peso <= 0 (p <= 0 verdadero)
    (0, 'urbana', 'normal', 1, None, ERROR),
    # CB03  camino P3: Peso > máximo (p <= 0 falso, p > máx. verdadero)
    (51, 'urbana', 'normal', 1, None, ERROR),
    # CB04  camino P4: Tramo 2 (L1 < p <= L2)
    (5, 'urbana', 'normal', 1, None, 9000),
    # CB05  camino P5: Tramo 3 (p > L2)
    (12, 'urbana', 'normal', 1, None, 10600),
    # CB06  camino P6: Zona rural
    (2, 'rural', 'normal', 1, None, 6900),
    # CB07  camino P7: Zona nacional
    (2, 'nacional', 'normal', 1, None, 8400),
    # CB08  camino P8: Zona distinta de las válidas
    (2, 'aerea', 'normal', 1, None, ERROR),
    # CB09  camino P9: Fin de semana (día 7)
    (2, 'urbana', 'normal', 7, None, 8000),
    # CB10  camino P10: Cliente frecuente
    (2, 'urbana', 'frecuente', 1, None, 5700),
    # CB11  camino P11: Cliente vip
    (2, 'urbana', 'vip', 1, None, 5400),
    # CB12  camino P12: Cupón presente pero distinto de ENVIO10
    (2, 'urbana', 'normal', 1, 'FALSO', ERROR),
    # CB13  camino P13: Cupón ENVIO10
    (2, 'urbana', 'normal', 1, 'ENVIO10', 5400),
    # CB14  camino P14: Costo mínimo (t < 5000)
    (1, 'urbana', 'vip', 1, 'ENVIO10', 5000),
]
IDS_CAJA_BLANCA = ["CB01", "CB02", "CB03", "CB04", "CB05", "CB06", "CB07", "CB08", "CB09", "CB10", "CB11", "CB12", "CB13", "CB14"]


@pytest.mark.parametrize("peso,zona,cliente,dia,cupon,esperado", CASOS_CAJA_BLANCA, ids=IDS_CAJA_BLANCA)
def test_caja_blanca(peso, zona, cliente, dia, cupon, esperado):
    _verificar(esperado, peso, zona, cliente, dia, cupon)


def test_cb15_argumento_flag():
    """P15: solo existe en v1.0.0; el refactor elimina el argumento flag."""
    if "flag" not in inspect.signature(calc).parameters:
        pytest.skip("flag eliminado en v2.0.0")
    assert calc(2, "urbana", "normal", 1, None, flag=True) == 6000
