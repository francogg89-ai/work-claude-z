# CHECKPOINT HUMANO — C-U2-7

## Estado

Este checkpoint es una propuesta sucesora de C-U2-6. No autoriza ejecución, instalación ni modificación del entorno. Solo será válido si el AUDITOR congela exactamente este checkpoint y el contrato C-U2-7, y si luego existe una H-2 nueva y una autorización humana nueva para esas identidades.

C-U2-6 permanece cerrado, agotado y fallido por P0. No se reabre ni se reintenta. La evidencia de C-U2-6 se conserva intacta.

## Intervención ambiental previa, no discriminante

La persona operadora debe trabajar en `unidad-2-circuito-minimo/sistema` y demostrar, antes de P0 y sin `.data`, túnel ni servidor:

```text
Get-Location
Test-Path .\.venv\Scripts\python.exe
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"
.\.venv\Scripts\python.exe -c "import pytest; print(pytest.__version__)"
.\.venv\Scripts\python.exe -m pip check
```

La salida completa se guarda en `evidencia-c-u2-7/entorno-preparacion.txt`, encabezando cada tramo con el comando efectivamente invocado. Debe quedar visible que el ejecutable real es el `.venv` del candidato y que pytest/dependencias están disponibles. Si falla cualquier comprobación, se detiene antes de P0. No se instala, no se modifica el entorno y se entrega la necesidad de autorización humana separada.

## Ejecución posterior, solo si la preparación pasa

Todos los comandos Python de la ejecución usan explícitamente:

```text
.\.venv\Scripts\python.exe
```

P0 es exactamente:

```text
.\.venv\Scripts\python.exe -m pytest -q tests/test_comandos_literales.py
```

La secuencia posterior es materialmente la de C-U2-6: C0, P1-P11, R5/R6, R3 antes de R0, R0, R1/R2/R4 y RZ, con doce conversaciones, los mismos estímulos y las mismas acciones humanas. No se reordenan, omiten, repiten ni adaptan pasos. Solo cambian el identificador `C-U2-7`, el directorio `evidencia-c-u2-7`, los marcadores sucesores y la forma del ejecutable Python.

Las acciones de navegador, ChatGPT, panel, formulario, instalación/autoridad del conector, capturas y Quick Tunnel las realiza la persona y se registran como tales. Si una acción exige instalar o modificar algo no disponible, se detiene y se solicita autorización humana específica.

## Reglas de detención

- La preparación ambiental falla: detenerse antes de P0.
- P0 falla, tiene omitidas o pruebas fallidas: preservar salida y detenerse; no reintentar.
- Cualquier paso posterior falla o no puede ejecutarse literalmente: preservar, bajar exposición si corresponde y detenerse.
- Nunca modificar evidencia de C-U2-4, C-U2-5 o C-U2-6.
- Nunca compartir secretos ni ejecutar con otro intérprete.

## Evidencia

La evidencia nueva queda en `evidencia-c-u2-7/`, incluyendo `entorno-preparacion.txt`, `p0-comandos.txt`, `DETENCION.md` si corresponde, y el paquete material completo solo si la corrida supera P0 y continúa. El checkpoint no se aplica hasta que el AUDITOR lo congele y el humano autorice la nueva ejecución.
