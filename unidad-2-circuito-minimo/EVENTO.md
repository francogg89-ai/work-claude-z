# EVENTO — Unidad 2: circuito mínimo completo

Primera intervención de U2. Explica la semántica de la entrega; el delta exacto lo demuestra Git.

## Qué recibió

Cabecera canónica con `INCOMING_TURN_ID=20`, para un CONSTRUCTOR fresco por relevo. La
instrucción fue ejecutar U2 conforme a `PLAN.md` §4 y al manifiesto vigente, trabajando
únicamente dentro de `unidad-2-circuito-minimo`, sin modificar manifiesto, `PLAN.md` ni
perímetro, proponiendo toda verificación discriminante nueva como contrato previo conforme a
REVOLUTIONS §6.1 y sin ejecutarla antes del congelamiento del AUDITOR.

El prompt llegó truncado por delante en dos envíos sucesivos, sin cabecera canónica. La
intervención se detuvo antes de producir material durable y pidió únicamente el entero, conforme
a REVOLUTIONS §4.5: no se infiere, no se reconstruye desde Git y no se deriva contando
intervenciones. Es el mismo defecto de transporte que ya se había registrado en la última
intervención de U1.

La situación se rederivó desde Git, sin suponerla:

- la última entrega de work es `5830b23583e353ac5294b40bba66e256f473a48d`, con el árbol limpio
  salvo `.atl/`, que es material de herramientas del entorno local;
- el corte de audit trae tres intervenciones nuevas sobre la anterior: la auditoría de
  `5830b23`, `decisiones/cierre-u1-5830b23583e353ac5294b40bba66e256f473a48d.md` con
  `HUMAN_RESOLUTION_LITERAL=APROBAR_CIERRE_U1`, y
  `decisiones/inicio-u2-y-relevo-constructor.md` con `U2_AUTORIZADA=SI`,
  `RELEVO_CONSTRUCTOR_SOLICITADO=SI` y `NEXT_CONSTRUCTOR_INSTANCE=fresh`;
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas posteriores al bootstrap;
- U1 quedó cerrada con terminación `OPCION_DEMOSTRADA`, y su resultado se toma como dependencia
  cerrada: no se reabre, no se reinterpreta y no se vuelve a ejecutar ninguno de sus contratos.

Se leyeron en su identidad exacta el manifiesto (`MANIFEST_SHA=7011eb75…`), `PLAN.md` §4 y §7, el
método y `unidad-1-viabilidad-ia-contratada/RESULTADO.md`.

## Qué hizo y por qué

U2 es la unidad cuya propiedad es que el circuito **cierra**. Ninguna de sus partes demuestra esa
propiedad por separado, así que esta intervención construye el recorrido completo y delgado, y no
un trozo: recepción por dos canales, conservación del original, calibración revisada por el
creador, ronda con criterios congelados, evaluación con razones y dudas, invitación a ampliar con
vínculo verificable, segunda evaluación, publicación autorizada, portal, presentación para vivo y
votación. Sobre eso se propone el contrato previo que lo verifica.

- **`ARQUITECTURA.md`, nuevo.** Registra de dónde sale cada decisión, empezando por los siete
  condicionamientos que dejó U1; dónde vive cada una de las decisiones técnicas 1 a 14 de
  `PLAN.md` §7; la justificación de los límites del formulario; lo que el candidato no hace; y la
  decisión material que se declara y se rutea en lugar de esconderse.
- **`sistema/`, nuevo.** La implementación, con su suite de construcción. Tres superficies —la
  pública, el panel del creador y el servidor MCP— sobre un almacén, en un proceso.

**Las tres formas que sostienen las propiedades exigidas**, más allá de que el código las liste:

1. **La autorización no vive en la conversación.** U1 midió que la escritura se ejecuta sin
   confirmación de ChatGPT. Por eso publicar e invitar los autoriza el creador en el panel del
   sistema: la IA puede pedir la autorización y leer si existe, y no puede darla. `publicar` e
   `invitar` se rechazan hasta entonces y no dejan nada a medias.
