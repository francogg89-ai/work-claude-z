# CONTRATO PREVIO DE VERIFICACIÓN — C-U2-7

## Naturaleza y antecedente

`C-U2-7` es un sucesor separado conforme a REVOLUTIONS §6.1. No reabre, corrige ni reintenta `C-U2-6`, que permanece cerrado, agotado y fallido por la regla de detención de P0. La causa trazada fue una selección incorrecta de intérprete: P0 se invocó con `C:\Python312\python.exe`, mientras el entorno previsto del candidato era `sistema\.venv\Scripts\python.exe`.

Se preservan sin cambios las propiedades, correcciones F-01..F-04, cierres D-11/D-12 y toda evidencia histórica de C-U2-4, C-U2-5 y C-U2-6. Las identidades del sucesor las fijará el AUDITOR al congelar.

## Objetivo del sucesor

Repetir la verificación discriminante de C-U2-6 únicamente si, antes de consumir P0, una preparación ambiental no discriminante demuestra objetivamente que todos los comandos se ejecutarán con el intérprete virtual del candidato y que `pytest==9.1.1` y las dependencias de `sistema/requirements.txt` están disponibles. La preparación no decide el resultado de los casos; solo evita agotar un contrato por una precondición implícita.

## Requisito de entorno explícito

El operador debe usar siempre el ejecutable relativo al repositorio:

```text
.\.venv\Scripts\python.exe
```

No se acepta que `python` dependa de PATH o de una activación implícita. Si el ejecutable no existe, si no puede importar pytest, si la versión no coincide o si las dependencias no satisfacen el entorno requerido, se detiene la preparación ambiental y se entrega la evidencia. No se instala ni modifica nada sin una autorización humana separada.

## Preparación ambiental no discriminante

Antes de P0, sin crear `.data` y sin abrir túnel, se registran en `evidencia-c-u2-7/entorno-preparacion.txt`, con el comando efectivamente invocado:

1. `Get-Location` y verificación de que la terminal está en `unidad-2-circuito-minimo/sistema`.
2. `Test-Path .\.venv\Scripts\python.exe`.
3. `.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"`.
4. `.\.venv\Scripts\python.exe -c "import pytest; print(pytest.__version__)"`.
5. `.\.venv\Scripts\python.exe -m pip check`.

La evidencia debe demostrar que el ejecutable real está dentro de `sistema\.venv`, que pytest está disponible y que el entorno es utilizable. Esta fase no ejecuta `circuit.launch`, no crea datos y no consume P0.

## Secuencia discriminante

Una vez aprobada la preparación ambiental y solo con el ejecutable explícito, se ejecuta la secuencia de C-U2-6 sin alterar orden, cardinalidad, estímulos, acciones humanas, controles, criterios ni reglas de detención. Todos los comandos Python se invocan como:

```text
.\.venv\Scripts\python.exe -m ...
```

La secuencia material, los mensajes M1, M1b, M2, M5 y M6, los doce bloques, R0, RZ, el baseline de M6, la evidencia, los secretos, los controles y los criterios C2.6, C2.7, C2.8, C2.10 y C2.11 son los del checkpoint sucesor C-U2-6, con estas sustituciones obligatorias: `C-U2-7`, `evidencia-c-u2-7`, marcadores `preparacion-c-u2-7` y `fin-c-u2-7`, y el ejecutable explícito indicado arriba.

P0 pasa a ser literalmente:

```text
.\.venv\Scripts\python.exe -m pytest -q tests/test_comandos_literales.py
```

Debe terminar con código 0, sin pruebas fallidas ni omitidas. Si no, se detiene, se preserva la salida y no se inicia C0 ni ningún paso posterior. No se reintenta.

## Evidencia y límites

Toda evidencia nueva pertenece exclusivamente a `unidad-2-circuito-minimo/evidencia-c-u2-7/`. La preparación ambiental queda separada de la evidencia discriminante. No se modifica ninguna evidencia histórica. No se instalan dependencias, no se abre Quick Tunnel, no se usa ChatGPT real y no se ejecuta C-U2-7 hasta una H-2 y autorización humana nuevas, ligadas al congelamiento exacto.

## Cierre de esta propuesta

Este contrato no autoriza ejecución. Requiere revisión del AUDITOR, fijación de `WORK_SHA` y blobs exactos, y un checkpoint humano congelado antes de cualquier preparación ambiental. Si la preparación requiere instalación o modificación, esa acción se devuelve al humano como una intervención separada.
