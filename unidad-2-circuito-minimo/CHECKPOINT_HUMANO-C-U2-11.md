# CHECKPOINT HUMANO — C-U2-11

## Estado y autoridad

Este documento es una propuesta no ejecutable del CONSTRUCTOR para el sucesor C-U2-11, vinculada a `INCOMING_TURN_ID=162`, `BASE_WORK_SHA=ce89a58c0862abced634224dea1dc42a27505b6a`, incidente auditor `1ddaa82eb668f0d09f1d99835c6e0d3b97ef3264`, auditoría C0 `e937a00dc0ec6cea427c5031971873e255281791`, contrato congelado C-U2-10 `2e96c72aaf0b18cc67fccba11282f545d4025d1b` y checkpoint congelado C-U2-10 `709595ae1cd12a46d3d432d9b6fddc79c4a596c2`.

No autoriza inspección, preflight, captura, gate, P0, C0, P1, uso de apps/servicios, cambios de configuración/estado/entorno ni ninguna otra acción material. Solo vale tras congelamiento exacto del AUDITOR y una H-2/autorización humana nueva y separada para las identidades congeladas, además de sobres del AUDITOR aplicables. El candidato base es el SHA indicado; el SHA final de la propuesta y sus blobs serán los que Git y el AUDITOR establezcan, no se inventan aquí.

## Antecedente y criterio corregido

C-U2-10 consumió una única inspección sin acreditarla: tres nombres —`Sonda propuestas U1`, `Sonda propuestas U1 v2`, `Circuito propuestas C-U2-5`— aparecieron en «Personal > Created by me» con `+`; no hubo clics ni cambios. No se guardaron PNG ni matriz. El símbolo no tenía etiqueta accesible ni tooltip observado; la interpretación humana previa no bastó. La inspección no se repite ni se transforma retroactivamente en evidencia.

C-U2-11 propone una inspección nueva, propia de su namespace, que exige para cada app una señal textual explícita de no instalación/no conexión, claramente asociada en la misma vista a su nombre exacto. El glifo `+` solo, botones sin etiqueta, entradas ausentes o listas vacías nunca acreditan el estado.

## Alcance único

Una prevalidación neutral del método de persistencia, seguida —solo si pasa— por una única inspección visual de lectura de las apps identificadas del circuito, guardado secuencial de PNG originales y una matriz por app; luego, detenerse para auditoría. No incluye reparación de ningún estado ni paso posterior. P1 y el resto del procedimiento de unidad quedan fuera.

El gate y P0 ya registrados en C-U2-10 son historia, no autorización reutilizable. C-U2-11 es solo una verificación visual C0 acotada; no requiere ni hereda dichos gate/P0 como autoridad operativa. Toda continuación posterior exige contrato sucesor separado, revisión auditora y nueva autorización humana.

## Preflight de guardado, requisito previo

Antes de abrir cualquier lista/detalle de apps, en una página neutral la persona debe probar el flujo manual: captura de pantalla de Windows (`Win+Shift+S` o alternativa ya disponible), pegar en Paint y guardar como PNG en:

```text
unidad-2-circuito-minimo/evidencia-c-u2-11/preflight/guardado-png-prueba.png
```

Luego debe reabrir ese mismo archivo desde la ruta y verificar que se visualiza y no está vacío. Registrar en `unidad-2-circuito-minimo/evidencia-c-u2-11/preflight/resultado.md` ruta, nombre, tamaño no nulo, método usado y resultado de lectura. La prueba debe ser neutral: no mostrar ni contener ninguna app, nombre, conexión o estado del circuito.

Este flujo es una propuesta de operación humana, no una capacidad verificada. No instalar software ni cambiar configuración para habilitarlo. Si no se puede guardar y reabrir desde el destino, o no se puede determinar con certeza que el PNG se conservó intacto, detenerse sin abrir la lista de apps y requerir nueva decisión humana/auditora. La API CUA de captura no se considera mecanismo de persistencia demostrado.

## Inspección única y registro

Solo si el preflight pasa y las autorizaciones/sobres previos existen:

