# CHECKPOINT HUMANO — segunda conexión real de la sonda con ChatGPT

## Prompt para el agente externo

> Vas a ayudar a una persona a ejecutar una prueba acotada de integración entre su cuenta de
> ChatGPT y un servidor MCP local, y a devolver evidencia. No decidís si la prueba se aprueba,
> no cambiás el criterio, no modificás el repositorio y no opinás sobre el diseño del sistema.
> Tu alcance es: ayudarla a ejecutar los pasos de este documento **tal como están escritos**, y
> ayudarla a reunir la evidencia pedida.
>
> Antes de empezar, confirmá con ella que el AUDITOR congeló los contratos C-U1-2A y C-U1-2B de
> `unidad-1-viabilidad-ia-contratada/EVENTO.md`, y cuál es el `WORK_SHA` congelado. Si no están
> congelados, detenete y avisale: la prueba no debe ejecutarse todavía.
>
> Todos los comandos son para **Windows PowerShell** (`powershell.exe`) y se copian tal cual; lo
> único que se completa es lo que aparece entre `<` y `>`. Si un comando falla, registrá el
> mensaje exacto y seguí "Si algo falla". No inventes comandos alternativos, no cambies el
> servicio de exposición y no modifiques archivos de la sonda.
>
> **La URL de la app lleva un secreto y vos nunca la ves.** Pasa del disco al portapapeles con
> `probe.url copiar`, se pega solo en ChatGPT y se borra enseguida con `probe.url limpiar`.
> Entre esos dos comandos la persona no te consulta ni te pega nada. Si necesita ayuda en ese
> tramo, primero ejecuta `probe.url limpiar`. Nunca le pidas que abra los archivos
> `.data\chatgpt-url*.txt` ni `.data\token`, ni que te muestre la configuración de la app.
>
> Regla que no podés relajar: lo que ChatGPT muestre tiene que coincidir con lo que registra la
> sonda. Si no coincide, es un resultado de la prueba: registralo tal cual y no repitas el pedido
> para "que salga bien".

## Contexto mínimo

- Trabajo `ideas-audiencia-ia`, carril Z, unidad 1: viabilidad de operar el sistema desde la IA
  que el creador ya tiene contratada.
- En la primera corrida, la cuenta Plus personal ejecutó lecturas y una escritura real. Pero al
  mostrar un original, el texto de ChatGPT cambió `SINTETICO` por `SINTÉTICO`: el modelo no copia,
  regenera. Esta corrida evalúa dos contratos con una sola ejecución: **A**, la integración
  completa, y **B**, una vista de la app que muestra el original sin pasar por el modelo.
- Los contratos, con sus criterios y su regla de atribución, están en
  `unidad-1-viabilidad-ia-contratada/EVENTO.md`.
- La sonda es un servidor mínimo y descartable, con 100 propuestas sintéticas y cinco
  herramientas. Registra cada solicitud y cada llamada que le llega; ese registro es la evidencia
  central.

## Por qué se detuvo el constructor

Ejecutar esta prueba exige operar una cuenta de ChatGPT y exponer un servidor local por HTTPS.
Nada de eso está dentro del perímetro delegado al constructor: son cuentas y servicios del
humano, y la exposición de red es un despliegue externo.

## Lo que el humano decide antes de ejecutar

1. **Qué cuenta y qué plan de ChatGPT** usa. Se declara, no se infiere.
2. **Si acepta la única exposición que ofrece esta prueba**: un Quick Tunnel de Cloudflare. No
   requiere cuenta ni tiene costo, está pensado solo para pruebas, publica la sonda en una URL
   `https://<aleatorio>.trycloudflare.com` mientras la ventana del túnel siga abierta, y no tiene
   garantía de disponibilidad. Si no lo acepta, la prueba no se ejecuta.

## Requisitos de la máquina

- Windows con **Windows PowerShell** y `curl.exe`, ambos incluidos en Windows 10 y 11.
- Python 3.12 accesible como `python`. Node.js, si está instalado, permite que G0 corra también
  las pruebas de la vista; si no está, esas pruebas se omiten.
