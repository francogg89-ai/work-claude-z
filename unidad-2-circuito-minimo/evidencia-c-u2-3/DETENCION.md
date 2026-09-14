# DETENCIÓN — ejecución de C-U2-3

Registro de la detención informada por el humano durante la ejecución de `C-U2-3`. Este archivo
preserva lo informado; no interpreta el fallo, no lo corrige y no dictamina. El veredicto
corresponde al AUDITOR.

## Informe humano, literal

```text
EJECUCION_C_U2_3=DETENIDA

WORK_SHA=193439f38d709a65e89cce9e69954395a0c7851b
CHECKPOINT_BLOB=7fd4e6eb1ded31553f9b9a352428fc0743e9701ff
EVENTO_BLOB=a769509cecfd1aa0b6081bda19f8a7a55fd2446c

PASO_COMPLETADO=init --seleccionadas 4 --votos 3
PASO_FALLIDO=sembrar --canal convocatoria-1 --cantidad 8
ERROR=circuit.store.ClosedChannelError: «Convocatoria de ejemplo» todavía no está abierta: el creador no revisó aún la interpretación de sus criterios.
CAUSA_OBSERVADA=El checkpoint ordena sembrar antes de abrir el panel y aprobar la interpretación de criterios, pero el sistema exige esa aprobación antes de aceptar propuestas.
ACCIONES_POSTERIORES=NINGUNA
TUNEL_ABIERTO=NO
SERVIDOR_LEVANTADO=NO
CHATGPT_USADO=NO
R0_R6_EJECUTADAS=NO
REINTENTO=NO
SECRETOS_COMPARTIDOS=NO
```

Declaración humana adicional, literal:

> La salida original fue preservada. El valor de la capacidad del panel fue redactado sin ocultar
> que apareció.

## Ubicación en el procedimiento

- `PASO_COMPLETADO` corresponde al paso 2 de «Preparación del sistema» de `CHECKPOINT_HUMANO.md`.
- `PASO_FALLIDO` corresponde al paso 3 de esa misma sección.
- Los pasos 4 a 7 de la preparación, R0, R1 a R6 y RZ no se ejecutaron, según el informe.

## Observaciones del CONSTRUCTOR al integrar

Sólo comprobaciones de identidad y de estado, sin tocar nada:

- **Identidad de `CHECKPOINT_BLOB`.** El valor informado tiene 41 caracteres y no es un
  identificador Git válido. El blob real de `unidad-2-circuito-minimo/CHECKPOINT_HUMANO.md` en
  `193439f38d709a65e89cce9e69954395a0c7851b` es `7fd4e6eb1ded31553f9ba352428fc0743e9701ff`, que
  coincide con la terna de `ACTIVACION-H-2.md`. Se preserva el valor informado tal cual; no se
  corrige ni se declara equivalente. Lo resuelve el AUDITOR.
- **`WORK_SHA` y `EVENTO_BLOB`.** Coinciden con Git y con la terna activada.
- **Clon de ejecución.** `C:/FRANCO_PERSONAL/Ideas_streaming/work-claude-z-c-u2-3` está en
  `193439f38d709a65e89cce9e69954395a0c7851b` y contiene `sistema/.data/` con `capacidad` y
  `circuito.sqlite`. No se abrió ni se copió su contenido: lleva la capacidad.
- **Salida original.** No se entregó al CONSTRUCTOR en este turno, más allá de la línea `ERROR`
  transcripta arriba. No se reconstruye ni se completa: si el AUDITOR la requiere, se solicita al
  humano, que declara tenerla preservada con la capacidad redactada.

## Qué no hace este registro

- No modifica `CHECKPOINT_HUMANO.md`, `EVENTO.md`, `ACTIVACION-H-2.md`, el candidato, los
  paquetes de evidencia anteriores, `RESULTADO-LOCAL.md`, `PLAN.md` ni el perímetro.
- No adapta el orden del procedimiento ni propone uno corregido.
- No reintenta, no abre exposición, no levanta el servidor y no usa ChatGPT.
