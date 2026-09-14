# ENTREGA — evidencia de la ejecución de C-U2-5

Paquete de evidencia de la ejecución autorizada de `C-U2-5`. Preserva lo ocurrido y declara las
incidencias; no dictamina el resultado del contrato, que corresponde al AUDITOR.

## Identidad

```text
CANDIDATE_WORK_SHA=3c6f7ef7a0091b80d67a52ec2a46f5082283f574
CONTRACT_BLOB_SHA=3764a7f61d093fcf9f51e4473baba57c90f8ed69
CHECKPOINT_BLOB_SHA=39b6379706d71c14767b3d2dacf81f3d93d17231
FREEZE_AUDIT_SHA=aeb4c994847cb2af17b01f19a11c6bd4b4e615c3
H2_Y_AUTORIZACION_AUDIT_SHA=194ccf1dae15b50f71c20eca93ac8e3d99f2aa27
BASE=https://attempting-basename-used-provided.trycloudflare.com
```

La URL de la exposición fue temporal y ya no existe.

## Quién hizo qué

| Actor | Acciones |
|---|---|
| CONSTRUCTOR | clon del candidato exacto y entorno virtual; P0; P1–P4; P6–P8; P9; P10; los marcadores antes de cada bloque; RZ; integración y redacción de este paquete. Cada comando del sistema se invocó con la forma literal del checkpoint, con el entorno virtual activado |
| Humano | P5 y P11 en el navegador; las conversaciones R5-1 a R4-2 en ChatGPT web; los envíos por el formulario; R0 completo; la autorización `publicar` de R1-1 en el panel; la revocación antes de R4-1; las transcripciones, textos, capturas y notas |

El CONSTRUCTOR no operó el navegador ni ChatGPT en esta ejecución.

## Secuencia registrada

| Bloque | Estado registrado | Artefactos |
|---|---|---|
| P0 | ejecutado; `7 passed`, `rc=0` | `p0-comandos.txt` |
| P1–P8 | ejecutados en orden; P7 imprimió `P-001` a `P-008` | `preparacion.txt` |
| P9–P10 | ejecutados; P10 con `python -m circuit.launch servir --expuesto --base <BASE>` | `p9-p10.txt` |
| P11 | ejecutado por el humano | `p9-p10.txt` (solicitud al panel) |
| R5-1, R5-2 | ejecutadas; un envío por el formulario en cada una | `transcripcion-R5-*.md`, `textos-R5-*.md`, `recepcion-P-009-R5-1.png`, `recepcion-P-010-R5-2.png` |
| R6-1, R6-2 | ejecutadas; un envío por el formulario en cada una | `transcripcion-R6-*.md`, `textos-R6-*.md`, `recepcion-P-011-R6-1.png`, `recepcion-P-012-R6-2.png` |
| R0 | ejecutado | `R0-conectar.png`, `R0-configuracion-conector.png`, `R0-configuracion-conector.txt`, `R0.md` |
| R1-1, R1-2 | ejecutadas | `transcripcion-R1-*.md`, `autorizacion-publicar-R1-1.md` |
| R2-1, R2-2 | ejecutadas | `transcripcion-R2-*.md` |
| R3-1 | ejecutada | `transcripcion-R3-1.md`, `estado-conector-R3.md` |
| R3-2 | **no ejecutada** (ver incidencias) | `R3-2-no-ejecutada.md` |
| R4-1, R4-2 | ejecutadas | `transcripcion-R4-*.md`, `reautorizacion-R4-*.md`, `image.png` |
| RZ | ejecutado; exposición bajada | `rz.txt`, `evidencia.json` |

Marcadores: `marcadores.txt` registra cada invocación; la exportación contiene, en orden,
`preparacion-c-u2-5`, `R5-1`, `R5-2`, `R6-1`, `R6-2`, `R0`, `R1-1`, `R1-2`, `R2-1`, `R2-2`,
`R3-1`, `R3-2`, `R4-1`, `R4-2` y `fin-c-u2-5`.

Transcripciones entregadas: **once**. Falta la de R3-2, que no se ejecutó.

## Incidencias declaradas

