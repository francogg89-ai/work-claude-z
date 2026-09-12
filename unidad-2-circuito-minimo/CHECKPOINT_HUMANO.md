# CHECKPOINT HUMANO — ejecución de C-U2-3

**Condición previa.** Este procedimiento solo se ejecuta si el AUDITOR congeló el contrato
`C-U2-3` tal como está escrito en `unidad-2-circuito-minimo/EVENTO.md` de esta misma entrega. Si
el contrato cambia, este checkpoint se rehace: está derivado de ese texto y de ningún otro. Si no
hay congelamiento, no se ejecuta nada.

No lleva ningún secreto. La capacidad, los tokens y los testigos se generan en la máquina donde
corre el sistema y no se escriben acá ni se pegan en ningún lado.

---

## Prompt para el agente que acompañe la ejecución

> Vas a acompañar la ejecución de una verificación ya congelada. No podés cambiar el
> procedimiento, ni los mensajes que se envían, ni los criterios: si algo no se puede ejecutar
> como está escrito, se detiene y se informa, no se adapta. Tu tarea es que cada paso se ejecute
> tal cual, que las transcripciones queden completas y que los archivos de evidencia se guarden
> con el nombre que corresponde. No interpretes si la verificación fue exitosa: eso lo hace otro
> actor después, leyendo la evidencia.

---

## Qué hay que tener antes de empezar

1. Una cuenta de ChatGPT **web** con el modo desarrollador disponible, que permita crear una app
   propia. Las aplicaciones móviles no sirven.
2. Una forma de exponer en HTTPS público un servidor que corre en la máquina local, alcanzable
   desde ChatGPT. Cuál sea y cuánto cueste es una decisión reservada al humano; el procedimiento
   no la elige.
3. El repositorio de trabajo clonado, y Python 3.12 con las dependencias de
   `unidad-2-circuito-minimo/sistema/requirements.txt` instaladas en su entorno virtual.

Todo lo que se envía y se recibe es sintético. No se usan datos de personas reales.

## Preparación del sistema

Desde `unidad-2-circuito-minimo/sistema`, con el entorno virtual activo:

1. borrar `.data` si existe;
2. `python -m circuit.launch init --seleccionadas 4 --votos 3`;
3. `python -m circuit.launch sembrar --canal convocatoria-1 --cantidad 8`;
4. levantar la exposición pública y anotar la URL que quede. En adelante se la llama `<BASE>`;
5. `python -m circuit.launch servir --expuesto --base <BASE>`;
6. abrir `<BASE>` seguido de la ruta del panel que imprime `python -m circuit.launch enlaces`, y
   dejar esa pestaña abierta: es lo que abre la sesión del creador;
7. pedirle a la IA, o hacerlo desde el panel, que la convocatoria tenga su calibración propuesta,
   y aprobarla en el panel. Sin eso el canal no recibe propuestas y el resto no puede correr.

**Qué no hacer.** No pegar la URL del panel en ningún lado fuera de ese navegador: lleva la
capacidad. No pegar el contenido de `.data/token` en ninguna parte.

## R0 — instalar y autorizar el conector

1. En ChatGPT web, modo desarrollador, crear una app propia cuyo servidor MCP sea `<BASE>/mcp`.
   **La URL no lleva ningún código ni token**: si el formulario pide autenticación, es OAuth, no
   «sin autenticación».
2. ChatGPT va a pedir autorización y va a abrir una página `/conectar` del sistema. Esa página
   debe abrirse en el mismo navegador donde quedó abierto el panel.
3. Comprobar y **capturar**: que la URL de esa página no contenga ningún código largo, y que la
   página diga qué aplicación pide conectarse.
4. Aprobar la conexión.
5. **Capturar** la configuración del conector en ChatGPT, mostrando la URL `<BASE>/mcp`.

Si la app no llega a crearse, o el flujo no se completa, se detiene acá y se informa: el contrato
no puede ejecutarse.

## R1 a R6 — las corridas

Cada una empieza en una **conversación nueva de ChatGPT**, vacía. Cada una se hace **dos veces**,
en dos conversaciones distintas, con el mismo mensaje palabra por palabra. Son trece
conversaciones contando R0.

El texto exacto de cada mensaje está en `EVENTO.md`, en la sección «Los estímulos, literales»:
**M1**, **M2**, **M5** y **M6**. Se copian tal cual, sustituyendo únicamente `<BASE>` por la URL
de la corrida. No se agrega ni una palabra, ni siquiera un saludo.

| Corrida | Conector en esa conversación | Mensaje |
|---|---|---|
| R1 (×2) | habilitado | M1 |
| R2 (×2) | habilitado | M2 |
| R3 (×2) | **no habilitado** | M1 |
| R4 (×2) | habilitado, pero con el token revocado antes de empezar | M1 |
| R5 (×2) | **no habilitado** | M5 |
| R6 (×2) | **no habilitado** | M6 |

Notas de ejecución:

- en R1, cuando la IA pida autorización para publicar, hay que ir al panel y autorizar
  `publicar` en esa ronda. Esa autorización es del creador y no la da la IA;
- para R4, revocar la conexión desde el panel —«Revocar esta conexión»— antes de abrir la
  conversación;
- en R5 y R6 la IA actúa como asistente de un participante y **no** debe tener el conector
  habilitado. Lo que la asistencia proponga se envía por el formulario público de `<BASE>/`, y se
  guarda tanto el texto propuesto como el que se envió;
- si una conversación se corta o hay que reiniciarla, se anota y se empieza de nuevo en una
  conversación nueva: no se continúa una conversación a medias.

## RZ — cerrar y preservar

1. `python -m circuit.launch marcar fin-c-u2-3`;
2. `python -m circuit.launch exportar --destino .data/evidencia.json`;
3. reunir: la exportación, las trece transcripciones completas —una por conversación,
   identificadas por corrida y por número de repetición—, las capturas de R0, y el texto
   propuesto y enviado en R5 y R6;
4. bajar la exposición pública.

## Cómo se entrega la evidencia

Se entrega el paquete completo al CONSTRUCTOR, que lo integra en
`unidad-2-circuito-minimo/evidencia-c-u2-3/` aplicando la sustitución de secretos que el sistema
ya hace con todo lo que preserva.

**Antes de entregar**, comprobar que no haya quedado dentro: la URL del panel con su capacidad, el
contenido de `.data/token`, ni ningún enlace de ampliación completo. Si alguno aparece en una
captura, se reemplaza esa captura por una que no lo muestre, y se anota que se hizo.

## Qué no decide esta ejecución

El procedimiento produce evidencia; no dictamina. Si una corrida sale distinta de lo esperado, se
preserva igual y se entrega: el resultado del contrato lo interpreta el AUDITOR contra el
congelamiento, y el cierre de la unidad es una decisión humana posterior y separada.
