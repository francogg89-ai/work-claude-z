# CHECKPOINT HUMANO — C-U2-12

## Estado

Propuesta no ejecutable sobre `BASE_WORK_SHA=82b49de2a191e1a409d3f1511fd8b6fbe2fe1b03`. C-U2-11 está consumido/agotado y C0 no fue acreditado. Sus evidencias no se reintentan ni reconstruyen. Referencias de auditoría/identidad: `ddd3c8cba086f3c967c104f4513c1bbd74846717`, `efc712117ef7045806314ac6cc2500bec9a8ead0`, `77b8633a21066ff6344d5d2f00a8dbea3fba2c75`; blobs de contrato/checkpoint `05d903d95635273449a31c1f22fa14dcc651713a` y `ff405cc11af02d53fb853432259a3211b3ad3066`.

C-U2-12 solo propone una inspección C0 futura, de lectura, de una pasada y sin reintentos. No hay autorización presente. Se requieren nuevo congelamiento auditor con identidades exactas, nuevo sobre, H-2 y autorización humana separada. No se hereda ninguna autorización; la afirmación previa de desconexión es contexto, no evidencia.

## Objetivos y método resumido

Alcance mínimo cerrado: `Sonda propuestas U1`, `Sonda propuestas U1 v2` y `Circuito propuestas C-U2-5`. Añadir otros solo si constan en manifiesto explícito congelado por el AUDITOR; no buscar ni explorar ampliamente.

Antes de iniciar C0, repetir un preflight neutral de guardado/reapertura PNG en `unidad-2-circuito-minimo/evidencia-c-u2-12/preflight/`, con `preflight/guardado-png-prueba.png` y `preflight/resultado.md`. Usar el mismo flujo local registrado en C-U2-11 (`Fn+PrtSc`, pegar en Paint, guardar PNG y reabrir exactamente desde disco); el preflight previo es solo antecedente, no se hereda. Si el flujo falla o es incierto, no iniciar C0 ni abrir apps; registrar `PREFLIGHT_NO_PASA`, que no consume C0. Tras autorizaciones y preflight satisfactorio, realizar una pasada única por cada app exacta en el orden listado: localizar el título y verificar antes de activarlo que sea un enlace ordinario (rol accesible/DOM `link`), same-origin y dirigido al detalle de esa app. Si no cumple, detenerse antes de activarlo. Nunca pulsar `+` ni botones de acción. Capturar el detalle con el mismo flujo local ya probado. Después de esa única captura, usar Atrás una vez para regresar al directorio esperado; si no vuelve, detenerse sin ruta alternativa. El detalle tendría que mostrar juntos nombre exacto y señal textual explícita asociada, por ejemplo `Instalar complemento`, `Agregar a ChatGPT` o `Conectar`; son ejemplos candidatos, no UI verificada. No pulsar controles de acción. Si aparece cualquier cambio de estado o diálogo inesperado, detener C0 inmediatamente.

Guardar una sola captura original e inalterada por cada app exacta, en una pasada, con nombres consecutivos `unidad-2-circuito-minimo/evidencia-c-u2-12/c0-estado-apps-01.png` en adelante (`NN`, sin huecos), usando `Fn+PrtSc` y Paint según el nuevo preflight, sin recortar ni editar. Crear `unidad-2-circuito-minimo/evidencia-c-u2-12/c0-matriz-estados.md` con una fila por app inspeccionada: nombre literal, vista/ruta, orden, texto literal, contexto que vincula nombre y señal, interpretación limitada, resultado, hora local y PNG correspondiente. Si ocurre ambigüedad, guardar únicamente la captura de la vista ya observada si es posible y registrar el punto de detención; no inspeccionar las apps siguientes ni completar filas/capturas retrospectivamente. Sin commit/push en C0. Detenerse tras la comprobación mínima de existencia/legibilidad. Toda materialización Git posterior exige sobre auditor separado.

## Regla de parada y veredicto

Cualquier `+` aislado, control sin etiqueta, entrada ausente, asociación/estado ambiguo, señal de ya conectado/instalado, enlace no conforme, cambio de estado, diálogo inesperado o problema de captura implica parada inmediata de todo C0 como `C0_NO_ACREDITADO`, sin inspeccionar apps posteriores, rutas alternas, reintentos ni sustitución/retrocreación de evidencia. Un preflight fallido ocurre antes de C0: informar `PREFLIGHT_NO_PASA`; C0 no se inicia ni se consume. El AUDITOR —no la persona ejecutora ni este checkpoint— decide acreditación.

No incluye mutaciones de apps, cambios de entorno/configuración, búsqueda amplia, apps fuera del manifiesto, servidor/túnel, gate, P1 ni pasos posteriores. Las etiquetas de acción citadas son solo ejemplos candidatos: no se verificó que existan. Este borrador no afirma haber verificado detalles ni UI. Como propuesta, no se ejecutarán pruebas, comandos u operaciones salvo comprobaciones documentales de solo lectura necesarias para formarla y publicarla.

## Límite de esta redacción

La intervención documental incluye el contrato, este checkpoint y un apéndice append-only en `EVENTO.md`. No se ejecutaron pruebas ni comandos operativos; solo comprobaciones documentales/Git de solo lectura necesarias para redactar y publicar. No se inspeccionó UI/detalles/apps ni se modificaron apps o entorno.
