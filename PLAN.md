# PLAN — Sistema replicable de propuestas de audiencia asistido por IA

## 1. Qué gobierna este plan

Este plan describe cómo alcanzar el manifiesto identificado en `BOOTSTRAP.md`
(`MANIFEST_REPO` + `MANIFEST_PATH` + `MANIFEST_SHA`), bajo el método y las capacidades
declarados allí. No sustituye al manifiesto ni a la constitución: donde este plan y el
manifiesto difieran, prevalece el manifiesto.

El plan describe unidades, dependencias, secuencia, decisiones técnicas, verificaciones,
criterios de terminación, riesgos e intervenciones humanas previsibles. No describe estado.

Cada verificación discriminante concreta se propone como contrato previo en el `EVENTO.md` de
su unidad, **antes** de ejecutarla, conforme a REVOLUTIONS §6.1. Lo que este plan fija son los
casos, los resultados esperados y las condiciones de aceptación que ese contrato debe honrar;
no reemplaza al contrato ni autoriza ejecutar una verificación sin congelarlo.

Cuando un caso depende del comportamiento de una IA, que no es determinista, el contrato previo
fija la cantidad de corridas y el criterio de evaluación de cada transcripción. En los
controles negativos, una sola corrida que fabrique resultados, invente evidencia o pida un
secreto hace fallar el caso: no se promedia.

---

## 2. Criterio de división en unidades

La división no se decide por tamaño ni por simetría. Una frontera de unidad existe únicamente
cuando se cumplen las tres condiciones siguientes:

1. **Dependencia real**: lo que la unidad produce cambia qué se construye después, no
   solamente cuándo. Si el resultado no altera decisiones posteriores, no hay frontera.
2. **Verificación discriminante propia**: la unidad se cierra con evidencia que ninguna otra
   unidad produce, y que puede fallar de una forma que las demás no detectan.
3. **Valor de la pausa**: la constitución del carril Z reserva al humano el cierre de cada
   unidad y la autorización de la siguiente. Cada frontera cuesta dos decisiones humanas. Una
   frontera que no le ofrece al humano una decisión distinguible no se justifica.

De ese criterio se sigue una consecuencia que este plan aplica deliberadamente: **varias
intervenciones dentro de una unidad no son varias unidades**. Una unidad puede entregarse y
auditarse en varias intervenciones sucesivas, cada una con su commit autoritativo. Partir por
volumen de trabajo multiplicaría decisiones humanas sin agregar poder discriminante.

Resultan cuatro unidades. Se descartaron expresamente estas alternativas:

- **Partir U1 en relevamiento documental y prueba empírica**: el relevamiento solo no termina
  nada. El manifiesto exige evidencia de una integración admitida, no un inventario de
  opciones. Una sub-unidad documental entregaría una afirmación no verificable.
- **Partir U2 por etapas del circuito (recepción / evaluación / publicación / votación)**: la
  propiedad que U2 debe demostrar es exactamente que el recorrido cierra de extremo a extremo.
  Cada trozo por separado es inverificable respecto de esa propiedad, y el humano pagaría tres
  fronteras adicionales sin poder aprobar nada distinguible.
- **Fusionar U2 y U3**: la propiedad de U2 es que el circuito **cierra**; la de U3 es que
  **resiste**. Fallan de modos distintos y con evidencia distinta. Fusionarlas obligaría al
  humano a pagar el endurecimiento antes de poder aprobar un circuito que funciona.
- **Partir U4 en instalación y documentación**: la instalación reproducible se verifica
  precisamente siguiendo la documentación de entrega. Es una sola evidencia.
- **Una unidad separada de portal público o de votación**: ambas pertenecen al recorrido
  mínimo de U2; separarlas rompe la propiedad que U2 demuestra.
- **Una unidad propia para los enlaces de entrada**: el enlace de la audiencia es la puerta de
  la recepción y solo se verifica con el circuito que alimenta (U2). El enlace del creador
  cumple dos funciones con verificaciones distintas: iniciar la operación, verificable apenas
  existe el circuito (U2), y acompañar la instalación, verificable solo sobre el material ya
  terminado (U4). Una unidad propia no tendría una propiedad verificable independiente.

Cada unidad vive en su propio directorio del repositorio de trabajo, junto con su `EVENTO.md`:

```text
unidad-1-viabilidad-ia-contratada/
unidad-2-circuito-minimo/
unidad-3-calidad-controles-votacion/
unidad-4-instalacion-entrega/
```

---

## 3. Unidad 1 — Viabilidad de operación desde la IA contratada

### Objetivo

Resolver, de forma acotada y antes de comprometer la construcción del portal, si el creador
puede operar el sistema desde la IA que ya tiene contratada, mediante una integración admitida
por esa cuenta, con capacidad de obtener propuestas, entregar una evaluación y guardar
resultados, iniciada por una petición breve del creador.

La IA de referencia es ChatGPT. No se afirma compatibilidad con otras IA.

### Por qué es una unidad

Su resultado decide la arquitectura de todo lo demás: la superficie que el sistema debe exponer
(descriptor de acciones, servidor de herramientas, u otra admitida), su modelo de
autenticación, sus límites de tamaño y de tiempo, y su costo. Construir el portal antes de
resolverlo es construir contra una interfaz no comprobada.

### Dependencias

Ninguna previa dentro del trabajo. Depende de la aprobación humana de este plan.

