# EVENTO — Unidad 1: viabilidad de operación desde la IA contratada

## Qué recibió

Cabecera canónica completa con `INCOMING_TURN_ID=10`, e instrucción de cerrar únicamente D-03
de la auditoría de la entrega anterior de U1, sin ejecutar la conexión real. La situación se
rederivó desde Git sobre el corte recibido: la última entrega de work es
`d0d965f46d056853f9fd205554d463cb6c79491f`; su auditoría aplicable existe con
`VEREDICTO=CORRECCION_REQUERIDA`, `CONTRATO_PREVIO_CONGELADO=NO`, y D-01 y D-02 cerrados;
`PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas. El plan aprobado sigue siendo el de
`PLAN_BLOB_SHA=6da2d46ba5a41f4a1d33688ac1ee15709e9dce74`.

## Corrección de D-03

D-03 se sostiene: un rechazo al crear la app antes de que llegue ninguna solicitud puede deberse
a la configuración concreta —URL, autenticación, dominio de exposición, metadatos— y no a la
capacidad de la cuenta; la guía de OpenAI para conectar un MCP manda resolver justamente esos
errores antes de continuar.

Revisada con ese criterio, la regla de atribución tenía otras dos cláusulas con el mismo
defecto, que se corrigen juntas:

- La cláusula (b) contaba contra la cuenta que la escritura "no se ejecute" con la exposición
  viva. Pero que el modelo no invoque una herramienta también puede ser selección de
  herramienta, no falta de capacidad.
- La cláusula (c) contaba la fabricación como fallo de cuenta o mecanismo. La fabricación es un
  fallo del comportamiento del modelo y no dice nada sobre la capacidad de la cuenta.

El criterio corregido es uno solo: **el fallo solo cuenta contra la cuenta cuando el propio
producto declara como causa el plan, el tipo de cuenta, una política, el rol o los permisos,
sobre la capacidad y no sobre esta configuración**, y, si el rechazo es sobre el uso de una
herramienta, con la exposición demostradamente viva. Todo otro fallo es no discriminante
respecto de la cuenta.

Además, se acota lo que ese fallo sostiene. Establece que la capacidad de M2 no está disponible
en la cuenta declarada; no establece por sí solo que ningún mecanismo admitido satisfaga U1,
porque para eso hace falta combinarlo con lo que el relevamiento dice de M1 y de M3.

Se conservan la regla binaria de éxito o fallo, los criterios E1 a E5, las puertas previas, la
única exposición y el procedimiento. En los criterios de fallo se reemplazó el lenguaje causal
—"no disponible en la cuenta", "bloqueada por el plan"— por observaciones, para que la causa la
asigne solo la regla de atribución. En `CHECKPOINT_HUMANO.md`, por coherencia literal, se pide
capturar y transcribir cada mensaje de rechazo o restricción y registrar en qué momento
apareció, porque la nueva regla depende de esa evidencia.

## Corrección anterior de D-01 y D-02

Los dos defectos se sostienen, y al corregirlos apareció un tercer caso de la misma clase que
el AUDITOR no había señalado.

- **D-01 — mecanismo inequívoco por alternativa.** Se ofrece una sola alternativa de exposición:
  endpoint HTTPS público mediante un Quick Tunnel de Cloudflare. Secure MCP Tunnel deja de
  ofrecerse, con la razón en `RELEVAMIENTO.md`. Para que un fallo procedimental no pueda leerse
  como incompatibilidad de la cuenta, la corrección no se limitó a separar ramas:
  - **Puertas previas G-1 a G2.** Candidato exacto, entorno, sonda en marcha y exposición
    certificada desde fuera, a través del túnel, antes de tocar ChatGPT. Si una puerta no se
    cumple, la ejecución del contrato no empezó.
  - **Registro de solicitudes HTTP en la sonda**, con marcadores de tiempo. Distingue una
    solicitud que nunca llegó, una que la sonda rechazó y una que la sonda aceptó. De esa
    distinción depende la regla de atribución que se agregó al contrato.
  - **E4 exige un rechazo registrado.** Antes, "ChatGPT no obtiene datos" podía cumplirse porque
    nada llegara a la sonda; ese control negativo no podía fallar.
- **Caso adicional de la misma clase.** F9 declara que los Quick Tunnels no soportan SSE, y el
  SDK responde por SSE por omisión; además, con la protección de `Host` y `Origin` activa, la
  sonda habría rechazado encabezados puestos por el túnel o por ChatGPT. Cualquiera de las dos
  cosas habría producido un fallo de la sonda con apariencia de incompatibilidad de la cuenta.
  La sonda pasa a usar HTTP sin estado, respuestas JSON y `405` para el stream por `GET`, y en
  modo público desactiva esa protección: el token de la URL sigue siendo la única llave.
- **D-02 — arranque ejecutable en Windows.** El checkpoint declara Windows PowerShell y usa solo
  comandos literales, sin variables de entorno ni asignaciones en línea. El token lo genera la
  propia sonda (`probe.launch --fresh`) en un archivo local ignorado por Git, y la puerta G2
  escribe las dos URLs para ChatGPT solo si la exposición quedó certificada. Así nadie tiene que
  copiar el token por la terminal ni reparar sintaxis. Como en Windows PowerShell 5.1 `>` escribe
  en UTF-16, la exportación escribe su archivo directamente en UTF-8.

## Qué hizo y por qué

La entrega anterior de esta unidad cubrió los pasos 1 a 4 de U1 del plan. El paso 5, la conexión real, no se
ejecuta: depende de una cuenta, un plan y una exposición de red que no pertenecen al perímetro
delegado, y su contrato previo debe congelarlo el AUDITOR antes de cualquier ejecución.

**Paso 1 — relevamiento.** En `RELEVAMIENTO.md`, contra documentación pública de OpenAI
consultada el 2026-09-10, con URL y fecha de actualización mostrada por cada página. Resultados
que condicionan el resto de la unidad:

- La creación de GPTs nuevos ya no está disponible en cuentas personales, de modo que GPT
  Actions solo aplica a espacios Business, Enterprise o Edu.
- La app MCP propia en modo desarrollador es el único mecanismo que al menos una fuente oficial
  declara disponible para cuentas personales.
- Las dos fuentes oficiales **se contradicen** sobre si una cuenta personal puede ejecutar
  acciones de escritura por ese mecanismo. La guía para desarrolladores declara elegibles a Plus
  y Pro con lectura y escritura; el centro de ayuda declara el MCP completo con escritura solo
  para Business, Enterprise y Edu, y atribuye a Pro únicamente lectura.

Esa contradicción no se resuelve leyendo más documentación: es exactamente lo que la conexión
real debe discriminar, y es la razón por la que el contrato de abajo se centra en la escritura.

**Pasos 2 y 3 — sonda mínima y comprobación local.** En `sonda/`, un servidor MCP deliberadamente
mínimo y descartable sobre datos sintéticos identificados como tales, con cuatro herramientas
—`list_proposals`, `get_proposal`, `save_evaluation`, `get_evaluations`—, paginación, 100
propuestas en alcance y 3 fuera de alcance. Decisiones de la sonda, ninguna de las cuales
compromete a U2:

- El control de acceso es una URL con capacidad: el endpoint solo existe en `/mcp/<token>`. El
  token lo genera `probe.launch` en `.data/token`, excluido de Git; ninguna aplicación se
  construye con un token de menos de 32 caracteres, y el registro de acceso de uvicorn está
  apagado para que el token no aparezca en la consola.
- Transporte sin SSE: HTTP sin estado, respuestas JSON y `405` para el stream por `GET`. En modo
  público se desactiva la protección de `Host` y `Origin`; en modo local se mantiene.
- Registro de cada solicitud HTTP —método, si la ruta coincidió con la del token, código de
  respuesta, método JSON-RPC, `Host`, `Origin` y `User-Agent`— sin guardar nunca la ruta, más
  marcadores de tiempo escritos con `probe.mark` y por la puerta G2.
- Los datos de contacto viven en su propia tabla y ningún método público los lee; existen para
  que las pruebas demuestren que no se filtran.
- El servidor registra cada llamada recibida. Ese registro es lo que permite distinguir una
  respuesta obtenida del sistema de una fabricada por el modelo.
- Las instrucciones del servidor prohíben presentar propuestas o evaluaciones no obtenidas de
  las herramientas y declaran el texto de las propuestas como dato no confiable.

**Paso 4 — contrato previo.** Propuesto más abajo, sin ejecutar.

## Verificación local realizada

No es la verificación discriminante de U1. Comprueba la sonda, no la integración, y se ejecuta
íntegramente dentro del perímetro. Entorno: Windows local del CONSTRUCTOR, Python 3.12.4, entorno
virtual propio de la sonda con `mcp==2.2.0`, `httpx==0.28.1`, `pytest==9.1.1`.

Suite de pruebas, desde Git Bash, con timeout acotado:

| Comando | Resultado |
|---|---|
| `python -m pytest -q` | `43 passed`, rc=0 |

Las pruebas cubren, además de lo anterior —determinismo y marcado sintético de los datos,
separación de contactos, paginación completa de las 100 propuestas, rechazo de fuera de
alcance, persistencia, anotaciones de lectura y escritura, registro de llamadas—, lo siguiente
sobre el servidor real en ambos modos: `404` sin token o con token inválido, respuestas
`application/json` y nunca SSE, `405` al `GET`, rechazo de un `Host` ajeno en modo local,
aceptación en modo público de `Host` y `Origin` puestos por terceros sin dejar de exigir el
token, ida y vuelta de escritura y lectura, registro de solicitudes sin el token, marcadores
intercalados en orden, la puerta G2 aprobando una sonda bien expuesta y fallando sin escribir
URLs cuando nada escucha, generación de un token nuevo en cada `--fresh` y exportación en UTF-8.

Comandos literales del checkpoint, ejecutados en **Windows PowerShell 5.1.26100** sobre una copia
limpia de la sonda, cada proceso de larga duración acotado:

| Comando del checkpoint | Resultado |
|---|---|
| `python --version`, `python -m venv .venv`, `pip install -r requirements.txt`, `pytest -q` (G0) | Python 3.12.4; rc=0 en los tres; `43 passed` |
| `.\.venv\Scripts\python.exe -m probe.launch --fresh` (G1) | escucha en `127.0.0.1:8000` y crea `.data\token`; detenido con `Stop-Process` |
| `.\.venv\Scripts\python.exe -m probe.check http://127.0.0.1:8000` | rc=1: la puerta G2 solo acepta una URL `https://` |
| `.\.venv\Scripts\python.exe -m probe.mark inicio-chatgpt`, y con una etiqueta inválida | rc=0, y rc=1 respectivamente |
| `.\.venv\Scripts\python.exe -m probe.export .data\evidencia-servidor.json` | rc=0; el primer byte es `{`, sin BOM UTF-16; contiene el marcador y no contiene el token |
| `curl.exe -sSL -o .data\cloudflared.exe <URL de F10>` y `.\.data\cloudflared.exe --version` | rc=0; `cloudflared version 2026.9.0`; **no se abrió ningún túnel** |
| `git diff --quiet <SHA> -- .` y `$LASTEXITCODE` (G-1), sobre el clon real | la sintaxis funciona y discrimina: contra la entrega anterior imprime `1`, porque la sonda cambió |

