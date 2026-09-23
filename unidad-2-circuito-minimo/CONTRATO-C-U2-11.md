# CONTRATO PREVIO DE VERIFICACIÓN — C-U2-11

## Estado, autoridad y procedencia

`C-U2-11` es una propuesta no ejecutable del CONSTRUCTOR para un sucesor separado, preparada en atención a `INCOMING_TURN_ID=162` y al incidente auditor `1ddaa82eb668f0d09f1d99835c6e0d3b97ef3264`. Se propone sobre `BASE_WORK_SHA=ce89a58c0862abced634224dea1dc42a27505b6a`. Las identidades congeladas de C-U2-10 que motivan el límite histórico son `CONTRACT_BLOB_SHA=2e96c72aaf0b18cc67fccba11282f545d4025d1b` y `CHECKPOINT_BLOB_SHA=709595ae1cd12a46d3d432d9b6fddc79c4a596c2`; C-U2-10 fue auditado en `e937a00dc0ec6cea427c5031971873e255281791`.

Esta intervención propone solo el remedio documental para una inspección C0 futura, única y discriminante. No congela identidades finales, no inicia handshake y no autoriza UI, inspección, captura, gate, P0, C0, P1, instalación, conexión, desconexión, eliminación, cambios de configuración, ejecución de apps/servicios ni cambios de entorno. Las identidades de contrato/checkpoint deberán ser fijadas posteriormente por el AUDITOR. Toda ejecución requiere una H-2 y autorización humanas nuevas y explícitas ligadas a esas identidades, además de los sobres del AUDITOR que el protocolo requiera.

## Incidente que esta propuesta corrige

En C-U2-10, la única inspección visual autorizada fue consumida, pero no acreditada: la página «Personal > Created by me» mostró las filas `Sonda propuestas U1`, `Sonda propuestas U1 v2` y `Circuito propuestas C-U2-5`, cada una acompañada por `+`. No se hicieron clics ni cambios de estado. No se guardaron PNG ni matriz local. El significado de `+` provino solo de una explicación humana previa; la interfaz observada no expuso tooltip ni etiqueta accesible que probara esa interpretación. El AUDITOR consideró ambiguo el resultado. No se permite repetir ni reconstruir aquella inspección, ni crear evidencia retroactiva para C-U2-10.

## Objetivo y alcance sucesor

El único objetivo propuesto para C-U2-11 es una nueva observación visual que determine, app por app, si las definiciones conocidas del circuito están efectivamente desconectadas/no instaladas, y que conserve evidencia durable y legible para auditoría. Debe discriminar el estado mediante texto explícito de la UI asociado a la app exacta; ni la presencia del glifo `+`, ni la ausencia de una app de una lista, ni la afirmación humana anterior bastan por sí solas.

El alcance de C-U2-11 termina inmediatamente después de completar (o detener) esa única inspección y preservar la matriz/capturas aprobadas. No incluye remediación de estado, ejecución de P1 ni ninguna otra actividad material. El gate y P0 de C-U2-10 son antecedentes históricos, no autorizaciones operativas heredables. C-U2-11 no los necesita ni los reutiliza para proponer o, si se autoriza más adelante, ejecutar su verificación visual C0 acotada. Cualquier paso posterior requerirá una propuesta separada, auditoría y autorización humana propias.

## Candidato, propiedad y límites

| Campo | Propuesta |
|---|---|
| Candidato base | `ce89a58c0862abced634224dea1dc42a27505b6a` |
| Propiedad | Estado instalado/conectado, observado explícitamente para cada app identificada como perteneciente al circuito |
| Entorno | Interfaz de cuenta personal de ChatGPT, en la sección donde la persona pueda abrir el estado/detalle de cada app; la ruta exacta de UI queda condicionada a lo visible en la futura ejecución autorizada |
| Fuente primaria | Texto explícito, visible en la interfaz y asociado inequívocamente al nombre exacto de cada app |
| Captura | Capturas PNG secuenciales, sin editar, operadas y guardadas por la persona en el namespace nuevo; matriz append-only con transcripción literal y referencia a cada PNG |
| Tamaño de muestra | Una inspección, una sola pasada por cada app identificada; cero reintentos |
| Unidad de evidencia | `unidad-2-circuito-minimo/evidencia-c-u2-11/` |
| Cierre | Detenerse tras la matriz y PNG, y devolver las identidades/resultados al AUDITOR; no continuar a P1 |

La lista mínima de objetivos es `Sonda propuestas U1`, `Sonda propuestas U1 v2` y `Circuito propuestas C-U2-5`. Se incluirá cualquier otra definición que la futura persona identifique con certeza como perteneciente al circuito. Si la relación de una app con el circuito no es inequívoca, no se la clasifica por conjetura: se detiene la inspección y se devuelve la incertidumbre al AUDITOR.

## Preflight obligatorio de persistencia — antes de abrir la UI de apps

