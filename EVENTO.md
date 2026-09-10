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
