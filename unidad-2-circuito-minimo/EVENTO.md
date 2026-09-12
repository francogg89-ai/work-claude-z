# EVENTO — Unidad 2: corrección de C2.3 y D-04, y contrato C-U2-2

Cuarta intervención de U2. Explica la semántica de la entrega; el delta exacto lo demuestra Git.

No se ejecutó ninguna verificación discriminante. `C-U2-1` quedó agotado con fallo y no se
repite; su evidencia histórica se conserva íntegra.

## Qué recibió

Cabecera canónica con `INCOMING_TURN_ID=26`, para el CONSTRUCTOR current.

La situación se rederivó desde Git sobre el corte recibido:

- la última entrega de work es `2fb0689de5287ce66c335a2f0a1f32e6e684f340`, con el árbol limpio
  salvo `.atl/`, que es material de herramientas del entorno local;
- la intervención auditora del corte es `auditorias/2fb0689de5287ce66c335a2f0a1f32e6e684f340.md`,
  con `CONTRATO_C_U2_1_EJECUTADO=SI`, `CONTRATO_C_U2_1_AGOTADO=SI`,
  `CONTRATO_C_U2_1_RESULTADO=FALLO`, `CASO_FALLIDO=C2.3`,
  `D_04=ABIERTO_REDACCION_INCOMPLETA_DE_TESTIGO_EN_EVIDENCIA` y `HUMAN_NEED_REAL_ACTUAL=NO`;
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

## Qué hizo y por qué

Las dos correcciones atacan el mismo error de fondo: una propiedad de privacidad quedaba sujeta
a que cada superficie y cada paso se acordaran de respetarla, en lugar de estar sostenida por la
forma del sistema. Las dos se corrigen en el lugar donde el dato se decide, no donde se lo ve.

### C2.3 — un campo privado no vuelve nunca a la página

El fallo observado: al rechazar un envío, el formulario se rendizaba de nuevo con lo que el
participante había escrito —para que no tuviera que tipearlo otra vez— y el contacto entraba en
esa respuesta, que después se preservó como artefacto.

Lo tentador era no preservar esas páginas, o no rendizar ningún valor. Ninguna de las dos toca
el problema: la primera esconde la evidencia y la segunda castiga al participante que ya escribió
cuatrocientos caracteres.

La corrección usa la declaración que ya existe. `form_block` descarta **todo campo declarado en
`domain.PRIVATE_FIELDS`** antes de rendizar, sea cual sea la página que esté armando. Los campos
publicables vuelven, el contacto se escribe de nuevo, y el aviso del formulario lo dice. La
separación entre lo privado y lo público deja de depender de qué página se arma: depende de la
misma declaración única que ya gobierna el aviso previo al envío, el portal y la vista de vivo.

### D-04 — los testigos se sustituyen por valor, no por forma

El defecto observado: la redacción reemplazaba el testigo cuando viajaba dentro de un enlace,
pero la respuesta de `preparar_invitacion` lo devolvía además como campo suelto, y esa forma
quedó en claro en `llamadas.jsonl`. La evidencia se declaraba sanitizada y no lo estaba.

Reconocer un secreto por la forma en que viaja es una carrera que se pierde. La corrección va por
los dos lados:

- **la sustitución es por valor**: `redact` lee los testigos emitidos en la base y reemplaza esos
  valores exactos en todo lo que se preserva, sin depender de adivinar dónde aparecen. El patrón
  sobre el enlace queda como segunda red, para un testigo que esa base no conozca;
- **el testigo deja de viajar como campo propio**: la herramienta devuelve el enlace que el
  participante tiene que abrir, y nada más. Cada lugar por el que pasa un secreto accionable es
  un lugar donde puede quedar copiado, y ese campo no lo necesitaba nadie.

La evidencia histórica de `C-U2-1` **no se tocó**: `unidad-2-circuito-minimo/evidencia/` queda
exactamente como la produjo aquella corrida, testigo en claro incluido. Reescribirla sería borrar
la prueba del defecto que la hizo visible.

## Contrato previo de verificación C-U2-2

Contrato nuevo, conforme a REVOLUTIONS §6.1. `C-U2-1` está agotado y no se repite. Se propone
**antes de ejecutarlo**; no se ejecutó ninguna de sus mitades y no se ejecutará hasta que el
AUDITOR lo congele.

**Candidato exacto.** El commit que cierra esta intervención en `francogg89-ai/work-claude-z`,
rama `main`. Su SHA se obtiene de Git después del cierre y viaja en el sobre de pase: no puede
escribirse dentro del commit que lo crea. Participa solo `unidad-2-circuito-minimo/`.

