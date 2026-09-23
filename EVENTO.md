# EVENTO — Corrección del plan previa a toda unidad

Intervención previa a toda unidad, en la raíz del repositorio de trabajo. Explica la semántica
de la entrega; el delta exacto sobre la entrega anterior lo demuestra Git.

## Qué recibió

Un `next_prompt` con la cabecera canónica completa e `INCOMING_TURN_ID=3` entero, que instruyó
atender la auditoría de la entrega anterior y corregir el mismo `PLAN.md` para cerrar los
defectos D-01 a D-04, sin ejecutar ninguna unidad material.

La situación se rederivó desde Git sobre el corte recibido, sin suponerla:

- D1: la última entrega de work es `437422f5de52f95ba5959d7a2a652fe1b5c16a4d`.
- D2: esa entrega tocó solo la raíz; no existe todavía ninguna unidad.
- D3–D5: la intervención auditora del corte es `auditorias/437422f5de52f95ba5959d7a2a652fe1b5c16a4d.md`,
  es decir, la auditoría aplicable a la última entrega, con `VEREDICTO=CORRECCION_REQUERIDA`.
- D6: `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`; el perímetro vigente es el de
  `BOOTSTRAP.md`, sin deltas posteriores.

Ambos clones se sincronizaron por avance rápido y el corte de audit desciende del bootstrap del
AUDITOR preservado en `BOOTSTRAP.md`.

## Qué hizo y por qué

Los cuatro defectos se comprobaron contra el manifiesto aprobado y se sostienen: el plan
anterior cubría las seis familias de verificación técnica, pero no todo el resultado
observable ni todo el alcance funcional. La corrección se hizo sobre el mismo `PLAN.md`.

- **D-01 — enlace de entrada del creador.** Se ubicó en dos unidades según qué verificación lo
  ejercita. En U2, el enlace inicia la operación del circuito, confirmando el acceso efectivo
  (C2.7), con un control negativo contra una IA que presente resultados que no obtuvo del
  sistema (C2.8, decisión técnica 10, riesgo R12). En U4, el mismo enlace se completa como
  acompañamiento de instalación adaptado a conocimientos, herramientas y permisos, verificado
  sobre perfiles sintéticos (C4.5) con su control negativo (C4.6). Se declara que eso no
  convierte la instalación por una persona externa en condición de cierre.
- **D-02 — entrada pública de audiencia.** El enlace público pasó a ser entregable de U2, con
  acceso directo (C2.9), acceso asistido por la IA de referencia (C2.10) y un control negativo
  de intención y evidencia (C2.11). La decisión técnica 11 fija que la IA del participante
  asiste la redacción y el envío se hace siempre por el mismo formulario: así el uso de IA es
  opcional y el sistema no depende de integrarse con la IA de cada participante.
- **D-03 — recepción permanente con cortes.** Se incorporó a U2 junto con las convocatorias
  delimitadas. La decisión técnica 12 introduce la ronda de evaluación como unidad común
  —cierre de convocatoria o corte del canal permanente—, que es lo que impide mezclar ventanas
  o criterios. C2.12 verifica la coexistencia y C2.13 es su control negativo; C3.4 extiende la
  reevaluación por cambio de criterios a los cortes.
- **D-04 — atribución y transparencia.** Cada regla quedó asignada separando comportamiento
  implementado de documentación o experiencia: transparencia previa al envío (U2, C2.14, con
  decisión técnica 14), fecha de recepción (U2, C2.15), colaboración de terceros deshabilitada
  por defecto y diferenciada al habilitarse (U3, C3.9 y C3.10, decisión técnica 13), similitud
  como señal (U3, C3.11), mejor redacción (U3, C3.12), y la documentación entregada que las
  explica (U4, C4.7).

Para cerrar la clase de defecto y no solo sus cuatro instancias, se agregó a `PLAN.md` un mapa
de cobertura que localiza cada exigencia del resultado observable y del alcance funcional en
una unidad y en los casos que la ejercitan. Al construirlo aparecieron dos exigencias del
manifiesto que tampoco estaban ejercitadas, y se incorporaron a U3 con el mismo criterio:

- la configuración de la votación no permite publicar propuestas privadas ni modificar la
  atribución, y no cambia después de abrir la ronda (C3.13);
- el límite configurable de volumen o de gasto (C3.14).

Otros cambios derivados, sin alterar la división ni la secuencia:

- §1 fija cómo se tratan en los contratos los casos que dependen de una IA no determinista.
- §2 justifica por qué los enlaces de entrada no forman una unidad propia.
- H-2 abarca también la exposición de los enlaces de entrada del creador y de la audiencia.

Se conservó `BOOTSTRAP.md` sin cambios: la corrección no toca ningún hecho constitutivo.

## Verificación de esta entrega

Es una intervención documental: ninguna verificación del plan se ejecutó, ni se ejecuta
ninguna unidad.

| Comprobación | Resultado |
|---|---|
| Comprobación cruzada de identificadores de caso en `PLAN.md` (script local de Python sobre el archivo) | 41 casos definidos, ninguno duplicado; todo caso citado en el mapa de cobertura existe, y todo caso definido está citado en el mapa |
| `git diff --stat` antes del commit | solo `PLAN.md` y `EVENTO.md` modificados; `BOOTSTRAP.md` sin cambios |

La correspondencia entre cada exigencia del manifiesto y su fila del mapa de cobertura es un
juicio del CONSTRUCTOR, no una comprobación mecánica: el script demuestra solo la consistencia
interna de los identificadores.

## Limitaciones

- El plan crece en casos; la división en cuatro unidades y la secuencia no cambian. El aumento
  recae sobre todo en U2, cuyo riesgo de alcance creciente (R4) sigue acotado a la versión más
  delgada que hace cerrar el ciclo con todas sus entradas.
- El directorio `.atl/` del árbol de trabajo es material de herramientas del entorno local,
  ajeno a esta entrega; queda sin seguimiento y fuera del commit.

## Necesidad humana detectada

NECESIDAD DEL HUMANO — ejecutar las unidades de `PLAN.md` sigue requiriendo la aprobación
humana del plan sobre su identidad exacta, reservada por la constitución del carril Z. La
auditoría anterior juzgó prematuro activarla mientras D-01 a D-04 siguieran abiertos; esta
entrega los corrige y vuelve a registrar la necesidad.

El CONSTRUCTOR registra y rutea esta necesidad; no declara que sea real ni activa al humano.
Esa determinación, y si el plan ya es suficiente para pedirla, corresponde al AUDITOR.

## Propuesta documental del CONSTRUCTOR — C-U2-11 (INCOMING_TURN_ID=162)

### Recepción y corte de trabajo

Se recibió el sobre auditor identificado por `INCOMING_TURN_ID=162` para preparar una propuesta no ejecutable de sucesor C-U2-11. El corte indicado es `BASE_WORK_SHA=ce89a58c0862abced634224dea1dc42a27505b6a`; la trazabilidad de auditoría recibida es `INCIDENT_AUDIT_SHA=1ddaa82eb668f0d09f1d99835c6e0d3b97ef3264` y `C0_AUDIT_SHA=e937a00dc0ec6cea427c5031971873e255281791`. Se preserva como historia C-U2-10 con `CONTRACT_BLOB_SHA=2e96c72aaf0b18cc67fccba11282f545d4025d1b` y `CHECKPOINT_BLOB_SHA=709595ae1cd12a46d3d432d9b6fddc79c4a596c2`.

### Hecho recibido, no reinterpretado

La pasada visual única de C-U2-10 mostró en «Personal > Created by me» exactamente `Sonda propuestas U1`, `Sonda propuestas U1 v2` y `Circuito propuestas C-U2-5`, cada una con `+`. No se hicieron clics ni cambios de estado. No se guardaron PNG ni matriz local. El glifo carecía de tooltip y etiqueta accesible observados; el significado atribuido por la explicación humana no quedó probado por la interfaz y el AUDITOR no acreditó C0. La pasada quedó consumida: no se repite ni se materializa evidencia retrospectiva.

### Diseño propuesto

Se propone una inspección C0 nueva y única, limitada a lectura, que exige texto explícito de estado asociado en pantalla al nombre exacto de cada app. Ni `+`, ni botones sin etiqueta, ni ausencia de entradas/lista vacía cuentan como prueba. Antes de abrir apps, la persona debe superar un preflight en página neutral: guardar manualmente con el flujo Windows/Paint un PNG en el destino de `evidencia-c-u2-11/preflight/`, reabrirlo desde disco y documentar lectura legible. Si no se prueba el guardado/relectura en el destino, no comienza la inspección. Durante la inspección, la persona preserva capturas PNG secuenciales sin editar y una matriz por app que transcribe la señal literal y referencia la imagen donde aparecen juntos nombre y estado; luego se detiene para revisión auditora.

