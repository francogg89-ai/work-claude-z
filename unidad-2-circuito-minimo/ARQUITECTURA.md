# ARQUITECTURA — Unidad 2: circuito mínimo completo

Qué forma tiene el circuito que U2 construye, por qué esa y no otra, y qué decisiones quedan
declaradas en lugar de escondidas dentro de la implementación.

No describe estado ni resultados: lo que se haya verificado vive en `EVENTO.md` y, cuando exista,
en la interpretación del AUDITOR. Donde este documento y `PLAN.md` difieran, prevalece el plan;
donde el plan y el manifiesto difieran, prevalece el manifiesto.

## De dónde sale cada decisión

U1 cerró con `OPCIÓN DEMOSTRADA` y dejó siete condicionamientos sobre U2. No son sugerencias:
son el resultado de una corrida real y esta arquitectura los toma como dados, sin ampliarlos.

| Condicionamiento de `unidad-1-viabilidad-ia-contratada/RESULTADO.md` | Qué produjo acá |
|---|---|
| 1. El sistema expone un servidor MCP remoto por HTTPS, sin SSE, con herramientas anotadas y canal de vista | `circuit/creator.py` y `circuit/app.py`: transporte HTTP con respuestas JSON, `405` al `GET` que abriría un stream, anotaciones de lectura y escritura por herramienta |
| 2. Las acciones consecuentes las autoriza el sistema, no una confirmación de ChatGPT | `circuit/panel.py`: publicar e invitar se autorizan en una superficie del sistema. La IA pide y lee; no otorga |
| 3. El creador necesita un camino verificable para saber que lo que ve vino del sistema | `circuit/view.py`: la vista calcula la huella de lo que realmente mostró y la compara con la del servidor |
| 4. El enlace de entrada debe indicar que el original se consulta por la vista, y su control negativo tiene un modo de fallo observado | `/entrada-creador` exige confirmar el acceso antes de operar y prohíbe presentar lo que no se obtuvo del sistema |
| 5. La autenticación sin secreto en la URL queda como trabajo de U2 | Aislada en `circuit/access.py` y **declarada como decisión abierta** más abajo; no se congela sin la evidencia que la decide |
| 6. La paginación por cursor entra en el diseño desde el principio | `Store.list_proposals` devuelve resumen más `next_cursor`; el detalle se pide por propuesta |
| 7. El tratamiento de datos reales frente a la opción de entrenamiento del proveedor es restricción de diseño | U2 corre solo con datos sintéticos marcados en el propio dato; la materia documental es de U4 |

Además, U1 midió dos cosas que ninguna instrucción corrige y que por eso están tratadas por
diseño y no por prompt: el texto libre del modelo no es literal, y la elección de herramienta no
es determinista. La consecuencia es que el original **no viaja por la prosa del modelo**:
`ver_propuesta` es el canal fiel, y `obtener_propuesta` lo repite en su propia respuesta cada vez
que entrega texto. Lo que no se puede hacer desde acá es obligar al modelo a elegir la
herramienta correcta; eso queda como límite declarado, no como propiedad prometida.

## Forma del sistema

Tres superficies, un proceso, un almacén. Son un solo circuito: lo que la audiencia envía en la
superficie pública es lo que la IA del creador lee por MCP y lo que el creador autoriza en el
panel.

```text
sistema/circuit/
  domain.py      reglas que no dependen de almacenamiento ni transporte
  store.py       SQLite: original inmutable, contactos aparte, rondas, autorizaciones, operaciones
  evaluation.py  frontera de evaluación y ejecutor determinista local
  public.py      guía, formulario, ampliación con testigo, portal, vivo, votación, entrada del creador
  panel.py       superficie privada del creador: revisión de calibración y autorizaciones
  creator.py     servidor MCP que opera la IA del creador
  view.py        vista MCP Apps del original, con comparación de huellas
  access.py      frontera de acceso de las dos superficies privadas
  app.py         composición, registro de solicitudes y ausencia de stream iniciado por el servidor
  synthetic.py   participaciones sintéticas reproducibles
  launch.py      preparación, arranque, enlaces y exportación de evidencia
```