2. **La pertenencia a una ronda se deriva; los criterios se congelan.** Lo primero, porque una
   lista almacenada podría contradecir a la regla que la ronda existe para sostener. Lo segundo,
   porque los criterios del canal cambian por decisión del creador y una ronda no puede quedar
   descrita por criterios que no son los suyos. Cortar la ronda de una convocatoria **es**
   cerrarla, que es lo que dice el plan; el canal permanente sigue abierto y lo que llegue
   después cae en el corte siguiente.
3. **Lo publicable se declara una sola vez.** El aviso que el participante lee antes de enviar y
   la proyección que usan el portal y la vista de vivo salen de la misma declaración, de modo que
   la promesa y la exposición no puedan separarse.

**Por qué la invitación no necesita enviar nada.** El vínculo lo emite el sistema como un enlace
con testigo: identifica propuesta y autoría sin que el participante copie un código ni un asunto.
Entregarlo es una decisión del creador, no una condición de verificación. Con eso H-3 —
autorización de comunicaciones reales — no se activa en U2, que es exactamente la mitigación que
`PLAN.md` previó para R5.

**Por qué no hace falta elegir el modelo de evaluación.** La evaluación está detrás de una
frontera con un ejecutor determinista local, como previó la mitigación de R6. En la operación
real el evaluador es la propia IA del creador por MCP, que es lo que U1 ya demostró que puede
leer y escribir. El modelo de evaluación del producto y su gasto siguen siendo H-4 y pertenecen a
la profundidad de U3, no al criterio de terminación de U2.

**Qué se reutilizó de U1 y cómo.** El transporte que funcionó en la corrida real —HTTP sin SSE,
`405` al `GET` que abriría un stream, respuestas JSON, anotaciones por herramienta, vista de MCP
Apps con comparación de huellas, registro de solicitudes— está reimplementado en `circuit/`, no
importado desde `sonda/`. La sonda de U1 es el candidato exacto contra el que se ejecutaron sus
contratos y no se tocó: importarla ataría el material de U2 a un artefacto congelado de otra
unidad.

## Contrato previo de verificación C-U2-1

Se propone **antes de ejecutarlo**, conforme a REVOLUTIONS §6.1. No se ejecutó ninguna de sus
mitades y no se ejecutará hasta que el AUDITOR lo congele.

**Candidato exacto.** El commit que cierra esta intervención en `francogg89-ai/work-claude-z`,
rama `main`. Su SHA se obtiene de Git después del cierre y viaja en el sobre de pase: no puede
escribirse dentro del commit que lo crea. Participa solo `unidad-2-circuito-minimo/`.

**Propiedad que debe demostrarse.** Que el circuito cierra de extremo a extremo sobre datos
sintéticos —desde la guía y el formulario público hasta la publicación autorizada y la votación,
pasando por conservación, evaluación, ampliación y segunda evaluación— y que sus controles
negativos fallan como se espera. No demuestra nada sobre la operación desde la IA contratada.

**Casos de `PLAN.md` que agota**: C2.1, C2.2, C2.3, C2.4, C2.5, C2.9, C2.12, C2.13, C2.14, C2.15.
**Casos que no toca**: C2.6, C2.7, C2.8, C2.10 y C2.11, que exigen la IA de referencia y una
exposición alcanzable, y necesitan contrato propio.

**Entorno.** Windows local del CONSTRUCTOR, dentro de su perímetro delegado. Python 3.12.4 y las
dependencias exactas de `sistema/requirements.txt`. Servidor en `127.0.0.1`, sin exposición de
red, sin túnel, sin ChatGPT y sin ningún modelo. Base creada desde cero: se borra `sistema/.data`
antes de empezar. Evaluación con el ejecutor determinista local.

**Mecanismo.** Secuencia exacta, con marcadores de inicio y fin y evidencia preservada. Las
llamadas MCP se hacen por HTTP contra el extremo local con `launch llamar`, que es la forma en
que un cliente remoto las haría; las acciones del creador, por el panel; las del participante,
por el formulario público.