Las expresiones de acción citadas en contrato/checkpoint son ejemplos condicionales; no se afirma que esa UI ni la capacidad de persistencia existan. No se usa como prueba la API de captura CUA, porque no se ha demostrado que guarde archivos. Cualquier ambigüedad, señal no explícita, estado instalado/conectado, afiliación dudosa o fallo de persistencia detiene C0 sin reintento ni alteración de apps. La evidencia y los nuevos documentos usan el namespace sucesor `evidencia-c-u2-11`; C-U2-10 permanece intacto.

### Autoridad y alcance

El gate y P0 C-U2-10 son históricos y no se heredan como autorizaciones. La propuesta C-U2-11 es exclusivamente remediación documental/inspección C0; no incluye P1 ni pasos posteriores. Requiere congelamiento exacto del AUDITOR, nuevas identidades, H-2/autorización humana específica y los sobres que correspondan antes de cualquier acción. Este registro y los documentos no autorizan UI ni ejecución.

### Archivos y verificación de alcance

Archivos de propuesta: `unidad-2-circuito-minimo/CONTRATO-C-U2-11.md`, `unidad-2-circuito-minimo/CHECKPOINT_HUMANO-C-U2-11.md` y este apéndice de `EVENTO.md`. Ningún otro archivo debe modificarse en esta entrega; no se hace commit ni push. No se ejecutaron gate, P0, C0, P1, app/servicio ni UI; no se tocó el entorno ni se creó evidencia operativa. La revisión y congelamiento corresponden al AUDITOR.

## Corrección append-only de alcance publicado — C-U2-11 (D27, INCOMING_TURN_ID=163)

La autodescripción en el apéndice anterior y en la primera versión publicada de `CONTRATO-C-U2-11.md` y `CHECKPOINT_HUMANO-C-U2-11.md`, que decía «no se hace commit ni push», fue inexacta respecto de la entrega materializada. `TARGET_WORK_SHA=8cf109d5ec183910e7599dd8dcbacb6e958eed20` fue efectivamente creado y publicado en `francogg89-ai/work-claude-z`. La corrección se agrega sin editar ni borrar el apéndice histórico. La propuesta documental fue la única materia de ese commit; no se ejecutó preflight, UI, C0, gate, P0 ni P1, no se creó evidencia operacional y no se modificó el entorno. Esta corrección documental tampoco autoriza acción operacional alguna.

## Propuesta documental del CONSTRUCTOR — C-U2-12 (INCOMING_TURN_ID=168)

### Recepción y corte de trabajo

Se recibió el sobre del AUDITOR con `AUDIT_SHA=ddd3c8cba086f3c967c104f4513c1bbd74846717`. C-U2-11 queda histórico, agotado y no acreditado en C0; su inspección no se repite ni se completa retroactivamente. La base de esta propuesta es `BASE_WORK_SHA=82b49de2a191e1a409d3f1511fd8b6fbe2fe1b03`. El humano autorizó exclusivamente analizar el resultado, proponer C-U2-12, crear sus documentos y publicarlos en un único commit; esta autoridad no se extiende a ninguna operación material de C-U2-12.

### Hallazgo y remedio propuesto

La única C0 de C-U2-11 mostró las tres apps objetivo en «Personal > Creados por mí», con un `+` visual y botones sin etiqueta accesible. El AUDITOR confirmó `C0_C_U2_11_CONSUMIDO_NO_ACREDITADO_POR_SENAL_AMBIGUA` en `ddd3c8cba086f3c967c104f4513c1bbd74846717`. No se abrieron detalles ni se activaron controles; no hubo reintento, cambio de apps, P1 ni commit/push operativo. La captura visual de esa pasada no se persistió como evidencia C0 local. La declaración humana previa sobre desconexión permanece solo como contexto.

C-U2-12 propone reemplazar la lista y el glifo `+` como fuente probatoria por una vista de detalle en solo lectura. En la C0 anterior, el árbol accesible mostró para cada objetivo un enlace `Abrir <nombre exacto>` hacia una ruta de detalle del mismo origen; ninguno se activó y el contenido del detalle sigue sin verificar. La secuencia propuesta es usar únicamente ese enlace ordinario si en la futura ejecución conserva rol accesible/DOM `link`, destino same-origin y ruta de detalle del app exacto; en caso contrario, detener antes de activarlo. Nunca usar `+` ni botones. Para cada app, una futura observación solo puede contar si el detalle muestra simultáneamente el nombre exacto y texto explícito asociado que indique una acción pendiente, como `Instalar complemento`, `Agregar a ChatGPT` o `Conectar`. Son ejemplos de criterio, no afirmaciones de que la UI actual los muestre.