Al terminar, el puerto 8000 quedó libre y no quedó ningún proceso de la sonda vivo.

Limitaciones: todo ocurrió en `127.0.0.1`. La puerta G2 con una URL `https://` real, el túnel y
ChatGPT no se ejercitaron, porque exponer la sonda está fuera del perímetro. La lógica de G2 se
probó contra el servidor real en modo público, pero sin túnel de por medio.

## Contrato previo de verificación — conexión real (C1.1 a C1.5)

Propuesto para congelamiento del AUDITOR. **No ejecutar ninguna de sus mitades antes de que el
AUDITOR lo congele.**

**Candidato exacto.** La sonda tal como queda en el directorio `unidad-1-viabilidad-ia-contratada/sonda`
en el `WORK_SHA` de esta entrega, con el conjunto de datos de `generate_dataset()` con su semilla
por omisión, sembrado en una base vacía.

**Propiedad que debe demostrarse.** Que desde la cuenta de ChatGPT del creador de referencia, por
una integración admitida por esa cuenta, una petición breve del creador permite obtener las
propuestas, obtener el original de una propuesta sin datos de contacto y guardar un resultado de
evaluación que después se recupera, sin transferencia manual de archivos; y que el acceso sin
capacidad válida y los recursos fuera del alcance declarado se rechazan.

