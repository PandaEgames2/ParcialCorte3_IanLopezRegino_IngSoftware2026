"""Pruebas de integración (v2.x): los componentes del refactor trabajando juntos."""
from decimal import Decimal

import pytest

import envios_refactorizado as m


def test_it01_factory_y_estrategia_rural():
    """Factory -> Estrategia: la zona rural recarga 15 % sobre la tarifa."""
    assert m.ZonaFactory.crear("rural").aplicar(Decimal("6000")) == Decimal("6900")


def test_it02_factory_rechaza_zona_desconocida():
    with pytest.raises(ValueError, match="zona inválida"):
        m.ZonaFactory.crear("aerea")


def test_it03_tuberia_descuentos_finde_redondeo():
    """TC25: descuentos -> fin de semana -> redondeo (regla E impar)."""
    valor = m._aplicar_descuentos(Decimal("9000"), "normal", "ENVIO10")   # 8.100
    valor = m._recargo_fin_de_semana(valor, 7)                            # 10.100
    assert m._redondear(valor) == 10100


def test_it04_zona_insular_bloquea_cupon():
    """R9: Estrategia insular + validador de cupón."""
    with pytest.raises(ValueError, match="cupón"):
        m._validar_cupon("ENVIO10", m.ZonaFactory.crear("insular"))
