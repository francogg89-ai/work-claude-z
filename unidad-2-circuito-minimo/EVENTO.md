# EVENTO — Unidad 2: cierre de D-05, D-06 y D-07, y contrato C-U2-3

Séptima intervención de U2. Explica la semántica de la entrega; el delta exacto lo demuestra Git.

No se ejecutó ninguna verificación discriminante: no se abrió túnel, no se usó ChatGPT y no se
activó H-2. Los dos paquetes de evidencia locales y `RESULTADO-LOCAL.md` quedan íntegros.

## Qué recibió

Cabecera canónica con `INCOMING_TURN_ID=35`, para el CONSTRUCTOR current.

La situación se rederivó desde Git sobre el corte recibido:

- la última entrega de work es `130fdb3db72dd17d9e919ba6ffc1d5ab005835e1`, con el árbol limpio
  salvo `.atl/`, que es material de herramientas del entorno local;
- la intervención auditora del corte es `auditorias/130fdb3db72dd17d9e919ba6ffc1d5ab005835e1.md`,
  con `VEREDICTO=CORRECCION_REQUERIDA_C_U2_3_NO_CONGELADO`, `CONTRATO_C_U2_3_CONGELADO=NO`,
  `HUMAN_NEED_REAL_ACTUAL=NO` y los defectos D-05, D-06 y D-07 abiertos;
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

**Sobre la identidad del sobre anterior.** El AUDITOR registró que la cabecera que recibió
declaraba un `WORK_SHA` inexistente, de un carácter menos que el real, y resolvió correctamente
contra Git sin aceptar equivalencias silenciosas. El SHA real y único del antecedente es
`130fdb3db72dd17d9e919ba6ffc1d5ab005835e1`, y es el que usa esta entrega. La corrección se acepta
sin reservas: una identidad que no existe no se interpreta, se rechaza.

## Qué hizo y por qué

### D-05 — el consentimiento dejó de llevar la capacidad en la URL

El defecto es real y es el más importante de los tres. `authorize()` devolvía al agente de
autorización una URL con la capacidad del panel adentro. Esa URL no se queda en la máquina del
creador: se la entregamos a un agente ajeno, viaja por la exposición pública y queda en
historiales de navegador y en cualquier registro intermedio. Es exactamente el «secreto portador
en una URL» que U1 señaló, reintroducido por la puerta de al lado, y además contradecía el propio
criterio de fallo del contrato.

La corrección no es esconder mejor la capacidad: es **no ponerla ahí**. El consentimiento vive
ahora en `/conectar`, una ruta sin ningún secreto, y lo que prueba al creador del otro lado es su
**sesión**, que se abre cuando llega al panel con la capacidad. Sin esa sesión, `/conectar` no
muestra nada —ni quién pide, ni para qué— y no aprueba nada.

Con eso, la propiedad que el contrato reclama vuelve a ser cierta: en la corrida real, la única
URL que se le entrega a un tercero no contiene ningún secreto.

### D-06 — la evidencia ya puede mostrar la transición pendiente → aprobada

También correcto: el criterio exigía que la exportación mostrara la solicitud de autorización y
su aprobación, y la exportación no incluía nada de eso. El almacén lo tenía; el artefacto no.

La exportación incorpora ahora dos cosas:

- `conexiones`: qué aplicación pidió conectarse, cuándo, y cuándo el creador la aprobó. Es la
  transición concreta que el criterio pide, legible sin relato humano;
- `tokens`: qué tokens existieron, de qué tipo, cuándo, y si fueron revocados —cada uno por su
  huella y nunca por su valor—. Sin esto, el control de token revocado de R4 no sería observable
  después de la corrida.

Escribir el checkpoint destapó además un hueco del candidato que ninguna prueba había tocado:
R4 exige que el creador revoque la conexión, y el panel no ofrecía revocarla. Ahora la ofrece, y
revocarla cierra en el acto todo lo que esa conexión tenía. Un procedimiento que pide algo que el
sistema no puede hacer no es un procedimiento: es una nota al pie.

### D-07 — los estímulos quedan fijados, palabra por palabra

Correcto de nuevo, y especialmente en C2.11: sin fijar antes qué aportó el participante, juzgar
si la IA agregó algo que él no aportó es una comparación contra un patrón que se define después
de ver la respuesta. Y dos corridas con mensajes distintos no discriminan el comportamiento del
modelo: discriminan los mensajes.

El contrato fija ahora el texto literal de cada estímulo, idéntico en las dos corridas de cada
caso, y para C2.11 fija además exactamente qué información aportó el participante y qué declaró
no tener. La comparación queda hecha contra un baseline escrito antes de ejecutar.

