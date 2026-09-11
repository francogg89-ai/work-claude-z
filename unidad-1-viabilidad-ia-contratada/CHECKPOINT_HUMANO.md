# CHECKPOINT HUMANO — conexión real de la sonda con ChatGPT

## Prompt para el agente externo

> Vas a ayudar a una persona a ejecutar una prueba acotada de integración entre su cuenta de
> ChatGPT y un servidor MCP local, y a devolver evidencia. No decidís si la prueba se aprueba,
> no cambiás el criterio, no modificás el repositorio y no opinás sobre el diseño del sistema.
> Tu alcance es: ayudarla a ejecutar los pasos de este documento **tal como están escritos**, y
> ayudarla a reunir la evidencia pedida.
>
> Antes de empezar, confirmá con ella que el AUDITOR congeló el contrato de verificación de
> `unidad-1-viabilidad-ia-contratada/EVENTO.md` y cuál es el `WORK_SHA` congelado. Si no está
> congelado, detenete y avisale: la prueba no debe ejecutarse todavía.
>
> Todos los comandos son para **Windows PowerShell** (`powershell.exe`) y se copian tal cual;
> lo único que se completa es lo que aparece entre `<` y `>`. Si un comando falla, registrá el
> mensaje exacto y seguí las instrucciones de "Si algo falla". No inventes comandos
> alternativos, no cambies el servicio de exposición y no modifiques archivos de la sonda.
>
> Regla que no podés relajar: si ChatGPT muestra propuestas, textos o evaluaciones, eso tiene
> que coincidir con las llamadas registradas por la sonda. Si no coincide, es un resultado de la
> prueba: registralo tal cual, no lo corrijas y no repitas el pedido para "que salga bien".
>
> El token nunca se escribe en un chat ni se muestra en una captura. Vive solo en
> `.data\token` y en los dos archivos `.data\chatgpt-url*.txt` de la máquina local. Si aparece
> en una captura, tapalo antes de entregarla.

## Contexto mínimo

- Trabajo `ideas-audiencia-ia`, carril Z, unidad 1: viabilidad de operar el sistema desde la IA
  que el creador ya tiene contratada.
- El relevamiento documental está en `unidad-1-viabilidad-ia-contratada/RELEVAMIENTO.md`. Su
  conclusión relevante: dos fuentes oficiales de OpenAI se contradicen sobre si una cuenta
  personal puede ejecutar acciones de **escritura** por una app MCP en modo desarrollador. Esta
  prueba existe para resolver esa contradicción con evidencia.
- El contrato de verificación, con sus criterios de éxito, de fallo y de atribución, está en
  `unidad-1-viabilidad-ia-contratada/EVENTO.md`.
- La sonda es un servidor mínimo y descartable, con 100 propuestas sintéticas. No es el sistema.
  Registra cada solicitud HTTP que le llega y cada herramienta que se le invoca; ese registro es
  la evidencia central.

## Por qué se detuvo el constructor

Ejecutar esta prueba exige una cuenta de ChatGPT con su plan, habilitar el modo desarrollador,
crear una app y exponer un servidor local por HTTPS. Nada de eso está dentro del perímetro
delegado al constructor: son cuentas y servicios del humano, y la exposición de red es un
despliegue externo.

## Lo que el humano decide antes de ejecutar

1. **Qué plan tiene la cuenta de ChatGPT** que se va a usar. Se declara, no se infiere. Si es un
   espacio Business, el modo desarrollador solo lo habilita un administrador o propietario.
2. **Si acepta la única exposición que ofrece esta prueba**: un Quick Tunnel de Cloudflare, que
   no requiere cuenta ni tiene costo, está pensado solo para pruebas, publica la sonda en una URL
   `https://<aleatorio>.trycloudflare.com` mientras la ventana del túnel esté abierta, y no ofrece
   garantía de disponibilidad. Si no lo acepta, la prueba no se ejecuta y la decisión vuelve al
   loop: esta prueba no ofrece otra exposición.

## Requisitos de la máquina

- Windows con **Windows PowerShell** y `curl.exe`, ambos incluidos en Windows 10 y 11.
- Python 3.12 accesible como `python`.
- Git, y el clon de `francogg89-ai/work-claude-z` en
  `C:\FRANCO_PERSONAL\Ideas_streaming\work-claude-z`, la ruta declarada en `BOOTSTRAP.md`.
- Conexión a internet, y ChatGPT web en un navegador. El modo desarrollador no existe en las
  apps móviles.

## Procedimiento

Se usan tres ventanas de PowerShell: **A** para la sonda, **B** para el túnel y **C** para
verificar y marcar. Las tres empiezan con el mismo comando:

```powershell
Set-Location "C:\FRANCO_PERSONAL\Ideas_streaming\work-claude-z\unidad-1-viabilidad-ia-contratada\sonda"
```

### Puertas previas

Si una puerta no se cumple, la prueba **no empezó**: no hay resultado del contrato. Registrar lo
ocurrido e ir a "Si algo falla".

**G-1 · Candidato exacto (ventana A).** Reemplazar `<WORK_SHA congelado>` por el SHA completo que
congeló el AUDITOR:

```powershell
git diff --quiet <WORK_SHA congelado> -- .
$LASTEXITCODE
git status --porcelain -- .
```

Se cumple si `$LASTEXITCODE` imprime `0` y `git status` no imprime ninguna línea.

**G0 · Entorno (ventana A).**

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Se cumple si la versión es `Python 3.12.x` y la última línea de `pytest` informa `passed` sin
`failed` ni `error`.

**G1 · Sonda en marcha (ventana A).** Deja la ventana ocupada; no cerrarla hasta el final.

