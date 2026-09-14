# DETENCIÓN — ejecución de C-U2-4 en P10

Registro de la ejecución autorizada del tramo P1-P11 y R5-1 a R6-2 de `C-U2-4`, detenida en P10.
Preserva lo ocurrido; no interpreta el resultado del contrato ni corrige el procedimiento. El
veredicto corresponde al AUDITOR.

## Identidad

```text
WORK_SHA=28cc00366c8c97bb102d3defdf25750aa993e046
CANDIDATE_WORK_SHA=8786d3985dacba1e7a7139c1a498e8ed5e93161f
CONTRACT_BLOB_SHA=35c306a90fd016fbf6243b06f7a9e987ea917f6e
CHECKPOINT_BLOB_SHA=4a04b324d79099e0f130549232f29df76a7231a2
H2_AUDIT_SHA=f43962f55c2c0441596d5bf50bcf442c11e5cb19
AUTORIZACION_R5_R6_AUDIT_SHA=ebdde19503e8702eec9e2e6fa6191099bb184375
```

Ejecutó el CONSTRUCTOR, desde el clon `work-claude-z-c-u2-4` en `8786d398…`, con Python 3.12.4 y
el navegador Chrome «Claude-work», salvo P5, que pulsó el humano (ver abajo).

## Resumen

```text
EJECUCION_C_U2_4=DETENIDA
PASOS_COMPLETADOS=P1,P2,P3,P4,P5,P6,P7,P8,P9
PASO_DETENIDO=P10
P11=NO_EJECUTADO
R5_R6_EJECUTADAS=NO
R0_R1_R4_RZ_EJECUTADAS=NO
CHATGPT_USADO=NO (solo se abrió la portada logueada para comprobar la sesión; no se envió ningún mensaje)
TUNEL_ABIERTO=SI, entre P9 y la detención; BAJADO a las 2026-09-14T15:47:37Z
SERVIDOR_EXPUESTO=SI, entre P10 y la detención; DETENIDO a las 2026-09-14T15:47:37Z
REINTENTO_DE_PASOS=NO
```

## Qué pasó en P10

El checkpoint y el contrato escriben P10 así:

```text
python -m circuit.launch servir --expuesto --base <BASE>
```

En el candidato, `--base` es una opción del analizador principal y no del subcomando `servir`.
Escrito en ese orden, el comando no se puede parsear. Se comprobó sin efectos —reemplazando el
arranque del servidor por una función vacía—:

```text
-c: error: unrecognized arguments: --base https://ejemplo.invalid
SystemExit 2
```

**Adaptación no autorizada, declarada.** Antes de esa comprobación, el CONSTRUCTOR lanzó P10 como
`python -m circuit.launch --base <BASE> servir --expuesto`, con `--base` antes del subcomando, sin
intentar primero la forma literal. Ese servidor arrancó (`p10-servir-expuesto.txt`) y estuvo
detrás del túnel. Al advertir que la forma literal no era la ejecutada, se comprobó que falla, se
aplicó la regla de detención del checkpoint —«si un paso no puede ejecutarse como está escrito, o
termina con error, se detiene la ejecución en ese punto… se baja la exposición»— y se bajaron el
servidor y el túnel. No se abrió `<BASE>` en el navegador, no hubo solicitudes de terceros
registradas y no se avanzó a P11.

`P4` usa `servir` sin `--base` y no tiene este problema.

## Observaciones de la ejecución

- **cloudflared.** Instalado desde la distribución oficial, `github.com/cloudflare/cloudflared`,
  release `2026.9.1`, `cloudflared-windows-amd64.exe`. SHA-256
  `2837888cc0f5d58f15b6dc478376de90b4d3ba5241c7947455d1e0a0df429712`, igual al publicado en las
  notas del release. Queda fuera de Git, en el espacio local.
- **Sesión de ChatGPT.** Antes de P1 se abrió `chatgpt.com` en el navegador para confirmar la
  sesión, sin crear conversación ni enviar mensajes.
- **P5, pulsado por el humano.** El CONSTRUCTOR hizo dos clics automatizados sobre «Aprobar la
  interpretación y abrir el canal»; ninguno produjo una solicitud al servidor y el canal siguió en
  preparación. En la página hay una extensión de navegador que inyecta scripts. No se forzó el
  envío por JavaScript ni por HTTP. El humano pulsó el botón en esa misma pestaña
  (`P5_PULSADO_POR_HUMANO`); el registro del servidor muestra
  `POST …/calibracion/aprobar 303` y la base quedó con `convocatoria-1` abierta y
  `reviewed_at=2026-09-14T15:45:41.587928+00:00`.
- **Solicitud extra al panel, durante P5.** Para diagnosticar el clic fallido, el CONSTRUCTOR hizo
  un `GET` directo al panel local con `curl`. Figura en `preparacion.txt` como la segunda
  `GET /creador/<capacidad> 200` y abrió una sesión de creador adicional en la base. No es parte
  del procedimiento.
- **Lecturas de la base.** Se consultó la base en solo lectura para verificar el estado del canal.
- **Capacidad.** El valor de la capacidad pasó por el contexto del CONSTRUCTOR y por las llamadas de
  automatización del navegador para abrir el panel en P5. No se escribió en Git, en mensajes ni en
  artefactos: en los registros preservados está sustituido por `<capacidad>`, con la cantidad de
  apariciones anotada en cada archivo.
- **Marcadores.** Solo `preparacion-c-u2-4` (P8). No se creó ningún marcador de corrida.

## Artefactos

| Archivo | Contenido |
|---|---|
| `preparacion.txt` | salida de P1 a P8 en orden, con la de P4 intercalada; capacidad redactada (6 apariciones) |
| `p9-tunel.txt` | salida de `cloudflared` desde P9 hasta la detención |
| `p10-servir-expuesto.txt` | salida del servidor lanzado con la forma adaptada, hasta la detención; capacidad redactada (1 aparición) |

`rc=1` al final de P4 corresponde a la detención del servidor en P6. No se ejecutó `exportar`: es
parte de RZ.

## Estado que queda

- Túnel y servidor detenidos. La URL de la exposición ya no existe.
- La base del clon conserva `convocatoria-1` abierta con `P-001` a `P-008`, el marcador de P8, las
  solicitudes de P4 y P10 y la sesión extra abierta por `curl`. No se borró ni se modificó después.
- `CONTRATO-C-U2-4.md`, `CHECKPOINT_HUMANO-C-U2-4.md`, el candidato y el material de `C-U2-3`
  no se modificaron.