### Contenido y secuencia interna

1. **Relevamiento de mecanismos admitidos**, contra documentación pública autoritativa del
   proveedor, citada con su URL y su fecha de consulta. Se enumeran únicamente los mecanismos
   que el proveedor admite para que la IA contratada invoque un sistema externo, con sus
   requisitos de plan, autenticación, exposición de red, límites y costos declarados.
2. **Sonda mínima local**: un servicio deliberadamente mínimo y descartable que exponga las
   operaciones imprescindibles para el viaje de ida y vuelta —listar propuestas, leer una
   propuesta, guardar un resultado de evaluación— sobre datos sintéticos identificados como
   tales, más el descriptor que el mecanismo relevado exija. La sonda existe para comprobar la
   interfaz, no para ser el sistema: su stack no compromete las decisiones de U2.
3. **Comprobación local de la sonda** por sus propias pruebas, sin intervención de la IA.
4. **Contrato previo de verificación** de la conexión real, propuesto en el `EVENTO.md` de la
   unidad antes de ejecutarla.
5. **Conexión real** desde la cuenta del creador. Requiere cuenta, plan y exposición de red que
   no pertenecen al perímetro delegado; se prevé como necesidad humana material (H-1, H-2).
6. **Resultado**: requisitos, límites, costos y acciones manuales identificados.

### Casos, resultados esperados y condiciones de aceptación

| Caso | Resultado esperado |
|---|---|
| C1.1 Petición breve del creador que obtiene la lista de propuestas | La IA recupera las propuestas sintéticas desde el sistema, sin transferencia manual de archivos |
| C1.2 Petición que obtiene el detalle de una propuesta | La IA recupera el original íntegro y sin datos de contacto |
| C1.3 Petición que guarda un resultado de evaluación | El sistema registra el resultado y lo devuelve al consultarlo de nuevo |
| C1.4 Control negativo: acceso sin autorización válida | El sistema rechaza la operación y la IA no obtiene datos |
| C1.5 Control negativo: petición de un recurso fuera del alcance declarado de la integración | La operación se rechaza o el mecanismo se declara fuera de alcance |

Condiciones de aceptación: C1.1, C1.2 y C1.3 se satisfacen en una misma sesión iniciada por una
petición breve; C1.4 y C1.5 fallan como se espera. Se registran, sin revelar secretos: cuenta y
plan usados, mecanismo, capacidades efectivamente disponibles, límites observados, consumo y
costo, y toda acción manual que el creador debió realizar.

C1.4 y C1.5 son el control negativo exigido por REVOLUTIONS §6.1: sin ellos, un mecanismo que
devuelve datos a cualquiera satisfaría C1.1 a C1.3 por accidente.

### Criterio de terminación

La unidad termina con exactamente uno de estos tres resultados, y con ninguno más:

- **Opción demostrada**: evidencia del viaje completo de lectura y escritura por una
  integración admitida, con requisitos, límites y costos identificados.
- **Incompatibilidad documentada**: evidencia de que ningún mecanismo admitido de la cuenta
  satisface el objetivo. Se eleva la incompatibilidad **antes** de sustituir el modo de
  operación por otro; el constructor no elige por su cuenta el reemplazo.
- **Decisión humana necesaria**: la comprobación exige una cuenta, un permiso, una exposición
  de red o un gasto reservados al humano. Se preserva el checkpoint y se entrega.

Explícitamente **no** son terminaciones: seguir buscando más mecanismos fuera de los relevados
en el paso 1, ampliar la sonda para que haga más de lo imprescindible, ni sustituir la
comprobación real por una simulación. Una simulación no demuestra una integración que el
trabajo afirme entregar funcionando.

### Riesgos propios

- **R1** El plan de la cuenta puede no admitir ningún mecanismo que cumpla el objetivo sin
  transferencia manual repetitiva. Mitigación: es un resultado válido de la unidad, no un
  fracaso; se documenta y se eleva.
- **R2** El mecanismo admitido puede exigir un extremo HTTPS alcanzable públicamente, con costo
  y superficie de exposición. Mitigación: se identifica en el paso 1, antes de construir.
- **R3** El límite de tamaño de respuesta del mecanismo puede no soportar 50–100 propuestas en
  una sola operación. Mitigación: se mide en C1.1 y condiciona el diseño de paginación de U2.

### Intervención humana previsible

H-1 (material) y H-2 (material). Ver §8.

---

## 4. Unidad 2 — Circuito mínimo completo

### Objetivo

Un recorrido completo y delgado, verificable de extremo a extremo, que empieza en los enlaces
de entrada del creador y de la audiencia: definición de criterios, convocatorias delimitadas y
recepción permanente con cortes, recepción por formulario breve con participación directa o
asistida por IA, conservación del original, evaluación asistida por IA con los criterios de
cada ronda, preselección con razones y dudas, invitación a ampliar, segunda evaluación
vinculada al original, publicación autorizada de finalistas y votación.

### Por qué es una unidad

Es la unidad cuya propiedad es que el circuito cierra. Ninguna de sus partes demuestra esa
propiedad por separado, y ninguna otra unidad la vuelve a demostrar.

### Dependencias

Depende del resultado de U1: la interfaz que el sistema expone a la IA del creador, su
autenticación y sus límites determinan la forma del backend. No se inicia sin ese resultado ni
sin la autorización humana correspondiente.

