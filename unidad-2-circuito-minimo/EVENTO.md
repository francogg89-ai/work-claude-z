# EVENTO — Unidad 2: circuito mínimo completo

Segunda intervención de U2: corrección del candidato y del contrato previo. Explica la semántica
de la entrega; el delta exacto lo demuestra Git.

## Qué recibió

Cabecera canónica completa con `INCOMING_TURN_ID=22`, para el CONSTRUCTOR current.

La situación se rederivó desde Git sobre el corte recibido:

- la última entrega de work es `b3ff71b7459bb0479483dac81ba0d929b66deb09`, el árbol estaba limpio
  salvo `.atl/`, que es material de herramientas del entorno local;
- la intervención auditora del corte es `auditorias/b3ff71b7459bb0479483dac81ba0d929b66deb09.md`,
  con `VEREDICTO=CORRECCION_REQUERIDA`, `CONTRATO_C_U2_1_CONGELADO=NO`,
  `CONTRATO_C_U2_1_EJECUTADO=NO` y `HUMAN_NEED_REAL_ACTUAL=NO`;
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

C-U2-1 no fue congelado y no se ejecutó, ni antes ni ahora. La instrucción fue corregir D-01,
D-02 y D-03, ajustar la caracterización de la autenticación, no modificar `PLAN.md`, manifiesto
ni perímetro, y no ejecutar ninguna verificación discriminante antes de un nuevo congelamiento.

## Qué hizo y por qué

Los tres defectos se comprobaron y se sostienen. Dos son del contrato; el primero es del
candidato, y por eso esta entrega cambia una propiedad del sistema y no solo un texto.

### D-01 — la revisión precede a la apertura, y ahora eso es estructural

El plan y el manifiesto ponen la revisión de la interpretación de los criterios **antes** de
abrir la convocatoria. El candidato anterior protegía la evaluación —no se podía cortar la ronda
sin revisión— pero dejaba que el canal recibiera desde su creación. La auditoría tiene razón: eso
es una propiedad distinta y no estaba sostenida.

La corrección no agrega una comprobación más, que sería una regla que alguien tiene que recordar.
Cambia los estados posibles de un canal de recepción:

- nace en `preparacion` y **no recibe nada**;
- el único camino a `abierta` es que el creador apruebe la calibración en el panel, con lo cual
  un canal está abierto **si y solo si** su calibración fue aprobada, y el estado no puede decir
  otra cosa;
- el creador puede además **devolver** la interpretación con una discrepancia: queda registrada
  junto a la interpretación que corrige, y el canal sigue sin abrirse. Eso es lo que el manifiesto
  llama «posibilidad de corregir discrepancias», y ahora es un camino real y no una casilla;
- proponer una interpretación nueva sobre un canal ya abierto se rechaza: sus criterios son los
  que los participantes leyeron.

Cortar la ronda de una convocatoria la cierra, como ya hacía. Con eso, los tres estados cubren el
ciclo entero y la recepción solo ocurre entre la aprobación y el corte.

### D-02 — el contrato fija ahora la cadena de identidad

El contrato anterior enumeraba pasos compatibles entre sí, no un recorrido. La corrección fija,
**antes de ejecutar**, qué objeto viaja por cada paso: una base creada desde cero, una secuencia
determinista de recepciones que fija los identificadores, y una regla de selección que es una
función total de la corrida y no una elección posterior. La sección del contrato la escribe
completa.

### D-03 — el contrato fija ahora qué evidencia produce la corrida

La observación es correcta: `all_calls()` guardaba herramienta, argumentos, resultado e instante,
pero no el cuerpo de cada respuesta, y las superficies HTML no quedaban en ningún artefacto. Sin
eso, «ninguna respuesta MCP trae un contacto» y «lo anunciado coincide con lo expuesto» dependían
de mirar la pantalla en el momento.

Ahora la corrida produce artefactos:

- `llamar` escribe el cuerpo completo de cada solicitud y cada respuesta MCP en
  `.data/llamadas.jsonl`;
