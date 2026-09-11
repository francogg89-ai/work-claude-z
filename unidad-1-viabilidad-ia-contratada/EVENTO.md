# EVENTO — Unidad 1: viabilidad de operación desde la IA contratada

## Qué recibió

Cabecera canónica completa con `INCOMING_TURN_ID=13`. La instrucción fue: rederivar, tratar el
contrato congelado como agotado con fallo no discriminante respecto de la cuenta, preservar la
evidencia positiva parcial, analizar el defecto de fidelidad, decidir el siguiente paso dentro de
U1 y considerar la incidencia de exposición del token.

La situación se rederivó desde Git sobre el corte recibido:

- La última entrega de work es `f181d3728b7e8fa09045a1f0ac6acd11f9e407e5`.
- Su auditoría aplicable congeló el contrato en `unidad-1-viabilidad-ia-contratada/EVENTO.md`,
  blob `e25937e38bcbafc259d06e1d2ebab54b4cd636fd`, y activó la necesidad humana material.
- La intervención auditora del corte es
  `resoluciones/H-U1-CONEXION-REAL-b5115ff0a28f06262e42968580711e6d64907960.md`, con
  `VEREDICTO=CONTRATO_EJECUTADO_FALLO_NO_DISCRIMINANTE_RESPECTO_DE_LA_CUENTA`,
  `CONTRATO_AGOTADO=SI` y `U1_CERRADA=NO`.
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

La evidencia humana se leyó en su identidad exacta, `francogg89-ai/error111 @ b5115ff0a28f06262e42968580711e6d64907960`,
en un clon temporal de solo lectura. El SHA-256 de `evidencia Z/evidencia-servidor.json`
coincide con el declarado:
`e0097aa99d79c0bc9d18c9dd29119c0c404da6430b19c16b5f08360703c13502`.

## Resultado del contrato agotado

Se toma tal como lo interpretó el AUDITOR y no se reabre: E1, E3, E4 y E5 satisfechos; E2 no
satisfecho; **fallo**, no discriminante respecto de la cuenta.

Se preserva como **evidencia positiva parcial**, sin convertirla en éxito del contrato ni en cierre
de U1: en la cuenta ChatGPT Plus personal usada, M2 ejecutó lecturas y una escritura real que
después se recuperó. El detalle está en `RELEVAMIENTO.md`, sección "Resultado empírico".

## Análisis técnico del defecto de fidelidad

**Qué pasó.** El original almacenado de `P-042` es
`[SINTETICO] Propongo un especial sobre música independiente.` ChatGPT mostró `[SINTÉTICO] …`.
Comparado carácter por carácter contra el candidato congelado, la única diferencia es la
posición 5: `E` en el original, `É` en lo mostrado.

**Dónde ocurrió.** No en la integración. La exportación registra `get_proposal` de `P-042`
correcta, y la sonda devuelve el registro almacenado sin transformarlo. La alteración ocurrió en
la presentación: el modelo regeneró el texto al escribir su respuesta y lo "corrigió".

**Por qué es estructural y no un accidente.** Un modelo de lenguaje no copia: vuelve a generar,
y tiende a normalizar lo que parece un error. El marcador `SINTETICO`, sin tilde, era un imán
para esa corrección. Las propuestas reales van a traer errores de tipeo, tildes faltantes y
ortografía informal. Además, en la corrida el modelo presentó su texto como "texto original
completo". Instruirlo para que transcriba literalmente puede bajar la frecuencia del problema,
pero no lo elimina: el producto quedaría librado a la suerte.

**Consecuencia de diseño.** El texto libre del modelo **no es un canal para originales**. La
preservación de originales que exige el manifiesto ya se cumple en el almacenamiento. Lo que
falta es que el creador pueda ver el original por un canal que no pase por el modelo. Esto
condiciona la arquitectura de U2 y por eso se resuelve en U1: si ChatGPT ofrece ese canal en la
cuenta de referencia, U2 puede usarlo; si no, U2 necesita otro, por ejemplo una vista del propio
sistema.

