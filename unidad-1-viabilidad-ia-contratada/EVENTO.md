# EVENTO — Unidad 1: viabilidad de operación desde la IA contratada

## Qué recibió

Cabecera canónica con `INCOMING_TURN_ID=16`, emitida después de la reanudación de la necesidad
humana material. La instrucción fue: rederivar desde Git, tratar `C-U1-2A` y `C-U1-2B` como
agotados con éxito, integrar durablemente la evidencia exacta, preservar las limitaciones
observadas, consolidar requisitos, límites, costos y consumo observados y acciones manuales, y
preparar un candidato de cierre de U1. Sin declarar U1 cerrada, sin iniciar U2, sin ejecutar otra
verificación discriminante y sin modificar manifiesto, `PLAN.md` ni perímetro.

El prompt llegó truncado por delante, sin cabecera canónica. La intervención se detuvo antes de
producir material durable y pidió el `INCOMING_TURN_ID`, conforme a REVOLUTIONS §4.5: no se
infiere, no se reconstruye desde Git y no se deriva contando intervenciones. Con el entero
recibido, la intervención continuó.

La situación se rederivó desde Git sobre el corte recibido:

- La última entrega de work es `cb023ed6c53dd63470da9463a6ea1697294f1055`, que es además el
  candidato exacto contra el que se ejecutaron los dos contratos. El árbol estaba limpio.
- Los blobs congelados coinciden con el árbol recibido: `EVENTO.md` en
  `606a381320675f1d71b014ab504da30e1468e946` y `CHECKPOINT_HUMANO.md` en
  `b3dcb702deec3cc9656eb4ec5025c8a515c96b1d`.
- La intervención auditora del corte es
  `resoluciones/H-U1-CONEXION-REAL-2-9c026956cf1cffd35d25f6c506b8a9236fa64989.md`, con
  `RESULTADO_C_U1_2A=EXITO`, `RESULTADO_C_U1_2B=EXITO`, ambos contratos agotados,
  `HUMAN_NEED_RESUELTA=SI` y `U1_CERRADA=NO`.
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

La evidencia se leyó en su identidad exacta, `francogg89-ai/error111 @
9c026956cf1cffd35d25f6c506b8a9236fa64989`, en un clon temporal de solo lectura.

## Qué hizo y por qué

Los dos contratos están agotados y su resultado se toma como lo interpretó el AUDITOR: no se
reabre, no se reinterpreta y no se propone ningún contrato nuevo. Lo que faltaba era el paso 6 de
U1 en `PLAN.md` —requisitos, límites, costos y acciones manuales identificados— como material
durable del trabajo y no solo como evidencia de una corrida.

- **`RESULTADO.md`, nuevo.** Consolida el resultado de la unidad: la clase de terminación que
  propone, la identidad exacta de todo lo que la sostiene, la cobertura de C1.1 a C1.5, los nueve
  requisitos identificados, los límites observados y declarados, costos y consumo, las acciones
  manuales separadas entre instalación, operación y prueba, lo que **no** quedó demostrado, lo que
  condiciona en U2 y el estado de R1, R2, R3, H-1, H-2 y H-6. Propone **opción demostrada** y dice
  expresamente que no declara el cierre.
- **`RELEVAMIENTO.md`, corrección puntual.** El relevamiento registra lo que la documentación
  dice; la segunda conexión resolvió empíricamente tres cosas que quedaban abiertas allí: que las
  vistas de MCP Apps funcionan en la cuenta Plus usada, que no hubo costo ni límite de uso
  observados, y que la elección de herramienta del modelo no es determinista. Se corrigieron esos
  puntos y se apunta a `RESULTADO.md` en lugar de repetir la consolidación.
- **`CHECKPOINT_HUMANO.md`, bloque de estado agregado.** El procedimiento quedó consumido. Sin
  ese aviso, el material de la unidad conserva una instrucción que se lee como pendiente, y
  repetirla sin un contrato nuevo congelado violaría REVOLUTIONS §6.1. El agregado es aditivo: no
  toca el procedimiento ni la evidencia que produjo.

**Por qué no se tocó la sonda.** Su código es el candidato exacto contra el que se ejecutaron los
contratos. Modificarlo rompería la correspondencia entre la evidencia y el candidato sin agregar
nada a lo que esta intervención debía producir. Tampoco se tocaron `PLAN.md`, `BOOTSTRAP.md` ni el
perímetro: las consecuencias de diseño que el resultado impone sobre U2 quedan registradas en
`RESULTADO.md` como condicionamientos, no como cambios de plan.

