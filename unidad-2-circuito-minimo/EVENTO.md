# EVENTO — Unidad 2: autenticación del extremo y contrato C-U2-3

Sexta intervención de U2. Explica la semántica de la entrega; el delta exacto lo demuestra Git.

No se ejecutó ninguna verificación discriminante: no se abrió túnel, no se usó ChatGPT y no se
activó H-2. `C-U2-2` está agotado con éxito y no se repite.

## Qué recibió

Cabecera canónica con `INCOMING_TURN_ID=33`, para el CONSTRUCTOR current.

La situación se rederivó desde Git sobre el corte recibido:

- la última entrega de work es `d7d405c2d8a82e6d81e5af5d8b6d3383375a8810`, con el árbol limpio
  salvo `.atl/`, que es material de herramientas del entorno local;
- la intervención auditora del corte es `auditorias/d7d405c2d8a82e6d81e5af5d8b6d3383375a8810.md`,
  con `CONTRATO_C_U2_2_RESULTADO=EXITO`, `CONTRATO_C_U2_2_AGOTADO=SI`, `C2_3=EXITO`,
  `D_04=CERRADO`, `EVIDENCIA_C_U2_1=INTACTA`, `HUMAN_NEED_REAL_ACTUAL=NO` y `U2_CERRADA=NO`;
- `PERIMETRO_ULTIMA_MODIFICACION=CONSTITUCION`, sin deltas.

La próxima acción que fijó el AUDITOR: integrar durablemente el éxito local, completar el
candidato necesario para la autenticación real, y proponer —sin ejecutar— un contrato §6.1 para
los casos reales pendientes.

## Qué hizo y por qué

### La autenticación del extremo, resuelta

U1 cerró dejando que el acceso por capacidad en la URL **no es apto para el producto**. Esta
entrega lo resuelve donde se planteó, y no era una decisión abierta: el producto probado admite
exactamente dos formas de conectar una app propia —URL pública sin autenticación, u OAuth—, así
que «autenticación sin secreto en la URL» significa el flujo de autorización de MCP y nada más.

`circuit/auth.py` es ese flujo, con el almacén detrás. El extremo del conector pasó a `/mcp`, sin
capacidad en la ruta: una llamada sin token responde `401` con `WWW-Authenticate`, que es donde el
anfitrión aprende a dónde autorizarse. El anfitrión se registra solo, pide autorización, y ahí
está la decisión de forma que más importa:

**el consentimiento vive en el panel del creador.** No se agrega una pantalla de login nueva con
credenciales nuevas que guardar —que sería otro secreto más que el creador tiene que cuidar—: es
una decisión más en la superficie donde ya autoriza publicar e invitar. Quien llega al panel es el
creador, que es exactamente la frontera que el panel ya tenía. Registrarse no es autorizarse: un
cliente registrado no tiene nada hasta que el creador aprueba. Aprobar es lo que emite el código;
el código se gasta una vez; el intercambio con PKCE entrega el token.

Lo que **no** cambió, y conviene decirlo porque es lo que sostiene una propiedad de U1: tener
token no alcanza para publicar ni invitar. Eso sigue exigiendo la autorización del creador por
ronda, en el panel, porque U1 midió que la escritura se ejecuta sin confirmación de ChatGPT.

La capacidad sigue gobernando el panel. Es la superficie local del creador y no es lo que U1
señaló; queda declarada como tal en `ARQUITECTURA.md`.

### El éxito local, integrado durablemente

`RESULTADO-LOCAL.md` consolida qué dejó demostrado el bloque local, sobre qué candidato exacto,
con la identidad de los dos contratos, sus dos congelamientos, sus dos interpretaciones y sus dos
paquetes de evidencia. Existe porque `EVENTO.md` se reemplaza en cada entrega y el resultado de
una unidad no puede vivir solo en la entrega que lo produjo.

Los dos paquetes de evidencia se conservan: `evidencia/` documenta el fallo de `C-U2-1` y el
defecto D-04 que hizo visible, y `evidencia-c-u2-2/` documenta el éxito.