- `capturar` guarda los bytes exactos que devolvió una superficie a un `GET`, y `enviar` hace lo
  mismo con un formulario, aceptaciones y rechazos por igual, compartiendo cookies por sesión
  para que una secuencia de votos sea del mismo participante;
- `exportar` agrega a la evidencia las calibraciones con su aprobación o su discrepancia, el
  conjunto derivado de cada ronda, sus autorizaciones, las evaluaciones con evaluador, razones y
  dudas, las invitaciones, los registros vinculados, los votos, los campos declarados publicables
  y privados, y un inventario con el SHA-256 de cada artefacto.

Al fijar el criterio de C2.14 apareció además una divergencia real del candidato: la vista de
vivo mostraba menos campos que el portal, y un ejemplo vacío no se rendizaba en ninguna de las
dos. Las dos superficies pasan ahora por la misma función, que recorre los campos declarados en
su orden declarado y muestra vacío lo que está vacío, de modo que la correspondencia es
estructural y no algo que haya que mantener a mano en dos lugares.

Nada de eso preserva un secreto: la capacidad del creador y el testigo de una invitación se
reemplazan por `<capacidad>` y `<testigo>` en todo lo que se escribe, y la marca del votante viaja
como huella. Por eso la evidencia de la corrida puede publicarse en el repositorio de trabajo.

### La autenticación: caracterización corregida

La auditoría corrige una afirmación de la entrega anterior y la corrección se acepta sin
reservas. La autenticación del extremo **pertenece al alcance aprobado de U2**: U1 dejó que el
secreto en la URL no es apto para el producto, y `PLAN.md` la ejercita en C2.6 —operación real con
acceso autorizado— y en C2.8 —sesión sin la integración disponible o sin autorización—. No
corresponde trasladar al humano una decisión técnica que está delegada.

El mecanismo queda decidido y no es una conjetura: el producto probado admite URL sin
autenticación u OAuth, y no hay una tercera forma, de modo que «autenticación sin secreto en la
URL» significa el flujo de autorización de MCP. El SDK instalado recibe `auth`, `token_verifier` y
`auth_server_provider` al construir el servidor y los propaga a la misma aplicación HTTP que ya
usa este candidato, así que no hay que suponer nada sobre su disponibilidad.

Se implementa y se ejercita en la intervención que prepare el contrato de la operación real,
junto con C2.6 y C2.8, porque solo una corrida real demuestra que el anfitrión completa el flujo.
Esa corrida hará previsible una necesidad humana material —cuenta, permisos y exposición
alcanzable— que **no está activa ahora**. Mientras tanto la capacidad es aquello sobre lo que
corre la verificación local, y `ARQUITECTURA.md` ya no la presenta como decisión abierta ni como
apta para el producto.

## Contrato previo de verificación C-U2-1, segunda propuesta

Sustituye íntegramente a la propuesta devuelta sin congelar en
`audit-chatgpt-z @ 7d5f64e6a2cf1d709e0a47228d6de5aca239afea`. Se propone **antes de ejecutarlo**
conforme a REVOLUTIONS §6.1; no se ejecutó ninguna de sus mitades y no se ejecutará hasta que el
AUDITOR lo congele.

**Candidato exacto.** El commit que cierra esta intervención en `francogg89-ai/work-claude-z`,
rama `main`. Su SHA se obtiene de Git después del cierre y viaja en el sobre de pase: no puede
escribirse dentro del commit que lo crea. Participa solo `unidad-2-circuito-minimo/`.

**Propiedad que debe demostrarse.** Que **una misma propuesta** recorre el circuito entero —desde
que se recibe por el formulario público hasta que se vota como finalista publicada, pasando por
la ronda, la evaluación, la invitación, la ampliación, la segunda evaluación y la publicación
autorizada—, que ese recorrido solo puede empezar después de que el creador aprobó la
interpretación de sus criterios, y que los controles negativos fallan como se espera. No demuestra
nada sobre la operación desde la IA contratada.

