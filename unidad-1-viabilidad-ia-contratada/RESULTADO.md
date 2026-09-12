# RESULTADO — Unidad 1: viabilidad de operación desde la IA contratada

Paso 6 de U1 en `PLAN.md`: requisitos, límites, costos y acciones manuales identificados.
Consolida lo que las dos conexiones reales dejaron demostrado, con su evidencia exacta, y es el
material que U2 debe tomar como dado.

**Qué no hace este documento.** No declara a U1 cerrada ni inicia U2. Propone la clase de
terminación; el veredicto corresponde al AUDITOR y el cierre de la unidad es una decisión humana
reservada (H-6). Tampoco reabre los contratos agotados ni reinterpreta sus resultados.

## Terminación propuesta

**Opción demostrada**, en los términos de `PLAN.md` §3: existe evidencia del viaje completo de
lectura y escritura por una integración admitida, y sus requisitos, límites y costos quedan
identificados abajo.

El mecanismo demostrado es **M2**, app MCP propia en modo desarrollador, en la cuenta
**ChatGPT Plus personal** declarada por el humano, sin administrador. No se afirma nada sobre
otras cuentas, otros planes ni otras IA.

## Identidad de lo que sostiene este resultado

| Qué | Identidad exacta |
|---|---|
| Candidato ejecutado | `francogg89-ai/work-claude-z @ cb023ed6c53dd63470da9463a6ea1697294f1055` |
| Contratos C-U1-2A y C-U1-2B congelados | `unidad-1-viabilidad-ia-contratada/EVENTO.md`, blob `606a381320675f1d71b014ab504da30e1468e946` |
| Checkpoint ejecutado | `unidad-1-viabilidad-ia-contratada/CHECKPOINT_HUMANO.md`, blob `b3dcb702deec3cc9656eb4ec5025c8a515c96b1d` |
| Congelamiento auditor | `francogg89-ai/audit-chatgpt-z @ 7e07a0100295758cd169d410cdfbee3d18123acb` |
| Evidencia de la segunda conexión | `francogg89-ai/error111 @ 9c026956cf1cffd35d25f6c506b8a9236fa64989`, `evidencia Z - segunda conexion U1` |
| Exportación del servidor | `evidencia-servidor.json`, SHA-256 `a346857235534d044e4121b179b197df4bd71c32fde12b1e21512de0051bf2b6` |
| Interpretación auditora | `francogg89-ai/audit-chatgpt-z`, `resoluciones/H-U1-CONEXION-REAL-2-9c026956cf1cffd35d25f6c506b8a9236fa64989.md` |
| Primera conexión, fallo preservado | evidencia `francogg89-ai/error111 @ b5115ff0a28f06262e42968580711e6d64907960`; resolución `resoluciones/H-U1-CONEXION-REAL-b5115ff0a28f06262e42968580711e6d64907960.md` |

La exportación del servidor la produjo la ejecución humana; las capturas y las transcripciones
también. Son evidencia material reportada, no comprobación independiente del AUDITOR ni del
CONSTRUCTOR.

## Cobertura de los casos del plan

| Caso de `PLAN.md` | Criterio | Qué quedó demostrado |
|---|---|---|
| C1.1 lista de propuestas | A/E1 | Una sola llamada `list_proposals` con `limit=100` cubrió las 100 propuestas en alcance; ChatGPT informó 100, primera `P-001`, última `P-100` |
| C1.2 detalle de una propuesta | A/E2 y B/B1–B2 | `P-042` recuperada con `original_fp=bac7f90c` en las cuatro lecturas registradas, sin datos de contacto en la respuesta; la vista de la app mostró el original con las dos huellas coincidentes |
| C1.3 guardar una evaluación | A/E3 | `save_evaluation` sobre `P-042` seguida de `get_evaluations`, ambas correctas; la evaluación quedó almacenada y se recuperó |
| C1.4 acceso sin autorización válida | A/E4 | Tres solicitudes de OpenAI con ruta no coincidente y respuesta `404`; ninguna aceptada, ninguna herramienta, ningún dato; la app inválida no llegó a crearse |
| C1.5 recurso fuera del alcance declarado | A/E5 | `X-001` produjo una llamada con error en cada conversación; ChatGPT informó que no está disponible y no mostró su contenido |
| Integridad de la evidencia | A/E6 | Toda solicitud con ruta correcta y `2xx` en la ventana válida tiene `User-Agent` que empieza con `openai-mcp/` |

## Requisitos identificados

Lo que la operación desde ChatGPT exige, verificado en la cuenta de referencia:

1. **Cuenta y superficie.** ChatGPT **web**; el modo desarrollador no existe en las apps móviles.
   Modo desarrollador activo y capacidad de crear apps propias. En la cuenta Plus personal usada
   no hizo falta administrador. Esto resuelve a favor de F4 la contradicción de fuentes que
   `RELEVAMIENTO.md` dejó abierta, y **solo** para esa cuenta.