### Contenido

- **Entrada del creador**: un enlace de entrada que el creador entrega a su IA. Contiene las
  instrucciones con las que la IA de referencia inicia la operación del circuito por el
  mecanismo de U1, confirmando primero el acceso efectivamente disponible en la sesión. Su
  función de acompañamiento de la instalación se completa y verifica en U4.
- **Criterios y convocatoria**: perfil habitual del creador y, por convocatoria, pregunta
  concreta, restricciones, criterios de selección, cantidad de seleccionadas y parámetros de
  votación. Revisión previa por el creador de una interpretación de sus criterios y de ejemplos
  de selección explicados, con posibilidad de corregir discrepancias. Los criterios quedan
  fijados para esa ronda de evaluación.
- **Modos de recepción**: convocatorias delimitadas, con su ventana de apertura y cierre, y un
  canal de recepción permanente evaluado por cortes. Ambos modos pueden coexistir. Cada
  propuesta pertenece a un único canal, y cada ronda —cierre de una convocatoria o corte del
  canal permanente— fija su conjunto de propuestas y sus criterios, sin mezclar ventanas ni
  criterios de otra ronda.
- **Recepción y entrada pública**: un enlace público para la audiencia, comprensible
  directamente por una persona y utilizable a través de su propia IA. La guía pública explica
  objetivo, criterios, condiciones, plazos y forma de participación. Formulario breve —qué se
  propone, por qué aporta, un ejemplo o detalle suficiente— con límites de extensión
  justificados y probados. La IA del participante puede ayudar a expresar la propuesta, sin
  inventar evidencia ni sustituir su intención; el envío se realiza siempre por el mismo
  formulario, de modo que participar con IA es opcional y participar sin ella es igualmente
  posible.
- **Transparencia al participante**: antes de enviar, el formulario y la guía informan qué se
  publicará, qué permanece privado y cómo se atribuirán sus aportes. La transparencia no exige
  publicar las propuestas privadas.
- **Conservación**: el original recibido es inmutable; se conserva con su fecha de recepción,
  presentada como recepción en el sistema y no como prueba de autoría universal. Las
  ampliaciones son registros nuevos vinculados, nunca sobrescrituras, y cada uno lleva su
  propio autor y su tipo de relación con el original. Los datos de contacto se guardan
  separados de la información publicable.
- **Evaluación**: aplicación de los criterios de la convocatoria; preselección con razones y
  dudas explícitas; cantidad configurable. El resultado no se presenta como medida objetiva ni
  universal del valor de las ideas.
- **Ampliación**: preguntas específicas a las seleccionadas, con autorización del creador. El
  vínculo entre la respuesta, la propuesta y su autor es verificable por el propio mecanismo de
  invitación y no depende de que el participante copie correctamente un asunto o un código.
- **Segunda evaluación**: conserva el vínculo con el original y explica cómo la ampliación
  afecta la selección.
- **Publicación y votación**: portal consultable de finalistas tras el cierre y la autorización
  del creador, con una lista común sin duplicados. Recomendación de IA, preferencia de audiencia
  y elección del creador se registran y se muestran como señales distinguibles. No se compone un
  cuarto ranking.
- **Operación conversacional**: el circuito implementado se opera desde la IA de referencia por
  el mecanismo demostrado en U1.

### Casos, resultados esperados y condiciones de aceptación

| Caso | Resultado esperado |
|---|---|
| C2.1 Ciclo completo con datos sintéticos: recepción, evaluación, invitación, ampliación, segunda evaluación, publicación autorizada y votación | El ciclo cierra sin intervención fuera de la prevista, y cada paso queda trazable |
| C2.2 Integridad del original tras una ampliación | El texto original es recuperable sin cambios y el vínculo autor–propuesta–ampliación es verificable |
| C2.3 Separación de datos privados y públicos | Ninguna vista publicable ni respuesta a la IA expone datos de contacto |
| C2.4 Publicación sin autorización del creador | La operación se rechaza; nada se publica |
| C2.5 Reintento de una invitación y de una publicación | No se duplican envíos ni entradas publicadas |
| C2.6 Operación conversacional real del circuito desde la IA de referencia | La petición breve del creador recorre el circuito por el mecanismo de U1, declarando cuenta, capacidades y límites probados |
| C2.7 Inicio desde el enlace de entrada del creador | La IA de referencia, recibiendo solo el enlace de entrada, confirma el acceso disponible y lleva al creador a operar el circuito implementado |
| C2.8 Control negativo: sesión sin la integración disponible o sin autorización | La IA declara la limitación y la acción necesaria; no presenta propuestas, evaluaciones ni resultados que no obtuvo del sistema |
| C2.9 Participación directa desde el enlace público, sin IA | Un participante sintético comprende la guía y envía su propuesta por el formulario |
| C2.10 Participación asistida desde el enlace público, con la IA de referencia actuando como IA del participante | La IA explica objetivo, criterios, condiciones, plazos y forma de participación, y ayuda a expresar la propuesta; el envío se hace por el mismo formulario |
| C2.11 Control negativo de intención y evidencia: participante sintético con una idea breve sin ejemplo ni datos | La asistencia pregunta o deja constancia de lo faltante; el texto resultante conserva la idea propuesta y no agrega datos, cifras, fuentes, experiencias ni ejemplos que el participante no aportó |
| C2.12 Coexistencia de una convocatoria delimitada abierta y del canal permanente | Cada propuesta pertenece a un solo canal; cada ronda se evalúa solo con sus propias propuestas y criterios; una propuesta permanente recibida después de un corte entra en el corte siguiente |
| C2.13 Control negativo de ventana: envío a una convocatoria cerrada | Se rechaza, indicando el canal permanente si está activo; nunca se reasigna en silencio a otro canal |
| C2.14 Transparencia previa al envío | El formulario y la guía muestran, antes de enviar, qué se publica, qué queda privado y cómo se atribuye; los campos declarados publicables coinciden exactamente con los que expone la vista pública |
| C2.15 Fecha de recepción en las superficies del sistema | Toda superficie que muestra la fecha la presenta como recepción en el sistema; ninguna afirma autoría original, originalidad ni prioridad a partir de ella |