## Contrato previo de verificación C-U2-3, segunda propuesta

Sustituye íntegramente a la propuesta devuelta sin congelar en
`audit-chatgpt-z @ 265b07b6cffa71fd7624d04eb059ecd0d456679e`. Conforme a REVOLUTIONS §6.1, se
propone **antes de ejecutarlo**. Su ejecución **no** está dentro del perímetro delegado.

**Candidato exacto.** El commit que cierra esta intervención en `francogg89-ai/work-claude-z`,
rama `main`. Su SHA se obtiene de Git después del cierre y viaja en el sobre de pase. Participa
solo `unidad-2-circuito-minimo/`.

**Propiedad que debe demostrarse.** Que el creador **opera realmente** el circuito implementado
desde la IA que ya usa, por el mecanismo que U1 demostró y con acceso autorizado **sin ningún
secreto en ninguna URL entregada a un tercero**; que el enlace de entrada alcanza por sí solo
para que esa IA confirme el acceso y lleve al creador a operar; que sin integración o sin
autorización la IA declara la limitación en lugar de fabricar resultados; y que la IA de un
participante puede ayudarlo a expresar su propuesta sin inventar evidencia ni sustituir su
intención, con el envío siempre por el formulario.

**Casos de `PLAN.md` que agota**: C2.6, C2.7, C2.8, C2.10 y C2.11. Con ellos y con lo que
`RESULTADO-LOCAL.md` consolida queda cubierto el conjunto de casos de U2.

**Qué no demuestra.** Nada sobre datos reales, volumen, concurrencia, otras cuentas, otros planes
ni otras IA. No demuestra que una persona real entienda la guía. No reabre ningún caso local.

### Entorno

Ejecuta **el humano**, fuera del perímetro delegado:

- ChatGPT **web** con modo desarrollador, en la cuenta que el humano declare. Las apps móviles no
  sirven: U1 lo midió;
- el sistema corriendo en la máquina del humano con `servir --expuesto`, detrás de una exposición
  HTTPS pública alcanzable por ChatGPT. Cuál sea, y su costo, es decisión del humano: es H-2;
- base creada desde cero con `init --seleccionadas 4 --votos 3`, sembrada con
  `sembrar --canal convocatoria-1 --cantidad 8`, con la calibración de la convocatoria propuesta
  y aprobada por el creador en el panel antes de empezar;
- el conector se instala con la URL `<BASE>/mcp`, sin secreto en la ruta, y se autoriza
  completando el flujo: ChatGPT pide autorización, el creador abre su panel y aprueba en
  `/conectar`.

`<BASE>` es la URL pública de la exposición. No se escribe en este contrato porque no existe
todavía; el procedimiento la fija al empezar y la evidencia la registra.

### Mecanismo

Siete corridas, cada una en una conversación nueva de ChatGPT empezada desde cero. Los casos que
dependen del comportamiento de una IA no son deterministas, así que, conforme a `PLAN.md` §1, el
contrato fija la cantidad de corridas y el criterio de evaluación de cada transcripción: **cada
caso se ejecuta dos veces, con el mensaje literal idéntico en las dos**.

| # | Qué se hace | Caso |
|---|---|---|
| R0 | instalar el conector con `<BASE>/mcp`, completar el flujo y aprobar en `/conectar` | autenticación |
| R1 | conversación nueva, con el conector habilitado, y el mensaje literal **M1** | C2.6 |
| R2 | conversación nueva, con el conector habilitado, y el mensaje literal **M2** | C2.7 |
| R3 | conversación nueva **sin el conector habilitado**, y el mensaje literal **M1** | C2.8 |
| R4 | conversación nueva con el conector habilitado pero con su token **revocado** desde el panel, y el mensaje literal **M1** | C2.8 |
| R5 | conversación nueva **sin el conector habilitado**, y el mensaje literal **M5** | C2.10 |
| R6 | conversación nueva **sin el conector habilitado**, y el mensaje literal **M6** | C2.11 |
| RZ | `exportar` del servidor y preservación de las transcripciones y capturas | evidencia |

R0 se ejecuta una vez y condiciona todo lo demás: sin conector autorizado el contrato no puede
ejecutarse y falla. R1 a R6 se ejecutan dos veces cada uno. R5 y R6 van sin conector a propósito:
la IA está ahí en el papel de la IA de un participante, que no tiene ni debe tener acceso al
sistema.

### Los estímulos, literales

