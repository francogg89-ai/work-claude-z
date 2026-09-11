# EVENTO — Unidad 1: viabilidad de operación desde la IA contratada

## Qué recibió

Cabecera canónica completa con `INCOMING_TURN_ID=6`, e instrucción de iniciar U1 conforme al
PLAN aprobado. La situación se rederivó desde Git sobre el corte recibido: la última entrega de
work es `8f75c827bbd1924555600e46fb04cf5ecee41559`, su auditoría aplicable existe con veredicto
`APTO_PARA_DECISION_HUMANA_SOBRE_PLAN`, y la intervención auditora del corte preserva la
decisión humana `APROBADO` sobre `PLAN.md` con `PLAN_BLOB_SHA=6da2d46ba5a41f4a1d33688ac1ee15709e9dce74`,
que coincide con el blob de `PLAN.md` en esa entrega. `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`
y `MODIFICA_PERIMETRO=NO`: el perímetro vigente es el de `BOOTSTRAP.md`.

## Qué hizo y por qué

Esta intervención cubre los pasos 1 a 4 de U1 del plan. El paso 5, la conexión real, no se
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

- El control de acceso es una URL con capacidad: el endpoint solo existe en `/mcp/<token>`, el
  token se toma del entorno, el servidor se niega a arrancar sin uno de al menos 32 caracteres y
  el registro de acceso está apagado para que el token no aparezca en la consola.
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

| Comando | Resultado |
|---|---|
| `python -m pytest -q` | `24 passed`, rc=0 |
| `python -m probe.server` sin `SONDA_TOKEN`, acotado con `timeout 10` | rc=1 antes del corte, con `ValueError: SONDA_TOKEN must be at least 32 URL-safe characters`; el proceso no queda esperando conexiones |
| Cliente MCP contra `/mcp/<token>` sobre el servidor real, acotado con `timeout 15` | lista las cuatro herramientas; `list_proposals` y `save_evaluation` sin error; `get_proposal` de una propuesta fuera de alcance devuelve error |
| `POST /mcp` y `POST /mcp/<token inválido>` | 404 en ambos casos |
| Recuento del token en el log del servidor | 0 apariciones |
| `python -m probe.export` | llamadas registradas `[list_proposals ok, save_evaluation ok, get_proposal error]`; la evaluación guardada se recupera; el volcado no contiene ninguna dirección de correo |

Las pruebas cubren: determinismo y marcado sintético del conjunto de datos, separación de
contactos, idempotencia de la siembra, paginación completa de las 100 propuestas sin duplicados,
ausencia de contacto en el detalle, rechazo de identificadores fuera de alcance, persistencia de
la evaluación tras reabrir la base, anotaciones de lectura y escritura de cada herramienta,
registro de todas las llamadas, rechazo de un token débil, 404 sin token válido y rechazo de una
cabecera `Host` ajena.

Limitación: todo esto ocurrió en `127.0.0.1`. No demuestra nada sobre el comportamiento detrás de
una exposición pública ni sobre ChatGPT.

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
M2 del relevamiento); sonda ejecutándose en el Windows local; exposición HTTPS elegida por el
humano entre las opciones del relevamiento.

**Mecanismo.** El del `CHECKPOINT_HUMANO.md` de esta unidad: arranque de la sonda con token nuevo
y base vacía, configuración de la app, una conversación con cuatro peticiones literales fijadas
allí, un intento con capacidad inválida, exportación de la evidencia del lado del servidor y
devolución de la evidencia solicitada.

**Criterio discriminante de éxito.** Se cumplen los cinco:

- E1 (C1.1) La exportación registra llamadas `list_proposals` correctas cuyas páginas cubren las
  100 propuestas en alcance, y la respuesta de ChatGPT informa 100 propuestas con primera `P-001`
  y última `P-100`.
- E2 (C1.2) La exportación registra `get_proposal` correcta de `P-042`; el texto que ChatGPT
  muestra coincide con el original almacenado y la respuesta no contiene ningún dato de contacto.
- E3 (C1.3) La exportación registra `save_evaluation` correcta sobre `P-042` y una
  `get_evaluations` posterior también correcta, y la evaluación aparece almacenada en la
  exportación.
- E4 (C1.4) Con la capacidad inválida, ChatGPT no obtiene herramientas ni datos, y la exportación
  no registra ninguna llamada originada en ese intento; además, una petición HTTP sin token
  contra la URL pública se rechaza.
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

No existe una tercera categoría: si la ejecución no puede completarse por el plan de la cuenta,
eso es fallo del mecanismo en esa cuenta y termina U1 como incompatibilidad documentada, con la
condición faltante identificada.

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