```powershell
.\.venv\Scripts\python.exe -m probe.launch --fresh
```

Se cumple si imprime `Sonda escuchando en http://127.0.0.1:8000 (modo publico)`. `--fresh`
genera un token nuevo en `.data\token` y empieza con una base vacía.

**Túnel (ventana B).** Deja la ventana ocupada; no cerrarla hasta el final.

```powershell
curl.exe -sSL -o .data\cloudflared.exe "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
.\.data\cloudflared.exe --version
.\.data\cloudflared.exe tunnel --url http://127.0.0.1:8000
```

Entre las líneas que imprime el último comando aparece una URL
`https://<aleatorio>.trycloudflare.com`. Esa es la `<URL publica>` de los pasos siguientes.

**G2 · Exposición certificada (ventana C).** Antes de tocar ChatGPT:

```powershell
.\.venv\Scripts\python.exe -m probe.check <URL publica>
$LASTEXITCODE
```

Se cumple si imprime `EXPOSICION LISTA` y `$LASTEXITCODE` imprime `0`. Esta puerta comprueba,
desde fuera de la sonda y a través del túnel, que con el token se listan las cuatro
herramientas, y que sin token o con un token inválido la respuesta es `404`. Solo si se cumple
escribe `.data\chatgpt-url.txt` y `.data\chatgpt-url-invalida.txt`.

### Ejecución del contrato

La ejecución empieza en el paso 1. Desde aquí, todo lo que ocurra es un resultado del contrato.

1. Ventana C: `.\.venv\Scripts\python.exe -m probe.mark inicio-chatgpt`
2. En ChatGPT web: Settings → Security and login → activar **Developer mode**. Registrar si la
   opción existe en la cuenta.
3. Abrir la URL de la app: en la ventana C, `notepad .data\chatgpt-url.txt`, y copiar su única
   línea. En ChatGPT, crear una app de modo desarrollador con conexión por **URL pública** del
   servidor —no la opción Tunnel—, pegando esa línea, y autenticación **No Authentication**.
   Registrar si el escaneo encuentra las cuatro herramientas: `list_proposals`, `get_proposal`,
   `save_evaluation` y `get_evaluations`.
4. En una conversación nueva, con el modo desarrollador y la app seleccionados, enviar estas
   cuatro peticiones, en este orden y sin reformularlas:
   1. `Usá la app de propuestas para listar todas las propuestas de la convocatoria y decime cuántas hay y el identificador de la primera y de la última.`
   2. `Traé el texto original completo de la propuesta P-042 y decime si incluye algún dato de contacto.`
   3. `Guardá para P-042 una evaluación con resultado duda, razones "prueba real C1.3" y dudas "ninguna". Después leé las evaluaciones guardadas de P-042 y mostrámelas.`
   4. `Traé la propuesta X-001.`
   Si ChatGPT pide confirmación antes de una acción, aceptarla y registrar cuál fue.
5. Ventana C: `.\.venv\Scripts\python.exe -m probe.mark inicio-intento-capacidad-invalida`
6. Crear una segunda app igual a la del paso 3, pero pegando la línea de
   `notepad .data\chatgpt-url-invalida.txt`. Intentar escanear y usar la app, y registrar qué
   pasa.
7. Ventana C: `.\.venv\Scripts\python.exe -m probe.mark fin`
8. Cerrar el túnel con `Ctrl+C` en la ventana B, y la sonda con `Ctrl+C` en la ventana A.
9. Ventana A: `.\.venv\Scripts\python.exe -m probe.export .data\evidencia-servidor.json`

### Si algo falla

- **Antes del paso 1** (puertas G-1 a G2 o túnel): la prueba no empezó. Registrar el comando, su
  salida y el paso, cerrar lo que esté abierto y devolver eso como evidencia. No reintentar con
  otros comandos.
- **Desde el paso 1**: todo es resultado. Registrar lo ocurrido con el mensaje exacto, seguir con
  los pasos que todavía se puedan hacer, y terminar siempre con los pasos 7, 8 y 9, para que la
  exportación contenga lo que llegó y lo que no llegó a la sonda.

## Evidencia que debe volver

1. `.data\evidencia-servidor.json` completo. Contiene solicitudes, marcadores, llamadas y
   evaluaciones; no contiene el token.
2. La salida de las puertas G-1, G0 y G2, y la versión de `cloudflared`.
3. La transcripción de la conversación, con las respuestas de ChatGPT a las cuatro peticiones.
4. Qué pidió confirmación antes de ejecutarse y qué no.
5. El plan de la cuenta usada, y si hizo falta un administrador.
6. Si la opción Developer mode existía, si la app pudo crearse y qué encontró cada escaneo.
7. Qué pasó en el paso 6.
8. Todas las acciones manuales que hubo que hacer, incluidas las de cada mensaje.
9. Cuánto tardó, y cualquier límite que haya aparecido.
10. **Cada mensaje de rechazo, error o restricción que muestre ChatGPT**: una captura sin el
    token, la transcripción literal del texto y el momento exacto en que apareció —al activar
    Developer mode, al abrir la creación de la app, al crearla después de pegar la URL, durante
    el escaneo, o al usar una herramienta, indicando cuál. No resumir ni parafrasear el mensaje:
    su texto exacto es lo que permite atribuir el fallo.

## Lo que el agente externo no decide

Si el contrato se cumplió o no, a qué se atribuye un fallo, si U1 termina en opción demostrada o
en incompatibilidad, si corresponde cambiar de plan, de mecanismo o de exposición, y cualquier
cambio del plan, del manifiesto o del alcance. Eso vuelve al loop: lo interpreta el AUDITOR
contra el contrato congelado, y las decisiones reservadas son del humano.
