# EVENTO — Unidad 2: ejecución de C-U2-2

Quinta intervención de U2: ejecución del contrato congelado `C-U2-2`. Explica la semántica de la
entrega; el delta exacto lo demuestra Git.

**Resultado: `C-U2-2` se cumple.** Los once criterios del contrato y la propiedad corregida de
D-01 se satisfacen, cada uno leído del artefacto que lo sostiene. Interpretarlo contra el
congelamiento corresponde al AUDITOR.

## Qué recibió

Cabecera canónica con `INCOMING_TURN_ID=30`, para el CONSTRUCTOR current.

La situación se rederivó desde Git sobre el corte recibido:

- la última entrega de work es `320a643b3880b2e6522b9dfb35a708c5fb898713`, con el árbol limpio
  salvo `.atl/`, que es material de herramientas del entorno local;
- la intervención auditora del corte es `auditorias/320a643b3880b2e6522b9dfb35a708c5fb898713.md`,
  con `VEREDICTO=CORRECCIONES_ACEPTADAS_Y_C_U2_2_CONGELADO`,
  `CONTRATO_C_U2_2_CONGELADO=SI`, `CONTRATO_C_U2_2_EJECUTADO=NO`, `EVIDENCIA_C_U2_1=INTACTA` y
  `HUMAN_NEED_REAL_ACTUAL=NO`;
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

Antes de tocar nada se comprobó la identidad exacta de lo congelado: `HEAD` igual a
`320a643b3880b2e6522b9dfb35a708c5fb898713`, y el blob de `unidad-2-circuito-minimo/EVENTO.md`
igual a `e3d439b57ff5555354cbfa4e4e92a91f630ca1f0`, que es `CONTRATO_C_U2_2_BLOB_SHA`. También se
comprobó que `unidad-2-circuito-minimo/evidencia-c-u2-2/` no existía: la corrida no se había
ejecutado antes de este pase. El texto del contrato ejecutado es ese blob, que sigue en Git; este
`EVENTO.md` lo reemplaza por el relato de la corrida, como en cada entrega.

## Cómo se ejecutó

Una sola vez, en el orden congelado A1→H3 más el paso Z, sobre el candidato congelado y sin
modificar ni el contrato ni el candidato en ningún momento. Windows local, Python 3.12.4,
servidor en `127.0.0.1:8000`, `sistema/.data` borrado antes de empezar, sin exposición de red, sin
túnel, sin ChatGPT y sin ningún modelo. Ningún paso se repitió.

`SEGUIDA` se resolvió por la regla congelada: las preseleccionadas de etapa 1 fueron `P-001`,
`P-002`, `P-003` y `P-004`, de modo que `SEGUIDA` es **`P-001`**, que además es la propuesta
enviada a mano por el formulario público en el paso B1. `TESTIGO` se leyó del campo `enlace` de la
respuesta de E3, que es el único lugar donde el candidato corregido lo devuelve.

## Resultado, criterio por criterio

Cada comprobación se lee de un artefacto, no de la pantalla ni de este relato.

| Caso | Resultado | Dónde se lee |
|---|---|---|
| C2.1 cadena completa | cumple | `P-001` aparece en la recepción, en el conjunto de `convocatoria-1:ronda-1`, en su evaluación de etapa 1, en la única invitación, en el único registro vinculado, en su evaluación de etapa 2, en la lista publicada y en un voto, todo en `evidencia.json`; la guía de A1 no ofrece formulario y la de A11 sí |
| C2.2 integridad del original | cumple | la huella de `ver_propuesta` antes y después de la ampliación es `5b97906e` en las dos llamadas de `llamadas.jsonl`; el registro lleva `kind=ampliacion_autor` y autoría propia; la evaluación de etapa 2 de `P-001` cita la ampliación |
| **C2.3 separación privado/público** | **cumple** | ninguna dirección de contacto aparece en `llamadas.jsonl`, ni en `evidencia.json`, ni en ninguna de las dieciocho capturas. En particular, las dos capturas de rechazo —`envio-antes-de-abrir.html` y `envio-a-convocatoria-cortada.html`— no contienen el contacto enviado **y sí conservan** el texto publicable que el participante había escrito |
| C2.4 publicación sin autorización | cumple | la llamada de D1 devuelve `isError: true`; `finalistas-sin-autorizacion.html` no nombra ninguna propuesta; la ronda figura autorizada recién después de F3 |
| C2.5 reintentos | cumple | las dos llamadas a `preparar_invitacion` devuelven el mismo objeto y hay una sola invitación; las dos a `publicar_finalistas` devuelven la misma respuesta, con el mismo `published_at`, y la lista publicada no repite |
| C2.9 participación directa | cumple | `guia-abierta.html` trae objetivo, criterios, condiciones, plazos y formulario; `recepcion-p001.html` confirma la recepción |
| C2.12 coexistencia y cortes | cumple | `convocatoria-1:ronda-1` = `P-001`…`P-009`; `permanente:ronda-1` = `P-010`…`P-013`; `permanente:ronda-2` = `P-014` |
| C2.13 ventana cerrada | cumple | `envio-a-convocatoria-cortada.html` rechaza y nombra el canal permanente abierto; no existe `P-015`: nada se reasignó |
| C2.14 transparencia previa | cumple | los siete campos declarados publicables en `evidencia.json` son exactamente los que anuncia `guia-abierta.html` y exactamente los que exponen `finalistas.html` y `vivo.html`; el campo privado no aparece en ninguna de las dos |
| C2.15 fecha de recepción | cumple | las siete capturas que muestran una fecha la presentan como «Recibida en el sistema»; las que hablan de autoría lo hacen para negarla |
| **D-04 evidencia sin secretos accionables** | **cumple** | el testigo emitido en la corrida no aparece en claro en `llamadas.jsonl`, ni en `evidencia.json`, ni en ninguna captura; la marca `<testigo>` aparece en los artefactos por donde habría viajado; y la respuesta de E3 no trae el testigo como campo propio |
| propiedad corregida de D-01 | cumple | A2 fue rechazado, A4 devolvió error, A3 muestra los dos canales en `preparacion` sin calibración, A7 muestra la calibración devuelta con la discrepancia `Falta el peso de la audiencia.`, y la primera recepción es posterior a la aprobación |
| artefactos | cumplen | los diecinueve del inventario existen y coinciden con su SHA-256, tanto en la corrida como en las copias entregadas |

