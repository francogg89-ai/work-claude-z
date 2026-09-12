# Relevamiento de mecanismos admitidos — IA de referencia ChatGPT

Paso 1 de U1. Enumera los mecanismos que el proveedor documenta para que ChatGPT invoque un
sistema externo, con sus requisitos de plan, autenticación, exposición de red, límites y costos
declarados. Fuente: documentación pública de OpenAI, consultada el 2026-09-10. Las fechas
relativas de actualización son las que mostraba cada página ese día.

Este documento registra lo que la documentación **dice**. No demuestra que un mecanismo
funcione en una cuenta concreta: eso lo resuelve la conexión real de U1.

## Fuentes

| Id | Fuente | Actualización mostrada |
|---|---|---|
| F1 | Help Center — Creating and editing GPTs: https://help.openai.com/en/articles/8554397-creating-and-editing-gpts | "Updated: 26 days ago" |
| F2 | Help Center — Developer mode and MCP apps in ChatGPT: https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt | "Updated: 20 days ago" |
| F3 | Help Center — Apps in ChatGPT: https://help.openai.com/en/articles/11487775-connectors-in-chatgpt | "Updated: yesterday" |
| F4 | Developers — ChatGPT Developer mode: https://developers.openai.com/api/docs/guides/developer-mode | sin fecha visible |
| F5 | Developers — Connect and test your plugin: https://developers.openai.com/plugins/deploy/connect-chatgpt | sin fecha visible |
| F6 | Developers — Secure MCP Tunnel: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels | sin fecha visible |
| F7 | Developers — GPT Actions, production notes: https://developers.openai.com/api/docs/actions/production | sin fecha visible |
| F8 | Developers — GPT Actions, introduction: https://developers.openai.com/api/docs/actions/introduction | sin fecha visible |
| F9 | Cloudflare — Quick Tunnels (TryCloudflare): https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/ | sin fecha visible |
| F10 | Cloudflare — descargas de `cloudflared`: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/ | sin fecha visible |
| F11 | Developers — Add UI to your MCP server: https://developers.openai.com/plugins/build/chatgpt-ui | consultada el 2026-09-11 |
| F12 | MCP Apps, especificación 2026-01-26: https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx | consultada el 2026-09-11 |

## Mecanismos

### M1 — GPT personalizado con Actions (OpenAPI)

- Llama APIs REST descritas en un esquema OpenAPI; admite lectura y escritura (F8).
- Autenticación: ninguna, API key u OAuth (F8).
- Límites: "45 seconds round trip for API calls"; "Request and response payloads must be less
  than 100,000 characters each"; TLS 1.2 o superior en el puerto 443 con certificado público
  válido; sin cabeceras personalizadas; solo contenido de texto (F7).
- Confirmación: `x-openai-isConsequential` controla si se pide confirmación antes de ejecutar
  (F7).
- **Plan**: "New GPT creation and publishing are not available on personal ChatGPT accounts,
  including Free, Go, Plus, and Pro." La creación queda disponible en espacios Business,
  Enterprise y Edu, según los permisos del espacio (F1).

Consecuencia para U1: un creador con cuenta personal no puede crear hoy un GPT con Actions. M1
solo aplica a espacios de trabajo.

### M2 — App MCP propia en modo desarrollador

- ChatGPT se conecta a un servidor MCP remoto; transporte SSE o HTTP con streaming; en la web
  solamente, no en móvil (F2, F4).
- Autenticación: OAuth, sin autenticación o mixta (F4).
- Confirmación: "Write actions by default require confirmation"; las herramientas sin la
  anotación `readOnlyHint` se tratan como escritura (F4).
- Invocación: se elige el modo desarrollador y la app en el menú de la conversación; la
  selección aplica al mensaje en que se hace (F2, F4).
- Exposición: el servidor debe ser alcanzable por un endpoint HTTPS público o por Secure MCP
  Tunnel; un túnel de desarrollo u otro servicio de reenvío HTTPS sirve para pruebas locales
  (F5). "ChatGPT connects to remote MCP servers" (F2).
- **Plan — las fuentes se contradicen**:
  - F4: "Eligibility: Available to Pro, Plus, Business, Enterprise, and Education accounts on
    the web", con "full Model Context Protocol (MCP) client support for all tools, both read and
    write".
  - F2: "Full MCP (Model Context Protocol) support, including modify/write actions, is rolling
    out in beta to ChatGPT Business, Enterprise, and Edu plans"; y "Full MCP is only available
    to Business and Enterprise/Edu users, currently. Pro users can connect MCPs with read/fetch
    permissions in developer mode." F2 no menciona Plus.
  - En Business, "Only admins/owners can enable developer mode" (F2).