**Entorno y fuente relevantes.** ChatGPT web, cuenta del creador de referencia, cuyo plan declara
el humano y no se infiere; modo desarrollador habilitado en esa cuenta; app MCP propia (mecanismo
M2 del relevamiento) configurada con la URL pública del servidor, no con la opción Tunnel; sonda
ejecutándose en el Windows local en modo público; exposición única por Quick Tunnel de
Cloudflare. Ninguna otra exposición forma parte de este contrato.

**Mecanismo.** El de `CHECKPOINT_HUMANO.md`, en Windows PowerShell y en dos tramos:

- **Puertas previas G-1 a G2**: candidato exacto, entorno con la suite en verde, sonda en marcha
  con token nuevo y base vacía, y exposición certificada desde fuera, a través del túnel, con
  las cuatro herramientas listadas con el token y `404` sin token y con token inválido. Mientras
  alguna no se cumpla, **la ejecución no empezó** y no existe resultado del contrato: lo ocurrido
  vuelve al loop como evidencia de precondición no satisfecha.
- **Ejecución**, que empieza con el marcador `inicio-chatgpt`: habilitar el modo desarrollador,
  crear la app con la URL escrita por G2, cuatro peticiones literales en una conversación,
  marcador `inicio-intento-capacidad-invalida`, segunda app con la URL inválida escrita por G2,
  marcador `fin`, cierre y exportación de la evidencia del servidor.