**Casos de `PLAN.md` que agota**: C2.1, C2.2, C2.3, C2.4, C2.5, C2.9, C2.12, C2.13, C2.14, C2.15.
**Casos que no toca**: C2.6, C2.7, C2.8, C2.10 y C2.11.

**Entorno.** Windows local del CONSTRUCTOR, dentro de su perímetro delegado. Python 3.12.4 y las
dependencias exactas de `sistema/requirements.txt`. Servidor en `127.0.0.1:8000`, sin exposición
de red, sin túnel, sin ChatGPT y sin ningún modelo. Se borra `sistema/.data` antes de empezar, de
modo que la base, la capacidad y los artefactos sean los de esta corrida y de ninguna otra.

### La cadena de identidad, fijada antes de la corrida

Todo lo que sigue queda determinado por el candidato, la secuencia y la semilla por omisión de
`synthetic.generate`, y ninguno de estos objetos puede elegirse después de ver un resultado.

| Nombre | Definición fijada ahora |
|---|---|
| `CANAL_CONV` | `convocatoria-1`, creado por `init` con `--seleccionadas 4 --votos 3` |
| `CANAL_PERM` | `permanente`, creado por el mismo `init` |
| `P-001` | la propuesta del paso B1, enviada por el formulario con el texto exacto que fija este contrato |
| `P-002`…`P-009` | las ocho de `sembrar --canal convocatoria-1 --cantidad 8`, en ese orden |
| `P-010`…`P-013` | las cuatro de `sembrar --canal permanente --cantidad 4 --desde 101`, en ese orden |
| `P-014` | la propuesta del paso H1, enviada al canal permanente después del primer corte |
| `RONDA_CONV` | `convocatoria-1:ronda-1`, la única ronda de la convocatoria |
| `RONDA_PERM_1` / `RONDA_PERM_2` | `permanente:ronda-1` y `permanente:ronda-2` |
| `SEGUIDA` | **la de menor identificador entre las preseleccionadas de `RONDA_CONV` en la etapa 1.** Si ese conjunto es vacío, el contrato falla |
| `INVITACION` | la creada con `id_operacion=inv-1` sobre `SEGUIDA`, y ninguna otra |
| `AMPLIACION` | el único registro vinculado creado con el testigo de `INVITACION` |
| `PUBLICADAS` | exactamente las preseleccionadas de `RONDA_CONV` en la etapa 2, publicadas con `id_operacion=pub-1` |

El texto exacto de `P-001`, que se envía en el paso B1:

```text
channel_id = convocatoria-1
what       = [SINTETICO] Propongo un episodio sobre divulgacion responsable, realizable con pocos recursos.
why        = Aporta porque responde dudas frecuentes del chat del canal y conecta con temas ya tratados.
example    = (vacío)
author     = Participante sintetico 000
contact    = participante000.sintetico@example.invalid
```

`SEGUIDA` es una regla y no un identificador porque nombrar hoy una propuesta concreta exigiría
haber corrido la evaluación, que es parte de lo que este contrato verifica. La regla es una
función total de la corrida congelada: no admite dos respuestas ni depende de qué se observe.

### Mecanismo

Secuencia exacta. Las llamadas MCP van por HTTP contra el extremo local con `launch llamar`, que
es como las haría un cliente remoto; las acciones del creador, por el panel; las del participante,
por el formulario. Todo lo que devuelve cada paso queda preservado como dice la sección siguiente.