Consecuencia para U1: M2 es el único mecanismo que al menos una fuente oficial declara disponible
para cuentas personales. Si la escritura funciona en una cuenta personal es exactamente la
incertidumbre que la documentación no resuelve y que la conexión real debe discriminar.

### M3 — App publicada en el directorio de plugins

- Desde el 9 de julio de 2026 el directorio de apps pasó a ser el directorio de plugins; una app
  enviada y aprobada puede distribuirse allí, y algunas apps pueden escribir (F3).
- Requiere endpoint HTTPS público para el envío (F5) y una revisión de OpenAI.

Queda **fuera del alcance** de la exploración de U1: exige publicar y someter a revisión externa,
que son acciones reservadas al humano, y una única app publicada para todos los creadores se
aproxima a una plataforma centralizada, mientras que el kit es replicable por cada creador.

## Opciones de exposición para M2

| Opción | Requisitos documentados | Observación |
|---|---|---|
| Túnel de desarrollo o servicio de reenvío HTTPS | admitido para pruebas locales (F5) | Expone el servidor local a internet; elegir y operar el servicio es una acción reservada al humano |
| Secure MCP Tunnel | `tunnel-client` con salida HTTPS a `api.openai.com:443`; organización de la Plataforma de OpenAI con permisos de túnel; asociación del túnel con el espacio de ChatGPT (F6) | Para cuentas personales, F6 indica usar la organización personal de la Plataforma; no verifica que la asociación funcione con una cuenta personal de ChatGPT |

Las dos opciones se configuran en ChatGPT de forma distinta: la primera con la URL pública del
servidor, la segunda eligiendo `Tunnel` y un `tunnel_id` (F5). Mezclarlas en un mismo
procedimiento haría indistinguible un error de configuración de una incompatibilidad de la
cuenta.

### Exposición ofrecida en la conexión real

Se ofrece **una sola**: un Quick Tunnel de Cloudflare, dentro de la primera opción.

- Se inicia con `cloudflared tunnel --url http://localhost:8080`, ajustando el puerto; no
  requiere cuenta de Cloudflare; imprime en la terminal un subdominio aleatorio (F9).
- "Quick Tunnels are intended for testing and development only"; límite de 200 solicitudes en
  curso; sin garantía de disponibilidad (F9).
- **"Quick Tunnels do not support Server-Sent Events (SSE)"** (F9). El SDK de MCP usado responde
  por SSE por omisión, así que la sonda se configuró para no usar SSE en ningún punto: HTTP sin
  estado, respuestas JSON y `405` ante el `GET` que abriría un stream iniciado por el servidor.
  Ambas formas son válidas en el transporte HTTP con streaming de MCP.
- En Windows, F10 ofrece descarga directa del ejecutable desde GitHub; la URL de la última
  versión para 64 bits se verificó el 2026-09-10.

Secure MCP Tunnel **no se ofrece** en esta prueba: agrega requisitos propios —organización de la
Plataforma, permisos de túnel y asociación con el espacio de ChatGPT— cuya falla no tiene
relación con la propiedad que se quiere demostrar, y que F6 no confirma para cuentas personales.
Queda disponible como alternativa para un contrato posterior, si la exposición elegida no
alcanzara.

## Resultado empírico de la primera conexión real

La conexión real ejecutada contra el contrato congelado en `f181d3728b7e8fa09045a1f0ac6acd11f9e407e5`
está interpretada en `francogg89-ai/audit-chatgpt-z @ 856df0c3f7b50b9255ea4acabd51685222a149fe`,
`resoluciones/H-U1-CONEXION-REAL-b5115ff0a28f06262e42968580711e6d64907960.md`. Para M2, en la cuenta
**ChatGPT Plus personal** usada, sin administrador:

- El modo desarrollador existió y pudo activarse; la app se creó por URL pública con
  "No Authentication", y el escaneo encontró las herramientas.
- Se ejecutaron lecturas y **una escritura real**, que después se recuperó. Esto resuelve, para
  esa cuenta, la contradicción entre F2 y F4 a favor de F4. No se extiende a otras cuentas ni a
  otros planes.
