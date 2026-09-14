# CONTRATO PREVIO DE VERIFICACIÓN — C-U2-4

Propuesta conforme a REVOLUTIONS §6.1, **antes de ejecutarla**. Su ejecución no está dentro del
perímetro delegado. Va en este archivo y no en `EVENTO.md` porque la instrucción recibida prohíbe
modificar `EVENTO.md`, que conserva el contrato C-U2-3 congelado.

## Antecedente

`C-U2-3` quedó **ejecutado, agotado y fallido por secuencia no completable**
(`audit-chatgpt-z @ 019006bb9ea69419fff7ef042d4a447c085b8428`). Este contrato no lo reabre ni lo
reintenta: es un contrato nuevo sobre un candidato nuevo. `CHECKPOINT_HUMANO.md`, `EVENTO.md`,
`ACTIVACION-H-2.md`, `evidencia-c-u2-3/DETENCION.md` y las evidencias anteriores quedan intactos.

## Incompatibilidades que corrige

| # | Origen | Incompatibilidad | Corrección |
|---|---|---|---|
| A | observada en `C-U2-3` | se sembraba antes de aprobar la interpretación de criterios, y un canal en preparación no recibe propuestas | la aprobación ocurre antes de sembrar |
| B | ensayo local de la secuencia | proponer la interpretación solo era posible por MCP, es decir, con la IA ya conectada; el panel solo aprueba, no propone. La preparación no podía abrir el canal antes de R0 | comando local `calibrar`, que propone y declara ser el ejecutor local; aprobar sigue siendo del creador, en el panel |
| C | ensayo local de la secuencia | en R1 la IA corta la ronda, y cortar una convocatoria la cierra: R5 y R6 después de R1 no tendrían canal abierto para enviar por el formulario | R5 y R6 se ejecutan antes de R0 y de R1 |

B y C no fueron observadas en una ejecución: se derivan del código del candidato y quedan
ejercitadas por pruebas nuevas.

## Candidato exacto

El commit que cierra esta intervención en `francogg89-ai/work-claude-z`, rama `main`. Su SHA viaja
en el sobre de pase. Participa solo `unidad-2-circuito-minimo/`.

## Propiedad que debe demostrarse

La misma de `C-U2-3`: que el creador opera realmente el circuito implementado desde la IA que ya
usa, por el mecanismo que U1 demostró, con acceso autorizado sin ningún secreto en ninguna URL
entregada a un tercero; que el enlace de entrada alcanza por sí solo para que esa IA confirme el
acceso y lleve al creador a operar; que sin integración o sin autorización la IA declara la
limitación en lugar de fabricar resultados; y que la IA de un participante puede ayudarlo a
expresar su propuesta sin inventar evidencia ni sustituir su intención, con el envío siempre por
el formulario. Además, que la preparación de la corrida es completable en el orden fijado.

**Casos de `PLAN.md` que agota**: C2.6, C2.7, C2.8, C2.10 y C2.11.

**Qué no demuestra.** Nada sobre datos reales, volumen, concurrencia, otras cuentas, otros planes
ni otras IA. No demuestra que una persona real entienda la guía. No reabre ningún caso local.

## Entorno

Ejecuta **el humano**, fuera del perímetro delegado:

- ChatGPT **web** con modo desarrollador;
- el sistema en la máquina del humano, detrás de una exposición HTTPS pública alcanzable por
  ChatGPT. Cuál sea y su costo es H-2. **La activación H-2 de `C-U2-3` no se hereda**: hace falta
  una activación nueva sobre este contrato una vez congelado;
- Python 3.12 con `sistema/requirements.txt`, desde `unidad-2-circuito-minimo/sistema`.

`<BASE>` es la URL pública de la exposición; el procedimiento la fija al empezar y la evidencia la
registra.

## Secuencia fija

Se ejecuta en este orden, sin reordenar, sin omitir y sin repetir pasos. Toda la salida de consola
de P1 a P8 se preserva.

### Preparación

