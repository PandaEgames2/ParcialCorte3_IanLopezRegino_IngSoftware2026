# Changelog
Todos los cambios notables de este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el
proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [2.1.0] - 2026-11-11
### Added
- Zona insular (San Andrés) con recargo del 70 % (R4).
- Regla R9: los envíos a zona insular no aceptan cupón ("la zona no acepta cupón").
- Pruebas TC37-TC40 (escritas antes que el código, TDD) e IT04.

## [2.0.0] - 2026-11-11
### Changed
- **BREAKING:** nueva firma `calc(peso, zona, cliente, dia, cupon=None)`; los parámetros
  p, z, c, d, cup pasan a tener nombres descriptivos.
- Cálculo dividido en funciones puras; constantes con nombre; dinero con Decimal.
- Zonas implementadas con el patrón Estrategia + Factory.
### Removed
- **BREAKING:** argumento `flag` y su `print` de depuración.
### Fixed
- DEF-01 el peso máximo es 45 kg (antes 50).
- DEF-02 una zona inválida lanza ValueError (antes se cobraba como urbana).
- DEF-03 el sábado recibe el recargo de fin de semana.
- DEF-04 el recargo de fin de semana se suma después de los descuentos.
- DEF-05 redondeo al múltiplo de $100 más cercano (los $50 suben).
- DEF-06 un cupón inexistente lanza ValueError.
- DEF-07 un día fuera de 1-7 lanza ValueError.
- DEF-08 el mensaje de error es exactamente "peso inválido".

## [1.0.0] - 2026-11-11
### Added
- Versión heredada de `calc()` con CONFIG diligenciado (código estudiantil 0182310059).
