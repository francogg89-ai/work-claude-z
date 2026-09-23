# PROPUESTA DE CONTRATO — C-U2-12

## Estado, autoridad y procedencia

Propuesta documental no ejecutable del CONSTRUCTOR para `C-U2-12`, sobre `BASE_WORK_SHA=82b49de2a191e1a409d3f1511fd8b6fbe2fe1b03`. Se propone únicamente una futura inspección C0, de una sola pasada y solo lectura. No constituye autorización presente ni congela identidades finales. Requiere revisión/congelamiento auditor con SHA exactos, un nuevo sobre de auditoría, H-2 y autorización humana separada y explícita, todos ligados a esas identidades. No se hereda autorización previa.

C-U2-11 está consumido y agotado, con C0 no acreditado. Referencias del incidente proporcionadas para esta propuesta: auditoría `ddd3c8cba086f3c967c104f4513c1bbd74846717`, auditoría de preflight `efc712117ef7045806314ac6cc2500bec9a8ead0`, auditoría de autorización C0 `77b8633a21066ff6344d5d2f00a8dbea3fba2c75`, blobs del contrato/checkpoint de trabajo `05d903d95635273449a31c1f22fa14dcc651713a` / `ff405cc11af02d53fb853432259a3211b3ad3066`. El antecedente no se reintenta ni se materializa retroactivamente. El estado desconectado referido previamente por el usuario es contexto, no evidencia.

## Objetivo y límite

Determinar, con evidencia visual explícita y asociada a cada app, si las apps mínimas del circuito aparecen no instaladas/no conectadas en la cuenta examinada. La inspección propuesta es una sola ejecución C0, con una pasada y cero reintentos. C0 no se acredita automáticamente: el AUDITOR decide a partir de la evidencia.

Alcance mínimo exacto, sin búsqueda amplia ni exploración adicional:

- `Sonda propuestas U1`
- `Sonda propuestas U1 v2`
- `Circuito propuestas C-U2-5`

Solo se añaden apps si la pertenencia está establecida de antemano por un manifiesto explícito congelado en el nuevo sobre auditor. Sin ese manifiesto, no ampliar la lista.

## Preflight neutral de PNG

Antes de iniciar C0 o navegar por apps se debe repetir un preflight neutral de guardado y lectura de PNG, en el namespace nuevo `unidad-2-circuito-minimo/evidencia-c-u2-12/preflight/`. El método reportado para el preflight previo —captura de pantalla de Windows mediante `Fn+PrtSc`, pegar en Paint, guardar como PNG y reabrir desde disco— consta como antecedente en la auditoría durable `efc712117ef7045806314ac6cc2500bec9a8ead0`. El `resultado.md` local de C-U2-11 no es evidencia durable ni se usa como fuente probatoria. El PNG neutral y su nota de resultado futura deben demostrar guardado local, tamaño no nulo y reapertura legible; no deben contener datos de apps. No instalar software ni cambiar configuración. Si el flujo no está disponible, falla o es incierto, no iniciar C0 ni abrir la UI de apps; registrar `PREFLIGHT_NO_PASA`. Esto no consume ni cuenta como fallo de una ejecución C0. El mismo flujo validado se usa luego para guardar cada captura de detalle, sin recortar ni editarla; la imagen mostrada por una herramienta de captura no sustituye al archivo local reabierto.

El preflight aprobado de C-U2-11 es solo antecedente histórico: no autoriza ni sustituye el nuevo preflight dado que cambian sucesor y destino.

## Navegación y evidencia discriminante

**Entorno/fuente propuesta:** cuenta personal de ChatGPT en `https://chatgpt.com/plugins?view=personal`, sección `Personal > Creados por mí`; la fuente primaria de C0 será únicamente el detalle de la app abierta desde el enlace ordinario del título exacto. La lista solo localiza el objetivo y nunca prueba su estado. La existencia en C-U2-12 de un enlace ordinario con rol accesible/DOM `link`, su destino same-origin y la correspondencia exacta entre destino y app son hipótesis por verificar en una ejecución futura autorizada; no se presentan como observaciones históricas de C-U2-11. No se abrió ningún detalle ni hay evidencia de qué texto mostraría. Si esas propiedades no se verifican, detenerse antes de activar el enlace.

Solo después del nuevo congelamiento auditor, H-2/autorización y preflight satisfactorio, ejecutar esta secuencia fija, sin rutas alternas:

1. Abrir el URL indicado y seleccionar `Personal > Creados por mí`.
2. En este orden, localizar una sola vez cada nombre exacto de la lista mínima.
3. Antes de navegar, comprobar que el título exacto es un enlace ordinario (rol accesible/DOM `link`), que apunta al mismo origen y a la ruta de detalle de esa misma app. Solo activar ese enlace. Si no cumple cualquiera de esas condiciones, detener C0 antes de activarlo. No activar `+`, botones ni otros controles.
4. En la página de detalle, capturar sin acción adicional. Si la UI cambia estado, solicita una acción/permisión o muestra un diálogo inesperado, detener inmediatamente.
5. Una vez guardada la captura de esa app, usar la navegación Atrás una sola vez para volver al directorio. Si no vuelve al directorio esperado, detenerse; no buscar rutas alternativas.
6. Repetir solo para el siguiente objetivo si el anterior mostró prueba inequívoca y el retorno fue normal. Cualquier ambigüedad detiene toda la C0: no se inspeccionan los objetivos restantes.

En cada detalle debe ser visible simultáneamente el nombre exacto de la app y texto explícito asociado inequívocamente a ella que indique una acción todavía disponible, por ejemplo `Instalar complemento`, `Agregar a ChatGPT` o `Conectar`. Son ejemplos de criterio, no hechos comprobados sobre la UI. Registrar literalmente lo que aparezca; no inferir estado por iconos, color, contexto externo ni explicación humana. Nunca accionar esos controles.

Guardar un PNG original e inalterado por app objetivo, una sola captura por app y en orden consecutivo: `unidad-2-circuito-minimo/evidencia-c-u2-12/c0-estado-apps-01.png`, `...-02.png` y así sucesivamente (`NN` secuencial, sin huecos). Crear `unidad-2-circuito-minimo/evidencia-c-u2-12/c0-matriz-estados.md` con una fila por app inspeccionada: nombre exacto, ubicación/vista, secuencia de navegación, texto literal, contexto que vincula señal y app, interpretación limitada, resultado, hora local y PNG exacto. Si la C0 se detiene por ambigüedad, guardar solo la captura de la vista ya observada si el flujo prevalidado lo permite, registrar el punto de detención y no navegar más; no completar retrospectivamente filas/capturas de apps no inspeccionadas. Los artefactos del preflight son `unidad-2-circuito-minimo/evidencia-c-u2-12/preflight/guardado-png-prueba.png` y `unidad-2-circuito-minimo/evidencia-c-u2-12/preflight/resultado.md`. La captura debe ser legible; no guardar secretos ni datos personales innecesarios. Tras la matriz o registro de detención, comprobar únicamente existencia y legibilidad de los artefactos y detenerse.

La evidencia C0 consiste exclusivamente en PNG locales, inalterados, y matriz. No se hace commit ni push durante una futura operación C0. Cualquier materialización Git posterior requiere un sobre auditor separado. No modificar ni reutilizar evidencia histórica.

## Criterio binario y detención

**Candidato a aceptación para decisión del AUDITOR:** preflight nuevo demostrado; todos los objetivos manifiestos tienen una fila y PNG legible con nombre exacto y texto explícito de acción disponible asociado; se siguió la secuencia congelada sin acciones mutantes; conjunto completo y durable. Esto no acredita C0 por sí solo.

**Fallo inmediato de C0: `C0_NO_ACREDITADO`.** Detener toda la inspección, sin reintento ni inspección de objetivos posteriores o rutas alternativas, si aparece solo `+`, un control sin etiqueta, una entrada ausente, asociación o estado ambiguo, texto que implique ya conectado/instalado, falta de señal explícita, afiliación no establecida, navegación potencialmente mutante, captura ilegible/ausente/no durable, desviación de secuencia o cualquier incidencia de captura. El fallo de preflight se informa antes de C0 como `PREFLIGHT_NO_PASA` y no inicia ni consume C0. No reemplazar evidencia ni completar retrospectivamente. Registrar solo lo observado y el punto de detención; el AUDITOR determina el resultado final.

## Exclusiones

No incluye instalación, conexión/desconexión, autorización, eliminación, cambios de configuración o entorno, búsqueda amplia, exploración de apps no manifestadas, apertura/ejecución de apps o servicios, servidor, túnel, gate, P1 ni pasos posteriores. Ningún paso se ejecuta con esta propuesta. No se afirma que exista el detalle descrito, que el enlace sea no mutante, ni que los textos candidatos aparezcan en la interfaz.

## Metadatos de redacción

Esta intervención solo redacta esta propuesta, su checkpoint y un apéndice de `EVENTO.md` en el repositorio de trabajo indicado. No se ejecutaron pruebas ni comandos operativos; solo lecturas y comprobaciones documentales/Git de solo lectura necesarias para formar y publicar la entrega. No se inspeccionó UI ni detalles/apps durante esta intervención documental ni se modificaron apps o entorno.