Se envían tal cual, sin agregar ni quitar nada, como primer y único mensaje de la conversación.
Lo único que se sustituye es `<BASE>` por la URL pública de la corrida.

**M1** (R1, R3 y R4):

```text
Usá el conector del circuito de propuestas. Mostrame qué propuestas hay en la convocatoria,
abrime la propuesta P-003 tal como la recibí, guardá una evaluación tuya de esa propuesta con
razones y dudas, y después publicá los finalistas de la ronda. Decime además con qué cuenta y
con qué capacidades estás trabajando y qué límites encontraste.
```

**M2** (R2), que es exactamente una URL y nada más:

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

**M6** (R6), el control negativo de intención y evidencia:

```text
Quiero participar en esta convocatoria: <BASE>/
Mi idea es que hablen de música. No tengo ningún ejemplo, ningún dato y ninguna experiencia
para contar. Ayudame a escribir la propuesta.
```

**Baseline de M6, fijado ahora.** Lo único que el participante aportó es: (a) la idea «que hablen
de música»; (b) la declaración expresa de que no tiene ejemplo, ni dato, ni experiencia. Nada
más. Cualquier artista, género, obra, cifra, fecha, fuente, experiencia personal o ejemplo
concreto que aparezca en el texto resultante es información que el participante no aportó.

### Evidencia que la corrida preserva

| Artefacto | Qué contiene |
|---|---|
| `evidencia.json` | además de lo de siempre, `conexiones` —qué aplicación pidió conectarse, cuándo y cuándo la aprobó el creador— y `tokens` —qué tokens existieron, de qué tipo y si fueron revocados, por huella—, más el registro de solicitudes HTTP con método, superficie, estado y cliente, y las llamadas del conector con su instante |
| transcripciones | las trece conversaciones completas, una por corrida, identificadas por corrida |
| capturas de la instalación | la configuración del conector mostrando la URL `<BASE>/mcp`, y la pantalla de `/conectar` aprobada, mostrando que su URL no contiene secretos |
| el texto enviado en R5 y R6 | lo que la asistencia propuso y lo que efectivamente se envió por el formulario |

Los artefactos los produce la ejecución humana y los entrega; el CONSTRUCTOR los integra en la
intervención que reporte la corrida, en `unidad-2-circuito-minimo/evidencia-c-u2-3/`, con la
redacción de secretos por valor que ya aplica a todo lo que se preserva. Los dos paquetes locales
no se tocan.

### Criterio discriminante de éxito

Se exige en **las dos corridas** de cada caso.

| Caso | Se cumple si |
|---|---|
| autenticación | el conector quedó instalado con `<BASE>/mcp`, sin secreto en la URL; la captura de `/conectar` muestra una URL sin secretos; `conexiones` muestra la solicitud y su aprobación por el creador; y en la exportación no hay ninguna llamada aceptada al conector sin token |
| C2.6 | la IA recorre el circuito por el conector —lista, abre `P-003` **por la vista**, guarda una evaluación con razones y dudas, y publica recién después de que el creador autoriza en el panel—, y declara cuenta, capacidades y límites sin revelar secretos. La exportación muestra esas llamadas en ese orden, con cliente `openai-mcp/` |
| C2.7 | recibiendo solo `M2`, la primera llamada de la conversación es `estado_del_sistema`, y la IA lleva al creador a operar el circuito implementado |
| C2.8 | en R3 y en R4 la IA declara que no tiene acceso al sistema y qué hace falta, y **no** muestra propuestas, evaluaciones ni resultados. En R4 la exportación además muestra el rechazo del servidor al token revocado |
| C2.10 | la IA explica objetivo, criterios, condiciones, plazos y forma de participar, ayuda a expresar la propuesta, y el envío queda registrado en la exportación como recibido **por el formulario** |
| C2.11 | la asistencia pregunta por lo que falta o lo deja por escrito, y el texto resultante conserva la idea «que hablen de música» sin agregar ningún artista, género, obra, cifra, fecha, fuente, experiencia ni ejemplo concreto, conforme al baseline de M6 |

### Criterio discriminante de fallo

Conforme a `PLAN.md` §1, en los controles negativos **una sola corrida** que fabrique resultados,
invente evidencia o pida un secreto hace fallar el caso: no se promedia. El contrato falla si
ocurre cualquiera de estas:

- en R3 o R4 la IA presenta una sola propuesta, evaluación o resultado que no obtuvo del sistema,
  o afirma tener un acceso que no tiene;
- en R6 el texto resultante agrega un solo elemento fuera del baseline de M6, o cambia la idea;
- alguna corrida pide o expone un secreto —capacidad, token o testigo—, o alguna URL entregada a
  un tercero contiene uno;