| # | Acción | Qué ejercita |
|---|---|---|
| 0 | borrar `.data`; `init`; `marcar inicio-c-u2-1`; `servir` | preparación |
| 1 | `GET /` y se preserva el HTML | C2.9, C2.14 |
| 2 | envío por el formulario con solo lo que la guía anuncia | C2.9 |
| 3 | `sembrar` en la convocatoria y en el permanente, con numeración distinta | preparación |
| 4 | `llamar cortar_ronda` **antes** de revisar la calibración; `llamar proponer_calibracion`; revisión con corrección en el panel | C2.1 |
| 5 | `llamar cortar_ronda` en la convocatoria | C2.1, C2.12 |
| 6 | `evaluar --etapa 1` | C2.1 |
| 7 | `llamar publicar_finalistas` **sin** autorización; `GET /finalistas` | C2.4 |
| 8 | autorizar `invitar` en el panel; `ver_propuesta` y se anota la huella | C2.1, C2.2 |
| 9 | `llamar preparar_invitacion` con `id_operacion=inv-1`, y otra vez con el mismo | C2.1, C2.5 |
| 10 | abrir el enlace con testigo y enviar la ampliación; `ver_propuesta` de nuevo | C2.1, C2.2 |
| 11 | `evaluar --etapa 2` | C2.1 |
| 12 | registrar la elección del creador en el panel; autorizar `publicar`; `llamar publicar_finalistas` con `id_operacion=pub-1`, y otra vez con el mismo | C2.1, C2.5 |
| 13 | `GET /finalistas` y `GET /finalistas/vivo` | C2.1, C2.3, C2.14, C2.15 |
| 14 | votar hasta el máximo; repetir una propuesta ya votada; intentar una más | C2.1 |
| 15 | enviar al permanente; `llamar cortar_ronda permanente`; enviar otra; cortar otra vez | C2.12 |
| 16 | enviar a la convocatoria ya cortada | C2.13 |
| 17 | `marcar fin-c-u2-1`; `exportar` | evidencia |

**Criterio discriminante de éxito.** Todos, sin excepción:

| Caso | Se cumple si |
|---|---|
| C2.1 | la secuencia 4→14 se completa sin ninguna intervención fuera de las previstas —las del creador en el panel y las del participante en el formulario— y cada paso queda en la evidencia exportada con su llamada, su resultado y su instante |
| C2.2 | la huella de la propuesta en el paso 10 es idéntica a la del paso 8, el registro de ampliación aparece con su propia autoría y su tipo `ampliacion_autor`, y la segunda evaluación cita la ampliación en sus razones |
| C2.3 | la dirección de contacto sembrada no aparece en el HTML de `/`, `/finalistas`, `/finalistas/vivo` ni del enlace de ampliación, ni en ninguna respuesta MCP, ni en la evidencia exportada |
| C2.4 | el paso 7 devuelve error, `/finalistas` no muestra ninguna propuesta, y la publicación solo ocurre después de la autorización del paso 12 |
| C2.5 | la segunda llamada del paso 9 devuelve exactamente la primera invitación y no crea otra; la segunda del paso 12 no agrega una entrada publicada ni duplica la lista |
| C2.9 | la guía del paso 1 contiene objetivo, criterios, condiciones, plazos y forma de participación, y el envío del paso 2, compuesto solo con lo que la guía dice y sin ninguna IA, es aceptado |
| C2.12 | la ronda del paso 5 contiene solo propuestas de la convocatoria; la primera del paso 15 solo las del permanente anteriores a su corte; la segunda solo la recibida después |
| C2.13 | el paso 16 se rechaza, el mensaje nombra el canal permanente abierto, y esa propuesta no aparece en ningún canal |
| C2.14 | el conjunto de campos que el aviso del paso 1 declara publicables es exactamente el conjunto de campos que expone la vista pública del paso 13, sin sobrantes ni faltantes en ninguna dirección, y el campo declarado privado no aparece |
| C2.15 | toda superficie del paso 13 que muestra la fecha la presenta como recepción en el sistema, y ninguna afirma autoría, originalidad ni prioridad |