**Propiedad que debe demostrarse.** La misma que `C-U2-1` no llegó a demostrar, sobre el
candidato corregido: que **una misma propuesta** recorre el circuito entero —desde que se recibe
por el formulario público hasta que se vota como finalista publicada, pasando por la ronda, la
evaluación, la invitación, la ampliación, la segunda evaluación y la publicación autorizada—, que
ese recorrido solo puede empezar después de que el creador aprobó la interpretación de sus
criterios, que los controles negativos fallan como se espera, y que **ningún dato privado ni
ningún secreto accionable queda en la evidencia que la corrida produce**. No demuestra nada sobre
la operación desde la IA contratada.

**Casos de `PLAN.md` que agota**: C2.1, C2.2, C2.3, C2.4, C2.5, C2.9, C2.12, C2.13, C2.14, C2.15.
**Casos que no toca**: C2.6, C2.7, C2.8, C2.10 y C2.11.

### Qué alcance de regresión es suficiente, y por qué

El AUDITOR preservó las observaciones positivas de la corrida anterior sobre el candidato
congelado, y advirtió que no se trasladan solas a un candidato distinto. Corresponde justificar
qué hay que volver a ejercitar.

Lo que cambió entre `bddc126ab0e7f15f386220015088cd27dd64a459` y este candidato:

| Módulo | Cambio |
|---|---|
| `circuit/public.py` | `form_block` descarta los campos privados antes de rendizar; cambia el aviso del campo de contacto |
| `circuit/creator.py` | `preparar_invitacion` ya no devuelve el testigo como campo propio |
| `circuit/store.py` | se agrega `witnesses()`, lectura usada solo por la preservación de artefactos |
| `circuit/launch.py` | `redact` sustituye los testigos por valor además de por patrón |

La pregunta no es cuántas líneas cambiaron sino **por dónde pasa cada observación**:

- `form_block` rendiza la guía pública y **todas** las páginas de rechazo del formulario. Por ahí
  pasan la evidencia de C2.9, la de C2.13, la del control A2 de la propiedad de D-01 y la mitad
  «anunciado» de C2.14.
- `preparar_invitacion` cambió la forma de su respuesta. Por ahí pasan la comparación de
  idempotencia de C2.5, el eslabón «invitación» de la cadena de C2.1 y el camino por el que la
  corrida obtiene el testigo para la ampliación de C2.2.
- `redact` interviene en **todo** artefacto que la corrida escribe. Una sustitución por valor
  puede, en principio, alterar un artefacto más de lo previsto. Por ahí pasa, por lo tanto, la
  legibilidad de cualquier criterio que se lea de un artefacto, que son todos.

No queda ningún caso cuya evidencia sea independiente de al menos uno de los componentes
tocados. El alcance suficiente es, entonces, **la secuencia completa otra vez**, y eso no es una
elección conservadora por las dudas: es lo que se sigue de dónde están los cambios.

Hay además una razón que no depende de los módulos. La propiedad central de U2 es que el
circuito **cierra**, y una cadena no se arma con eslabones observados en dos candidatos
distintos: hacerlo sería reintroducir exactamente el defecto D-02 que la auditoría cerró. Un
alcance parcial obligaría a afirmar que los pedazos no ejercitados siguen valiendo, que es
justamente lo que el AUDITOR dijo que no se traslada solo.

Por eso `C-U2-2` repite la secuencia congelada de `C-U2-1` sin recortes, con los criterios
agregados que se detallan abajo. La corrida anterior costó minutos de máquina y ninguna
intervención humana: no hay nada que economizar recortando el alcance, y sí hay algo que perder.

### La cadena de identidad, fijada antes de la corrida

Idéntica a la de `C-U2-1`, porque la secuencia de recepciones no cambió. Todo queda determinado
por el candidato, la secuencia y la semilla por omisión de `synthetic.generate`, y ninguno de
estos objetos puede elegirse después de ver un resultado.

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
| `TESTIGO` | el que aparece dentro del campo `enlace` de la respuesta de `INVITACION`, que es el único lugar donde el candidato lo devuelve |
| `AMPLIACION` | el único registro vinculado creado con `TESTIGO` |
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

### Entorno