Condiciones de aceptación: C2.1, C2.2, C2.3, C2.6, C2.7, C2.9, C2.10, C2.12, C2.14 y C2.15 se
satisfacen; C2.4, C2.5, C2.8, C2.11 y C2.13 fallan o se neutralizan como se espera. Todos los
datos son sintéticos y quedan identificados como tales. C2.10 y C2.11 usan la IA de referencia
en el papel de IA del participante y no demuestran compatibilidad con otras IA.

C2.4, C2.5, C2.8, C2.11 y C2.13 son controles negativos: una publicación que siempre publica, un
reintento que siempre reenvía, una IA que responde aunque no haya leído nada, una asistencia
que completa lo que falta y un formulario que acepta cualquier envío satisfarían los casos
positivos sin demostrar nada. En C2.14, una divergencia en cualquier dirección entre lo
anunciado y lo expuesto hace fallar el caso.

### Criterio de terminación

El ciclo completo se ejecuta con datos sintéticos y con evidencia preservada de cada caso; los
controles negativos se comportan como se espera; la operación conversacional se ejercita
realmente por el mecanismo demostrado en U1 —o, si U1 terminó en incompatibilidad documentada,
la unidad no se inicia y la sustitución del modo de operación queda como decisión humana.

### Riesgos propios

- **R4** Alcance creciente: cada parte del circuito admite profundidad indefinida. Mitigación:
  U2 entrega la versión más delgada que hace cerrar el ciclo; la profundidad pertenece a U3.
- **R5** El vínculo verificable de la ampliación puede requerir enviar comunicaciones reales.
  Mitigación: el mecanismo se diseña sobre un enlace con testigo emitido por el sistema, de modo
  que el envío real sea una decisión humana separada y no una condición de la verificación.
- **R6** La evaluación depende de un modelo cuyo costo y elección están reservados al humano.
  Mitigación: la evaluación se implementa detrás de una frontera que admite un ejecutor
  sintético determinista para las pruebas locales, sin que eso sustituya la prueba real.
- **R12** La IA del creador, sin acceso efectivo al sistema, puede simular haber leído o
  evaluado propuestas. Mitigación: las instrucciones de entrada exigen confirmar el acceso
  antes de operar y prohíben presentar resultados no obtenidos del sistema; C2.8 lo ejercita.
- **R13** La asistencia de IA al participante puede embellecer la propuesta o completarla con
  evidencia inventada, y así favorecer además la buena redacción en la evaluación. Mitigación:
  C2.11 en U2 y la revisión de sesgos de U3.

### Intervención humana previsible

H-2, H-3 y H-4. Ver §8.

---

## 5. Unidad 3 — Calidad de selección, controles y votación configurable

### Objetivo

Endurecer el recorrido ya cerrado: calidad y explicabilidad de la selección, tratamiento de
contenido no confiable, controles de votación y su configuración, y comportamiento bajo el
volumen inicial previsto.

### Por qué es una unidad

Su propiedad es que el circuito resiste. Se ejercita con casos que U2 no contiene —descartadas,
duplicadas, ambiguas, adversariales, volumen, error y reintento— y falla de modos que la
verificación de U2 no detecta.

### Dependencias

Depende de U2: no se puede endurecer un recorrido que todavía no cierra.

### Contenido

- **Calidad de selección**: comparación de la evaluación con los ejemplos revisados por el
  creador; revisión de las no seleccionadas para detectar omisiones y sesgos; agrupación de
  semejantes que no borra originales, participantes ni diferencias sustantivas.
- **Sesgos**: evaluación explícita del riesgo de favorecer buena redacción, ideas
  convencionales, orden de presentación o textos preparados para influir en el evaluador, con
  el resultado documentado y sus límites declarados.
- **Contenido no confiable**: las propuestas y los enlaces aportados por participantes se tratan
  como datos, nunca como instrucciones; no alteran el comportamiento del evaluador, no acceden a
  datos privados y no autorizan acciones.
- **Votación configurable**: máximo de votos por participante por convocatoria, con tres como
  valor predeterminado; un voto por participante y por propuesta hasta ese máximo; lista común
  sin duplicados; fechas de apertura y cierre; visibilidad de resultados durante o después del
  cierre. Las condiciones se fijan antes de abrir la votación y se mantienen durante esa ronda.
  Ninguna configuración permite publicar propuestas privadas sin la autorización prevista ni
  modifica las reglas de atribución. Los controles empleados y sus límites se explican, sin
  prometer identidad única de personas.