1. Inspeccionar una sola vez, sin accionar controles de estado, los nombres mínimos `Sonda propuestas U1`, `Sonda propuestas U1 v2` y `Circuito propuestas C-U2-5`, más cualquier otra app cuya pertenencia al circuito sea inequívoca.
2. Para cada una, permanecer en una vista de lectura que muestre simultáneamente nombre exacto y texto explícito de estado, por ejemplo un control etiquetado `Instalar complemento` o `Agregar`/`Conectar`, si el texto/contexto visible se refiere inequívocamente a esa app. Son ejemplos condicionales, no afirmaciones sobre la UI existente.
3. No pulsar `+` ni controles etiquetados o no etiquetados. No instalar, conectar, reconectar, desconectar, eliminar, autorizar ni cambiar configuración. No entrar a una vista si navegar a ella pudiera cambiar el estado.
4. Guardar cada pantalla pertinente como PNG original, completo y sin edición, secuencialmente en `evidencia-c-u2-11/c0-estado-apps-01.png`, `...-02.png`, etc. Cada archivo debe permitir leer en una misma captura el nombre y su señal. No reutilizar número ni dejar huecos.
5. Crear `evidencia-c-u2-11/c0-matriz-estados.md`, una fila por cada app, con nombre literal, ubicación observada, texto literal, vínculo contextual con el nombre, interpretación, resultado, hora local y referencia al PNG exacto que muestra ambos.
6. Tras la última fila, detenerse inmediatamente. Verificar solo la existencia/apertura de los archivos y completitud formal de matriz/capturas. Entregar la evidencia al AUDITOR; no continuar a P1.

## Decisión y regla de parada

**C0 propuesto para revisión auditora** si y solo si el preflight queda probado, cada app mínima y cada app adicional inequívoca tiene registro completo, el PNG es legible y sin alterar, y cada señal es texto explícito ligado al nombre exacto que acredita que no está conectada/instalada. La persona no dicta el veredicto final: lo emite el AUDITOR.

Detener una vez y marcar `C0_NO_ACREDITADO` si: falla preflight; no se ofrece señal explícita; solo aparece `+`, botón sin etiqueta, ausencia de entrada o lista vacía; el texto no está asociado inequívocamente con la app; aparece instalada/conectada; la afiliación es incierta; la captura no muestra nombre y señal legibles, no puede guardarse/abrirse, está editada o falta; o la inspección requeriría un cambio. Registrar lo observado y el punto de parada, sin inferencias. No repetir inspección, crear capturas sustitutas, completar matriz retrospectivamente ni modificar el estado de la app. Requerir nueva intervención humana/auditora.

## Evidencia, namespace y preservación

Solo para una futura ejecución autorizada, el namespace es `unidad-2-circuito-minimo/evidencia-c-u2-11/`. Artefactos propuestos: preflight PNG y nota bajo `preflight/`; capturas consecutivas `c0-estado-apps-NN.png`; `c0-matriz-estados.md`; y `DETENCION.md` si aplica. No escribir, cambiar ni derivar evidencia retroactiva en `evidencia-c-u2-10/` u otro namespace histórico. En esta propuesta no se crea ninguno de esos artefactos operativos.

## Límites y responsabilidad

Una captura acredita únicamente lo que la UI presentó en ese momento y cuenta; no verifica estado interno del proveedor ni su persistencia. La redacción no confirma que exista una acción de UI adecuada ni que Paint o el flujo de captura/guardado esté disponible. El preflight es precisamente una condición previa falsable. La suficiencia de señal, método, matriz, legibilidad y pertenencia corresponde al AUDITOR; cualquier ambigüedad se resuelve deteniendo, no suponiendo.

## Límite de esta entrega

La propuesta documental fue materializada y publicada en un único commit, `8cf109d5ec183910e7599dd8dcbacb6e958eed20`, que contiene este checkpoint, el contrato C-U2-11 y un apéndice append-only inicial en `EVENTO.md`. No se abrió UI ni se ejecutó preflight, gate, P0, C0, P1, app o servicio; no se creó evidencia operacional ni se modificó el entorno. La propuesta permanece pendiente de revisión y congelamiento del AUDITOR.
