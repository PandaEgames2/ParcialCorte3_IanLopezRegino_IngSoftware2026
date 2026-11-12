"""envios_refactorizado.py  -  EnvíaYa, cálculo del costo de un envío.

Versión 2.1.0  (v2.0.0 + solicitud de cambio: zona insular).
Parámetros del código estudiantil 0182310059:
A=3 B=1 C=0 D=0 E=5 F=9  ->  PMAX=45, L1=3, L2=10, RR=15 %, RN=40 %, V=10 %, S=$2.000
"""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

# ---------------------------------------------------------------- constantes
PESO_MAX_KG = Decimal("45")             # PMAX
LIMITE_TRAMO_1_KG = Decimal("3")        # L1 (incluido: regla D par)
LIMITE_TRAMO_2_KG = Decimal("10")       # L2 (incluido)
TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
TARIFA_KG_ADICIONAL = Decimal("800")
RECARGO_RURAL = Decimal("0.15")         # RR
RECARGO_NACIONAL = Decimal("0.40")      # RN
RECARGO_INSULAR = Decimal("0.70")       # [CAMBIO] zona insular
DESC_FRECUENTE = Decimal("0.05")
DESC_VIP = Decimal("0.10")              # V
DESC_CUPON_ENVIO10 = Decimal("0.10")
RECARGO_FINDE = Decimal("2000")         # S
DIAS_FIN_DE_SEMANA = (6, 7)             # 6 = sábado, 7 = domingo
COSTO_MINIMO = Decimal("5000")
MULTIPLO_REDONDEO = Decimal("100")

DESCUENTO_POR_CLIENTE = {"normal": Decimal("0"),
                         "frecuente": DESC_FRECUENTE,
                         "vip": DESC_VIP}
DESCUENTO_POR_CUPON = {"ENVIO10": DESC_CUPON_ENVIO10}


# ---------------------------------------------------- patrón Estrategia (zonas)
class EstrategiaZona(ABC):
    """Cada zona sabe cuánto recarga y si acepta cupones."""
    acepta_cupon = True

    @property
    @abstractmethod
    def recargo(self) -> Decimal: ...

    def aplicar(self, tarifa: Decimal) -> Decimal:
        return tarifa * (1 + self.recargo)


class ZonaUrbana(EstrategiaZona):
    recargo = Decimal("0")


class ZonaRural(EstrategiaZona):
    recargo = RECARGO_RURAL


class ZonaNacional(EstrategiaZona):
    recargo = RECARGO_NACIONAL


# [CAMBIO-INICIO] solicitud de cambio (A+F) mod 3 = 0: zona insular
class ZonaInsular(EstrategiaZona):
    recargo = RECARGO_INSULAR
    acepta_cupon = False                # R9
# [CAMBIO-FIN]


class ZonaFactory:
    _zonas = {"urbana": ZonaUrbana, "rural": ZonaRural, "nacional": ZonaNacional,
              "insular": ZonaInsular}   # [CAMBIO] quitar "insular" en v2.0.0

    @classmethod
    def crear(cls, nombre) -> EstrategiaZona:
        try:
            return cls._zonas[nombre]()
        except KeyError:
            raise ValueError("zona inválida") from None


# ------------------------------------------------------------ funciones puras
def _validar_peso(peso: Decimal) -> None:
    if peso <= 0 or peso > PESO_MAX_KG:
        raise ValueError("peso inválido")


def _validar_dia(dia) -> None:
    if dia not in range(1, 8):
        raise ValueError("día inválido")


def _validar_cupon(cupon, zona: EstrategiaZona) -> None:
    if cupon is None:
        return
    if not zona.acepta_cupon:           # [CAMBIO] R9
        raise ValueError("la zona no acepta cupón")
    if cupon not in DESCUENTO_POR_CUPON:
        raise ValueError("cupón inválido")


def _tarifa_base(peso: Decimal) -> Decimal:
    if peso <= LIMITE_TRAMO_1_KG:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2_KG:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2_KG) * TARIFA_KG_ADICIONAL


def _aplicar_descuentos(valor: Decimal, cliente, cupon) -> Decimal:
    """Regla B impar: primero el cliente y luego el cupón, de forma sucesiva."""
    valor = valor * (1 - DESCUENTO_POR_CLIENTE.get(cliente, Decimal("0")))
    if cupon is not None:
        valor = valor * (1 - DESCUENTO_POR_CUPON[cupon])
    return valor


def _recargo_fin_de_semana(valor: Decimal, dia) -> Decimal:
    """Regla E impar: se suma después de los descuentos."""
    return valor + RECARGO_FINDE if dia in DIAS_FIN_DE_SEMANA else valor


def _redondear(valor: Decimal) -> int:
    """Múltiplo de $100 más cercano; los $50 suben."""
    unidades = (valor / MULTIPLO_REDONDEO).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(unidades * MULTIPLO_REDONDEO)


# ----------------------------------------------------------------- función pública
def calc(peso, zona, cliente, dia, cupon=None) -> int:
    peso = Decimal(str(peso))
    _validar_peso(peso)
    estrategia = ZonaFactory.crear(zona)
    _validar_dia(dia)
    _validar_cupon(cupon, estrategia)

    valor = estrategia.aplicar(_tarifa_base(peso))
    valor = _aplicar_descuentos(valor, cliente, cupon)
    valor = _recargo_fin_de_semana(valor, dia)
    valor = max(valor, COSTO_MINIMO)
    return _redondear(valor)
