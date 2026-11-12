# Notas de la versión

## v2.1.0 — nueva funcionalidad
Los envíos a San Andrés (zona `insular`) cuestan un 70 % más que la tarifa base y **no admiten cupón**:
cualquier cupón, aunque sea `ENVIO10`, lanza `ValueError`. No hay que cambiar nada en los usos existentes.

## v2.0.0 — cambio importante (breaking)
El cálculo del costo quedó ordenado, probado y sin los 8 defectos conocidos (DEF-01 a DEF-08).

Cómo migrar:
1. Elimine el argumento `flag`; si necesita ver el costo, imprima el valor que retorna `calc`.
2. Si llama con palabras clave, use `peso`, `zona`, `cliente`, `dia` y `cupon`.
3. Capture `ValueError`: ahora se lanza para zona, día o cupón inválidos, que antes se ignoraban.
4. Espere cambios de valores: sábado con recargo, recargo después de descuentos y redondeo al más cercano.
