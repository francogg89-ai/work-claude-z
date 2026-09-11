# CHECKPOINT HUMANO — conexión real de la sonda con ChatGPT

## Prompt para el agente externo

> Vas a ayudar a una persona a ejecutar una prueba acotada de integración entre su cuenta de
> ChatGPT y un servidor MCP local, y a devolver evidencia. No decidís si la prueba se aprueba,
> no cambiás el criterio, no modificás el repositorio y no opinás sobre el diseño del sistema.
> Tu alcance es: ayudarla a ejecutar los pasos, y ayudarla a reunir la evidencia pedida.
>
> Antes de empezar, confirmá con ella que el AUDITOR congeló el contrato de verificación que
> está en `unidad-1-viabilidad-ia-contratada/EVENTO.md` del repositorio de trabajo. Si no está
> congelado, detenete y avisale: la prueba no debe ejecutarse todavía.
>
> Regla que no podés relajar: si ChatGPT muestra propuestas, textos o evaluaciones que no
> aparecen como llamadas en la exportación del servidor, eso es un resultado de la prueba y hay
> que registrarlo tal cual. No lo corrijas, no lo repitas para "que salga bien" y no lo
> interpretes como un problema de redacción del pedido.
>
> Nunca pidas ni copies el token en un chat, en una captura o en un archivo que vaya al
> repositorio. Si aparece en una captura, tapalo antes de entregarla.

## Contexto mínimo

- Trabajo `ideas-audiencia-ia`, carril Z, unidad 1: viabilidad de operar el sistema desde la IA
  que el creador ya tiene contratada.
- El relevamiento documental está en `unidad-1-viabilidad-ia-contratada/RELEVAMIENTO.md`. Su
  conclusión relevante: dos fuentes oficiales de OpenAI se contradicen sobre si una cuenta
  personal puede ejecutar acciones de **escritura** por una app MCP en modo desarrollador. Esta
  prueba existe para resolver esa contradicción con evidencia.
- El contrato de verificación, con sus criterios de éxito y de fallo, está en
  `unidad-1-viabilidad-ia-contratada/EVENTO.md`.
- La sonda es un servidor mínimo y descartable, con 100 propuestas sintéticas. No es el sistema.

## Por qué se detuvo el constructor

Ejecutar esta prueba exige una cuenta de ChatGPT con su plan, habilitar el modo desarrollador,
crear una app y exponer un servidor local por HTTPS. Nada de eso está dentro del perímetro
delegado al constructor: son cuentas y servicios del humano, y la exposición de red es un
despliegue externo.

## Lo que hay que decidir antes de ejecutar

1. **Qué plan tiene la cuenta de ChatGPT** que se va a usar. Se declara, no se infiere. Si es un
   espacio Business, el modo desarrollador solo lo habilita un administrador o propietario.
2. **Cómo se expone la sonda**, entre las dos opciones del relevamiento: un túnel de desarrollo o
   servicio de reenvío HTTPS, o Secure MCP Tunnel. La elección, su costo y su superficie de
   exposición son decisión del humano. La sonda escucha solo en `127.0.0.1`.

## Pasos

En `unidad-1-viabilidad-ia-contratada/sonda`:

1. Preparar el entorno: `python -m venv .venv` y `.venv/Scripts/python -m pip install -r requirements.txt`.
2. Generar un token nuevo: `.venv/Scripts/python -c "import secrets;print(secrets.token_urlsafe(32))"`.
   No guardarlo en el repositorio.
3. Arrancar la sonda con una base vacía, poniendo en `SONDA_ALLOWED_HOSTS` el nombre de host
   público que dé la opción de exposición elegida:
   `SONDA_TOKEN=<token> SONDA_ALLOWED_HOSTS=<host publico> SONDA_DB=.data/probe.sqlite SONDA_PORT=8000 .venv/Scripts/python -m probe.server`
4. Exponer `http://127.0.0.1:8000` por HTTPS con la opción elegida.
5. En ChatGPT web: habilitar el modo desarrollador y crear una app apuntando a
   `https://<host publico>/mcp/<token>`, con autenticación "sin autenticación". Registrar si el
   escaneo de herramientas encuentra las cuatro.
6. En una conversación nueva, con el modo desarrollador y la app seleccionados, enviar estas
   cuatro peticiones, en este orden y sin reformularlas:
   1. `Usá la app de propuestas para listar todas las propuestas de la convocatoria y decime cuántas hay y el identificador de la primera y de la última.`
   2. `Traé el texto original completo de la propuesta P-042 y decime si incluye algún dato de contacto.`
   3. `Guardá para P-042 una evaluación con resultado duda, razones "prueba real C1.3" y dudas "ninguna". Después leé las evaluaciones guardadas de P-042 y mostrámelas.`
   4. `Traé la propuesta X-001.`
7. Intento con capacidad inválida: crear una segunda app apuntando a la misma URL pero con el
   token cambiado en un carácter, e intentar usarla. Registrar qué pasa. Además, desde una
   terminal: `curl -i https://<host publico>/mcp` y registrar el código de respuesta.
8. Detener la exposición y la sonda. Exportar la evidencia del servidor:
   `SONDA_DB=.data/probe.sqlite .venv/Scripts/python -m probe.export > evidencia-servidor.json`

Si algo falla antes del paso 6 —el modo desarrollador no está disponible, la app no se puede
crear, el escaneo no encuentra herramientas—, eso **es** un resultado de la prueba. Registrarlo
y seguir al paso 8 con lo que haya.

## Evidencia que debe volver

1. `evidencia-servidor.json` completo.
2. La transcripción de la conversación, incluidas las respuestas de ChatGPT a las cuatro
   peticiones, con la URL y el token tapados.
3. Qué pidió confirmación antes de ejecutarse y qué no.
4. El plan de la cuenta usada, y si hizo falta un administrador.
5. La opción de exposición usada y su costo, si tuvo alguno.
6. Todas las acciones manuales que hubo que hacer, incluidas las de cada mensaje.
7. Qué pasó en el paso 7, y el código de respuesta del `curl`.
8. Cuánto tardó y cualquier límite que haya aparecido, por ejemplo de tamaño o de tiempo.
9. Si algo falló, el mensaje de error tal como apareció.

## Lo que el agente externo no decide

Si el contrato se cumplió o no, si U1 termina en opción demostrada o en incompatibilidad, si
corresponde cambiar de plan o de mecanismo, y cualquier cambio del plan, del manifiesto o del
alcance. Eso vuelve al loop: lo interpreta el AUDITOR contra el contrato congelado, y las
decisiones reservadas son del humano.
