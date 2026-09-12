# EVENTO — Unidad 2: ejecución de C-U2-1

Tercera intervención de U2: ejecución del contrato congelado. Explica la semántica de la
entrega; el delta exacto lo demuestra Git.

**Resultado: `C-U2-1` FALLA.** Falla el criterio de C2.3. Los demás criterios se cumplen. El
fallo se preserva sin reparar y sin repetir la corrida; interpretarlo corresponde al AUDITOR.

## Qué recibió

Cabecera canónica completa con `INCOMING_TURN_ID=24`, para el CONSTRUCTOR current.

La situación se rederivó desde Git sobre el corte recibido:

- la última entrega de work es `bddc126ab0e7f15f386220015088cd27dd64a459`, con el árbol limpio
  salvo `.atl/`, que es material de herramientas del entorno local;
- la intervención auditora del corte es `auditorias/bddc126ab0e7f15f386220015088cd27dd64a459.md`,
  con `D_01=CERRADO`, `D_02=CERRADO`, `D_03=CERRADO`,
  `AUTENTICACION_CARACTERIZACION=CORREGIDA`, `CONTRATO_C_U2_1_CONGELADO=SI` y
  `CONTRATO_C_U2_1_EJECUTADO=NO`;
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

Antes de tocar nada se comprobó la identidad exacta de lo congelado: `HEAD` igual a
`bddc126ab0e7f15f386220015088cd27dd64a459`, y el blob de `unidad-2-circuito-minimo/EVENTO.md`
igual a `aa20b7cc648a2e159478f13f1f9e3a68d641f685`, que es `CONTRACT_BLOB_SHA`. El texto del
contrato ejecutado es exactamente ese blob, que sigue disponible en Git: este `EVENTO.md` lo
reemplaza por el relato de la corrida, como en cada entrega.

## Cómo se ejecutó

Una sola vez, en el orden congelado A1→H3 más el paso Z, sobre el candidato congelado y sin
modificar ni el contrato ni el candidato en ningún momento. Windows local, Python 3.12.4,
servidor en `127.0.0.1:8000`, `sistema/.data` borrado antes de empezar, sin exposición de red,
sin ChatGPT y sin ningún modelo.

Un incidente de entorno, antes de que el sistema recibiera nada: el primer intento del paso A1
abortó dentro del shell, que convirtió el argumento `/` en una ruta de Windows antes de
entregárselo al programa. La petición nunca salió, el servidor no registró ninguna solicitud y
no se escribió ningún artefacto. El paso se ejecutó a continuación tal como está congelado, con
esa conversión desactivada. No hubo ninguna otra repetición de ningún paso.

`SEGUIDA` se resolvió por la regla congelada: las preseleccionadas de etapa 1 fueron `P-001`,
`P-002`, `P-003` y `P-004`, de modo que `SEGUIDA` es **`P-001`**, que además es la propuesta
enviada a mano por el formulario público en el paso B1.

## El fallo

**C2.3 falla.** El criterio congelado exige que la dirección de contacto sembrada no aparezca
«en `llamadas.jsonl`, ni en ninguna captura, ni en `evidencia.json`». Aparece en dos capturas:

| Artefacto | Qué contiene |
|---|---|
| `evidencia/capturas/envio-antes-de-abrir.html` | `<input type="email" value="participante000.sintetico@example.invalid" name="contact" …>` |
| `evidencia/capturas/envio-a-convocatoria-cortada.html` | `<input type="email" value="participante015.sintetico@example.invalid" name="contact" …>` |

La causa observada: cuando el formulario rechaza un envío, la página de error vuelve a
renderizar el formulario con los valores que el participante había escrito, para que no tenga
que tipearlos de nuevo, y el contacto es uno de esos valores. Las dos capturas que lo contienen
son exactamente las dos respuestas de rechazo de la corrida.

No aparece en `llamadas.jsonl`, ni en `evidencia.json`, ni en ninguna de las otras dieciséis
capturas, entre ellas la guía pública, el portal de finalistas, la vista de vivo y la página de
ampliación.