## Contrato previo de verificación C-U2-3

Contrato nuevo, conforme a REVOLUTIONS §6.1. Se propone **antes de ejecutarlo**; no se ejecutó
ninguna de sus mitades y no se ejecutará hasta que el AUDITOR lo congele. Su ejecución **no** está
dentro del perímetro delegado: exige una cuenta de la IA de referencia y una exposición de red
alcanzable, que son del humano.

**Candidato exacto.** El commit que cierra esta intervención en `francogg89-ai/work-claude-z`,
rama `main`. Su SHA se obtiene de Git después del cierre y viaja en el sobre de pase. Participa
solo `unidad-2-circuito-minimo/`.

**Propiedad que debe demostrarse.** Que el creador **opera realmente** el circuito implementado
desde la IA que ya usa, por el mecanismo que U1 demostró y con acceso autorizado sin secreto en la
URL; que el enlace de entrada alcanza por sí solo para que esa IA confirme el acceso y lleve al
creador a operar; que sin integración o sin autorización la IA declara la limitación en lugar de
fabricar resultados; y que la IA de un participante puede ayudarlo a expresar su propuesta sin
inventar evidencia ni sustituir su intención, con el envío siempre por el formulario.

**Casos de `PLAN.md` que agota**: C2.6, C2.7, C2.8, C2.10 y C2.11. Con ellos, y con lo que
`RESULTADO-LOCAL.md` consolida, queda cubierto el conjunto de casos de U2.

**Qué no demuestra.** Nada sobre datos reales, volumen, concurrencia, otras cuentas, otros planes
ni otras IA. No demuestra que una persona real entienda la guía. No reabre ningún caso local.

### Entorno

Ejecuta **el humano**, fuera del perímetro delegado:

- ChatGPT **web** con modo desarrollador, en la cuenta que el humano declare. Las apps móviles no
  sirven: U1 lo midió;
- el sistema corriendo en la máquina del humano con `servir --expuesto`, detrás de una exposición
  HTTPS pública alcanzable por ChatGPT. Cuál sea esa exposición, y su costo, es decisión del
  humano: es H-2;
- base creada desde cero y sembrada con datos sintéticos, con la convocatoria y el canal
  permanente abiertos por aprobación del creador antes de empezar;
- el conector se instala **con la URL `/mcp` del sistema y sin secreto en la ruta**, y se autoriza
  completando el flujo: ChatGPT pide autorización, el humano aprueba en el panel.

### Mecanismo

Cinco conversaciones nuevas de ChatGPT, cada una empezando desde cero. Los casos que dependen del
comportamiento de una IA no son deterministas, así que, conforme a `PLAN.md` §1, el contrato fija
la cantidad de corridas: **cada caso se ejecuta en dos conversaciones independientes**.

| # | Acción | Caso |
|---|---|---|
| R0 | instalar el conector con la URL `/mcp`, completar el flujo de autorización y aprobar en el panel | autenticación |
| R1 | conversación nueva: pedir en una frase breve que liste las propuestas, muestre una por la vista, guarde una evaluación, pida autorización para publicar y publique después de que el creador autorice en el panel | C2.6 |
| R2 | conversación nueva que recibe **solo** la URL del enlace de entrada del creador, sin ninguna otra instrucción | C2.7 |
| R3 | conversación nueva con el conector **no habilitado** en la sesión, pidiendo lo mismo que R1 | C2.8 |
| R4 | conversación nueva con el conector habilitado pero con el token **revocado** desde el panel, pidiendo lo mismo que R1 | C2.8 |
| R5 | conversación nueva actuando como IA de un participante, que recibe la URL de la guía pública y ayuda a escribir y enviar una propuesta | C2.10 |
| R6 | conversación nueva actuando como IA de un participante con una idea breve, sin ejemplo ni datos | C2.11 |
| RZ | `exportar` del servidor y preservación de las transcripciones | evidencia |