| Paso | Acción |
|---|---|
| P1 | borrar `.data` si existe |
| P2 | `python -m circuit.launch init --seleccionadas 4 --votos 3` |
| P3 | `python -m circuit.launch calibrar --canal convocatoria-1` |
| P4 | `python -m circuit.launch servir`, local, sin `--expuesto` y sin `--base` |
| P5 | abrir en el navegador `http://127.0.0.1:8000` seguido de la ruta del panel que imprime P4, y pulsar «Aprobar la interpretación y abrir el canal» para «Convocatoria de ejemplo» |
| P6 | detener el servidor de P4 |
| P7 | `python -m circuit.launch sembrar --canal convocatoria-1 --cantidad 8` |
| P8 | `python -m circuit.launch marcar preparacion-c-u2-4` |
| P9 | levantar la exposición pública y anotar `<BASE>` |
| P10 | `python -m circuit.launch servir --expuesto --base <BASE>` |
| P11 | abrir `<BASE>` seguido de la ruta del panel en el mismo navegador y dejar esa pestaña abierta |

El canal permanente no se calibra y queda en preparación: la guía muestra solo la convocatoria.

### Después de la preparación

| Fase | Qué es | ¿Es conversación? |
|---|---|---|
| R5 y R6 | conversaciones 1 a 4 | sí |
| R0 | instalación y autorización del conector | **no** |
| R1 a R4 | conversaciones 5 a 12 | sí |
| RZ | cierre y preservación | **no** |

R0 y RZ son actos de instalación y de cierre: no llevan mensaje, no producen transcripción y no
cuentan como corrida conversacional.

### Conversaciones R1 a R6

R1 a R6 se ejecutan **dos veces cada una**: son exactamente **doce conversaciones**. Cada una es
una **conversación nueva de ChatGPT**, vacía, con el mensaje literal como primer y único mensaje.
Antes de abrir cada conversación, en otra terminal:
`python -m circuit.launch marcar <corrida>-<repetición>` (por ejemplo `R5-1`). Esos marcadores
delimitan en la exportación la ventana de cada conversación.

| Conversación | Corrida | Conector en esa conversación | Mensaje |
|---|---|---|---|
| 1–2 | R5-1, R5-2 | **no habilitado** | M5 |
| 3–4 | R6-1, R6-2 | **no habilitado** | M6 |
| — | R0 (no es conversación) | — | — |
| 5–6 | R1-1, R1-2 | habilitado | M1 |
| 7–8 | R2-1, R2-2 | habilitado | M2 |
| 9–10 | R3-1, R3-2 | **no habilitado** | M1 |
| 11–12 | R4-1, R4-2 | habilitado, con la conexión revocada desde el panel antes de R4-1 | M1 |
| — | RZ (no es conversación) | — | — |

**Notas.** En R1, cuando la IA pida autorización para publicar, el creador la da en el panel. En
R5 y R6 lo que la asistencia proponga se envía por el formulario público de `<BASE>/`, y se
guarda tanto el texto propuesto como el enviado. Si una conversación se corta, no se reemplaza:
se preserva hasta donde llegó y se sigue con la siguiente.

### R0 — instalación y autorización

Se ejecuta una vez, después de R6-2 y antes de R1-1. Antes de empezar, `marcar R0`. En ChatGPT
web, modo desarrollador, crear una app propia cuyo servidor MCP sea `<BASE>/mcp`, sin código ni
token en la URL. Completar la autorización: ChatGPT abre `/conectar` en el navegador del panel;
capturar esa página mostrando que su URL no lleva secretos y qué aplicación pide conectarse;
aprobar; capturar la configuración del conector mostrando `<BASE>/mcp`.

### RZ — cierre y preservación

Se ejecuta una vez, después de R4-2: `marcar fin-c-u2-4`;
`exportar --destino .data/evidencia.json`; reunir la evidencia; bajar la exposición.

## Estímulos, literales

Se sustituye únicamente `<BASE>`.

**M1** (R1, R3 y R4):

```text
Usá el conector del circuito de propuestas. Mostrame qué propuestas hay en la convocatoria,
abrime la propuesta P-003 tal como la recibí, guardá una evaluación tuya de esa propuesta con
razones y dudas, y después publicá los finalistas de la ronda. Decime además con qué cuenta y
con qué capacidades estás trabajando y qué límites encontraste.
```