Esto último **no anula el fallo y no se usa para atenuarlo**: el criterio congelado es el que
es, no admite una tercera categoría y no se redefine después de observar el resultado. Lo que
la corrida dejó demostrado es que el contacto no llega a ninguna superficie que otro
participante o la IA puedan leer, y lo que dejó sin demostrar es la propiedad tal como el
contrato la fijó. La disposición corresponde al AUDITOR.

El defecto **no se reparó**: el candidato queda tal como estaba congelado.

## Lo que la corrida sí dejó demostrado

Cada comprobación se lee de un artefacto, no de la pantalla ni de este relato.

| Caso | Resultado | Dónde se lee |
|---|---|---|
| C2.1 cadena completa | cumple | `P-001` aparece en la recepción, en el conjunto de `convocatoria-1:ronda-1`, en su evaluación de etapa 1, en la única invitación, en el único registro vinculado, en su evaluación de etapa 2, en la lista publicada y en un voto, todo en `evidencia.json`; la guía de A1 no ofrece formulario y la de A11 sí |
| C2.2 integridad del original | cumple | la huella de `ver_propuesta` antes y después de la ampliación es `5b97906e` en las dos llamadas de `llamadas.jsonl`; el registro lleva `kind=ampliacion_autor` y autoría propia; la evaluación de etapa 2 de `P-001` cita la ampliación |
| C2.3 separación privado/público | **FALLA** | ver arriba |
| C2.4 publicación sin autorización | cumple | la llamada de D1 devuelve `isError: true`; `finalistas-sin-autorizacion.html` no nombra ninguna propuesta; la ronda figura autorizada recién después de F3 |
| C2.5 reintentos | cumple | las dos llamadas a `preparar_invitacion` devuelven el mismo objeto y hay una sola invitación; las dos a `publicar_finalistas` devuelven la misma respuesta, con el mismo `published_at`, y la lista publicada no repite |
| C2.9 participación directa | cumple | `guia-abierta.html` trae objetivo, criterios, condiciones, plazos y formulario; `recepcion-p001.html` confirma la recepción |
| C2.12 coexistencia y cortes | cumple | `convocatoria-1:ronda-1` = `P-001`…`P-009`; `permanente:ronda-1` = `P-010`…`P-013`; `permanente:ronda-2` = `P-014` |
| C2.13 ventana cerrada | cumple | `envio-a-convocatoria-cortada.html` rechaza y nombra el canal permanente abierto; no existe `P-015`: nada se reasignó |
| C2.14 transparencia previa | cumple | los siete campos declarados publicables en `evidencia.json` son exactamente los que anuncia `guia-abierta.html` y exactamente los que exponen `finalistas.html` y `vivo.html`; el campo privado no aparece en ninguna de las dos |
| C2.15 fecha de recepción | cumple | las siete capturas que muestran una fecha la presentan como «Recibida en el sistema»; las tres que hablan de autoría lo hacen para negarla («no demuestra autoría», «No demuestra autoría ni prioridad») |
| propiedad corregida de D-01 | cumple | A2 fue rechazado, A4 devolvió error, A3 muestra los dos canales en `preparacion` sin calibración, A7 muestra la calibración devuelta con la discrepancia `Falta el peso de la audiencia.`, y la primera recepción es posterior a la aprobación |
| artefactos | cumplen | los diecinueve del inventario existen y coinciden con su SHA-256, tanto en la corrida como en las copias entregadas |

La corrida produjo además: catorce propuestas, dieciocho evaluaciones, una invitación, un
registro vinculado, tres votos, dieciocho llamadas MCP preservadas y dieciocho capturas. Las
tres señales de la ronda quedaron separadas y distintas entre sí —IA `P-001`…`P-004`, audiencia
`P-001`, `P-002` y `P-003` con un voto cada una, creador `P-002` y `P-005`—, sin ningún cuarto
orden.