**El canal candidato.** Las vistas de MCP Apps (`RELEVAMIENTO.md`, "Presentación fiel de
contenido"). La herramienta devuelve el original como `structuredContent`, el anfitrión se lo
entrega a la vista, y la vista lo inserta con `textContent`. El modelo solo elige la herramienta
y su argumento.

## Otros hallazgos de la evidencia

- ChatGPT descubre el servidor con `server/discover`, no con `initialize`. La condición de
  atribución que nombraba `initialize` se generaliza a "el método de descubrimiento".
- En el intervalo de capacidad inválida, los `GET` recibieron `405` en lugar de `404`, porque el
  guardia del stream respondía antes de mirar la ruta. No expuso datos, pero dejaba ver un
  comportamiento distinto sin token válido. Corregido: ahora el `405` es solo para la ruta del
  token.
- La escritura se ejecutó **sin confirmación** del usuario, contra lo que dice la documentación.
  Riesgo para U2: las acciones que exigen autorización del creador —publicar, invitar— no pueden
  depender de la confirmación de ChatGPT.
- El cliente se identifica como `openai-mcp/1.0.0`. Eso permite el control de integridad E6.

## Incidencia de exposición del token y respuesta

La URL con el token terminó pegada en la conversación del agente auxiliar. La causa de fondo es
que el procedimiento mostraba la URL en pantalla —con `notepad`— y dependía de copiarla a mano.
La respuesta ataca eso sin cambiar el mecanismo de acceso:

1. **La URL no se muestra nunca.** `probe.url copiar` la pasa al portapapeles sin imprimirla;
   se pega solo en ChatGPT, y `probe.url limpiar` lo vacía enseguida. El procedimiento ya no abre
   los archivos que contienen la URL.
2. **El agente auxiliar no participa en ese tramo.** El checkpoint lo prohíbe entre `copiar` y
   `limpiar`; si se necesita ayuda en ese momento, primero se limpia el portapapeles.
3. **Uso ajeno detectable.** El criterio E6 exige que toda solicitud aceptada durante la
   conversación venga de ChatGPT. Si un token filtrado se usara durante la ejecución, E6 falla,
   y la evidencia contaminada no puede producir un éxito.
4. **La exposición no sobrevive a la ejecución.** Cada ejecución arranca con token nuevo
   (`--fresh`), y el subdominio aleatorio del túnel muere al cerrarlo: una URL filtrada no sirve
   después de la corrida.

Límites: el portapapeles igual puede pegarse en otro lugar durante esos segundos, y el
`User-Agent` se puede falsificar; E6 detecta el mal uso accidental, no uno adversarial. La
solución de fondo —autenticación sin secreto en la URL, como OAuth— cambia el mecanismo de
acceso y queda para U2, como ya establecía la limitación de U1.

## Decisión: siguiente paso dentro de U1

Una nueva corrida real, con **dos contratos independientes** evaluados sobre la misma ejecución:

- **C-U1-2A, integración.** Verifica lo que U1 necesita para terminar como opción demostrada:
  lectura, recuperación exacta del original por la IA —comprobada del lado del servidor con una
  huella—, escritura y recuperación, controles de acceso y alcance, e integridad de la evidencia.
- **C-U1-2B, vista fiel.** Verifica si el creador puede ver un original exactamente como se
  recibió, dentro de ChatGPT, mediante una vista de MCP Apps.

**Por qué dos contratos y no uno.** El contrato agotado mezclaba dos propiedades: que la IA
recupere el original, que es integración, y que se lo muestre literalmente al creador, que es
presentación. La corrida mostró que se separan y que fallan por causas distintas. Un contrato
único haría que un fallo de la vista, que es un mecanismo nuevo y no verificado en Plus,
bloqueara la conclusión sobre la integración, o al revés. Con dos contratos, cada resultado es
binario y sostiene solo su propiedad. Ninguno reinterpreta el resultado del contrato agotado, que
sigue siendo un fallo.

**Por qué el nuevo E2 de A no exige literalidad al modelo, y por qué eso no es mover el arco.**
El criterio no se afloja: se mueve a la capa donde el diseño lo puede garantizar. La literalidad
del original pasa a verificarse en B, con un mecanismo construido para eso y sobre el mismo
caso que falló. A verifica la recuperación exacta en el servidor. Que el texto libre del modelo
no es literal ya no es algo a comprobar: es un límite documentado, y el diseño deja de depender
de él.

**Alternativas descartadas.**

- *Cerrar U1 con la evidencia parcial.* El contrato congelado falló, y el AUDITOR indicó no
  convertirlo en cierre.
- *Repetir el mismo contrato instruyendo al modelo a transcribir literalmente.* Probabilístico, y
  dejaría al producto dependiendo de la suerte.
- *Postergar la vista fiel a U2.* U2 construiría sobre un supuesto no verificado, cuando el costo
  de verificarlo ahora es una herramienta más y una petición más en la corrida que el humano
  tiene que hacer de todos modos.
- *Pasar a OAuth para eliminar la URL portadora.* Cambio de mecanismo de acceso, fuera de lo que
  U1 necesita demostrar.

## Cambios en la sonda y en el procedimiento

- **Herramienta nueva `show_proposal`**, de lectura, enlazada por `_meta.ui.resourceUri` al
  recurso `ui://sonda/propuesta.html`, servido como `text/html;profile=mcp-app` con la extensión
  Apps del SDK. Devuelve el original como `structuredContent` tipado, más su huella.
- **La vista** completa el saludo de MCP Apps, inserta los campos con `textContent`, calcula la
  huella FNV-1a de 32 bits sobre el texto efectivamente mostrado, y muestra tres líneas: "Huella
  de lo mostrado", "Huella del servidor" y "Coinciden".
- **Huella en cada llamada que devuelve una propuesta**: `original_fp` en el registro de
  llamadas. La huella esperada de `P-042` en el candidato es `bac7f90c`; la del texto que ChatGPT
  mostró en la corrida agotada es `b60c8421`.
- **`405` solo en la ruta del token**; cualquier otra ruta, también por `GET`, devuelve `404`.
- **`probe.url`** para copiar y limpiar las URLs sin mostrarlas. La puerta G2 espera ahora cinco
  herramientas.
- **Instrucciones del servidor**: avisan al modelo que su transcripción no es literal y que, para
  mostrar un original, use `show_proposal`.

## Verificación local realizada

No es la verificación discriminante de U1. Se ejecutó en el Windows local del CONSTRUCTOR, con
timeouts acotados. No se abrió ningún túnel ni se usó ChatGPT.

| Comando | Resultado |
|---|---|
| `python -m pytest -q`, suite completa antes de agregar `tests/test_widget.py` | `57 passed`, rc=0 |
| `python -m pytest -q -rs tests/test_fingerprint.py` | `4 passed`, sin omitidas: la paridad de huella entre JavaScript y Python corrió en Node |
| `python -m pytest -q -rs tests/test_widget.py`, que ejecuta el script real de la vista en Node con un DOM mínimo y un anfitrión simulado | `3 passed`: saludo en orden; original de `P-042` con huella `bac7f90c` y "SI"; la alteración observada da `b60c8421` y "NO"; un `<img onerror>` se muestra como texto |
| Portapapeles real de Windows con un valor ficticio | copia exacta, verificada con `Get-Clipboard -Raw`, sin caracteres agregados; queda vacío tras `limpiar` |
| Comandos nuevos del checkpoint en Windows PowerShell 5.1, sobre copia limpia | G0 con `57 passed`; G1 escucha; `probe.url copiar` antes de G2, rc=1; G2 local con cinco herramientas; `show_proposal` por HTTP real devuelve huella `bac7f90c` y la plantilla con el tipo correcto; el portapapeles queda igual a la URL certificada y vacío tras `limpiar`; la exportación registra `resources/read`, `server/discover`, `tools/list` y `tools/call`, la huella de `show_proposal` y ningún rastro del token |

**Verificación interrumpida.** Una verificación local posterior quedó interrumpida por el humano
y, por su instrucción, no se repitió. En consecuencia, **la suite completa con
`tests/test_widget.py` incluido nunca se ejecutó como una sola corrida**: las 57 pruebas previas
y las 3 de la vista pasaron por separado. La puerta G0 del contrato nuevo ejecuta la suite
completa en la máquina del humano antes de empezar; si allí falla, la ejecución no empieza. Al
cerrar esta intervención no quedó ningún proceso de la sonda vivo y el puerto 8000 estaba libre.

Limitaciones: la vista se probó con un anfitrión simulado, no con ChatGPT. La lógica de G2 se
probó sin túnel de por medio.

## Mecanismo común a los dos contratos

El de `CHECKPOINT_HUMANO.md`, en Windows PowerShell:

- **Puertas previas G-1 a G2.** Candidato exacto, suite en verde, sonda en marcha con token nuevo
  y base vacía, y exposición certificada desde fuera, a través del túnel: las cinco herramientas
  con el token, y `404` sin token y con token inválido. Mientras alguna no se cumpla, la
  ejecución no empezó y no existe resultado de ningún contrato.
- **Ejecución**, que empieza con el marcador `inicio-chatgpt`:
  1. borrar las apps de la sonda de corridas anteriores;
  2. crear la app nueva pegando la URL con `probe.url copiar`, y limpiar enseguida;
  3. una conversación con cinco peticiones literales;
  4. marcador `inicio-intento-capacidad-invalida`, y segunda app con la URL inválida, con el
     mismo copiar y limpiar;
  5. marcador `fin`, cierre y exportación.

**Entorno.** ChatGPT web, en la cuenta que declare el humano; modo desarrollador; app MCP propia
por URL pública, sin la opción Tunnel; sonda en modo público en el Windows local; exposición
única por Quick Tunnel de Cloudflare.

**Corridas.** Hasta dos conversaciones dentro de la misma ejecución, antes del marcador
`inicio-intento-capacidad-invalida`. La segunda solo se admite si en la primera ChatGPT respondió
alguna petición sin invocar la app; no se admite para reintentar un resultado observado. Cada
contrato debe satisfacerse dentro de una sola conversación. Cualquier corrida con fabricación
hace fallar el contrato A.

**Regla de atribución, común a los dos contratos.** Todo fallo pertenece a una y solo una de estas
clases:

- **Indisponibilidad declarada de la capacidad en la cuenta.** Exige las tres condiciones:
  1. un mensaje de la interfaz de ChatGPT, capturado y transcrito literalmente, atribuye la
     imposibilidad al plan, al tipo de cuenta, a una política del espacio de trabajo, al rol o
     a los permisos;
  2. la capacidad rechazada es habilitar el modo desarrollador, acceder a la creación de apps
     propias, usar una herramienta ya escaneada o mostrar su vista, y el mensaje no menciona la
     URL, el endpoint, la conexión, la autenticación, el esquema, las herramientas ni el escaneo;
  3. si el rechazo es sobre el uso de una herramienta o de su vista, el registro muestra el
     descubrimiento —`server/discover` o `initialize`— y `tools/list` aceptados, y una solicitud
     posterior de la misma ejecución que llegó a la sonda.
- **No discriminante respecto de la cuenta.** Todo otro fallo, incluidos: un rechazo de creación
  o de escaneo sin un mensaje que cumpla 1 y 2; la ausencia de solicitudes; errores de la sonda;
  la no invocación de una herramienta sin un mensaje de restricción; la fabricación; y el fallo
  de E6.

Un fallo de la primera clase sostiene solo que la capacidad concreta no está disponible en la
cuenta declarada, según el propio producto. No sostiene por sí solo que ningún mecanismo admitido
satisfaga U1: esa conclusión exige combinarlo con `RELEVAMIENTO.md`, la evalúa el AUDITOR, y
sustituir el modo de operación es decisión del humano.

## Contrato previo C-U1-2A — integración

Propuesto para congelamiento del AUDITOR. **No ejecutar ninguna de sus partes antes de que el
AUDITOR lo congele.**

**Candidato exacto.** La sonda en `unidad-1-viabilidad-ia-contratada/sonda` en el `WORK_SHA` de
esta entrega, con los datos de `generate_dataset()` con su semilla por omisión, sembrados en una
base vacía.

**Propiedad.** Desde la cuenta de ChatGPT declarada, por M2, una petición breve del creador permite
obtener las propuestas, hacer que la IA recupere el original exacto de una propuesta sin datos de
contacto, y guardar una evaluación que después se recupera, sin transferencia manual de archivos;
y se rechazan el acceso sin capacidad válida y los recursos fuera del alcance declarado. Todo
esto con evidencia atribuible solo a ChatGPT.

**Criterio de éxito.** Se cumplen los seis, dentro de una misma conversación salvo E4:

- E1 (C1.1) La exportación registra llamadas `list_proposals` correctas cuyas páginas cubren las
  100 propuestas en alcance, y ChatGPT informa 100 propuestas, con primera `P-001` y última
  `P-100`.
- E2 (C1.2) La exportación registra una llamada correcta, `get_proposal` o `show_proposal`, que
  devuelve `P-042` con `original_fp` igual a `bac7f90c`; y la respuesta de ChatGPT no contiene
  ningún dato de contacto. La literalidad del texto libre del modelo no es criterio: está
  documentada como límite y se verifica por otro canal en C-U1-2B.
- E3 (C1.3) La exportación registra `save_evaluation` correcta sobre `P-042` con los valores
  pedidos, seguida de una `get_evaluations` correcta, y la evaluación aparece almacenada en la
  exportación.
- E4 (C1.4) Entre los marcadores `inicio-intento-capacidad-invalida` y `fin`, la exportación
  registra al menos una solicitud con ruta no coincidente y respuesta `404`, ninguna solicitud
  aceptada y ninguna llamada a herramientas; y ChatGPT no obtiene herramientas ni datos con esa
  app. Si en ese intervalo no llega ninguna solicitud, E4 no se cumple.
- E5 (C1.5) La exportación registra una llamada de `X-001` con error, y ChatGPT informa que no
  está disponible sin mostrar su contenido.
- E6 (integridad de la evidencia) Toda solicitud con ruta correcta y respuesta `2xx` entre los
  marcadores `inicio-chatgpt` e `inicio-intento-capacidad-invalida` tiene un `User-Agent` que
  empieza con `openai-mcp/`.

**Criterio de fallo.** No se cumple alguno de E1 a E6; o ChatGPT presenta propuestas, textos o
evaluaciones sin la llamada correspondiente en la exportación; o se obtiene cualquier dato con
la capacidad inválida; o se devuelve contenido de `X-001` o algún dato de contacto. Toda ejecución
iniciada termina en éxito o en fallo.

**Control negativo.** E4, E5, E6 y el control de fabricación. Sin ellos, un servidor que responde
a cualquiera, un modelo que contesta de memoria o un cliente ajeno con un token filtrado
satisfarían E1 a E3 por accidente.

**Alcance del éxito.** Sostiene que M2 permite, en la cuenta declarada, el viaje completo de
lectura y escritura que U1 exige, con los límites documentados. Es la evidencia sobre la que el
AUDITOR evalúa si U1 termina como opción demostrada; no es por sí mismo el cierre de U1, que es
decisión humana.

## Contrato previo C-U1-2B — vista fiel del original

Propuesto para congelamiento del AUDITOR. **No ejecutar ninguna de sus partes antes de que el
AUDITOR lo congele.** Es independiente de C-U1-2A: su resultado no condiciona el de A, y
viceversa.

**Candidato exacto.** El mismo que C-U1-2A, en particular `show_proposal` y el recurso
`ui://sonda/propuesta.html` de `probe/widget.py`.

**Propiedad.** Dentro de ChatGPT, en la cuenta declarada, el creador puede ver el original de una
propuesta exactamente como se recibió, mediante la vista de MCP Apps, sin depender de la
transcripción del modelo. Se usa `P-042`, el caso que el modelo alteró en la corrida agotada.

**Criterio de éxito.** Se cumplen los dos, en una misma conversación:

- B1 La exportación registra `show_proposal` de `P-042` correcta con `original_fp` igual a
  `bac7f90c`, y una solicitud `resources/read` aceptada con `User-Agent` que empieza con
  `openai-mcp/`: el anfitrión pidió la plantilla de la vista.
- B2 En respuesta a la tercera petición, ChatGPT renderiza la vista de la app, y **dentro de la
  vista**, no en el texto de la respuesta del modelo, se leen las tres líneas: "Huella de lo
  mostrado: bac7f90c", "Huella del servidor: bac7f90c" y "Coinciden: SI". La evidencia es una
  captura en la que la vista se distingue de la respuesta del modelo, más la transcripción
  literal de esas tres líneas.

**Criterio de fallo.** No se renderiza ninguna vista; o alguna de las tres líneas difiere; o
`show_proposal` no se invoca, agotadas las corridas admitidas; o no hay `resources/read`
aceptada; o las líneas aparecen solo en el texto del modelo.

**Control negativo.** La huella de la vista se calcula sobre el texto que la vista efectivamente
mostró y se compara con dos valores fijados antes de la ejecución: el del servidor y el de este
contrato. Si el texto mostrado difiriera en un solo carácter, por ejemplo con la alteración
observada en la corrida agotada, la huella sería `b60c8421` y "Coinciden" diría "NO": lo
comprueban `tests/test_fingerprint.py` y `tests/test_widget.py`. Exigir que las líneas estén
dentro de la vista impide que el modelo las satisfaga escribiéndolas en su respuesta.

**Alcance.** El éxito sostiene que la cuenta declarada ofrece un canal fiel para mostrar originales
dentro de ChatGPT, utilizable en U2. El fallo, cualquiera sea su atribución, no afecta a C-U1-2A:
indica que U2 necesita otro canal fiel, y no se concluye nada más.

## Limitaciones conocidas de ambos contratos

- El acceso es por URL con capacidad, no por OAuth. El token es un secreto portador que queda en
  la configuración de la app de ChatGPT.
- Datos sintéticos; una sola cuenta y un solo plan; ningún resultado se extiende a otras cuentas,
  a otros planes ni a otras IA.
- La exportación, las capturas y las transcripciones las produce quien ejecuta: son evidencia
  reportada, no comprobación independiente del AUDITOR.
- El comportamiento de ChatGPT no es determinista.
- E6 se apoya en el `User-Agent`, que puede falsificarse: detecta el uso accidental de un token
  filtrado, no uno adversarial.
- La huella FNV-1a de 32 bits detecta alteraciones accidentales. No es una garantía criptográfica.
- La vista solo se probó localmente, con un anfitrión simulado.
- La puerta G2 corre desde la misma máquina que expone la sonda, y el Quick Tunnel no tiene
  garantía de disponibilidad. Una caída se ve como ausencia de solicitudes y es un fallo no
  discriminante respecto de la cuenta.

## Necesidad humana detectada

NECESIDAD DEL HUMANO — la nueva corrida real exige, otra vez, operar la cuenta de ChatGPT y
exponer la sonda por HTTPS. Son acciones reservadas al humano, fuera del perímetro delegado. Se
actualiza `CHECKPOINT_HUMANO.md` para los dos contratos, con el nuevo manejo de la URL. Corresponde
a H-1 y H-2 del plan.

El CONSTRUCTOR registra y rutea esta necesidad; no declara que sea real. Esa determinación, y el
congelamiento previo de C-U1-2A y C-U1-2B, corresponden al AUDITOR.

## Limitaciones de esta entrega

- La sonda sigue siendo descartable y no compromete la arquitectura de U2.
- `sonda/.venv` y `sonda/.data` quedan fuera de Git.
- El directorio `.atl/` en la raíz del árbol es material de herramientas del entorno local, ajeno
  a esta entrega.