La ejecución futura no comienza examinando apps. Primero, en una página neutral que no sea la lista ni el detalle de ninguna app del circuito, la persona debe demostrar que dispone de un flujo local de guardado PNG utilizable y que puede leer de vuelta el archivo en el destino propuesto. El método propuesto es una captura de pantalla de Windows operada por la persona (`Win+Shift+S` o herramienta equivalente ya disponible), pegada en Paint y guardada explícitamente como PNG. No requiere instalación ni cambio de configuración. La persona vuelve a abrir el PNG guardado desde la ruta y comprueba que se visualiza; se registra ruta, nombre, tamaño no nulo y resultado de lectura en una nota de preflight.

El destino propuesto es `unidad-2-circuito-minimo/evidencia-c-u2-11/preflight/guardado-png-prueba.png`, con nota `unidad-2-circuito-minimo/evidencia-c-u2-11/preflight/resultado.md`. Estos son artefactos futuros, no se crean en esta propuesta. El preflight no debe contener nombres, configuración ni estados de apps del circuito y no cuenta como evidencia de C0.

El preflight pasa únicamente si la persona crea el PNG en ese destino, lo reabre desde disco y confirma que no está vacío y es legible, sin instalar software ni modificar el entorno. Si Paint, el guardado en la ruta, la reapertura, la lectura o la escritura no están disponibles, falla o no puede demostrarse con certeza, no se abre la UI de apps: se detiene antes de consumir la inspección única, se documenta la limitación sin fabricar prueba, y se requiere nueva intervención humana / decisión auditora. Este contrato no afirma que la capacidad del capturador CUA ni ninguna otra herramienta de captura/guardado esté verificada.

## Método discriminante propuesto para la única inspección C0

Solo después de que un AUDITOR congele contrato y checkpoint y se presenten H-2/autorización humana nuevas más los sobres requeridos, la persona:

1. Confirma que el preflight PNG descrito arriba pasó y que su artefacto puede leerse en el destino exacto.
2. Abre la lista pertinente y localiza, sin pulsar botones de acción, cada app objetivo por nombre exacto.
3. Para cada objetivo, usa únicamente una navegación de lectura a su página/detalle/estado si la UI la ofrece sin instalar, conectar, desconectar, eliminar o alterar configuración. El panel debe mostrar simultáneamente el nombre exacto de esa app y una señal textual explícita de estado. Una señal admisible de desconexión/no instalación será texto inequívoco asociado al nombre, por ejemplo una acción visible `Instalar complemento` o `Agregar`/`Conectar` cuyo texto completo y contexto indiquen explícitamente la acción y la app a la que corresponde. La frase real debe copiarse literalmente; los ejemplos no afirman que esa UI exista.
4. No hace clic en `+`, `Instalar`, `Agregar`, `Conectar`, `Desconectar`, `Eliminar`, autorización ni controles de configuración. No confirma ni inicia ninguna transición. Si entrar a una vista pudiera producir un cambio de estado, no entra.
5. Captura cada vista relevante en secuencia como PNG original, sin recorte, anotación, composición, edición ni sustitución. Cada imagen debe mostrar simultáneamente el nombre exacto y el texto de estado que se invoca como prueba. Guarda, como mínimo, `c0-estado-apps-01.png`, `c0-estado-apps-02.png`, etc. en `evidencia-c-u2-11/`, con numeración consecutiva, sin huecos ni reutilización. Una imagen puede cubrir más de una app solo si cada nombre exacto y su señal completa son legibles en el mismo PNG.
6. Completa `evidencia-c-u2-11/c0-matriz-estados.md` con una fila por app: nombre exacto, ubicación/ruta de UI observada, texto literal, contexto que lo vincula a esa app, interpretación limitada, nombre de PNG que muestra simultáneamente nombre y estado, resultado y cualquier incertidumbre. Registra además secuencia y hora local de observación; no añadas secretos ni datos personales.
7. Se detiene inmediatamente tras guardar las capturas y matriz y verifica solo que los archivos esperados existen, se pueden abrir, y el conjunto de nombres/capturas está completo. No hace más navegación de auditoría, ni inicia otros pasos.

La propiedad a inferir se considera positiva solo cuando la señal textual visible es explícita e inequívoca y está ligada en pantalla a la app exacta. Las expresiones de ejemplo son criterios candidatos, no hechos verificados sobre la UI actual. La validez final de la evidencia corresponde al AUDITOR.

## Criterios de aceptación, fallo y limitaciones

**Aceptación propuesta:** el preflight previo demuestra el flujo de guardado PNG; existe exactamente una pasada de inspección; todas las apps mínimas y las adicionales inequívocas tienen una fila y PNG legible; cada PNG muestra nombre exacto y señal textual explícita de no instalación/no conexión; no se accionó ningún control de cambio de estado; y la persona se detuvo al finalizar. Aun cumpliendo esos criterios, el resultado requiere veredicto auditor y no se autoacredita.