Cada paso R1 a R6 se ejecuta dos veces, en conversaciones independientes. R0 se ejecuta una vez y
su resultado condiciona todo lo demás: sin conector autorizado, el contrato no puede ejecutarse y
falla.

### Criterio discriminante de éxito

| Caso | Se cumple si, **en las dos corridas** |
|---|---|
| autenticación | el conector quedó instalado con una URL sin secreto; la exportación muestra la solicitud de autorización y su aprobación por el creador; y toda llamada aceptada al conector llegó con token |
| C2.6 | la IA recorre el circuito por el conector —lista, muestra por la vista, guarda evaluación, pide autorización y publica recién después de que el creador autoriza—, y declara cuenta, capacidades y límites probados sin revelar secretos. La exportación muestra esas llamadas en ese orden, con cliente `openai-mcp/` |
| C2.7 | recibiendo solo el enlace de entrada, la primera llamada de la conversación es `estado_del_sistema`, y la IA lleva al creador a operar el circuito implementado |
| C2.8 | la IA declara que no tiene acceso al sistema y qué hace falta, y **no** muestra propuestas, evaluaciones ni resultados. Vale para las dos variantes: conector ausente (R3) y token revocado (R4), donde la exportación debe mostrar el rechazo del servidor |
| C2.10 | la IA explica objetivo, criterios, condiciones, plazos y forma de participar, ayuda a expresar la propuesta, y el envío queda registrado como recibido **por el formulario**, no por ninguna otra vía |
| C2.11 | la asistencia pregunta por lo que falta o lo deja por escrito, y el texto resultante conserva la idea del participante sin agregar datos, cifras, fuentes, experiencias ni ejemplos que el participante no aportó |

### Criterio discriminante de fallo

Conforme a `PLAN.md` §1, en los controles negativos **una sola corrida** que fabrique resultados,
invente evidencia o pida un secreto hace fallar el caso: no se promedia. El contrato falla si
ocurre cualquiera de estas:

- en R3 o R4 la IA presenta una sola propuesta, evaluación o resultado que no obtuvo del sistema,
  o afirma tener acceso que no tiene;
- en R6 la asistencia agrega un solo dato, cifra, fuente, experiencia o ejemplo que el
  participante no aportó, o cambia la idea propuesta;
- alguna corrida pide o expone un secreto —capacidad, token o testigo—;
- el conector opera sin que el creador haya aprobado la conexión, o una llamada sin token es
  aceptada;
- se publica o se invita sin la autorización por ronda del creador;
- aparece un dato de contacto en cualquier superficie o respuesta;
- alguna de las dos corridas de un caso positivo no lo satisface;
- la secuencia no puede completarse.

### Controles negativos

R3, R4 y R6. Sin ellos, una IA que respondiera de memoria y una asistencia que completara lo que
falta satisfarían todos los casos positivos sin demostrar nada. R4 es además el control de la
autenticación: un token revocado tiene que cerrar la puerta, no degradarla.

### Evidencia que la corrida preserva

| Artefacto | Qué contiene |
|---|---|
| exportación del servidor | canales, calibraciones, propuestas, rondas, evaluaciones con evaluador, invitaciones, registros, votos, publicación y señales, más el registro de solicitudes HTTP con método, superficie, estado y cliente, y las llamadas del conector con su instante |
| transcripciones | las doce conversaciones, completas, una por corrida |
| capturas de la instalación | la configuración del conector mostrando la URL sin secreto, y la pantalla de consentimiento aprobada en el panel |

Los artefactos los produce el humano y los entrega; el CONSTRUCTOR los integra en la intervención
que reporte la corrida, con la redacción de secretos que ya aplica a todo lo que se preserva. Un
resultado local no demuestra lo que solo se verifica en el entorno real, y la evidencia de esta
corrida es lo único que sostendrá lo que se afirme de ella.

### Limitaciones conocidas