| # | Acción | Qué ejercita |
|---|---|---|
| 0 | borrar `.data`; `init --seleccionadas 4 --votos 3`; `marcar inicio-c-u2-1`; `servir` | preparación |
| A1 | `capturar --ruta / --nombre guia-antes-de-abrir` | D-01 |
| A2 | `enviar --ruta /propuestas --nombre envio-antes-de-abrir` con el texto de `P-001` | D-01 |
| A3 | `llamar estado_del_sistema` | D-01 |
| A4 | `llamar cortar_ronda {"channel_id":"convocatoria-1"}` | D-01 |
| A5 | `llamar proponer_calibracion` sobre `CANAL_CONV` | C2.1 |
| A6 | en el panel, **devolver** la interpretación con la discrepancia `Falta el peso de la audiencia.` | C2.1 |
| A7 | `llamar estado_del_sistema` | C2.1 |
| A8 | `llamar proponer_calibracion` sobre `CANAL_CONV` con una interpretación nueva | C2.1 |
| A9 | en el panel, **aprobar** la interpretación de `CANAL_CONV` | C2.1 |
| A10 | `llamar proponer_calibracion` sobre `CANAL_PERM` y aprobarla en el panel | C2.1, C2.12 |
| A11 | `capturar --ruta / --nombre guia-abierta` | C2.9, C2.14 |
| B1 | `enviar --ruta /propuestas --nombre recepcion-p001` con el texto exacto de arriba | C2.9, C2.15 |
| B2 | `sembrar --canal convocatoria-1 --cantidad 8` | preparación |
| B3 | `sembrar --canal permanente --cantidad 4 --desde 101` | preparación |
| C1 | `llamar cortar_ronda {"channel_id":"convocatoria-1"}` | C2.1, C2.12 |
| C2 | `evaluar --ronda convocatoria-1:ronda-1 --etapa 1` | C2.1 |
| C3 | `llamar senales_de_la_ronda {"round_id":"convocatoria-1:ronda-1"}` | C2.1 |
| D1 | `llamar publicar_finalistas` sobre `RONDA_CONV`, **sin autorización**, `id_operacion=pub-1` | C2.4 |
| D2 | `capturar --ruta /finalistas --nombre finalistas-sin-autorizacion` | C2.4 |
| E1 | `llamar ver_propuesta` sobre `SEGUIDA` | C2.2 |
| E2 | en el panel, autorizar `invitar` en `RONDA_CONV` | C2.1 |
| E3 | `llamar preparar_invitacion` sobre `SEGUIDA` con `id_operacion=inv-1` | C2.1 |
| E4 | `llamar preparar_invitacion` otra vez, con el mismo `id_operacion` y los mismos argumentos | C2.5 |
| E5 | `capturar --ruta /ampliar/<testigo> --nombre ampliar-formulario` | C2.1 |
| E6 | `enviar --ruta /ampliar/<testigo> --nombre ampliar-envio --dato body=Con dos invitados del propio canal y material libre.` | C2.1, C2.2 |
| E7 | `llamar ver_propuesta` sobre `SEGUIDA` | C2.2 |
| E8 | `llamar obtener_propuesta` sobre `SEGUIDA` | C2.2, C2.3 |
| F1 | `evaluar --ronda convocatoria-1:ronda-1 --etapa 2` | C2.1, C2.2 |
| F2 | en el panel, registrar la elección del creador en `RONDA_CONV` | C2.1 |
| F3 | en el panel, autorizar `publicar` en `RONDA_CONV` | C2.1, C2.4 |
| F4 | `llamar publicar_finalistas` con `PUBLICADAS` e `id_operacion=pub-1` | C2.1, C2.4 |
| F5 | `llamar publicar_finalistas` otra vez, con el mismo `id_operacion` y los mismos argumentos | C2.5 |
| F6 | `capturar --ruta /finalistas --nombre finalistas` y `--ruta /finalistas/vivo --nombre vivo` | C2.1, C2.3, C2.14, C2.15 |
| G1 | con `--sesion votante-1`: `capturar --ruta /finalistas`, y `enviar --ruta /votos` por las tres primeras de `PUBLICADAS` en orden de identificador | C2.1 |
| G2 | con la misma sesión, votar otra vez `SEGUIDA` | C2.1 |
| G3 | con la misma sesión, votar la cuarta de `PUBLICADAS` | C2.1 |
| G4 | `capturar --ruta /finalistas --nombre finalistas-con-votos` | C2.1 |
| H1 | `enviar --ruta /propuestas --nombre recepcion-permanente-tardia` al canal permanente | C2.12 |
| H2 | `llamar cortar_ronda {"channel_id":"permanente"}` dos veces: antes de H1 y después | C2.12 |
| H3 | `enviar --ruta /propuestas --nombre envio-a-convocatoria-cortada` a `CANAL_CONV` | C2.13 |
| Z | `marcar fin-c-u2-1`; `exportar`; copiar los artefactos a `unidad-2-circuito-minimo/evidencia/` | evidencia |