Windows local del CONSTRUCTOR, dentro de su perímetro delegado. Python 3.12.4 y las dependencias
exactas de `sistema/requirements.txt`. Servidor en `127.0.0.1:8000`, sin exposición de red, sin
túnel, sin ChatGPT y sin ningún modelo. Se borra `sistema/.data` antes de empezar, de modo que la
base, la capacidad y los artefactos sean los de esta corrida y de ninguna otra. La evidencia se
escribe en `unidad-2-circuito-minimo/evidencia-c-u2-2/`, que es un destino nuevo:
`unidad-2-circuito-minimo/evidencia/` es la de `C-U2-1` y no se toca.

### Mecanismo

La secuencia congelada de `C-U2-1`, sin recortes, con una sola precisión nueva en E5: el testigo
se lee del campo `enlace` de la respuesta de E3, porque el candidato corregido ya no lo devuelve
como campo suelto.

| # | Acción | Qué ejercita |
|---|---|---|
| 0 | borrar `.data`; `init --seleccionadas 4 --votos 3`; `marcar inicio-c-u2-2`; `servir` | preparación |
| A1 | `capturar --ruta / --nombre guia-antes-de-abrir` | D-01 |
| A2 | `enviar --ruta /propuestas --nombre envio-antes-de-abrir` con el texto de `P-001` | D-01, C2.3 |
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
| B3 | `sembrar --canal permanente --cantidad 4 --desde 101`; después, `llamar cortar_ronda {"channel_id":"permanente"}` | C2.12 |
| C1 | `llamar cortar_ronda {"channel_id":"convocatoria-1"}` | C2.1, C2.12 |
| C2 | `evaluar --ronda convocatoria-1:ronda-1 --etapa 1` | C2.1 |
| C3 | `llamar senales_de_la_ronda {"round_id":"convocatoria-1:ronda-1"}` | C2.1 |
| D1 | `llamar publicar_finalistas` sobre `RONDA_CONV`, **sin autorización**, `id_operacion=pub-1` | C2.4 |
| D2 | `capturar --ruta /finalistas --nombre finalistas-sin-autorizacion` | C2.4 |
| E1 | `llamar ver_propuesta` sobre `SEGUIDA` | C2.2 |
| E2 | en el panel, autorizar `invitar` en `RONDA_CONV` | C2.1 |
| E3 | `llamar preparar_invitacion` sobre `SEGUIDA` con `id_operacion=inv-1`; `TESTIGO` sale de su campo `enlace` | C2.1, D-04 |
| E4 | `llamar preparar_invitacion` otra vez, con el mismo `id_operacion` y los mismos argumentos | C2.5 |
| E5 | `capturar --ruta /ampliar/<TESTIGO> --nombre ampliar-formulario` | C2.1 |
| E6 | `enviar --ruta /ampliar/<TESTIGO> --nombre ampliar-envio --dato body=Con dos invitados del propio canal y material libre.` | C2.1, C2.2 |
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
| H2 | `llamar cortar_ronda {"channel_id":"permanente"}` | C2.12 |
| H3 | `enviar --ruta /propuestas --nombre envio-a-convocatoria-cortada` a `CANAL_CONV` | C2.13, C2.3 |
| Z | `marcar fin-c-u2-2`; `exportar`; copiar los artefactos a `unidad-2-circuito-minimo/evidencia-c-u2-2/` | evidencia |

Los dos cortes del canal permanente quedan explícitos en su lugar: el primero al final de B3 y el
segundo en H2, después de H1.

### Evidencia que la corrida preserva

| Artefacto | Qué contiene |
|---|---|
| `evidencia-c-u2-2/llamadas.jsonl` | cuerpo completo de cada solicitud y cada respuesta MCP, en orden |
| `evidencia-c-u2-2/capturas/*.html` | bytes exactos de cada superficie de los pasos A1, A2, A11, B1, D2, E5, E6, F6, G1, G2, G3, G4, H1 y H3, con los nombres que fija la tabla |
| `evidencia-c-u2-2/evidencia.json` | canales con su estado, calibraciones con aprobación o discrepancia, propuestas, rondas con su conjunto derivado y sus autorizaciones, evaluaciones con evaluador, razones y dudas, invitaciones, registros vinculados, votos, lista publicada con sus tres señales, campos declarados publicables y privados, y el registro de solicitudes HTTP con su método, superficie y estado |
| `evidencia-c-u2-2/evidencia.json` → `artefactos` | nombre, tamaño y SHA-256 de cada archivo anterior |

### Criterio discriminante de éxito