- **Atribución y colaboración**: la colaboración de terceros es una opción por convocatoria,
  deshabilitada por defecto. Habilitada, una mejora de otra persona se registra y se muestra
  como contribución diferenciada, con su propio autor y vinculada al original, distinta del
  original y de las ampliaciones de su autor. Ninguna contribución modifica el original ni su
  atribución.
- **Similitud y redacción**: la similitud detectada por IA se registra y se presenta como señal
  para revisión, nunca como prueba de copia, y no descarta ni fusiona propuestas por sí sola.
  Una mejor redacción de una idea existente no la convierte por sí sola en una idea distinta
  ni le otorga atribución preferente.
- **Descubrimiento de omitidas**: incorporación manual por el creador y un mecanismo explícito
  de rotación o muestreo, justificado y proporcional al uso inicial.
- **Presentación durante un vivo**: la vista de finalistas apta para mostrarse en streaming.
- **Volumen y recuperación**: comportamiento con 50–100 propuestas breves como escenario
  inicial —no como predicción de participación ni como límite universal—, tiempos, consumo y
  recuperación de errores sin pérdida de datos ni duplicación de acciones. Un límite de
  volumen o de gasto configurable por ronda, para que el creador acote el consumo.

### Casos, resultados esperados y condiciones de aceptación

| Caso | Resultado esperado |
|---|---|
| C3.1 Propuestas descartadas, duplicadas y ambiguas | Se clasifican con razones; los originales y los participantes se conservan |
| C3.2 Propuesta adversarial con instrucciones embebidas y enlace hostil | El evaluador no obedece la instrucción, no accede a datos privados y no ejecuta la acción pedida |
| C3.3 Comparación de la selección con los ejemplos revisados por el creador | Las discrepancias se exponen y se pueden corregir recalibrando |
| C3.4 Cambio de criterios durante la evaluación, en una convocatoria y en un corte del canal permanente | Todas las propuestas de esa ronda se reevalúan bajo el mismo criterio |
| C3.5 Voto repetido sobre la misma propuesta y exceso del máximo configurado | Se rechazan; el conteo no se altera |
| C3.6 Propuesta presente en más de una lista | Aporta un solo voto |
| C3.7 Volumen de 50–100 propuestas sintéticas | Se registran tiempos y consumo; el circuito completa la evaluación |
| C3.8 Interrupción y reintento durante una operación de volumen | No hay pérdida de datos ni acciones duplicadas |
| C3.9 Contribución de un tercero con la colaboración habilitada | Queda registrada y visible como contribución diferenciada, con su propio autor, vinculada al original y distinta de las ampliaciones del autor |
| C3.10 Control negativo: contribución de un tercero con la colaboración deshabilitada, e intento de alterar el original mediante una contribución | La primera se rechaza; en ninguna configuración el original ni su atribución cambian |
| C3.11 Dos propuestas de autores distintos con similitud alta | Ambas se conservan con sus autores y fechas, se marcan para revisión, no se descartan ni fusionan automáticamente, y ninguna superficie las presenta como copia |
| C3.12 La misma idea en una versión pobremente redactada y en otra pulida | Se agrupan como la misma idea y se conservan ambas; la versión pulida no se presenta como idea distinta ni recibe atribución preferente por la redacción |
| C3.13 Control negativo de configuración: cambios de visibilidad, fechas o máximo de votos antes y después de abrir la ronda | Antes de abrir, ningún cambio publica una propuesta no autorizada ni altera la atribución; después de abrir, los cambios se rechazan |
| C3.14 Límite de volumen o de gasto configurado por debajo del total de la ronda | La evaluación se detiene en el límite y lo declara; las propuestas restantes se conservan sin evaluar y no se presentan como evaluadas |

Condiciones de aceptación: C3.1, C3.3, C3.4, C3.7, C3.9, C3.11, C3.12 y C3.14 se satisfacen con
evidencia preservada; C3.2, C3.5, C3.6, C3.8, C3.10 y C3.13 se comportan como controles
negativos y fallan como se espera. Los límites de cada control se declaran expresamente: no se
promete ausencia de fraude ni identidad única de personas.

### Criterio de terminación

Todos los casos ejercitados con evidencia preservada, el resultado de la revisión de sesgos
documentado con sus límites, y los controles de votación descritos junto con lo que no
garantizan.

### Riesgos propios

- **R7** Un control de votación fuerte puede volver la participación incómoda. Mitigación: el
  control se elige por su costo para el participante y su límite se declara, en lugar de
  prometer una garantía que no puede sostenerse.
- **R8** La detección de similitud puede tratarse como prueba de copia. Mitigación: se registra
  y se presenta como señal para revisión humana, nunca como conclusión.
- **R9** El volumen medido localmente no demuestra el comportamiento en el entorno real.
  Mitigación: se declara explícitamente como limitación de la evidencia.

### Intervención humana previsible

H-4. Ver §8.

---

## 6. Unidad 4 — Instalación reproducible, entrega y piloto

### Objetivo

Que otra persona pueda instalar y operar el kit siguiendo las instrucciones, y que la entrega
declare con precisión qué está demostrado y qué no.

### Por qué es una unidad

Su verificación es cualitativamente distinta: se ejerce en un entorno de prueba limpio, sobre
el material ya terminado, y su fallo típico —una instrucción que solo funciona en la máquina de
quien la escribió— no lo detecta ninguna verificación anterior.

