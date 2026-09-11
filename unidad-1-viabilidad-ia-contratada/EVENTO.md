# EVENTO — Unidad 1: viabilidad de operación desde la IA contratada

## Qué recibió

Cabecera canónica completa con `INCOMING_TURN_ID=8`, e instrucción de cerrar D-01 y D-02 de la
auditoría de la entrega anterior de U1 sin ejecutar la conexión real. La situación se rederivó
desde Git sobre el corte recibido: la última entrega de work es
`d3f6d4393567d8bf8d76e97b2de760905d9319a7`; su auditoría aplicable existe con
`VEREDICTO=CORRECCION_REQUERIDA` y `CONTRATO_PREVIO_CONGELADO=NO`;
`PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas. El plan aprobado sigue siendo el de
`PLAN_BLOB_SHA=6da2d46ba5a41f4a1d33688ac1ee15709e9dce74`.

## Corrección de D-01 y D-02

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

- El modo desarrollador o la creación de la app no están disponibles en la cuenta declarada.
- La app se conecta pero la herramienta de escritura no puede ejecutarse o queda bloqueada por el
  plan.
- ChatGPT presenta propuestas, textos o evaluaciones sin la llamada correspondiente en la
  exportación. Esto hace fallar el contrato en cualquier corrida, sin promediar.
- Con la capacidad inválida se obtiene cualquier dato.
- Se devuelve contenido de `X-001` o cualquier dato de contacto.

- No se cumple alguno de E1 a E5 por cualquier otro motivo.

No existe una tercera categoría: toda ejecución iniciada termina en éxito o en fallo.

**Atribución del fallo.** Todo fallo se atribuye, con la exportación, a una de dos causas
excluyentes. Solo la primera sostiene que U1 termine en incompatibilidad documentada.

- **Fallo de cuenta o mecanismo.** (a) La interfaz de ChatGPT niega el modo desarrollador o la
  creación de la app antes de que llegue ninguna solicitud a la sonda. (b) Después de un escaneo
  que listó las cuatro herramientas, con solicitudes aceptadas por la sonda, ChatGPT no ejecuta la
  escritura o una lectura, y el registro muestra que la exposición seguía viva: una solicitud
  posterior de la misma ejecución —la lectura de `X-001` de la cuarta petición o el escaneo de la
  segunda app— sí llegó a la sonda. (c) Hay fabricación.
- **Fallo procedimental, de exposición o de sonda.** Cualquier otro fallo; en particular, que
  después del marcador `inicio-chatgpt` no llegue ninguna solicitud de ChatGPT a la sonda, que la
  sonda responda con error a solicitudes con la ruta correcta, o que el escaneo no liste las
  cuatro herramientas. Este fallo no permite concluir nada sobre la cuenta: U1 necesita un
  contrato nuevo.

La distinción la hace el registro de solicitudes, no la interpretación de un mensaje de
ChatGPT: la puerta G2 ya demostró, antes de empezar, que la exposición y la sonda responden desde
fuera con la misma URL y el mismo token.

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
  ChatGPT exigiera SSE, el escaneo fallaría con solicitudes aceptadas y el fallo quedaría
  atribuido como procedimental, no como incompatibilidad de la cuenta.
- La puerta G2 se ejecuta desde la misma máquina que expone la sonda: demuestra que el túnel
  funciona para un cliente externo, no que la red de OpenAI llegue a él. Si no llega, la regla de
  atribución lo clasifica como procedimental.
- El Quick Tunnel es un servicio de pruebas sin garantía de disponibilidad. Una caída durante la
  ejecución se ve en el registro como ausencia de toda solicitud posterior, y se atribuye como
  procedimental. Por eso una escritura que no llega solo cuenta contra la cuenta si una
  solicitud posterior sí llegó.

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