El orden real de H2 es: el primer corte del canal permanente ocurre inmediatamente después de
B3, y el segundo después de H1. La tabla los junta para leerlos como un solo caso.

### Evidencia que la corrida preserva

Antes de ejecutar queda fijado qué artefacto sostiene cada observación. Ninguna depende de
memoria, de relato posterior ni de repetir la corrida.

| Artefacto | Qué contiene |
|---|---|
| `evidencia/llamadas.jsonl` | cuerpo completo de cada solicitud y cada respuesta MCP de los pasos A3, A4, A5, A7, A8, A10, C1, C3, D1, E1, E3, E4, E7, E8, F4, F5 y H2, en orden |
| `evidencia/capturas/*.html` | bytes exactos de cada superficie de los pasos A1, A2, A11, B1, D2, E5, E6, F6, G1, G2, G3, G4, H1 y H3, con los nombres que fija la tabla |
| `evidencia/evidencia.json` | canales con su estado, calibraciones con aprobación o discrepancia, propuestas, rondas con su conjunto derivado y sus autorizaciones, evaluaciones con evaluador, razones y dudas, invitaciones, registros vinculados, votos, lista publicada con sus tres señales, campos declarados publicables y privados, y el registro de solicitudes HTTP con su método, superficie y estado |
| `evidencia/evidencia.json` → `artefactos` | nombre, tamaño y SHA-256 de cada archivo anterior |

Los artefactos se copian desde `.data` a `unidad-2-circuito-minimo/evidencia/` y se entregan en el
mismo commit que reporte la corrida. No llevan secretos: la capacidad y los testigos aparecen
como `<capacidad>` y `<testigo>`, y la marca del votante como huella.

### Criterio discriminante de éxito

Todos, sin excepción, y cada uno leído del artefacto que lo sostiene:

| Caso | Se cumple si |
|---|---|
| C2.1 | la secuencia A1→H3 se completa sin ninguna intervención fuera de las previstas —las del creador en el panel y las del participante en el formulario—; `SEGUIDA` aparece con el mismo identificador en la recepción, en el conjunto de `RONDA_CONV`, en su evaluación de etapa 1, en `INVITACION`, en `AMPLIACION`, en su evaluación de etapa 2, en `PUBLICADAS` y en un voto; y la guía capturada en A1 no ofrece formulario mientras la de A11 sí |
| C2.2 | la huella que devuelve E7 es idéntica a la de E1; `AMPLIACION` figura en E8 y en la evidencia con su propia autoría y tipo `ampliacion_autor`; y la evaluación de etapa 2 de `SEGUIDA` cita la ampliación en sus razones |
| C2.3 | la cadena `participante000.sintetico@example.invalid`, y ninguna otra dirección sembrada, no aparece en `llamadas.jsonl`, ni en ninguna captura, ni en `evidencia.json` |
| C2.4 | D1 devuelve error; la captura D2 no nombra ninguna propuesta; y la publicación solo existe después de la autorización de F3. D1 usa a propósito el mismo `id_operacion` que F4: un rechazo no debe consumir el identificador de operación, y si lo consumiera F4 no publicaría y el contrato fallaría |
| C2.5 | E4 devuelve exactamente el mismo objeto que E3 y la evidencia tiene una sola invitación; F5 devuelve exactamente lo mismo que F4 y la lista publicada no repite ninguna entrada |
| C2.9 | la captura A11 contiene objetivo, criterios, condiciones, plazos y forma de participación; y el envío de B1, compuesto solo con lo que esa guía dice y sin ninguna IA, es aceptado |
| C2.12 | el conjunto de `RONDA_CONV` en la evidencia son exactamente `P-001`…`P-009`; el de `RONDA_PERM_1` exactamente `P-010`…`P-013`; y el de `RONDA_PERM_2` exactamente `P-014` |
| C2.13 | la captura H3 muestra el rechazo, nombra el canal permanente, y `P-014` sigue siendo la única propuesta del permanente posterior al primer corte: nada se reasignó |
| C2.14 | el conjunto de campos que la captura A11 anuncia como publicables es exactamente el conjunto `campos_declarados.publicables` de la evidencia, y exactamente el conjunto de campos que muestran las capturas de F6, sin sobrantes ni faltantes en ninguna dirección; y el campo declarado privado no aparece en ninguna de esas capturas |
| C2.15 | toda superficie capturada que muestra una fecha la presenta como recepción en el sistema, y ninguna afirma autoría, originalidad ni prioridad |