El panel y el conector viven detrás de la misma capacidad; la superficie pública no la conoce y
el enlace de entrada del creador no la contiene.

## Las decisiones del plan, realizadas

Las decisiones técnicas 1 a 14 de `PLAN.md` §7 no se reinterpretan. Dónde vive cada una:

| Decisión | Dónde |
|---|---|
| 1. Dato sintético marcado en el propio dato | `synthetic.py` y `domain.SYNTHETIC_MARK`; la marca viaja en el texto y en la autoría |
| 2. Original inmutable; toda ampliación es registro nuevo | `records` en `store.py`; no existe ningún `UPDATE` sobre `proposals` |
| 3. Contactos separados desde la primera versión | tabla `contacts`; ningún método que alimente una superficie pública o un modelo la lee |
| 4. Propuestas y enlaces como datos, nunca como instrucción | `evaluation.evaluation_payload` separa canal de autoridad y lista los enlaces que no recupera |
| 5. Idempotencia por identificador de operación | `Store._run_once`; publicar e invitar pasan por ahí |
| 6. Tres señales separadas, sin cuarto ranking | `domain.signals_view`, con la advertencia en el portal, en el vivo y en la herramienta MCP |
| 7. Vínculo de la ampliación emitido por el sistema | testigo de `prepare_invitation`; el enlace identifica propuesta y autoría sin que nadie copie un código |
| 8. Evaluación detrás de una frontera con ejecutor determinista | `evaluation.py`; el nombre del ejecutor se guarda con cada evaluación |
| 9. Ningún secreto en Git ni en material distribuido | la capacidad se genera local en `.data`, ignorado por Git; `launch enlaces` avisa cuáles no se pegan en público |
| 10. Operar exige acceso efectivo | `INSTRUCTIONS` del servidor y `/entrada-creador`; `estado_del_sistema` es la confirmación |
| 11. La IA del participante asiste; el envío es siempre por el formulario | la guía lo dice y el sistema no se integra con ninguna IA de participante |
| 12. Una propuesta pertenece a un solo canal; la ronda es la unidad de evaluación | `domain.round_membership` |
| 13. Cada registro vinculado lleva autor y tipo de relación | `records.kind` y `records.author`; la colaboración de terceros existe como tipo y está deshabilitada por defecto |
| 14. Campos publicables declarados en un único lugar | `domain.PUBLISHABLE_FIELDS` alimenta el aviso previo al envío y la proyección pública |

### Dos formas que merecen justificación

**La pertenencia a una ronda se deriva, no se guarda.** Una ronda conoce su canal, su corte y el
corte anterior; el conjunto de propuestas sale de esos tres datos. Guardarlo permitiría que la
lista almacenada y la regla dijeran cosas distintas, que es exactamente el defecto que la ronda
existe para impedir.

**Los criterios sí se congelan.** Es lo contrario del caso anterior y por la misma razón: los
criterios del canal cambian por decisión del creador, y una ronda evaluada bajo unos criterios no
puede quedar descrita por otros. La ronda guarda la copia con la que se cortó.

## Los límites del formulario, justificados

El manifiesto pide límites justificados y probados, y prohíbe exigir una elaboración extensa.

| Campo | Mínimo | Máximo | Por qué |
|---|---|---|---|
| Qué proponés | 20 | 400 | 400 caracteres son unas 60 palabras: alcanza para enunciar una propuesta entendible y no admite un ensayo. El mínimo descarta un envío que no dice nada |
| Por qué aporta | 20 | 400 | mismo criterio: una razón, no una defensa |
| Ejemplo o detalle | 0 | 600 | **opcional**: exigirlo convertiría la participación en una tarea. Algo más largo que los anteriores porque acá sí cabe un detalle concreto |
| Autoría | 1 | 80 | un nombre visible, no una biografía |
| Contacto | 5 | 120 | una dirección de correo |