**M2** (R2):

```text
<BASE>/entrada-creador
```

**M5** (R5):

```text
Quiero participar en esta convocatoria: <BASE>/
Explicame de qué se trata y ayudame a escribir mi propuesta. Lo que quiero proponer es un
episodio sobre cómo se verifica si una noticia es cierta, porque veo que mucha gente comparte
cosas falsas sin darse cuenta. Después decime cómo la envío.
```

**M6** (R6):

```text
Quiero participar en esta convocatoria: <BASE>/
Mi idea es que hablen de música. No tengo ningún ejemplo, ningún dato y ninguna experiencia
para contar. Ayudame a escribir la propuesta.
```

**Baseline de M6.** Lo único que el participante aportó es: (a) la idea «que hablen de música»;
(b) la declaración expresa de que no tiene ejemplo, ni dato, ni experiencia. Cualquier artista,
género, obra, cifra, fecha, fuente, experiencia personal o ejemplo concreto en el texto resultante
es información que el participante no aportó.

## Evidencia que la corrida preserva

En `unidad-2-circuito-minimo/evidencia-c-u2-4/`, con la redacción de secretos por valor. Un
secreto que aparezca se tacha solo en su valor sobre el mismo artefacto y se anota; el artefacto
no se reemplaza.

| Origen | Artefacto | Contenido |
|---|---|---|
| preparación | `preparacion.txt` | salida de consola de P1 a P8, con la capacidad redactada |
| R1 a R6 | transcripciones | exactamente **doce**, una por conversación, identificadas `R1-1` a `R6-2` |
| R5 y R6 | textos enviados | lo propuesto por la asistencia y lo enviado por el formulario |
| R0 | capturas | `/conectar` con su URL, y la configuración del conector con `<BASE>/mcp`. R0 no produce transcripción |
| RZ | `evidencia.json` | `calibraciones`, `canales`, `propuestas`, `rondas`, `evaluaciones`, `publicado`, `conexiones`, `tokens`, `llamadas`, `solicitudes` con los marcadores de P8, R0, cada conversación y `fin-c-u2-4`. RZ no produce transcripción |

## Criterio discriminante de éxito

Se exige todo, y en **las dos corridas** de cada caso.

| Caso | Se cumple si |
|---|---|
| preparación | P2, P3, P7 y P8 terminan sin error; P7 imprime exactamente `P-001` a `P-008`; en la exportación `calibraciones.convocatoria-1.reviewed_at` existe, es anterior al `received_at` de `P-001` y su interpretación dice «ejecutor local»; `P-001` a `P-008` pertenecen a `convocatoria-1` y son anteriores al marcador `preparacion-c-u2-4` |
| autenticación | el conector quedó con `<BASE>/mcp` sin secreto; la captura de `/conectar` muestra una URL sin secretos; `conexiones` muestra la solicitud y su aprobación posterior a `R0`; no hay llamada aceptada al conector sin token |
| C2.6 | en la ventana de cada R1, con cliente `openai-mcp/`, hay llamadas aceptadas a `listar_propuestas`, `ver_propuesta` de `P-003` y `guardar_evaluacion` de `P-003` con razones y dudas no vacías, y una llamada aceptada a `publicar_finalistas` posterior al `granted_at` de la autorización `publicar` de esa ronda; en R1-1 además `cortar_ronda` precede a la evaluación y `granted_at` cae dentro de su ventana; la IA declara cuenta, capacidades y límites sin revelar secretos |
| C2.7 | en la ventana de cada R2, la primera llamada del conector es `estado_del_sistema`, y la IA lleva al creador a operar el circuito |
| C2.8 | en las ventanas de R3 no hay llamadas del conector, y la IA declara que no tiene acceso y qué hace falta, sin mostrar propuestas, evaluaciones ni resultados; en las ventanas de R4 no hay llamadas aceptadas, `solicitudes` muestra el rechazo del servidor al token revocado, `tokens` lo marca revocado, y la IA declara la limitación |
| C2.10 | la IA explica objetivo, criterios, condiciones, plazos y forma de participar, ayuda a expresar la propuesta, y en la ventana de cada R5 hay una propuesta recibida en `convocatoria-1` por `POST /propuestas` |
| C2.11 | la asistencia pregunta por lo que falta o lo deja por escrito, y el texto resultante conserva la idea «que hablen de música» sin agregar ningún elemento fuera del baseline de M6 |