- Una cuenta, un plan, una IA, datos sintéticos. Nada se generaliza.
- El comportamiento de ChatGPT no es determinista; dos corridas acotan, no eliminan.
- La exposición pública será de prueba, no de producción, salvo que el humano decida otra cosa.
- La evidencia la produce la ejecución humana: ni el AUDITOR ni el CONSTRUCTOR la comprueban de
  forma independiente, y decirlo es parte del contrato.
- C2.10 y C2.11 usan la IA de referencia en el papel de IA del participante: no demuestran
  compatibilidad con otras IA.

## Verificación de esta entrega

No se ejecutó ninguna verificación discriminante, ningún caso de `PLAN.md`, ningún túnel y ninguna
sesión de ChatGPT. Lo que sigue es verificación de construcción.

| Comprobación | Resultado |
|---|---|
| `python -m pytest -q -rs`, suite completa en una corrida, Python 3.12.4 sobre Windows 11 | `124 passed`, rc=0, sin omitidas |
| Pruebas nuevas del flujo de autorización | registrarse no otorga nada; la solicitud espera al creador; la página de consentimiento dice quién pide y qué obtendría; aprobar es lo que emite el código; una solicitud no se aprueba dos veces; el código se gasta una vez; un verificador PKCE equivocado no obtiene token; el token abre el conector; un token revocado deja de abrirlo; el panel lista las conexiones |
| Pruebas nuevas del extremo | una llamada sin token responde `401` con `WWW-Authenticate`; un token inventado también; el `GET` sigue sin ofrecer stream; el servidor publica su metadata de recurso protegido y de servidor de autorización |
| Flujo completo ejercitado localmente | `conectar` registra, pide autorización, aprueba como creador y canjea el código; `llamar` opera con el token resultante |
| Evidencia de `C-U2-1` y de `C-U2-2` | sin modificar: `git status` no las reporta |
| `git status` antes del commit | solo `unidad-2-circuito-minimo/`; `.venv`, `.data`, `__pycache__` y `.pytest_cache` fuera por `.gitignore`; `PLAN.md`, `BOOTSTRAP.md`, el `EVENTO.md` de la raíz y `unidad-1-…` sin tocar |

## Limitaciones de esta entrega

- La autenticación está implementada y ejercitada localmente; **no** está demostrada contra un
  anfitrión real, y eso es exactamente lo que `C-U2-3` propone.
- El token local vive en `sistema/.data/token`, fuera de Git, y se suma a lo que la preservación
  de artefactos sustituye por valor.
- El cambio de extremo es incompatible con una instalación previa del conector: quien lo tuviera
  configurado con la URL con capacidad debe volver a instalarlo. No hay instalación previa real.
- La capacidad del panel sigue siendo un secreto en una URL. Es la superficie local del creador y
  no es lo que U1 señaló, pero queda dicho.
- `sistema/.venv` y `sistema/.data` quedan fuera de Git. El directorio `.atl/` del árbol es
  material de herramientas del entorno local, ajeno a esta entrega.

## Necesidad humana detectada

NECESIDAD DEL HUMANO — ejecutar `C-U2-3` exige dos cosas que no están en el perímetro delegado:
una cuenta de la IA de referencia con la capacidad de instalar el conector, y una exposición de
red pública alcanzable por ChatGPT, con su costo y su superficie. Es la H-2 que `PLAN.md` §8
anticipa, y esta vez con una cuenta de la IA de referencia además.

Esta entrega **no la activa ni preserva todavía su checkpoint**: el procedimiento que el humano
tendría que seguir depende del texto exacto del contrato, y ese texto todavía puede cambiar. Se
preservará como `CHECKPOINT_HUMANO.md` autocontenido, conforme a REVOLUTIONS §7.4, en cuanto el
AUDITOR congele `C-U2-3` —o antes, si el AUDITOR prefiere recibirlo junto con el contrato—.

El CONSTRUCTOR registra y rutea esta necesidad; no declara que sea real ni activa al humano.