### Dependencias

Depende de U2 y U3: se instala y se documenta lo que ya está construido y endurecido.

### Contenido

- Enlace de entrada del creador completado como guía de instalación asistida por IA: la IA de
  referencia, iniciada desde ese enlace, determina los conocimientos, herramientas y permisos
  del creador antes de proponer pasos, y adapta el acompañamiento a ellos. Pasos mínimos y
  operación conversacional priorizados; cuentas, permisos, servicios, límites y acciones
  manuales documentados. Ante una capacidad ausente, el acompañamiento la declara junto con la
  acción humana necesaria, en lugar de proponer un rodeo no admitido.
- Guía de operación del creador e instrucciones públicas de participación, incluida la
  explicación al participante de qué se publica, cómo se atribuyen sus aportes, cómo se trata
  la similitud, por qué una mejor redacción no crea por sí sola una idea distinta, y qué
  demuestra y qué no la fecha de recepción.
- Ejemplos y configuración de ejemplo reproducibles.
- Documentación de límites y costos, separando costos de IA, de alojamiento y de
  comunicaciones, con el consumo del caso probado y los límites de volumen o gasto disponibles.
- Procedimiento del piloto posterior: registro de tiempo de revisión, utilidad percibida,
  omisiones, costos y dificultades de instalación.
- Declaración de alcance de la evidencia: la utilidad con audiencia real y la instalación por
  una persona externa sin conocimientos técnicos no están demostradas hasta realizar esas
  pruebas, y los resultados técnicos no las sustituyen.
- Credenciales fuera del código y de la documentación distribuida.

### Casos, resultados esperados y condiciones de aceptación

| Caso | Resultado esperado |
|---|---|
| C4.1 Instalación en un entorno de prueba limpio siguiendo únicamente las instrucciones | El sistema queda operable; se registran obstáculos y pasos humanos encontrados |
| C4.2 Ciclo mínimo ejecutado sobre la instalación resultante | El circuito cierra en la instalación nueva |
| C4.3 Revisión del material distribuible en busca de secretos | No hay credenciales en el código ni en la documentación |
| C4.4 Instrucción deliberadamente incompleta o dependiente del entorno de origen | El procedimiento de instalación la detecta en lugar de completarla implícitamente |
| C4.5 Acompañamiento adaptado desde el enlace de entrada, con perfiles sintéticos de creador que difieren en conocimientos, herramientas y permisos —al menos: sin conocimientos técnicos y con la capacidad requerida en la cuenta; sin esa capacidad; con conocimientos técnicos— | La IA de referencia determina esas condiciones antes de proponer pasos, y en cada perfil ofrece solo pasos ejecutables con ellas; el acompañamiento difiere entre perfiles de forma observable |
| C4.6 Control negativo del acompañamiento: perfil sin la capacidad requerida | Declara la incompatibilidad y la acción humana necesaria; no propone un rodeo no admitido ni afirma una instalación exitosa; en ningún perfil pide pegar secretos en la conversación |
| C4.7 Documentación de atribución y transparencia entregada | Explica qué se publica, cómo se atribuye, y los límites de similitud, redacción y fecha de recepción, sin ninguna afirmación de autoría incompatible con esas reglas |

Condiciones de aceptación: C4.1, C4.2, C4.3, C4.5 y C4.7 se satisfacen; C4.4 y C4.6 se
comportan como controles negativos. El entorno de prueba limpio y su grado de aislamiento se
declaran, junto con lo que ese entorno no representa.

C4.5 y C4.6 son conversaciones reales con la IA de referencia sobre perfiles sintéticos
declarados como tales. Demuestran el comportamiento del acompañamiento, no que una persona
externa sin conocimientos técnicos logre instalar el kit: esa validación pertenece al piloto
posterior y no es condición de cierre.

### Criterio de terminación

Instalación reproducida con su registro de obstáculos, ciclo mínimo ejecutado sobre ella,
material distribuible sin secretos, y documentación de entrega y de piloto completa, incluida
la declaración de lo no demostrado.

### Riesgos propios

- **R10** Un entorno de prueba en la misma máquina puede heredar dependencias ya instaladas y
  ocultar un requisito. Mitigación: se declara el aislamiento efectivamente logrado y sus
  límites, en lugar de afirmar reproducibilidad universal.
- **R11** La publicación del kit exige condiciones de uso y licencia. Mitigación: se prevé como
  decisión humana previa a publicar, no como decisión técnica.

### Intervención humana previsible

H-5. Ver §8.

---

## 7. Secuencia, dependencias y decisiones técnicas

### Dependencias

```text
U1  viabilidad de operación desde la IA contratada
      |  su resultado determina la interfaz, la autenticación y los límites del sistema
      v
U2  circuito mínimo completo
      |  su recorrido cerrado es lo que U3 endurece
      v
U3  calidad de selección, controles y votación configurable
      |  su material terminado es lo que U4 instala y documenta
      v
U4  instalación reproducible, entrega y piloto
```

La secuencia es estrictamente lineal: ninguna unidad posterior puede ejecutarse con evidencia
válida antes de la anterior. Entre unidades se interpone la decisión humana reservada por la
constitución del carril Z.

### Decisiones técnicas que este plan toma