El alcance mínimo propuesto se limita a `Sonda propuestas U1`, `Sonda propuestas U1 v2` y `Circuito propuestas C-U2-5`. Solo se admitirían adicionales incluidos en un manifiesto explícito congelado por el AUDITOR. Se propone repetir antes un preflight neutral en `unidad-2-circuito-minimo/evidencia-c-u2-12/preflight/`, usando el flujo local `Fn+PrtSc`, Paint, guardado PNG y reapertura desde disco que el reporte de C-U2-11 registra; el resultado de C-U2-11 queda como antecedente histórico, no como autorización ni sustituto del nuevo preflight. Las capturas futuras se guardarían en orden `c0-estado-apps-NN.png` y una matriz local incluiría texto literal, asociación visual, resultado, hora local y referencia a la captura. Si una app no cumple el criterio, se preservaría solo la vista observada si el flujo ya validado lo permite y se detendría sin inspeccionar objetivos restantes.

### Autoridad, evidencia y detención

La propuesta no autoriza ejecución. Si el AUDITOR la congela, cualquier ejecución futura requerirá nuevas identidades y autorización humana, además de los sobres aplicables. El mecanismo futuro propuesto conserva PNG locales originales e inalterados y una matriz local que vincule cada nombre, texto literal y captura. Un `+` aislado, control sin etiqueta, entrada ausente, señal ambigua, texto no vinculado al nombre exacto, estado instalado/conectado, ruta de navegación incierta o fallo de captura implica detener la única pasada y reportar `C0_NO_ACREDITADO`; cero reintentos. El AUDITOR decide la acreditación. No se heredan autorizaciones ni se incluyen cambios de apps, P1 o pasos posteriores; cualquier materialización Git futura de evidencia requerirá sobre auditor separado.

### Archivos y límite de esta intervención

La entrega documental comprende `unidad-2-circuito-minimo/CONTRATO-C-U2-12.md`, `unidad-2-circuito-minimo/CHECKPOINT_HUMANO-C-U2-12.md` y este apéndice append-only de `EVENTO.md`. Se permitió el commit y push de este único conjunto documental. No se ejecutaron pruebas ni pasos operativos, no se inspeccionó la UI ni detalles/apps durante esta intervención documental, no se modificaron apps ni entorno y no se creó evidencia operacional de C-U2-12. Cualquier ejecución futura queda sujeta a revisión auditora y nueva autorización humana.

## Corrección append-only de propuesta C-U2-12 — D28-D30 (INCOMING_TURN_ID=169)

Esta corrección no edita ni elimina los apéndices previos de `EVENTO.md`.

- **D28 — navegación como hipótesis:** la afirmación del apéndice anterior de C-U2-12 sobre enlaces accesibles `Abrir <nombre exacto>` observados en C-U2-11 no está respaldada como hecho observado y queda corregida. La existencia de un enlace, su rol accesible/DOM `link`, el destino same-origin y la correspondencia exacta con la app son hipótesis a verificar en una futura ejecución autorizada antes de activarlo. Ningún detalle se abrió en C-U2-11. El contrato y el checkpoint corregidos expresan esta condición.
- **D29 — autoridad documental:** la atribución del apéndice anterior a una autorización humana para la propuesta C-U2-12 fue incorrecta. El alcance documental original deriva del sobre/decisión del AUDITOR `AUDIT_SHA=ddd3c8cba086f3c967c104f4513c1bbd74846717`; no debe representarse como una nueva autorización humana. La autorización humana actual habilita únicamente este commit documental correctivo y su push.
- **D30 — antecedente durable del preflight:** `unidad-2-circuito-minimo/evidencia-c-u2-11/preflight/resultado.md` es un artefacto local y no se trata como evidencia durable. La auditoría durable `efc712117ef7045806314ac6cc2500bec9a8ead0` preserva el antecedente de que el método fue reportado; C-U2-12 sigue exigiendo un preflight nuevo antes de cualquier ejecución futura.

El alcance de esta corrección es documental. No se ejecutaron preflight, inspección de UI, C0, P1 ni pruebas operativas; no se modificaron apps ni entorno. Se publica en el único commit correctivo autorizado para revisión del AUDITOR. No autoriza acción operativa alguna.