- Git, y el clon de `francogg89-ai/work-claude-z` en
  `C:\FRANCO_PERSONAL\Ideas_streaming\work-claude-z`, la ruta declarada en `BOOTSTRAP.md`.
- ChatGPT web en un navegador. El modo desarrollador no existe en las apps móviles.

## Procedimiento

Tres ventanas de PowerShell: **A** para la sonda, **B** para el túnel y **C** para verificar,
marcar y manejar el portapapeles. Las tres empiezan con:

```powershell
Set-Location "C:\FRANCO_PERSONAL\Ideas_streaming\work-claude-z\unidad-1-viabilidad-ia-contratada\sonda"
```

### Puertas previas

Si una puerta no se cumple, la prueba **no empezó** y no hay resultado de ningún contrato.
Registrar lo ocurrido e ir a "Si algo falla".

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

Se cumple si la versión es `Python 3.12.x` y la última línea de `pytest` informa `passed`, sin
`failed` ni `error`.

**G1 · Sonda en marcha (ventana A).** La ventana queda ocupada hasta el final.

```powershell
.\.venv\Scripts\python.exe -m probe.launch --fresh
```

Se cumple si imprime `Sonda escuchando en http://127.0.0.1:8000 (modo publico)`. `--fresh`
genera un token nuevo y empieza con una base vacía.

**Túnel (ventana B).** La ventana queda ocupada hasta el final.

```powershell
curl.exe -sSL -o .data\cloudflared.exe "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
.\.data\cloudflared.exe --version
.\.data\cloudflared.exe tunnel --url http://127.0.0.1:8000
```

Entre lo que imprime el último comando aparece una URL `https://<aleatorio>.trycloudflare.com`.
Esa es la `<URL publica>` del paso siguiente. No contiene el token.

**G2 · Exposición certificada (ventana C).**

```powershell
.\.venv\Scripts\python.exe -m probe.check <URL publica>
$LASTEXITCODE
```

Se cumple si imprime `EXPOSICION LISTA` y `$LASTEXITCODE` imprime `0`. Comprueba, a través del
túnel, que con el token se listan las cinco herramientas —`get_evaluations`, `get_proposal`,
`list_proposals`, `save_evaluation` y `show_proposal`— y que sin token o con un token inválido la
respuesta es `404`.

### Ejecución de los contratos

La ejecución empieza en el paso 1. Desde ahí, todo lo que ocurra es un resultado.

1. Ventana C: `.\.venv\Scripts\python.exe -m probe.mark inicio-chatgpt`
2. En ChatGPT web, confirmar que **Developer mode** está activo en Settings → Security and login.
   **Borrar las apps de la sonda creadas en corridas anteriores**: apuntan a un túnel que ya no
   existe y confundirían la prueba.
3. En ChatGPT, abrir la creación de una app de modo desarrollador con conexión por **URL pública**
   —no la opción Tunnel—, nombre `Sonda propuestas U1 v2` y autenticación **No Authentication**.
   Con el campo URL listo:
   - Ventana C: `.\.venv\Scripts\python.exe -m probe.url copiar`
   - Pegar en el campo URL de ChatGPT, y nada más.
   - Ventana C, enseguida: `.\.venv\Scripts\python.exe -m probe.url limpiar`
   - Crear la app. Registrar si el escaneo encontró las cinco herramientas y si ChatGPT pidió
     alguna confirmación.