**Criterio discriminante de éxito.** Se cumplen los cinco:

- E1 (C1.1) La exportación registra llamadas `list_proposals` correctas cuyas páginas cubren las
  100 propuestas en alcance, y la respuesta de ChatGPT informa 100 propuestas con primera `P-001`
  y última `P-100`.
- E2 (C1.2) La exportación registra `get_proposal` correcta de `P-042`; el texto que ChatGPT
  muestra coincide con el original almacenado y la respuesta no contiene ningún dato de contacto.
- E3 (C1.3) La exportación registra `save_evaluation` correcta sobre `P-042` y una
  `get_evaluations` posterior también correcta, y la evaluación aparece almacenada en la
  exportación.
- E4 (C1.4) Entre los marcadores `inicio-intento-capacidad-invalida` y `fin`, la exportación
  registra al menos una solicitud llegada con ruta no coincidente y respuesta `404`, ninguna
  solicitud aceptada y ninguna llamada a herramientas; y ChatGPT no obtiene herramientas ni
  datos con esa app. Si en ese intervalo no llega ninguna solicitud, E4 no se cumple: el control
  no se ejercitó.
- E5 (C1.5) La exportación registra `get_proposal` de `X-001` con error, y ChatGPT informa que no
  está disponible sin mostrar su contenido.

**Criterio discriminante de fallo.** Cualquiera de estos:

- El modo desarrollador no puede habilitarse, o la app no puede crearse o no completa el escaneo.
- La herramienta de escritura o alguna lectura no llega a ejecutarse.
- ChatGPT presenta propuestas, textos o evaluaciones sin la llamada correspondiente en la
  exportación. Esto hace fallar el contrato en cualquier corrida, sin promediar.
- Con la capacidad inválida se obtiene cualquier dato.
- Se devuelve contenido de `X-001` o cualquier dato de contacto.
- No se cumple alguno de E1 a E5 por cualquier otro motivo.

Estos criterios describen observaciones, no causas. No existe una tercera categoría: toda
ejecución iniciada termina en éxito o en fallo. La atribución siguiente clasifica el fallo por su
causa, sin crear otra salida.

**Atribución del fallo.** Todo fallo pertenece a una y solo una de estas dos clases.

- **Fallo por indisponibilidad declarada de la capacidad en la cuenta.** Exige las tres
  condiciones:
  1. **El producto declara la causa.** Un mensaje de la interfaz de ChatGPT, capturado y
     transcrito literalmente, atribuye la imposibilidad al plan, al tipo de cuenta, a una
     política del espacio de trabajo, al rol o a los permisos.
  2. **La causa declarada es la capacidad, no esta configuración.** La capacidad rechazada es
     habilitar el modo desarrollador, acceder a la creación de apps propias o usar una
     herramienta ya escaneada; y el mensaje no menciona la URL, el endpoint, la conexión, la
     autenticación, el esquema, las herramientas ni el escaneo.
  3. **Si el rechazo es sobre el uso de una herramienta**, el registro muestra que el escaneo
     se aceptó —`initialize` y `tools/list` con ruta correcta y respuesta `200`— y que una
     solicitud posterior de la misma ejecución llegó a la sonda, de modo que la exposición
     seguía viva.
- **Fallo no discriminante respecto de la cuenta.** Todo otro fallo. En particular:
  - un rechazo al crear o configurar la app, o un escaneo fallido, sin un mensaje que cumpla las
    condiciones 1 y 2, aunque ninguna solicitud haya llegado a la sonda;
  - la opción del modo desarrollador ausente sin un mensaje que declare la causa;
  - que después del marcador `inicio-chatgpt` no llegue ninguna solicitud, que la sonda responda
    con error a solicitudes con la ruta correcta, o que el escaneo no liste las cuatro
    herramientas;
  - que el modelo no invoque una herramienta sin un mensaje de restricción, porque eso puede ser
    selección de herramienta y no falta de capacidad;
  - una restricción declarada sobre una herramienta sin una solicitud posterior que pruebe que la
    exposición seguía viva;
  - la fabricación, que además se registra como hallazgo sobre el comportamiento del modelo,
    pertinente al riesgo R12 del plan.

  Este fallo no permite concluir nada sobre la cuenta ni sobre la disponibilidad de M2: para otra
  ejecución hace falta un contrato nuevo, que corrija la condición identificada.