Todos, sin excepción, y cada uno leído del artefacto que lo sostiene. Los nueve primeros son los
de `C-U2-1`, sin cambios; los dos últimos son los que esta corrección obliga a agregar.

| Caso | Se cumple si |
|---|---|
| C2.1 | la secuencia A1→H3 se completa sin ninguna intervención fuera de las previstas —las del creador en el panel y las del participante en el formulario—; `SEGUIDA` aparece con el mismo identificador en la recepción, en el conjunto de `RONDA_CONV`, en su evaluación de etapa 1, en `INVITACION`, en `AMPLIACION`, en su evaluación de etapa 2, en `PUBLICADAS` y en un voto; y la guía capturada en A1 no ofrece formulario mientras la de A11 sí |
| C2.2 | la huella que devuelve E7 es idéntica a la de E1; `AMPLIACION` figura en E8 y en la evidencia con su propia autoría y tipo `ampliacion_autor`; y la evaluación de etapa 2 de `SEGUIDA` cita la ampliación en sus razones |
| C2.4 | D1 devuelve error; la captura D2 no nombra ninguna propuesta; y la publicación solo existe después de la autorización de F3. D1 usa a propósito el mismo `id_operacion` que F4: un rechazo no debe consumir el identificador de operación, y si lo consumiera F4 no publicaría y el contrato fallaría |
| C2.5 | E4 devuelve exactamente el mismo objeto que E3 y la evidencia tiene una sola invitación; F5 devuelve exactamente lo mismo que F4 y la lista publicada no repite ninguna entrada |
| C2.9 | la captura A11 contiene objetivo, criterios, condiciones, plazos y forma de participación; y el envío de B1, compuesto solo con lo que esa guía dice y sin ninguna IA, es aceptado |
| C2.12 | el conjunto de `RONDA_CONV` en la evidencia son exactamente `P-001`…`P-009`; el de `RONDA_PERM_1` exactamente `P-010`…`P-013`; y el de `RONDA_PERM_2` exactamente `P-014` |
| C2.13 | la captura H3 muestra el rechazo, nombra el canal permanente, y `P-014` sigue siendo la única propuesta del permanente posterior al primer corte: nada se reasignó |
| C2.14 | el conjunto de campos que la captura A11 anuncia como publicables es exactamente el conjunto `campos_declarados.publicables` de la evidencia, y exactamente el conjunto de campos que muestran las capturas de F6, sin sobrantes ni faltantes en ninguna dirección; y el campo declarado privado no aparece en ninguna de esas capturas |
| C2.15 | toda superficie capturada que muestra una fecha la presenta como recepción en el sistema, y ninguna afirma autoría, originalidad ni prioridad |
| **C2.3** | ninguna de las direcciones de contacto usadas en la corrida —la de `P-001`, las sembradas y las de H1 y H3— aparece en `llamadas.jsonl`, ni en **ninguna** captura, ni en `evidencia.json`. En particular, las capturas de A2, H3 y cualquier otro rechazo de formulario no contienen el contacto enviado, **y sí contienen los campos publicables que el participante había escrito**: una corrección que vaciara el formulario entero también haría fallar este criterio |
| **D-04** | ningún testigo emitido en la corrida aparece en claro en `llamadas.jsonl`, ni en ninguna captura, ni en `evidencia.json`; la marca `<testigo>` aparece al menos una vez en los artefactos donde el testigo habría viajado; y la respuesta de E3 no trae el testigo como campo propio |

Además, como la propiedad corregida de D-01 sigue siendo parte de lo que se demuestra: A2 debe
ser rechazado, A4 debe devolver error, A3 debe mostrar los dos canales en `preparacion`, A7 debe
mostrar la calibración devuelta con su discrepancia, y la evidencia no debe contener ninguna
propuesta anterior a A9.

### Criterio discriminante de fallo

El contrato falla si ocurre cualquiera de estas: una dirección de contacto aparece en cualquier
artefacto; un testigo emitido aparece en claro en cualquier artefacto; una captura de rechazo
pierde los campos publicables que el participante había escrito; A2 es aceptado o A4 corta una
ronda; el conjunto de preseleccionadas de `RONDA_CONV` en la etapa 1 es vacío, de modo que
`SEGUIDA` no existe; alguno de los pasos posteriores actúa sobre una propuesta distinta de
`SEGUIDA`; D1 publica algo; una repetición de E4 o F5 produce una segunda invitación o una
segunda entrada publicada; el texto original cambia después de la ampliación; H3 es aceptado o su
propuesta se reasigna a otro canal; los campos anunciados y los expuestos difieren en cualquier
dirección; alguna superficie presenta la fecha como prueba de autoría; una propuesta queda en dos
rondas o en ninguna pudiendo estar en una; algún artefacto falta o no coincide con su SHA-256; o
la secuencia no puede completarse.