Además, como la corrección de D-01 es parte de la propiedad: A2 debe ser rechazado, A4 debe
devolver error, A3 debe mostrar los dos canales en `preparacion`, A7 debe mostrar la calibración
devuelta con su discrepancia, y la evidencia no debe contener ninguna propuesta anterior a A9.

### Criterio discriminante de fallo

El contrato falla si ocurre cualquiera de estas: A2 es aceptado o A4 corta una ronda; el conjunto
de preseleccionadas de `RONDA_CONV` en la etapa 1 es vacío, de modo que `SEGUIDA` no existe;
alguno de los pasos posteriores actúa sobre una propuesta distinta de `SEGUIDA`; D1 publica algo;
una repetición de E4 o F5 produce una segunda invitación o una segunda entrada publicada; el texto
original cambia después de la ampliación; una dirección de contacto aparece en cualquier
artefacto; H3 es aceptado o su propuesta se reasigna a otro canal; los campos anunciados y los
expuestos difieren en cualquier dirección; alguna superficie presenta la fecha como prueba de
autoría; una propuesta queda en dos rondas o en ninguna pudiendo estar en una; algún artefacto
falta o no coincide con su SHA-256; o la secuencia no puede completarse.

No hay tercera categoría: toda observación de la corrida se resuelve dentro de estos dos
criterios. Si algo del escenario impide ejecutar un paso, el contrato falla y se propone otro.

### Controles negativos

C2.4, C2.5 y C2.13 son los controles de este contrato, junto con A2 y A4, que son el control de
la propiedad corregida en D-01. Son indispensables: un sistema que publicara siempre, un reintento
que actuara dos veces, un formulario que aceptara cualquier envío y un canal que recibiera desde
su creación satisfarían todos los casos positivos sin demostrar nada.

### Limitaciones conocidas

- Es una corrida local. No demuestra ninguna propiedad de la integración real con la IA
  contratada, y decirlo es parte del contrato (RT-1).
- El «participante sintético» de C2.9 es el CONSTRUCTOR siguiendo la guía. Demuestra que la guía
  contiene lo que hace falta y que el envío se acepta; **no** demuestra que una persona real la
  entienda, cosa que solo decide el piloto, que el manifiesto deja fuera del cierre técnico.
- La evaluación la produce el ejecutor determinista. No es un modelo y no sustituye ninguna prueba
  de integración (RT-2).
- El control de votación marca el navegador. No comprueba identidad de personas y el contrato no
  se lo atribuye.
- La comparación de C2.14 la hace una persona leyendo dos artefactos. El contrato fija qué se
  compara y contra qué, no automatiza la comparación.
- Los datos son sintéticos y están marcados como tales en el propio dato.

### Por qué sigue sin proponerse el contrato de la operación real

C2.6, C2.7, C2.8, C2.10 y C2.11 exigen la IA de referencia y una exposición alcanzable, y además
la autenticación del extremo, que se implementa junto con ellos. Ese contrato se propone cuando el
circuito local esté demostrado y el mecanismo de autenticación esté implementado, para no gastar
una intervención humana material sobre un candidato que todavía puede cambiar. Es un juicio sobre
el orden, no sobre la necesidad.

## Verificación de esta entrega