Los dos rechazos de votación siguen siendo distinguibles entre sí: el repetido dice «Ya votaste
esta propuesta en esta ronda» y el cuarto dice «Alcanzaste el máximo de 3 votos de esta ronda».

La corrida produjo catorce propuestas, dieciocho evaluaciones, una invitación, un registro
vinculado, tres votos, dieciocho llamadas MCP preservadas y dieciocho capturas. Las tres señales
quedaron separadas y distintas entre sí —IA `P-001`…`P-004`, audiencia `P-001`, `P-002` y `P-003`
con un voto cada una, creador `P-002` y `P-005`—, sin ningún cuarto orden.

## Qué cambió respecto de la corrida anterior

`C-U2-1` había fallado por C2.3 y había dejado abierto D-04. Las dos correcciones se comportaron
como el contrato exigía, y la comprobación es discriminante en las dos direcciones:

- las capturas de rechazo ya no traen el contacto, **y siguen trayendo** el texto publicable que
  el participante escribió. Una corrección que hubiera vaciado el formulario entero habría hecho
  fallar el criterio igual que la fuga;
- el testigo no aparece en claro en ningún artefacto y la marca `<testigo>` está donde habría
  viajado, con la respuesta de la invitación ya sin el campo suelto.

El resto del recorrido se ejercitó completo, como justificaba el alcance de regresión del
contrato, y reprodujo los mismos identificadores, conjuntos y huellas que la corrida anterior.

## Evidencia entregada

En `unidad-2-circuito-minimo/evidencia-c-u2-2/`: `evidencia.json`, `llamadas.jsonl` y dieciocho
capturas. Las copias coinciden con el SHA-256 que registró la corrida.

`unidad-2-circuito-minimo/evidencia/`, que es la de `C-U2-1`, **no se tocó**: `git status` no la
reporta. Sigue conservando el testigo en claro que hizo visible D-04, porque reescribirla borraría
la prueba del defecto.

## Verificación de esta entrega

| Comprobación | Resultado |
|---|---|
| Identidad de lo congelado antes de ejecutar | `HEAD` = `320a643…`; blob de `EVENTO.md` = `e3d439b5…` = `CONTRATO_C_U2_2_BLOB_SHA`; `evidencia-c-u2-2/` inexistente |
| Ejecución de la secuencia congelada | una sola vez, A1→H3 y Z, sin repetir ningún paso |
| Lectura de los criterios contra los artefactos | cuarenta y una comprobaciones; las cuarenta y una se cumplen |
| Integridad de las copias entregadas | los diecinueve artefactos coinciden con el SHA-256 que registró la corrida |
| Evidencia histórica de `C-U2-1` | sin modificar |
| `git status` antes del commit | solo `unidad-2-circuito-minimo/`; `.venv`, `.data`, `__pycache__` y `.pytest_cache` fuera por `.gitignore`; `PLAN.md`, `BOOTSTRAP.md`, el `EVENTO.md` de la raíz y `unidad-1-…` sin tocar |

## Limitaciones

- Es una corrida local. No demuestra ninguna propiedad de la integración real con la IA
  contratada (RT-1), y no satisface ni sustituye C2.6, C2.7, C2.8, C2.10 ni C2.11.
- No demuestra la autenticación real del extremo, que sigue sin implementarse.
- La evaluación la produjo el ejecutor determinista local, cuyo nombre viaja en las dieciocho
  evaluaciones de la evidencia. No es un modelo (RT-2).
- El «participante sintético» fue el CONSTRUCTOR siguiendo la guía: demuestra que la guía contiene
  lo que hace falta, no que una persona real la entienda.
- El control de votación marca el navegador y no comprueba identidad de personas.
- El criterio de D-04 comprueba que los testigos de **esta** corrida no quedan en claro; no es una
  demostración general contra cualquier forma futura de filtración.
- Todos los datos son sintéticos y están marcados como tales en el propio dato.
- El contrato queda agotado: produjo su resultado. Cualquier corrida nueva necesita un contrato
  nuevo conforme a REVOLUTIONS §6.1, y esta entrega no lo propone.

## Necesidad humana detectada

Ninguna activa. La corrida y su lectura están dentro del perímetro delegado, y esta entrega no
preserva ningún checkpoint.

Sigue anticipada, no activada, la necesidad material de `PLAN.md` §8 H-2 —exposición de red
alcanzable, con su costo y su superficie— junto con una cuenta de la IA de referencia, para la
corrida real que ejercitará C2.6, C2.7, C2.8, C2.10, C2.11 y la autenticación del extremo. No se
activa por anticipación.