No hay tercera categoría: toda observación de la corrida se resuelve dentro de estos dos
criterios. Si algo del escenario impide ejecutar un paso, el contrato falla y se propone otro.

### Controles negativos

A2 y A4 controlan la propiedad de D-01; C2.4, C2.5 y C2.13 controlan publicación, reintento y
ventana. El control del criterio nuevo de C2.3 es el propio A2/H3: son rechazos, que es
exactamente el momento en que el servidor tiene el contacto en la mano y está por responder con
una página. Sin ellos, un sistema que devolviera el contacto en cualquier error seguiría pasando
todos los casos positivos.

### Limitaciones conocidas

- Es una corrida local. No demuestra ninguna propiedad de la integración real con la IA
  contratada (RT-1), y no satisface ni sustituye C2.6, C2.7, C2.8, C2.10 ni C2.11.
- No demuestra la autenticación real del extremo.
- La evaluación la produce el ejecutor determinista. No es un modelo (RT-2).
- El «participante sintético» de C2.9 es el CONSTRUCTOR siguiendo la guía; no demuestra que una
  persona real la entienda.
- El control de votación marca el navegador y no comprueba identidad de personas.
- La comparación de C2.14 la hace una persona leyendo dos artefactos.
- El criterio de D-04 comprueba que los testigos de **esta** corrida no quedan en claro. No es una
  demostración general de que ningún secreto futuro pueda filtrarse por una forma no prevista.
- Los datos son sintéticos y están marcados como tales en el propio dato.

## Verificación de esta entrega

No se ejecutó ninguna verificación discriminante, ningún caso de `PLAN.md`, ningún túnel y
ninguna sesión de ChatGPT. Lo que sigue es verificación de construcción: comprueba mecanismos del
candidato y **no** satisface ningún caso C2.x.

| Comprobación | Resultado |
|---|---|
| `python -m pytest -q -rs`, suite completa en una corrida, Python 3.12.4 sobre Windows 11 | `116 passed`, rc=0, sin omitidas |
| Pruebas nuevas de la corrección de C2.3 | una página de rechazo no devuelve el contacto enviado y sí devuelve los campos publicables; ningún campo declarado privado vuelve escrito a la página |
| Pruebas nuevas de la corrección de D-04 | la respuesta de la invitación no trae el testigo como campo propio y su enlace sigue terminando en el testigo emitido; la llamada preservada sustituye el testigo por valor y no lo contiene |
| Evidencia histórica de `C-U2-1` | `unidad-2-circuito-minimo/evidencia/` sin modificar: `git status` no la reporta |
| `git status` antes del commit | solo `unidad-2-circuito-minimo/`; `.venv`, `.data`, `__pycache__` y `.pytest_cache` fuera por `.gitignore`; `PLAN.md`, `BOOTSTRAP.md`, el `EVENTO.md` de la raíz y `unidad-1-…` sin tocar |

## Limitaciones de esta entrega

- **Nada está verificado contra `PLAN.md`.** Las correcciones se comprueban con pruebas de
  construcción; los casos C2.x esperan el congelamiento de `C-U2-2`.
- El fallo de C2.3 está corregido en el candidato, no demostrado: demostrarlo es lo que el
  contrato propone.
- La autenticación del extremo sigue sin implementarse; el mecanismo está decidido y pertenece a
  la intervención que prepare el contrato de la operación real.
- El sistema no estuvo expuesto a la red en ningún momento de esta intervención.
- `sistema/.venv` y `sistema/.data` quedan fuera de Git. El directorio `.atl/` del árbol es
  material de herramientas del entorno local, ajeno a esta entrega.

## Necesidad humana detectada

Ninguna activa. Para continuar —que el AUDITOR evalúe y, si es suficiente, congele `C-U2-2`— no
hace falta nada fuera del perímetro delegado vigente, y por eso esta entrega no preserva ningún
checkpoint.

Sigue anticipada, no activada, la necesidad material de `PLAN.md` §8 H-2 —exposición de red
alcanzable, con su costo y su superficie— junto con una cuenta de la IA de referencia, para la
corrida real que ejercitará C2.6, C2.7, C2.8, C2.10, C2.11 y la autenticación del extremo. No se
activa por anticipación.
