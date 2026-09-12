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
| 5. La autenticación sin secreto en la URL queda como trabajo de U2 | Resuelta: `circuit/auth.py` es el servidor de autorización del sistema y el extremo del conector vive en `/mcp`, sin secreto en la ruta. Lo que abre el conector es un token que el creador aprobó |
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
  access.py      capacidad del panel del creador
  auth.py        servidor de autorización del conector: registro, consentimiento, código y token
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

### Cuatro formas que merecen justificación

**Aprobar la interpretación de los criterios es lo que abre el canal.** El manifiesto y
`PLAN.md` ponen la revisión del creador **antes** de abrir la convocatoria. Si abrir y revisar
fueran dos actos separados, la propiedad dependería de que alguien se acuerde del orden. Acá un
canal nace en `preparacion`, no recibe nada, y el único camino a `abierta` es
`approve_calibration`: un canal está abierto **si y solo si** su calibración fue aprobada, y el
estado no puede decir otra cosa. El creador también puede devolver la interpretación con una
discrepancia: queda registrada junto a la interpretación que corrige y el canal sigue sin abrir.
Cortar la ronda de una convocatoria la cierra, y desde entonces tampoco recibe.

**La pertenencia a una ronda se deriva, no se guarda.** Una ronda conoce su canal, su corte y el
corte anterior; el conjunto de propuestas sale de esos tres datos. Guardarlo permitiría que la
lista almacenada y la regla dijeran cosas distintas, que es exactamente el defecto que la ronda
existe para impedir.

**Los criterios sí se congelan.** Es lo contrario del caso anterior y por la misma razón: los
criterios del canal cambian por decisión del creador, y una ronda evaluada bajo unos criterios no
puede quedar descrita por otros. La ronda guarda la copia con la que se cortó.

**La declaración de campos manda en las dos direcciones.** `domain.PUBLISHABLE_FIELDS` alimenta
el aviso previo al envío, la proyección del almacén y el renderizado del portal y de la vista de
vivo, recorridos en su orden declarado; un campo vacío se muestra vacío en vez de desaparecer,
porque un campo que se esfuma cuando no tiene texto también separa lo prometido de lo expuesto.
Y `domain.PRIVATE_FIELDS` manda en la dirección contraria: **un campo declarado privado no vuelve
nunca a la página**. La corrida de `C-U2-1` mostró dónde importaba: al rechazar un envío, el
formulario se rendizaba otra vez con lo que el participante había escrito, para que no tuviera
que tipearlo de nuevo, y el contacto entraba en esa respuesta y de ahí en la evidencia. Ahora los
campos privados se descartan antes de rendizar; los largos vuelven y el contacto se escribe de
nuevo. La separación deja de depender de qué página se esté armando.

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

## La autenticación del extremo

U1 registró que el acceso por capacidad en la URL **no es apto para el producto** y dejó la
autenticación sin secreto en la URL como trabajo de U2. `PLAN.md` la ejercita: C2.6 exige
operación real con acceso autorizado y C2.8 ejercita una sesión sin la integración disponible
**o sin autorización**. Está resuelta.

**Por qué este mecanismo y no otro.** El producto probado admite exactamente dos formas de
conectar una app propia: una URL pública sin autenticación, u OAuth. No hay una tercera. Entonces
«autenticación sin secreto en la URL» significa el flujo de autorización de MCP y nada más. No es
una preferencia de diseño: es lo único que queda cuando se descarta lo que U1 descartó.

**Cómo quedó.** El servidor es a la vez servidor de autorización y servidor de recurso, porque es
un solo proceso que el creador instala:

- el conector vive en `/mcp`, sin capacidad en la ruta. Una llamada sin token responde `401` con
  `WWW-Authenticate`, y ahí es donde el anfitrión aprende a dónde ir a autorizarse;
- el anfitrión se registra solo —registro dinámico— y pide autorización. Registrarse no es
  autorizarse: un cliente registrado no tiene nada hasta que el creador decide;
- la solicitud queda estacionada y el anfitrión es enviado a `/conectar`, **una ruta sin ningún
  secreto**. Esto importa: esa URL se le entrega a un agente de autorización ajeno, viaja por la
  exposición pública y queda en historiales y registros intermedios, así que poner ahí la
  capacidad del panel habría reintroducido exactamente el problema que U1 señaló;
- lo que prueba al creador del otro lado es su **sesión**, abierta al llegar al panel con la
  capacidad. Sin esa sesión `/conectar` no muestra nada: ni quién pide, ni para qué. Consentir no
  es una pantalla de login nueva con credenciales nuevas que guardar: es una decisión más del
  creador, al lado de las que autorizan publicar e invitar;
- aprobar es lo que emite el código; el código se gasta una sola vez; el intercambio con PKCE
  entrega el token que el conector lleva desde entonces. El panel lista qué aplicaciones están
  conectadas y cuáles esperan decisión.