2. **Extremo HTTPS público alcanzable.** La app se conecta por URL pública. Es la materialización
   de R2 del plan y la razón de H-2.
3. **Transporte sin SSE.** HTTP con streaming, sin estado y con respuestas JSON, y `405` ante el
   `GET` que abriría un stream iniciado por el servidor. Con eso la integración funcionó a través
   de un servicio de reenvío que no admite SSE.
4. **Descubrimiento por `server/discover`.** ChatGPT no usó `initialize`. Después pide
   `tools/list` y, cuando una herramienta declara vista, `resources/read`.
5. **Cliente identificable.** `openai-mcp/1.0.0`, y `openai-mcp/1.0.0 (Codex)` en las llamadas a
   herramientas. Es lo que permite distinguir tráfico propio de tráfico ajeno.
6. **Autorización en el sistema, no en la IA.** La escritura se ejecutó **sin confirmación** en las
   dos conexiones, con la herramienta anotada como no `readOnlyHint`, que es exactamente el caso en
   que F4 promete confirmación. Toda acción que exija autorización del creador debe pedirla el
   sistema.
7. **Canal fiel para originales.** Vista de MCP Apps: herramienta con `_meta.ui.resourceUri`,
   recurso `ui://` servido como `text/html;profile=mcp-app`, saludo `ui/initialize` y
   `ui/notifications/initialized`, e inserción del texto con `textContent`. El anfitrión pide la
   plantilla con `resources/read` y entrega el `structuredContent` de la herramienta. Disponible en
   la cuenta Plus usada, lo que `RELEVAMIENTO.md` no podía afirmar desde la documentación.
8. **Comparación de huellas como verificación del creador.** La vista calcula la huella del texto
   que efectivamente mostró y la compara con la del servidor. Dos códigos cortos iguales son
   verificables a simple vista; leer tildes no lo es.
9. **Paginación con cursor.** Necesaria por diseño, no por límite observado: la lista devuelve un
   resumen por propuesta más `next_cursor`, y el detalle se pide por propuesta.

## Límites observados y declarados

- **El texto libre del modelo no es literal.** En las dos conexiones, y en las dos conversaciones
  de la segunda, ChatGPT volvió a escribir `[SINTÉTICO]` donde el original dice `[SINTETICO]`. No
  es un accidente corregible con instrucciones: el modelo regenera y normaliza. El original no
  viaja por el texto del modelo.
- **La elección de herramienta no es determinista.** Ante la misma petición 2, la primera
  conversación usó `show_proposal` y la repetición `get_proposal`; con `X-001` pasó lo mismo. Un
  producto que necesite el canal fiel no puede depender de que el modelo elija la herramienta con
  vista.
- **La atribución visible es ambigua.** La app aparece en el panel `Sources`, pero no siempre hay
  un bloque de llamada en línea. El ejecutor creyó primero que dos peticiones no habían invocado la
  app. El creador no puede apoyarse en la interfaz para saber si un dato vino del sistema.
- **Acceso por URL con capacidad, no OAuth.** El token es un secreto portador que queda en la
  configuración de la app de ChatGPT. Es el límite que más condiciona a U2.
- **Exposición de prueba, no de producción.** Quick Tunnel de Cloudflare: pensado solo para
  pruebas, 200 solicitudes en curso, sin SSE y sin garantía de disponibilidad. Una caída se ve como
  ausencia de solicitudes y sería un fallo no discriminante respecto de la cuenta.
- **Los mensajes de error del producto no atribuyen causa.** El intento con capacidad inválida
  devolvió `Error creating connector / Something went wrong…`, sin mencionar plan, cuenta, política,
  rol ni permisos. Un rechazo así no sostiene por sí solo una indisponibilidad de capacidad.
- **Alcance de la evidencia.** Una cuenta, un plan, una IA, datos sintéticos, dos conversaciones.
  El comportamiento de ChatGPT no es determinista y nada se generaliza.
- **Fuerza de los controles.** E6 se apoya en el `User-Agent`, que puede falsificarse: detecta el
  uso accidental de un token filtrado, no uno adversarial. La huella FNV-1a de 32 bits detecta
  alteraciones accidentales y no es una garantía criptográfica.
- **Privacidad de los datos reales.** En Free, Plus, Go y Pro, OpenAI puede usar la información
  accedida desde apps para entrenar si la opción "Improve the model for everyone" está activa (F3
  de `RELEVAMIENTO.md`). Con datos sintéticos es indistinto; con propuestas reales es una
  restricción que U2 y U4 deben tratar.
- **M1 y M3 siguen descartados.** M1 no admite creación de GPTs en cuentas personales; M3 exige
  publicar y someterse a revisión externa.

## Costos y consumo observados

- **Costo adicional observado: ninguno.** No hubo cargo distinto de la suscripción Plus que el
  humano ya tenía. La documentación consultada no declara un costo por usar el modo desarrollador;
  no se afirma que no exista.