No se ejecutó ninguna verificación discriminante, ningún caso de `PLAN.md`, ningún túnel y ninguna
sesión de ChatGPT. Lo que sigue es verificación de construcción: comprueba mecanismos del
candidato y **no** satisface ningún caso C2.x.

| Comprobación | Resultado |
|---|---|
| `python -m pytest -q -rs`, suite completa en una corrida, Python 3.12.4 sobre Windows 11 | `113 passed`, rc=0, sin omitidas |
| Pruebas nuevas de la propiedad corregida en D-01 | un canal en preparación no ofrece formulario, rechaza el envío y no se puede cortar; aprobar en el panel es lo que lo abre; devolver con discrepancia lo deja cerrado y registra el texto; proponer calibración sobre un canal abierto se rechaza |
| Pruebas nuevas de los artefactos de D-03 | la llamada preservada conserva la respuesta y no la capacidad; un rechazo de formulario queda guardado con su texto; una sesión mantiene la marca del votante entre llamadas; la página de ampliación capturada no lleva el testigo; el inventario trae SHA-256 de cada artefacto |
| Pruebas nuevas de la correspondencia de campos | las dos superficies públicas muestran exactamente los campos declarados publicables, ninguno privado, y un campo vacío se muestra vacío en vez de desaparecer |
| Pruebas nuevas del cuerpo de la evidencia | la exportación trae el conjunto derivado de la ronda, las evaluaciones con sus dudas, los registros vinculados con su cuerpo, los votos y la lista publicada, y no contiene el testigo |
| `git status` antes del commit | solo `unidad-2-circuito-minimo/`; `.venv`, `.data`, `__pycache__` y `.pytest_cache` fuera por `.gitignore`; `PLAN.md`, `BOOTSTRAP.md`, el `EVENTO.md` de la raíz y `unidad-1-…` sin tocar |

## Limitaciones de esta entrega

- **Nada está verificado contra `PLAN.md`.** Los casos C2.x son verificaciones discriminantes y no
  se ejecutaron: eso es lo que pide el contrato de arriba.
- La suite de construcción comprueba mecanismos, no el recorrido completo con evidencia
  preservada. Que cada pieza funcione aislada no demuestra que el circuito cierre.
- La autenticación del extremo sigue sin implementarse: el mecanismo está decidido y su
  implementación pertenece a la intervención que prepare el contrato de la operación real.
- El sistema no estuvo expuesto a la red en ningún momento de esta intervención.
- La elección de herramienta del modelo no es determinista y desde acá no se puede forzar; está
  tratada con instrucciones y con un aviso dentro de cada respuesta de datos, y queda como límite
  declarado.
- El testigo de ampliación es un enlace no adivinable: quien lo obtenga puede responder en nombre
  de esa autoría. Es el precio de no depender de que el participante copie un código.
- La redacción de secretos en los artefactos es una sustitución de texto sobre la capacidad y
  sobre los testigos que aparecen en una URL. Es suficiente para lo que este candidato produce, y
  no es una garantía general contra cualquier filtración futura.
- `sistema/.venv` y `sistema/.data` quedan fuera de Git. El directorio `.atl/` del árbol es
  material de herramientas del entorno local, ajeno a esta entrega.

## Necesidad humana detectada

Ninguna activa. Para continuar —que el AUDITOR evalúe y, si es suficiente, congele C-U2-1— no hace
falta nada fuera del perímetro delegado vigente, y por eso esta entrega no preserva ningún
checkpoint.

Queda anticipada, no activada, la necesidad material de `PLAN.md` §8 H-2 —exposición de red
alcanzable, con su costo y su superficie— junto con una cuenta de la IA de referencia, para la
corrida real que ejercitará C2.6, C2.7, C2.8, C2.10, C2.11 y la autenticación del extremo. Se
preservará con su checkpoint cuando ese contrato se proponga.

H-3 no se activa: el diseño de la invitación evitó la dependencia de comunicaciones reales. H-4 no
se activa en U2: la evaluación corre detrás de su frontera con el ejecutor determinista y, en la
operación real, con la propia IA del creador.