1. **R0, pausa por la URL de `/conectar`.** La página abrió con `?solicitud=SOL-…`. El humano se
   detuvo antes de autorizar y pidió clasificación. El CONSTRUCTOR respondió, contra el código del
   candidato y el contrato, que ese identificador no es capacidad, token ni testigo, y que el paso
   se podía ejecutar como estaba escrito; el humano continuó. El CONSTRUCTOR declara que su propia
   instrucción previa agregó «que no debe llevar ningún código largo», frase que proviene del
   checkpoint de `C-U2-3` y no está en el de `C-U2-5`; eso originó la pausa.
2. **R0, captura truncada.** La interfaz de ChatGPT trunca la URL del conector en la captura. El
   humano preservó además el texto copiado de la configuración con la URL completa terminada en
   `/mcp` (`R0-configuracion-conector.txt`). `R0.md` es idéntico byte a byte a ese archivo. La
   configuración mostraba «No app actions available yet»; no se pulsó Refresh ni se reintentó.
3. **R3-1, conector.** El humano no seleccionó el conector en la conversación, pero la conexión
   global seguía activa. El registro del servidor muestra siete `POST /mcp 200` en la ventana de
   R3-1.
4. **R3-2, no ejecutada.** La interfaz de ChatGPT no ofrece deshabilitar el conector solo en una
   conversación; la única opción era desconectarlo globalmente, cosa que el procedimiento no
   ordena en ese punto. El CONSTRUCTOR no autorizó ni reinterpretar «sin el conector habilitado» ni
   adelantar la desconexión, y aplicó la regla de continuidad del checkpoint para una conversación
   que «no puede completarse»: no se envió el mensaje, no hubo conversación de reemplazo y se siguió
   con R4-1. El marcador `R3-2` se había colocado antes y quedó sin conversación.
5. **Revocación antes de R4-1.** El humano declara haber pulsado una vez «Revocar esta conexión»;
   el registro del servidor muestra dos `POST …/revocar 303`. El panel siguió mostrando la
   aplicación como autorizada, que es lo que el candidato hace: revocar marca los tokens y la lista
   del panel se arma con las solicitudes aprobadas. La exportación muestra los dos tokens de la
   conexión revocados.
6. **R4-1 y R4-2, pedido de reconexión.** ChatGPT pidió reconectar la app; el humano pulsó «Not
   now» en ambas y no reautorizó. `image.png` es la captura de ese pedido; por contenido y hora
   corresponde a R4-1.
7. **R1-1, autorización.** El humano autorizó `publicar` una vez desde el panel; la conversación no
   retomó por sí sola y no se agregó texto.
8. **Datos de contacto.** Los envíos usaron contactos sintéticos `@example.invalid`. En los
   archivos de textos el valor del contacto no se transcribió, por indicación del CONSTRUCTOR, para
   que no quede un dato de contacto en un artefacto. Ningún archivo de texto del paquete contiene una
   dirección de correo.
9. **Direcciones IP.** `p9-p10.txt` conserva, como las emite el servidor, las direcciones IP de los
   clientes que llegaron por la exposición, entre ellas la del navegador del humano. No son un
   secreto del checkpoint y no se redactaron; se señalan por tratarse de un dato de red personal.
10. **Codificación de `rz.txt`.** La salida de `taskkill` llega en la página de códigos de la
    consola de Windows; se convirtió a UTF-8 sin quitar líneas.

## Secretos

- La capacidad del panel apareció en las consolas de P4 y P10 y se sustituyó por `<capacidad>` en
  cada aparición: 5 en `preparacion.txt` y 11 en `p9-p10.txt`, cada archivo con su nota.
- Se buscó por valor, en todos los artefactos de texto, la capacidad, los tokens emitidos, los
  testigos, los contactos de la base y enlaces de ampliación completos: fuera de esas 16
  apariciones de capacidad, redactadas, no hay ninguna. Las capturas se revisaron visualmente:
  ninguna muestra la URL del panel ni un token.
- La capacidad no está en ningún archivo del repositorio. Pasó por el contexto del CONSTRUCTOR solo
  para redactarla por valor.

## Estado que queda

- Servidor y Quick Tunnel detenidos; la URL de `<BASE>` ya no existe.
- La base del clon de ejecución `work-claude-z-c-u2-5` queda como la dejó RZ.
- En ChatGPT sigue instalada la app «Circuito propuestas C-U2-5», con su conexión revocada en el
  sistema.
- `evidencia-c-u2-4/**`, contratos, checkpoints y demás material histórico no se modificaron.