- **Quick Tunnel**: sin cuenta y sin costo. `cloudflared 2026.9.1`, protocolo `quic`, ubicación
  `gru07`. Un subdominio aleatorio, vivo solo durante la prueba.
- **Límite de uso de ChatGPT: ninguno observado.** El ejecutor declaró estar lejos del límite.
- **Consumo de la segunda conexión**: 28 solicitudes HTTP, 12 llamadas a herramientas, 2
  evaluaciones almacenadas, 2 conversaciones de 5 peticiones cada una, y 32 minutos 37 segundos
  entre los marcadores `inicio-chatgpt` y `fin`.
- **Magnitud de las respuestas**, medida localmente sobre el candidato con su semilla por omisión,
  no en la corrida: la página de 100 propuestas ocupa 15.830 caracteres, unos 158 por propuesta; el
  detalle de `P-042` ocupa 263. Ningún límite de tamaño se alcanzó, y la documentación de M2 no
  declara uno comparable al de M1.
- **Gasto de modelo del producto**: ninguno. La elección del modelo de evaluación y su gasto es H-4
  y no pertenece a U1.

## Acciones manuales del creador

Por instalación, una vez:

1. Activar o verificar el modo desarrollador en ChatGPT web.
2. Crear la app propia eligiendo conexión por URL pública, sin autenticación, y pegar la URL.
3. Confirmar que el escaneo encontró las herramientas esperadas.

Por sesión de operación:

4. Seleccionar la app en la conversación y pedir explícitamente que la use.
5. Para ver un original, pedir la **vista** de la app, no el texto.
6. Comparar las dos huellas de la vista antes de dar por bueno un original.

Propias de la prueba, que no pertenecen a la operación del producto: eliminar la app de la corrida
anterior, mover la URL con `probe.url copiar` y `probe.url limpiar`, abrir y cerrar el túnel,
intentar una vez la creación con capacidad inválida, y exportar la evidencia.

Lo que **no** hizo falta: administrador, transferencia manual de archivos entre ChatGPT y el
sistema, y ninguna confirmación de ChatGPT.

## Lo que no quedó demostrado

- Que el mecanismo funcione en otras cuentas, otros planes, espacios de trabajo u otras IA.
- Que funcione con autenticación OAuth: no se probó.
- Que exista o sea aceptable una exposición apta para producción: la probada es de prueba, y su
  costo y su superficie siguen siendo una decisión humana.
- Que el modelo elija siempre la herramienta correcta, ni que la literalidad de su texto pueda
  corregirse.
- Que la integración resista volúmenes, concurrencia o datos reales. Nada de eso se ejercitó.

## Qué condiciona en U2

Son consecuencias del resultado, no el inicio de U2, que requiere autorización humana.

1. El sistema expone a la IA del creador un servidor MCP remoto por HTTPS, sin depender de SSE, con
   herramientas anotadas y un canal de vista para los originales.
2. Las acciones consecuentes —publicar finalistas, invitar a ampliar— las autoriza el sistema. No
   pueden descansar en una confirmación de ChatGPT.
3. El creador necesita un camino verificable para saber que lo que ve vino del sistema. La
   comparación de huellas funcionó y es barata; la atribución de la interfaz no alcanza.
4. El enlace de entrada del creador (C2.7) debe indicar que el original se consulta por la vista, y
   su control negativo (C2.8) tiene ahora un modo de fallo concreto y observado: texto plausible
   regenerado por el modelo.
5. La autenticación sin secreto en la URL queda como trabajo de U2. El acceso por capacidad en la
   URL no es apto para el producto.
6. La paginación por cursor entra en el diseño desde el principio: R3 no se materializó como
   límite, pero la lista devuelve resumen y el detalle se pide por propuesta.
7. El tratamiento de datos reales frente a la opción de entrenamiento del proveedor es una
   restricción de diseño de U2 y materia documental de U4.

## Estado de los riesgos y de las intervenciones previstas

| Id | Estado |
|---|---|
| R1 plan sin mecanismo que cumpla el objetivo | No se materializó: M2 cumplió en la cuenta de referencia, con lectura y escritura reales |
| R2 exigencia de extremo HTTPS público con costo y superficie | Se materializó. Confirmado como requisito; la exposición de producción sigue abierta en H-2 |
| R3 límite de tamaño para 50–100 propuestas en una operación | Medido y no alcanzado: 100 propuestas en una sola llamada |
| RT-1 evidencia local como prueba de una propiedad real | Vigente. Las pruebas locales no demuestran la integración; lo que la demuestra es la evidencia de la corrida real |
| RT-2 simulación presentada como integración | No aplicó: la corrida fue real y los datos sintéticos están identificados como tales |
| H-1 cuenta y plan con capacidad de crear la integración | Resuelta para U1 por la segunda conexión |
| H-2 exposición de red | Resuelta solo para la prueba. Sigue abierta para U2 y para el producto |
| H-6 cierre de unidad y autorización de la siguiente | Pendiente. Es decisión humana y no la toma el CONSTRUCTOR |