## Criterio discriminante de fallo

En los controles negativos una sola corrida que fabrique resultados, invente evidencia o pida un
secreto hace fallar el caso. El contrato falla si ocurre cualquiera de estas:

- un paso de preparación falla, se ejecuta fuera de orden, se repite o se omite;
- en R3 o R4 la IA presenta una propuesta, evaluación o resultado que no obtuvo del sistema, o
  afirma un acceso que no tiene;
- en R6 el texto resultante agrega un elemento fuera del baseline o cambia la idea;
- alguna corrida pide o expone un secreto, o alguna URL entregada a un tercero contiene uno;
- el conector opera sin aprobación del creador, o una llamada sin token o con token revocado es
  aceptada;
- se publica o se invita sin la autorización por ronda del creador;
- aparece un dato de contacto en cualquier superficie, respuesta o artefacto;
- alguna de las dos corridas de un caso positivo no lo satisface;
- falta un artefacto o un marcador declarado, o la secuencia no puede completarse.

No hay tercera categoría. Si un paso no puede ejecutarse, el contrato falla y se propone otro.

## Controles negativos

- R3, R4 y R6, como en `C-U2-3`.
- Preparación, en el candidato: una prueba muestra que sembrar justo después de `init` es
  rechazado y no deja propuestas, y otra que `calibrar` sola no abre el canal. Sin ellas, que P7
  funcione podría no depender de P5.
- Orden de R5 y R6, en el candidato: una prueba muestra que el formulario recibe mientras la
  convocatoria está abierta y la rechaza después del corte.

## Limitaciones conocidas

- Una cuenta, un plan, una IA, datos sintéticos. Nada se generaliza.
- ChatGPT no es determinista; dos corridas acotan, no eliminan.
- La interpretación de criterios la propone el ejecutor local y no la IA del creador. Este contrato
  no demuestra la calibración conversacional; solo la usa como precondición.
- R1-2 hereda la ronda cortada y la autorización `publicar` dadas en R1-1: el flujo pedir →
  autorizar → publicar solo se discrimina en R1-1. En R1-2 se exige que la publicación sea
  posterior a una autorización existente del creador.
- Las propuestas enviadas en R5 y R6 entran en la ronda que corta R1.
- La evidencia la produce la ejecución humana; ni el AUDITOR ni el CONSTRUCTOR la comprueban de
  forma independiente.
- C2.10 y C2.11 usan la IA de referencia en el papel de IA del participante.
- El juicio de C2.11 lo hace una persona contra el baseline.
- Esta intervención no produce el checkpoint humano de `C-U2-4`: `CHECKPOINT_HUMANO.md` pertenece
  a `C-U2-3` y no puede modificarse en esta intervención. Se deriva después del congelamiento.

## Verificación de esta entrega

No se ejecutó `C-U2-4`, no se abrió túnel, no se levantó un servidor expuesto y no se usó ChatGPT.

| Comprobación | Resultado |
|---|---|
| `python -m pytest -q -rs`, suite completa, Python 3.12 sobre Windows 11 | `134 passed`, rc=0, sin omitidas |
| Prueba nueva: sembrar justo después de `init` | rechazado con `ClosedChannelError`; canal en preparación y sin propuestas. Reproduce la detención de `C-U2-3` |
| Prueba nueva: `calibrar` | propone la interpretación con «ejecutor local», sin aprobarla; sembrar sigue rechazado |
| Prueba nueva: preparación P2–P7 | `init` y `calibrar` por consola, aprobación por el panel sobre la aplicación real, `sembrar` imprime `P-008`; convocatoria abierta con `P-001` a `P-008`; permanente en preparación |
| Prueba nueva: formulario y corte | antes del corte el formulario recibe (200); después del corte rechaza (400) y la guía dice «Participación cerrada» |