**Fallo / no acreditación:** preflight no demostrado; no hay una vista de estado apropiada; señal ausente o ambigua; aparece solamente `+`, botón sin etiqueta, entrada ausente o lista vacía; la señal no se liga a la app exacta; el estado aparece instalado/conectado; afiliación incierta; nombre o señal ilegibles; PNG ausente/ilegible/editado; matriz incompleta; o se produce cualquier acción/modificación no autorizada. En cualquiera de esos casos se detiene la única inspección, registra lo observado sin interpretaciones especulativas y devuelve `C0_NO_ACREDITADO` al AUDITOR. No repite, corrige, reemplaza, completa post hoc ni intenta obtener otra captura mediante una segunda inspección.

**Límites:** la evidencia es una observación de interfaz en una cuenta, en un instante y para las apps enumeradas. No prueba estados de otras cuentas, cambios posteriores ni aplicaciones de afiliación desconocida. Capturas demuestran lo que la interfaz mostró, no el estado interno del proveedor. Ni la semántica de controles de UI ni la disponibilidad del flujo de guardado están verificados al redactar esta propuesta.

## Prohibiciones y regla de detención

La futura autorización, si se concede, abarca solo preflight neutral y una inspección C0 de lectura con persistencia de evidencia. Prohíbe instalar, conectar, reconectar, desconectar, eliminar, autorizar, cambiar configuraciones, pulsar acciones con efectos, modificar entorno/dependencias, ejecutar app/servicio, abrir túnel, ejecutar gate/P0/P1 o realizar pasos posteriores. El preflight fallido detiene antes de abrir la lista de apps. Todo estado indeterminado, UI ambigua o guardado fallido detiene el intento. No hay reintento dentro de C-U2-11. Una nueva observación exigiría sucesor separado, nueva revisión, nuevas identidades y nueva autorización humana.

## Intervenciones humanas previsibles y secuencia de autoridad

1. El AUDITOR revisa esta propuesta y el checkpoint; puede aceptarlos, corregirlos o rechazarlos y fija identidades exactas si los congela.
2. El humano debe emitir una H-2/autorización nueva que identifique C-U2-11, WORK base/candidato, blobs de contrato/checkpoint, alcance de una única inspección y todas las prohibiciones. La autorización anterior de C-U2-10 no habilita este sucesor.
3. El AUDITOR emite los sobres separados que correspondan para una futura ejecución de solo lectura. Sin esos sobres, no se ejecuta nada.
4. La persona ejecuta primero el preflight de persistencia. Solo si pasa puede comenzar la única inspección C0 autorizada.
5. La persona guarda PNG y matriz, se detiene y entrega el resultado al AUDITOR. Si falla una condición, se detiene y requiere nueva intervención; no reintenta.

## Evidencia propuesta

Namespace exclusivo: `unidad-2-circuito-minimo/evidencia-c-u2-11/`.

- `preflight/guardado-png-prueba.png` y `preflight/resultado.md`: comprobación neutral del flujo de guardado y lectura, anterior a la inspección.
- `c0-estado-apps-01.png`, `c0-estado-apps-02.png`, etc.: capturas originales, secuenciales, sin modificar.
- `c0-matriz-estados.md`: una fila por app, con texto literal, vínculo visual app-estado y referencia al PNG.
- `DETENCION.md`: solo si el futuro intento autorizado debe detenerse; conservar causa y punto de parada, sin completar evidencia ni alterar capturas previas.

No se reutiliza, cambia ni completa evidencia histórica de C-U2-10. En particular, el `+` de aquella inspección y la captura local preexistente no son evidencia del sucesor.

## Control de alcance de esta intervención documental

La propuesta se redactó sobre el HEAD `ce89a58c0862abced634224dea1dc42a27505b6a`; los dos documentos de C-U2-11 y la entrada append-only inicial de `EVENTO.md` fueron materializados y publicados juntos en el único commit documental `8cf109d5ec183910e7599dd8dcbacb6e958eed20`. No se ejecutaron gate, P0, C0, P1, ninguna app/servicio ni operación de UI; no se materializó evidencia operacional; no se alteró el entorno. Esta declaración describe el alcance real de la entrega y no sustituye la verificación auditora del delta.

## Decisiones técnicas tomadas y diferidas

- **Tomada:** sustituir la inferencia desde el glifo `+` por texto de estado explícito y vinculado visualmente al nombre exacto de la app; es el cambio mínimo que discrimina instalación/conexión sin mutar estado.
- **Tomada:** hacer del guardado y la relectura PNG un preflight neutral, previo e invalidante, porque la pasada C-U2-10 no produjo evidencia local durable.
- **Tomada:** usar captura PNG secuencial original y matriz por app como dos registros complementarios; no se presume que la API de captura CUA guarde archivos.
- **Diferida al AUDITOR:** si la señal textual observada realmente existe y es suficiente, si la vista propuesta no cambia estado, y si el alcance/nombres deben ajustarse antes de congelar.
- **Diferida a la persona y la futura ejecución:** disponibilidad efectiva de Paint/guardado/relectura en el destino y la ruta de UI, que deben probarse condicionalmente; no se aseveran como hechos.