Son reversibles, no congelan tecnología y protegen propiedades exigidas por el manifiesto:

1. Los datos de prueba son sintéticos y quedan identificados como tales en el propio dato, no
   solo en la documentación.
2. El original recibido es inmutable. Toda ampliación o mejora es un registro nuevo vinculado.
3. Los datos de contacto viven separados de la información publicable desde la primera versión,
   no como un filtrado posterior de presentación.
4. Las propuestas y los enlaces de participantes se tratan como datos en todo punto donde
   intervenga un modelo: la instrucción del sistema y el contenido del participante nunca
   comparten el mismo canal de autoridad, y los enlaces aportados no se recuperan durante la
   evaluación.
5. Toda operación que publique o envíe algo es idempotente respecto de un identificador de
   operación, para que un reintento no duplique acciones.
6. La recomendación de IA, la preferencia de audiencia y la elección del creador se almacenan y
   se presentan como tres señales separadas. No se compone un cuarto ranking.
7. El vínculo de una ampliación con su propuesta y su autor lo emite el sistema y es
   verificable por sí mismo; no depende de la correcta transcripción por parte del participante.
8. La evaluación se implementa detrás de una frontera que admite un ejecutor determinista para
   pruebas locales. Esa frontera no convierte una simulación en prueba de la integración real.
9. Ningún secreto entra en Git, en la documentación distribuida ni en el sobre de pase.
10. Operar exige acceso efectivo: las instrucciones del enlace de entrada obligan a la IA del
    creador a confirmar el acceso real antes de operar y le prohíben presentar propuestas,
    evaluaciones o resultados que no obtuvo del sistema.
11. La IA del participante asiste la redacción; el envío se hace siempre por el mismo
    formulario. El sistema no requiere integración con la IA del participante, y lo que
    almacena como original es lo que el participante envía.
12. Toda propuesta pertenece a un único canal de recepción: una convocatoria delimitada o el
    canal permanente. La unidad de evaluación es la ronda —cierre de convocatoria o corte del
    canal permanente—, y cada ronda fija su conjunto de propuestas y sus criterios.
13. Todo registro vinculado a una propuesta lleva su propio autor y su tipo de relación
    —ampliación del autor o contribución de un tercero—, de modo que la atribución no pueda
    colapsar. La colaboración de terceros está deshabilitada por defecto.
14. Los campos publicables se declaran en un único lugar, que alimenta el aviso al
    participante y delimita la vista pública.

### Decisiones técnicas deliberadamente diferidas

No se congelan sin evidencia. Cada una indica qué evidencia la decide:

| Decisión | Evidencia que la decide |
|---|---|
| Mecanismo de integración con la IA contratada | Resultado de U1 |
| Lenguaje, framework y persistencia del backend | Requisitos de la interfaz demostrada en U1 |
| Forma de exposición pública del sistema | Requisitos del mecanismo de U1 y decisión humana de costo |
| Modelo de evaluación del producto y su costo | Decisión humana; medición del caso probado |
| Canal de invitación a ampliar | Diseño de U2 y decisión humana sobre comunicaciones reales |

### Mapa de las verificaciones del manifiesto

| Verificación del manifiesto | Unidad que la produce |
|---|---|
| 1. Ciclo completo | U2 |
| 2. Integridad de originales, vínculos y separación privado/público | U2 |
| 3. Aplicación de criterios; descartadas, duplicadas, ambiguas y adversariales | U3 |
| 4. Acceso autorizado desde la IA de referencia y operación conversacional real | mecanismo en U1; operación del circuito implementado en U2 |
| 5. Instalación reproducible en entorno limpio | U4 |
| 6. Volumen, tiempos, consumo y recuperación de errores | U3 |

### Cobertura del resultado observable y del alcance funcional

Cada exigencia del manifiesto queda localizada en una unidad y en un caso que la ejercita, o en
una decisión técnica que la protege. Donde una exigencia tiene comportamiento implementado y
superficie de documentación o de experiencia, se indican ambas.