- ChatGPT **no pidió confirmación** antes de la escritura, aunque F4 dice que las acciones de
  escritura la requieren por omisión. El producto no puede apoyarse en esa confirmación para
  proteger acciones que exigen autorización del creador.
- El cliente se identifica como `openai-mcp/1.0.0`, y como `openai-mcp/1.0.0 (Codex)` en las
  llamadas a herramientas. Descubre el servidor con `server/discover`, no con `initialize`.
- Al mostrar un original, **el texto del modelo no fue literal**: cambió `SINTETICO` por
  `SINTÉTICO`. El servidor había devuelto el original exacto.

## Resultado empírico de la segunda conexión real

Ejecutada contra los contratos `C-U1-2A` y `C-U1-2B` congelados en
`cb023ed6c53dd63470da9463a6ea1697294f1055`, e interpretada en
`francogg89-ai/audit-chatgpt-z`,
`resoluciones/H-U1-CONEXION-REAL-2-9c026956cf1cffd35d25f6c506b8a9236fa64989.md`. Los dos contratos
resultaron en éxito. La consolidación completa está en `RESULTADO.md`; acá quedan solo los puntos
que la documentación no resolvía:

- **Las vistas de MCP Apps funcionan en la cuenta Plus personal usada.** El anfitrión pidió la
  plantilla con `resources/read` y renderizó la vista, que mostró el original de `P-042` con la
  huella del texto mostrado igual a la del servidor. Ninguna fuente lo declaraba para apps de modo
  desarrollador en Plus.
- **La falta de confirmación antes de escribir se repitió**, con la herramienta anotada como no
  `readOnlyHint`. Es el caso en que F4 promete confirmación y no la hubo.
- **La elección de herramienta no es determinista**: ante la misma petición, una conversación usó
  `show_proposal` y la otra `get_proposal`. La documentación no describe cómo el modelo elige entre
  una herramienta con vista y otra sin vista.
- **La atribución visible de la app aparece en el panel `Sources`**, no siempre como bloque de
  llamada en línea. No es una señal en la que el creador pueda apoyarse.
- **El rechazo de una app inválida no atribuye causa**: `Error creating connector / Something went
  wrong…`, sin mención de plan, cuenta, política, rol ni permisos.

## Presentación fiel de contenido

El texto que el modelo escribe es una regeneración, no una copia. Para mostrar un original sin
alteraciones hace falta un canal que no pase por el modelo.

- Una herramienta puede declarar un recurso de interfaz con `_meta.ui.resourceUri`, que apunta a
  un recurso `ui://` servido como `text/html;profile=mcp-app`. ChatGPT lo renderiza en un iframe,
  y el anfitrión le entrega el resultado de la herramienta por `ui/notifications/tool-result`
  (F11, F12).
- La vista debe iniciar el saludo con `ui/initialize` y avisar `ui/notifications/initialized`;
  el anfitrión le envía el resultado después de ese saludo (F12).
- La vista recibe el `structuredContent` de la herramienta. El modelo solo elige la herramienta y
  su argumento: no transcribe el contenido.
- F11 recomienda mantener las herramientas útiles sin interfaz, para clientes que no la
  renderizan.
- Ninguna fuente consultada declara expresamente la disponibilidad de estas vistas para apps de
  modo desarrollador en Plus. La segunda conexión real lo verificó empíricamente para la cuenta
  usada, y solo para ella.

## Costos y datos

- La documentación consultada no declara un costo adicional por usar el modo desarrollador. No
  se afirma que no exista. En las dos conexiones reales no se observó ningún cargo distinto de la
  suscripción Plus ya contratada, ni ningún límite de uso de ChatGPT.
- En Free, Plus, Go y Pro, "OpenAI may use information accessed from apps to train our models
  if your 'Improve the model for everyone' setting is on" (F3). La sonda usa solo datos
  sintéticos; para las propuestas reales del producto es una restricción de privacidad que U2 y
  U4 deben tratar.

## Mecanismo seleccionado para la conexión real

**M2**, porque es el único documentado para cuentas personales y también está disponible en los
espacios de trabajo. M1 se descarta para la conexión real por no admitir creación en cuentas
personales; si la cuenta de referencia fuese un espacio de trabajo y M2 fallara, probar M1
requeriría un contrato nuevo. M3 queda fuera por las razones indicadas.