4. En una conversación nueva, con el modo desarrollador y la app seleccionados, enviar estas cinco
   peticiones, en este orden y sin reformularlas:
   1. `Usá la app de propuestas para listar todas las propuestas de la convocatoria y decime cuántas hay y el identificador de la primera y de la última.`
   2. `Traé el texto original completo de la propuesta P-042 y decime si incluye algún dato de contacto.`
   3. `Mostrá la propuesta P-042 en la vista de la app, tal como se recibió.`
   4. `Guardá para P-042 una evaluación con resultado duda, razones "prueba real C1.3" y dudas "ninguna". Después leé las evaluaciones guardadas de P-042 y mostrámelas.`
   5. `Traé la propuesta X-001.`

   En la petición 3, si aparece una vista de la app, sacar una captura en la que se distinga la
   vista del texto de la respuesta, y copiar a mano sus tres últimas líneas: "Huella de lo
   mostrado", "Huella del servidor" y "Coinciden".

   Si ChatGPT respondió alguna petición **sin mostrar una llamada a la app**, repetir las cinco
   peticiones una sola vez en una conversación nueva, antes del paso 5. No se repite por ningún
   otro motivo.
5. Ventana C: `.\.venv\Scripts\python.exe -m probe.mark inicio-intento-capacidad-invalida`
6. Crear una segunda app igual a la del paso 3, pero con el portapapeles cargado por
   `.\.venv\Scripts\python.exe -m probe.url copiar-invalida`, pegando y limpiando enseguida con
   `.\.venv\Scripts\python.exe -m probe.url limpiar`. Intentar crearla y usarla una sola vez.
   Registrar qué pasa.
7. Ventana C: `.\.venv\Scripts\python.exe -m probe.mark fin`
8. Cerrar el túnel con `Ctrl+C` en la ventana B, y la sonda con `Ctrl+C` en la ventana A.
9. Ventana A: `.\.venv\Scripts\python.exe -m probe.export .data\evidencia-servidor.json`

### Si algo falla

- **Antes del paso 1** —puertas G-1 a G2 o túnel—: la prueba no empezó. Registrar el comando, su
  salida y el paso, cerrar lo que esté abierto y devolver eso como evidencia. No reintentar con
  otros comandos.
- **Desde el paso 1**: todo es resultado. Registrar lo ocurrido con su mensaje exacto, seguir con
  los pasos que todavía se puedan hacer, y terminar siempre con los pasos 7, 8 y 9.
- **Si la URL o el token se muestran o se pegan en otro lugar que no sea ChatGPT**: registrarlo como
  incidencia, sin copiar el valor en ningún lado, y seguir. El criterio E6 y el `--fresh` de la
  próxima ejecución acotan el efecto.

## Evidencia que debe volver

1. `.data\evidencia-servidor.json` completo. Contiene solicitudes, marcadores, llamadas,
   evaluaciones y huellas; no contiene el token.
2. La salida de las puertas G-1, G0 y G2, y la versión de `cloudflared`.
3. La transcripción de la conversación, con las respuestas de ChatGPT a las cinco peticiones.
4. **De la petición 3**: la captura de la vista y la transcripción literal de sus tres líneas de
   huella; o, si no apareció ninguna vista, lo que ChatGPT mostró en su lugar.
5. Qué pidió confirmación antes de ejecutarse, y qué no.
6. El plan de la cuenta usada, y si hizo falta un administrador.
7. Qué encontró el escaneo de cada app, y qué pasó en el paso 6.
8. Todas las acciones manuales que hubo que hacer, incluidas las de cada mensaje.
9. Cuánto tardó, y cualquier límite que haya aparecido.
10. **Cada mensaje de rechazo, error o restricción que muestre ChatGPT**: una captura sin la URL, la
    transcripción literal del texto y el momento exacto en que apareció —al activar Developer
    mode, al abrir la creación de la app, al crearla después de pegar la URL, durante el escaneo,
    al usar una herramienta o al mostrar la vista, indicando cuál—. No resumir ni parafrasear: el
    texto exacto es lo que permite atribuir un fallo.
11. Cualquier incidencia con la URL o el token, sin su valor.

## Lo que el agente externo no decide

Si los contratos se cumplieron o no, a qué se atribuye un fallo, si U1 termina en opción
demostrada o en incompatibilidad, si corresponde cambiar de plan, de mecanismo o de exposición, y
cualquier cambio del plan, del manifiesto o del alcance. Eso vuelve al loop: lo interpreta el
AUDITOR contra los contratos congelados, y las decisiones reservadas son del humano.