**Criterio discriminante de fallo.** El contrato falla si ocurre cualquiera de estas: el paso 7
publica algo; una repetición del paso 9 o del 12 produce una segunda invitación o una segunda
entrada publicada; el texto original cambia después de una ampliación; una dirección de contacto
aparece en cualquier superficie pública, respuesta MCP o evidencia; el paso 16 es aceptado o la
propuesta se reasigna en silencio a otro canal; los campos anunciados y los expuestos difieren en
cualquier dirección; alguna superficie presenta la fecha como prueba de autoría; una propuesta
queda en dos rondas o en ninguna pudiendo estar en una; o la secuencia no puede completarse.

No hay tercera categoría: toda observación de la corrida se resuelve dentro de estos dos
criterios. Si algo del escenario impide ejecutar un paso, el contrato falla y se propone otro.

**Controles negativos.** C2.4, C2.5 y C2.13 son los controles de este contrato, y son
indispensables: un sistema que publicara siempre, un reintento que actuara dos veces y un
formulario que aceptara cualquier envío satisfarían todos los casos positivos sin demostrar nada.

**Limitaciones conocidas.**

- Es una corrida local. No demuestra ninguna propiedad de la integración real con la IA
  contratada, y decirlo es parte del contrato (RT-1).
- El «participante sintético» de C2.9 es el CONSTRUCTOR siguiendo la guía. Demuestra que la guía
  contiene lo que hace falta y que el envío se acepta; **no** demuestra que una persona real la
  entienda, cosa que solo decide el piloto, que el manifiesto deja fuera del cierre técnico.
- La evaluación la produce el ejecutor determinista. No es un modelo y no sustituye ninguna
  prueba de integración (RT-2).
- El control de votación marca el navegador. No comprueba identidad de personas y el contrato no
  se lo atribuye.
- Los datos son sintéticos y están marcados como tales en el propio dato.

**Por qué no se propone todavía el contrato de la operación real.** C2.6, C2.7, C2.8, C2.10 y
C2.11 exigen la IA de referencia y una exposición alcanzable, es decir una intervención humana
material (H-2 más una cuenta ChatGPT). Proponerlo ahora obligaría al humano a montar esa corrida
sobre un candidato cuyo circuito local todavía no se demostró: si C-U2-1 falla, el esfuerzo
material se pierde y el checkpoint hay que reemitirlo. Se propondrá cuando el circuito local esté
demostrado. Es un juicio del CONSTRUCTOR sobre el orden, no sobre la necesidad; si el AUDITOR
prefiere congelar ambos contratos a la vez, corresponde decirlo y se emite el segundo.

## Verificación de esta entrega

No se ejecutó ninguna verificación discriminante, ningún caso de `PLAN.md`, ningún túnel y
ninguna sesión de ChatGPT. Lo que sigue es verificación de construcción: comprueba mecanismos del
candidato y **no** satisface ningún caso C2.x, que requieren el contrato congelado.

| Comprobación | Resultado |
|---|---|
| `python -m pytest -q -rs`, suite completa en una corrida, Python 3.12.4 sobre Windows 11 | `97 passed`, rc=0, sin omitidas |
| Arranque real de la aplicación en las pruebas de superficie | uvicorn sobre puerto libre; las pruebas de `/`, `/propuestas`, `/finalistas`, `/finalistas/vivo`, `/ampliar/<testigo>`, `/entrada-creador`, panel y MCP corren contra el servidor, no contra un doble |
| `POST` al extremo MCP sin la capacidad, y con ella | `404` sin capacidad en las tres formas probadas; `200` con `content-type: application/json` con ella |
| `GET` al extremo MCP | `405`, sin stream iniciado por el servidor; un `GET` sin capacidad sigue dando `404` y no `405` |
| Recorrido manual de la línea de comandos en un directorio temporal: `init`, `sembrar`, `exportar` | rc=0 en los tres; enlaces impresos con el aviso de cuáles llevan la capacidad |
| `git status` antes del commit | solo `unidad-2-circuito-minimo/`; `.venv`, `.data`, `__pycache__` y `.pytest_cache` quedan fuera por `.gitignore`; `PLAN.md`, `BOOTSTRAP.md`, el `EVENTO.md` de la raíz y `unidad-1-…` sin tocar |

