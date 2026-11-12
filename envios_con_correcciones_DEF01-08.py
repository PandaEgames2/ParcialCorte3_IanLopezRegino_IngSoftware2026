# envios.py
import math

CONFIG = {
    "L1": 3,  # <- pon tus valores
    "L2": 10,
    "RECARGO_RURAL": 0.15,  # como fracción, ej. 0.15
    "RECARGO_NACIONAL": 0.40,
    "DESC_VIP": 0.10,
    "RECARGO_FINDE": 2000,  # en pesos
}

def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > 45:
        raise ValueError("peso inválido")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    else:
        raise ValueError("zona invalida")                                                    # DEF-02
    if d < 1 or d > 7:
        raise ValueError("dia invalido")                                                     # DEF-07
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup != None:
        if cup == "ENVIO10":
            t = t - t * 0.10
        else:
            raise ValueError("cupon invalido")                                               # DEF-06
    # fin de semana (después de los descuentos)                                              # DEF-04
    if d >= 6:                                                                               # DEF-03
        t = t + CONFIG["RECARGO_FINDE"]
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(math.floor(t / 100 + 0.5)) * 100