| Exigencia del manifiesto | Comportamiento implementado | Documentación o experiencia | Casos |
|---|---|---|---|
| Circuito completo demostrado con datos de prueba | U2 | U4 | C2.1, C4.2 |
| Enlace de entrada del creador con acompañamiento adaptado | U2 (inicio de operación) | U4 (instalación adaptada) | C2.7, C2.8, C4.5, C4.6 |
| Operación por petición breve, con acceso autorizado y devolución de resultados, sin transferencia manual repetitiva | U1, U2 | U4 | C1.1–C1.5, C2.6 |
| Acciones humanas y capacidades efectivas de la integración probada | U1 | U4 | C1.1–C1.3, C4.1 |
| Enlace de audiencia, directo y a través de su IA, con IA opcional | U2 | U2, U4 | C2.9, C2.10 |
| La guía ayuda sin inventar evidencia ni sustituir intención | U2 | U2 | C2.11 |
| Perfil habitual y criterios por convocatoria; interpretación y ejemplos revisados | U2 | U2 | C2.1, C3.3 |
| Criterios conservados por ronda; reevaluación si cambian | U2, U3 | — | C3.4 |
| Recepción permanente con cortes y convocatorias delimitadas | U2 | U2 | C2.12, C2.13 |
| Formulario breve con límites de extensión justificados y probados | U2 | U2 | C2.1, C2.9 |
| Privacidad durante la selección; original, fecha y ampliaciones; contactos separados | U2 | — | C2.2, C2.3 |
| Evaluación con razones y dudas, cantidad configurable, sin medida objetiva | U2 | U4 | C2.1 |
| Revisión de no seleccionadas; agrupación sin borrar originales | U3 | — | C3.1, C3.3 |
| Ampliación con vínculo verificable y segunda evaluación vinculada | U2 | — | C2.1, C2.2 |
| Publicación autorizada, portal consultable y presentación para vivo | U2, U3 | — | C2.1, C2.4 |
| Tres señales distinguibles, sin cuarto ranking; lista común sin duplicados | U2, U3 | U4 | C2.1, C3.6 |
| Votación configurable, fijada antes de abrir, sin publicar privadas ni alterar atribución | U3 | U4 | C3.5, C3.6, C3.13 |
| Incorporación de omitidas y rotación o muestreo | U3 | U4 | C3.1 |
| Informar al participante qué se publica y cómo se atribuye | U2 | U2, U4 | C2.14, C4.7 |
| Contribuciones de terceros diferenciadas, cuando se habilite la colaboración | U3 | U4 | C3.9, C3.10 |
| Similitud como señal y no como prueba de copia | U3 | U4 | C3.11, C4.7 |
| Mejor redacción no crea por sí sola una idea distinta | U3 | U4 | C3.12, C4.7 |
| Fecha de recepción no demuestra autoría universal | U2 | U2, U4 | C2.15, C4.7 |
| Contenido de participantes no confiable | U2, U3 | — | C3.2 |
| Sin envíos repetidos ni publicaciones duplicadas al reintentar | U2, U3 | — | C2.5, C3.8 |
| Costos separados, límites de volumen o gasto, consumo demostrado | U3 | U4 | C3.7, C3.14 |
| Instalación guiada reproducible; credenciales fuera del material distribuido | U4 | U4 | C4.1, C4.3, C4.4 |
| Procedimiento de piloto y declaración de lo no demostrado | — | U4 | criterio de terminación de U4 |

---

## 8. Intervenciones humanas previsibles

Anticiparlas permite planificar; no las habilita por adelantado. Cuando llegue el momento, el
auditor comprueba primero si siguen siendo necesarias: pueden haber dejado de serlo porque la
capacidad ya fue delegada, el acceso ya fue aprovisionado o el diseño evitó la dependencia.

| Id | Unidad | Necesidad | Tipo previsto |
|---|---|---|---|
| H-1 | U1 | Cuenta y plan de la IA de referencia con la capacidad de crear la integración relevada, y ejecución de la conexión en esa cuenta | material |
| H-2 | U1 y U2 | Exposición de red alcanzable por la integración y por los enlaces de entrada del creador y de la audiencia, con su costo y su superficie | material |
| H-3 | U2 | Autorización de envío de comunicaciones reales, si el diseño de la invitación no logra evitar la dependencia | material |
| H-4 | U2 y U3 | Elección del modelo de evaluación del producto y autorización del gasto asociado | no material |
| H-5 | U4 | Condiciones de uso, licencia y publicación del kit | no material |
| H-6 | todas | Cierre de cada unidad y autorización para iniciar la siguiente | no material |

Además, la incompatibilidad documentada prevista como terminación de U1 es una decisión humana
en cuanto se proponga sustituir el modo de operación: el constructor la eleva, no la sustituye.

Cuando una de estas necesidades sea material, se preserva `<unidad>/CHECKPOINT_HUMANO.md`
autocontenido conforme a REVOLUTIONS §7.4, y la intervención se cierra normalmente.

---

## 9. Riesgos transversales

- **RT-1 Evidencia local presentada como prueba de una propiedad real.** Un resultado local no
  demuestra lo que solo puede verificarse en un entorno real, y decirlo es parte de cada
  entrega.
- **RT-2 Simulación presentada como integración.** Una simulación no sustituye la prueba de una
  integración que el trabajo afirme entregar funcionando. Los datos sintéticos y las
  simulaciones se identifican como tales.
- **RT-3 Deriva hacia una plataforma comercial centralizada.** Está excluida por el manifiesto.
  Cada mecanismo nuevo debe justificar qué propiedad exigida protege.
- **RT-4 Presentar el ranking como calidad objetiva.** Excluido: el resultado distingue señales
  y no promete una medida universal del valor de las ideas.
- **RT-5 Exposición de contactos o publicación prematura.** Se ataca por diseño en U2 y se
  ejercita con controles negativos en U2 y U3.
- **RT-6 Concurrencia y drift sobre recursos externos.** Cuando una decisión dependa del estado
  real de un servicio, se comprueba en el punto de uso; si contradice lo esperado, se detiene la
  operación dependiente.

---

## 10. Lo que este plan no hace

No fija la cantidad de unidades por simetría con la orientación del manifiesto: las cuatro
resultan del criterio de §2 y cada una se justifica por su dependencia y su verificación
propias.

No congela tecnologías antes de la evidencia que las decide. No autoriza ninguna unidad: el
plan requiere auditoría y aprobación humana antes de ejecutarlas. No sustituye los contratos
previos de verificación de cada corrida. No promete compatibilidad con otras IA, ausencia de
fraude, originalidad absoluta, ni la validación con audiencia real, que corresponde al piloto
posterior a cargo del humano.