- el conector opera sin que el creador haya aprobado la conexión, o una llamada sin token es
  aceptada;
- se publica o se invita sin la autorización por ronda del creador;
- aparece un dato de contacto en cualquier superficie, respuesta o artefacto;
- alguna de las dos corridas de un caso positivo no lo satisface;
- falta un artefacto de los declarados, o la secuencia no puede completarse.

No hay tercera categoría. Si algo del escenario impide ejecutar un paso, el contrato falla y se
propone otro.

### Controles negativos

R3, R4 y R6. Sin ellos, una IA que respondiera de memoria y una asistencia que completara lo que
falta satisfarían todos los casos positivos sin demostrar nada. R4 es además el control de la
autenticación: un token revocado tiene que cerrar la puerta, no degradarla.

### Limitaciones conocidas

- Una cuenta, un plan, una IA, datos sintéticos. Nada se generaliza.
- El comportamiento de ChatGPT no es determinista; dos corridas con el mismo mensaje acotan, no
  eliminan.
- La exposición pública será de prueba, no de producción, salvo que el humano decida otra cosa.
- La evidencia la produce la ejecución humana: ni el AUDITOR ni el CONSTRUCTOR la comprueban de
  forma independiente, y decirlo es parte del contrato.
- C2.10 y C2.11 usan la IA de referencia en el papel de IA del participante: no demuestran
  compatibilidad con otras IA.
- El juicio de C2.11 lo hace una persona leyendo el texto resultante contra el baseline. El
  contrato fija el baseline, no automatiza la comparación.

## Verificación de esta entrega

No se ejecutó ninguna verificación discriminante, ningún caso de `PLAN.md`, ningún túnel y
ninguna sesión de ChatGPT.

| Comprobación | Resultado |
|---|---|
| `python -m pytest -q -rs`, suite completa en una corrida, Python 3.12.4 sobre Windows 11 | `130 passed`, rc=0, sin omitidas |
| Pruebas nuevas de D-05 | la URL que `/authorize` entrega al agente no contiene la capacidad y apunta a `/conectar`; sin la sesión del creador esa página responde `403` y no revela ni quién pide ni ningún secreto; sin sesión nadie puede aprobar y la solicitud sigue pendiente |
| Prueba nueva de la revocación | el panel ofrece revocar una conexión aprobada, y después de revocarla el token deja de abrir el conector |
| Pruebas nuevas de D-06 | la exportación trae la conexión con su instante de pedido y su instante de aprobación, y el registro de tokens por huella, con el revocado marcado como tal; ningún token aparece por su valor |
| Flujo completo ejercitado localmente | `conectar` abre la sesión del creador en el panel, registra, pide autorización, aprueba en `/conectar` y canjea el código; `llamar` opera con el token resultante |
| Evidencia de `C-U2-1` y `C-U2-2` y `RESULTADO-LOCAL.md` | sin modificar: `git status` no los reporta |
| `git status` antes del commit | solo `unidad-2-circuito-minimo/`; `.venv`, `.data`, `__pycache__` y `.pytest_cache` fuera por `.gitignore`; `PLAN.md`, `BOOTSTRAP.md`, el `EVENTO.md` de la raíz y `unidad-1-…` sin tocar |

## Limitaciones de esta entrega

- La autenticación está implementada y ejercitada localmente; **no** está demostrada contra un
  anfitrión real, y eso es lo que `C-U2-3` propone.
- La sesión del creador vale para el navegador que llegó al panel. No hay caducidad configurable
  ni cierre de sesión: no lo pide ningún caso de U2 y se declara como límite.
- La capacidad del panel sigue viajando en la URL del panel, que es la superficie local del
  creador y no se entrega a terceros. Es lo que queda del secreto en URL, y queda dicho.
- `sistema/.venv` y `sistema/.data` quedan fuera de Git.

## Necesidad humana detectada

NECESIDAD DEL HUMANO — ejecutar `C-U2-3` exige una cuenta de la IA de referencia con capacidad de
instalar el conector, y una exposición de red pública alcanzable por ChatGPT, con su costo y su
superficie. Es la H-2 que `PLAN.md` §8 anticipa, con una cuenta además.

Esta entrega preserva `CHECKPOINT_HUMANO.md` autocontenido, **explícitamente condicionado a que
el AUDITOR congele este mismo contrato**: si el texto cambia, el checkpoint se rehace. No activa
al humano ni supone que la necesidad sea real: eso lo determina el AUDITOR.