**Qué sigue sin demostrarse acá.** Que un anfitrión real complete este flujo. Eso solo lo muestra
una corrida real contra el producto, y es lo que el contrato correspondiente tiene que ejercitar
junto con C2.6 y C2.8. La verificación local demuestra que el flujo emite, valida y revoca
tokens; no demuestra interoperabilidad.

**Qué no cambió.** La capacidad sigue gobernando el panel, que es la superficie local del creador
y no es lo que U1 señaló. Y tener un token no alcanza para publicar ni invitar: eso sigue
exigiendo la autorización del creador por ronda, en el panel.

## Qué preserva una corrida

Una verificación que dependa de lo que alguien recuerde, relate después o pueda repetir no es
auditable. Por eso la corrida produce artefactos y no solamente pantalla:

| Artefacto | Qué conserva | Para qué alcanza |
|---|---|---|
| `.data/llamadas.jsonl` | el cuerpo completo de cada solicitud y cada respuesta MCP, en el orden en que ocurrieron | comprobar qué devolvió realmente cada herramienta, incluido que ninguna respuesta trae un contacto |
| `.data/capturas/*.html` | los bytes exactos que devolvió cada superficie, tanto al consultarla (`capturar`) como al enviarle un formulario (`enviar`), aceptaciones y rechazos por igual | comparar lo anunciado antes del envío con lo expuesto después, leer cómo se presenta la fecha y leer el texto exacto de cada rechazo |
| `.data/sesiones/*.json` | las cookies de cada participante sintético entre llamadas | que una secuencia de votos sea del mismo participante y no de uno nuevo cada vez |
| `.data/evidencia.json` | canales y su estado, calibraciones con su aprobación o su discrepancia, propuestas, rondas con su conjunto derivado y sus autorizaciones, evaluaciones con evaluador, razones y dudas, invitaciones, registros vinculados, votos, llamadas, solicitudes y lista publicada con sus tres señales | seguir un identificador a lo largo de todo el recorrido sin repetir la corrida |
| `.data/evidencia.json` → `conexiones` y `tokens` | qué aplicación pidió conectarse, cuándo, y cuándo el creador la aprobó; y qué tokens existieron, de qué tipo y si fueron revocados, cada uno por su huella y nunca por su valor | comprobar después que la autorización ocurrió y que un token revocado dejó de servir, sin depender del relato |
| `artefactos` dentro de la evidencia | nombre, tamaño y SHA-256 de cada archivo anterior | comprobar que lo que se lee después es lo que la corrida produjo |

Dos cosas no salen nunca en la evidencia: el contacto de un participante, y los secretos que
permitirían actuar en nombre de otro. La capacidad del creador y los testigos de las invitaciones
se reemplazan por `<capacidad>` y `<testigo>` en todo lo que se preserva; la marca del votante
viaja como huella. Cada sustitución se ve como tal, y el resto queda textual.

**Los testigos se sustituyen por valor, no por forma.** La corrida de `C-U2-1` demostró que
reconocer un testigo por la forma en que viaja no alcanza: la sustitución cubría el enlace y no
el campo suelto que devolvía la herramienta, y el testigo quedó en claro en la evidencia. Ahora
la sustitución lee los testigos emitidos y reemplaza esos valores exactos, sin depender de
adivinar dónde aparecen; el patrón sobre el enlace queda como segunda red para un testigo que esa
base no conozca. Y el testigo dejó de viajar como campo propio en la respuesta de la herramienta:
va solo dentro del enlace que el participante tiene que abrir, porque cada lugar por el que pasa
un secreto accionable es un lugar donde puede quedar copiado.

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
- **No demuestra interoperabilidad de la autenticación.** El flujo está implementado y se
  ejercita localmente; que un anfitrión real lo complete pertenece al contrato de la corrida real.
- **No expone el sistema a la red.** La exposición pública sigue siendo H-2 y decisión humana de
  costo.
- **No implementa la votación configurable** más allá del máximo por participante con tres por
  omisión: fijar la configuración antes de abrir y no cambiarla durante la ronda es C3.13, en U3.

## Riesgos propios de esta forma

- **La elección de herramienta del modelo no es determinista.** Si el modelo responde con su
  propia transcripción en lugar de abrir la vista, el creador ve texto plausible no literal. Se
  mitiga con instrucciones y con el aviso dentro de cada respuesta de datos; no se elimina.
- **La capacidad del panel sigue siendo un secreto portador en una URL.** Es la superficie local
  del creador, no el conector, y no es lo que U1 señaló; queda declarada como tal. El conector ya
  no depende de ella.
- **El ejecutor determinista podría leerse como evaluación real.** Mitigado porque el nombre del
  ejecutor se guarda con cada evaluación y viaja en la evidencia exportada.
- **El testigo de ampliación es un enlace no adivinable.** Quien lo obtenga puede responder en
  nombre de esa autoría. Es el precio de no depender de que el participante copie un código, y
  queda acotado a una respuesta por invitación.