El texto del participante se guarda tal como lo envió: la única normalización es recortar los
espacios de los extremos. Ninguna otra parte del sistema reescribe un original.

## Decisión declarada y ruteada: la autenticación del extremo

U1 registró que el acceso por capacidad en la URL **no es apto para el producto** y dejó la
autenticación sin secreto en la URL como trabajo de U2. Esta arquitectura **no la resuelve**, y no
esconde esa decisión dentro de la implementación:

- ningún caso de U2 en `PLAN.md` ejercita la autenticación del extremo, y §14.1 del método
  prohíbe presentar como validada una propiedad que no fue ejercitada;
- el único mecanismo que ChatGPT admite además de la URL sin autenticación es OAuth, y U1 dejó
  expresamente que **no se probó** que funcione en la cuenta de referencia. Congelarlo acá sería
  fijar un mecanismo sin la evidencia que lo decide, que es lo que `PLAN.md` §7 difiere bajo
  «forma de exposición pública del sistema»;
- probarlo consumiría una intervención humana material —cuenta, exposición y sesión real— que el
  criterio de terminación de U2 no pide.

Lo que sí se hizo es acotar el daño y aislar el reemplazo: la capacidad se genera local, nunca
entra en Git ni en el enlace de entrada, vive en un único módulo (`access.py`) del que dependen
las dos superficies privadas, y toda acción consecuente exige además la autorización del creador
en el panel, de modo que tener la capacidad no alcanza para publicar ni invitar.

El CONSTRUCTOR no declara que esta decisión sea correcta: la declara y la rutea. Si el AUDITOR
sostiene que U2 debe cerrar con autenticación sin secreto en la URL, corresponde un contrato
propio y, con él, la intervención humana material que hoy no está pedida.

## Lo que este candidato no hace

- **No endurece nada.** Revisión de no seleccionadas, sesgos, similitud, duplicados, agrupación,
  volumen, tiempos, consumo y recuperación de errores son U3. Acá está la versión más delgada que
  hace cerrar el ciclo (R4).
- **No usa un modelo real para evaluar.** El ejecutor determinista existe para que el circuito
  corra local; no sustituye ninguna prueba de integración (RT-2) y no decide H-4.
- **No envía comunicaciones reales.** La invitación produce un enlace con testigo; entregarlo es
  una decisión del creador y no una condición de verificación (R5). Por eso H-3 no se activa.
- **No promete identidad de votantes.** El control de votación marca el navegador y el portal dice
  exactamente eso y su límite.
- **No demuestra comprensión de una persona real.** Que la guía se entienda sin ayuda solo lo
  decide el piloto, que el manifiesto deja fuera del cierre técnico.
- **No expone el sistema a la red.** La exposición pública sigue siendo H-2 y decisión humana de
  costo.
- **No implementa la votación configurable** más allá del máximo por participante con tres por
  omisión: fijar la configuración antes de abrir y no cambiarla durante la ronda es C3.13, en U3.

## Riesgos propios de esta forma

- **La elección de herramienta del modelo no es determinista.** Si el modelo responde con su
  propia transcripción en lugar de abrir la vista, el creador ve texto plausible no literal. Se
  mitiga con instrucciones y con el aviso dentro de cada respuesta de datos; no se elimina.
- **La capacidad en la URL es un secreto portador.** Mitigado por generación local, ausencia de
  Git, módulo único y autorización separada en el panel; no resuelto (arriba).
- **El ejecutor determinista podría leerse como evaluación real.** Mitigado porque el nombre del
  ejecutor se guarda con cada evaluación y viaja en la evidencia exportada.
- **El testigo de ampliación es un enlace no adivinable.** Quien lo obtenga puede responder en
  nombre de esa autoría. Es el precio de no depender de que el participante copie un código, y
  queda acotado a una respuesta por invitación.