**Alcance de la conclusión.** El registro de solicitudes discrimina si la exposición y la sonda
respondieron, y el mensaje literal del producto discrimina la causa de un rechazo; se necesitan
ambos. Aun así, un fallo de la primera clase sostiene solo esto: *la capacidad que M2 requiere no
está disponible en la cuenta declarada, según el propio producto*. **No sostiene por sí solo que
ningún mecanismo admitido satisfaga U1.** Esa terminación de U1 exige combinarlo con lo que
`RELEVAMIENTO.md` establece para M1, de forma documental, y para M3, que quedó fuera por una
decisión de alcance y no por una prueba. Esa combinación la evalúa el AUDITOR, y sustituir el modo
de operación o reconsiderar M3 es decisión del humano, conforme al criterio de terminación de U1
del plan.

**Corridas.** Hasta dos conversaciones. El éxito exige que una sola conversación satisfaga E1,
E2, E3 y E5. La segunda conversación solo se admite si en la primera ChatGPT no llegó a invocar
una herramienta; no se admite para reintentar un resultado observado como fallo. Cualquier
corrida con fabricación hace fallar el contrato.

**Control negativo.** E4 y E5, más el control de fabricación: sin ellos, un servidor que responde
a cualquiera y un modelo que contesta de memoria satisfarían E1 a E3 por accidente.

**Limitaciones conocidas.**

- Demuestra control de acceso por URL con capacidad, no OAuth. U1 no demuestra OAuth, y el modelo
  de autenticación del producto queda como decisión de U2 informada por este resultado.
- El token viaja dentro de la URL configurada en la app de ChatGPT: es un secreto portador. No
  entra en Git ni en este documento.
- Datos sintéticos; una sola cuenta y un solo plan; ningún resultado se extiende a otros planes,
  a otras cuentas ni a otras IA.
- La exportación y las transcripciones las produce quien ejecuta, no el AUDITOR: es evidencia
  reportada, no comprobación independiente.
- El comportamiento de ChatGPT no es determinista.
- La sonda responde en JSON y sin stream por `GET`, formas válidas del transporte de MCP. Si
  ChatGPT exigiera SSE, el escaneo fallaría con solicitudes aceptadas, y el fallo sería no
  discriminante respecto de la cuenta.
- La puerta G2 se ejecuta desde la misma máquina que expone la sonda: demuestra que el túnel
  funciona para un cliente externo, no que la red de OpenAI llegue a él. Si no llega, el fallo es
  no discriminante respecto de la cuenta.
- El Quick Tunnel es un servicio de pruebas sin garantía de disponibilidad. Una caída durante la
  ejecución se ve en el registro como ausencia de toda solicitud posterior, y el fallo es no
  discriminante respecto de la cuenta. Por eso un rechazo sobre una herramienta solo cuenta
  contra la cuenta si una solicitud posterior sí llegó.
- Que la interfaz declare como causa el plan o los permisos es la única evidencia admitida de
  indisponibilidad en la cuenta. Si el producto rechaza sin declarar la causa, el contrato no
  puede concluir que la cuenta carece de la capacidad, aunque la causa real fuera esa: el
  contrato prefiere no concluir antes que concluir de más.

## Necesidad humana detectada

NECESIDAD DEL HUMANO — la conexión real exige una cuenta de ChatGPT con su plan, habilitar el
modo desarrollador en ella, crear la app y exponer la sonda por HTTPS. Nada de eso está
comprendido en el perímetro delegado vigente: son acciones sobre servicios y cuentas reservadas
al humano, y la exposición de red es además un despliegue externo.

Se preserva `CHECKPOINT_HUMANO.md` en esta unidad, autocontenido y sin secretos, conforme a
REVOLUTIONS §7.4. Corresponde a H-1 y H-2 del plan.

El CONSTRUCTOR registra y rutea esta necesidad; no declara que sea real. Esa determinación, y el
congelamiento previo del contrato, corresponden al AUDITOR.

## Limitaciones de esta entrega

- La sonda no es el sistema y su stack no compromete a U2. Sirve para comprobar la interfaz.
- El directorio `sonda/.venv` y la base de datos local quedan fuera de Git por `.gitignore`: son
  reconstruibles con `requirements.txt` y con la siembra determinista.
- El directorio `.atl/` en la raíz del árbol es material de herramientas del entorno local, ajeno
  a esta entrega.