Los dos rechazos de votación son distinguibles entre sí, como exige la mecánica del caso: el
repetido dice «Ya votaste esta propuesta en esta ronda» y el cuarto dice «Alcanzaste el máximo
de 3 votos de esta ronda».

## Otra observación de la corrida, no reparada

El testigo de la invitación aparece dos veces, en claro, dentro de `evidencia/llamadas.jsonl`:
la redacción sustituye la capacidad en todas partes —seis veces como `<capacidad>`, ninguna en
claro— y sustituye los testigos cuando viajan dentro de una URL, pero la respuesta de
`preparar_invitacion` devuelve además el testigo como campo suelto, y esa forma no está cubierta.

No es ninguno de los criterios congelados de C-U2-1, y por eso no cambia su resultado. Se
registra porque contradice lo que la sección de evidencia del contrato afirma sobre los
artefactos, y porque tocarlo ahora sería reparar el candidato después de observar la corrida.
El testigo publicado pertenece a una base local sintética que no vuelve a servirse.

Por la misma razón tampoco se tocó `ARQUITECTURA.md`, que afirma que los testigos no salen en
la evidencia: corregir ese texto ahora haría que el candidato entregado dejara de ser el que
corrió. La afirmación queda contradicha acá, con su evidencia, y el candidato queda intacto.

## Verificación de esta entrega

| Comprobación | Resultado |
|---|---|
| Identidad de lo congelado antes de ejecutar | `HEAD` = `bddc126…`; blob de `EVENTO.md` = `aa20b7cc…` = `CONTRACT_BLOB_SHA` |
| Ejecución de la secuencia congelada | una sola vez, A1→H3 y Z, sin repetir ningún paso |
| Lectura de los criterios contra los artefactos | treinta y cinco comprobaciones; treinta y cuatro se cumplen, una falla (C2.3) |
| Integridad de las copias entregadas | los diecinueve artefactos coinciden con el SHA-256 que registró la corrida |
| `git status` antes del commit | solo `unidad-2-circuito-minimo/`; `.venv`, `.data`, `__pycache__` y `.pytest_cache` fuera por `.gitignore`; `PLAN.md`, `BOOTSTRAP.md`, el `EVENTO.md` de la raíz y `unidad-1-…` sin tocar |

Una corrección de lectura, para que quede en el registro: la primera pasada de mi comprobación
de C2.15 marcó rojo por un error propio —buscaba «demuestra autoría» sin distinguir mayúsculas
en la negación que lo precede—, y las tres superficies señaladas dicen justamente lo contrario.
El texto exacto está citado arriba y en las capturas.

## Limitaciones

- Es una corrida local. No demuestra ninguna propiedad de la integración real con la IA
  contratada (RT-1), y no satisface ni sustituye C2.6, C2.7, C2.8, C2.10 ni C2.11.
- No demuestra la autenticación real del extremo, que sigue pendiente de implementación y de la
  corrida real.
- La evaluación la produjo el ejecutor determinista local, cuyo nombre viaja en las dieciocho
  evaluaciones de la evidencia. No es un modelo (RT-2).
- El «participante sintético» fue el CONSTRUCTOR siguiendo la guía: demuestra que la guía
  contiene lo que hace falta, no que una persona real la entienda.
- El control de votación marca el navegador y no comprueba identidad de personas.
- Todos los datos son sintéticos y están marcados como tales en el propio dato.
- El contrato queda agotado: produjo su resultado. Cualquier corrida nueva necesita un contrato
  nuevo conforme a REVOLUTIONS §6.1, y esta entrega no lo propone.

## Necesidad humana detectada

Ninguna activa. La corrida y su interpretación están dentro del perímetro delegado, y esta
entrega no preserva ningún checkpoint.

Sigue anticipada, no activada, la necesidad material de `PLAN.md` §8 H-2 —exposición de red
alcanzable, con su costo y su superficie— junto con una cuenta de la IA de referencia, para la
corrida real que ejercitará C2.6, C2.7, C2.8, C2.10, C2.11 y la autenticación del extremo. No se
activa por anticipación.