**Dos hallazgos que no estaban en la resolución auditora** y que salieron de leer la exportación
llamada por llamada, porque cambian el diseño de U2:

- Ante la misma petición, la primera conversación usó `show_proposal` y la repetición
  `get_proposal`; con `X-001` pasó lo mismo. El canal fiel no puede depender de que el modelo
  elija la herramienta con vista.
- La atribución de la app aparece en el panel `Sources` y no siempre como bloque de llamada en
  línea. El ejecutor creyó primero que dos peticiones no habían invocado la app. El creador no
  puede apoyarse en la interfaz para saber si un dato vino del sistema, y eso le da un modo de
  fallo concreto al control negativo C2.8 de U2.

## Verificación de esta entrega

Es una intervención documental: no se ejecutó ninguna verificación discriminante, no se abrió
ningún túnel y no se usó ChatGPT.

| Comprobación | Resultado |
|---|---|
| Identidad del corte y de los blobs congelados, por `git rev-parse` | `HEAD` igual al `WORK_SHA` congelado; `EVENTO.md` y `CHECKPOINT_HUMANO.md` iguales a los blobs del congelamiento |
| SHA-256 de los diez archivos de evidencia contra `SHA256SUMS.txt`, sobre los blobs de Git del commit exacto | los diez coinciden; `evidencia-servidor.json` da `a346857235534d044e4121b179b197df4bd71c32fde12b1e21512de0051bf2b6`, igual al declarado |
| Lectura directa de `evidencia-servidor.json` | 28 solicitudes, 12 llamadas, 2 evaluaciones; `original_fp=bac7f90c` en las cuatro lecturas de `P-042`; `resources/read` aceptado; tres `404` con ruta no coincidente entre los marcadores de capacidad inválida; `User-Agent openai-mcp/` en toda la ventana válida |
| `python -m pytest -q -rs`, suite completa en una sola corrida, Python 3.12.4 y Node v20.15.1 | `60 passed in 18.47s`, rc=0, sin omitidas |
| Medición local del tamaño de respuesta sobre el candidato con su semilla por omisión | página de 100 propuestas: 15.830 caracteres; detalle de `P-042`: 263 caracteres y huella `bac7f90c` |

La suite completa nunca se había ejecutado como una sola corrida: la entrega anterior lo declaró
como limitación. Queda cerrada por dos caminos independientes —la puerta G0 de la corrida humana,
con `60 passed`, y esta corrida local— y ninguno de los dos demuestra la integración, que solo la
evidencia de la corrida real sostiene.

## Limitaciones de esta entrega

- La exportación, las capturas y las transcripciones las produjo la ejecución humana. Son
  evidencia material reportada; ni el AUDITOR ni el CONSTRUCTOR la comprobaron de forma
  independiente. Lo único verificable desde acá es su integridad frente a los hashes declarados.
- La medición de tamaño de respuesta es local y sobre datos sintéticos: describe el candidato, no
  la corrida ni volúmenes reales.
- Todo el resultado está acotado a una cuenta, un plan, una IA y datos sintéticos, y el
  comportamiento de ChatGPT no es determinista.
- Los contratos `C-U1-2A` y `C-U1-2B` ya no están en el árbol de trabajo, porque `EVENTO.md` se
  actualiza por entrega y no acumula versiones. Su texto congelado sigue disponible en Git, en el
  blob `606a381320675f1d71b014ab504da30e1468e946`, citado en `RESULTADO.md`.
- `sonda/.venv` y `sonda/.data` quedan fuera de Git. El directorio `.atl/` del árbol es material
  de herramientas del entorno local, ajeno a esta entrega.

## Necesidad humana detectada

NECESIDAD DEL HUMANO — el cierre de U1 y la autorización para iniciar U2 son decisiones humanas
reservadas y separadas por la constitución del carril Z, y corresponden a H-6 del plan. No son
materiales: no exigen operar una cuenta, exponer una red ni gastar, y por eso esta entrega no
preserva ningún checkpoint nuevo. Con `RESULTADO.md` el candidato de cierre queda completo y
auditable.

El CONSTRUCTOR registra y rutea esta necesidad; no declara que sea real ni activa al humano. Esa
determinación, y el veredicto sobre si U1 termina como opción demostrada, corresponden al AUDITOR.