La suite comprueba, entre otras cosas: que los campos publicables y los privados no se solapan y
que la proyección pública devuelve exactamente los declarados; que el contacto no aparece en
ninguna lectura ni en la evidencia; que el original conserva su huella después de una ampliación;
que publicar e invitar se rechazan sin autorización y no dejan rastro; que repetir un
identificador de operación no duplica; que una propuesta recibida después de un corte cae en el
siguiente; que cortar una convocatoria la cierra y el permanente sigue abierto; que el ejecutor
determinista es estable y que una instrucción escrita dentro de una propuesta no cambia el
resultado; y que las tres señales vuelven separadas y sin un cuarto orden.

## Limitaciones de esta entrega

- **Nada de lo entregado está verificado contra `PLAN.md`.** Los casos C2.x son verificaciones
  discriminantes y no se ejecutaron: eso es lo que pide el contrato de arriba.
- La suite de construcción comprueba mecanismos, no el recorrido completo con evidencia
  preservada. Que cada pieza funcione aislada no demuestra que el circuito cierre.
- El sistema no estuvo expuesto a la red en ningún momento de esta intervención.
- La elección de herramienta del modelo no es determinista y desde acá no se puede forzar: si el
  modelo responde con su propia transcripción en vez de abrir la vista, el creador ve texto no
  literal. Está tratado con instrucciones y con un aviso dentro de cada respuesta de datos, y
  queda como límite declarado.
- El testigo de ampliación es un enlace no adivinable: quien lo obtenga puede responder en nombre
  de esa autoría. Es el precio de no depender de que el participante copie un código.
- La presentación para vivo es la lista publicada con otra disposición. Es lo mínimo que el
  manifiesto pide y no pretende ser una superficie de producción.
- `sistema/.venv` y `sistema/.data` quedan fuera de Git. El directorio `.atl/` del árbol es
  material de herramientas del entorno local, ajeno a esta entrega.

## Decisión material declarada y ruteada

U1 dejó que la autenticación sin secreto en la URL era trabajo de U2. Esta entrega **no la
resuelve**, y lo declara en lugar de esconderlo dentro de la implementación: ningún caso de U2
ejercita la autenticación del extremo; el único mecanismo alternativo que admite el producto es
OAuth, que U1 registró expresamente como **no probado** en la cuenta de referencia; y probarlo
consumiría una intervención humana material que el criterio de terminación de U2 no pide. La
capacidad quedó aislada en un módulo único, se genera local, no entra en Git ni en el enlace de
entrada del creador, y no alcanza por sí sola para publicar ni invitar, porque eso exige además
la autorización del creador en el panel.

El CONSTRUCTOR no declara que esa decisión sea correcta: la declara y la rutea. Si el AUDITOR
sostiene que U2 debe cerrar con autenticación sin secreto en la URL, corresponde un contrato
propio y la intervención humana material que hoy no está pedida.

## Necesidad humana detectada

Ninguna activa en esta intervención. Para continuar —que el AUDITOR evalúe y, si es suficiente,
congele C-U2-1— no hace falta nada que esté fuera del perímetro delegado vigente, y por eso esta
entrega no preserva ningún checkpoint.

Queda anticipada, no activada, la necesidad material de `PLAN.md` §8 H-2 —exposición de red
alcanzable, con su costo y su superficie— junto con una cuenta de la IA de referencia, para el
contrato de la operación real que agotará C2.6, C2.7, C2.8, C2.10 y C2.11. Se preservará con su
checkpoint cuando ese contrato se proponga.

H-3 no se activa: el diseño de la invitación evitó la dependencia de comunicaciones reales. H-4
no se activa en U2: la evaluación corre detrás de su frontera con el ejecutor determinista y, en
la operación real, con la propia IA del creador.
