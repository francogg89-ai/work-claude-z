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

## Costos y datos

- La documentación consultada no declara un costo adicional por usar el modo desarrollador. No
  se afirma que no exista.
- En Free, Plus, Go y Pro, "OpenAI may use information accessed from apps to train our models
  if your 'Improve the model for everyone' setting is on" (F3). La sonda usa solo datos
  sintéticos; para las propuestas reales del producto es una restricción de privacidad que U2 y
  U4 deben tratar.

## Mecanismo seleccionado para la conexión real

**M2**, porque es el único documentado para cuentas personales y también está disponible en los
espacios de trabajo. M1 se descarta para la conexión real por no admitir creación en cuentas
personales; si la cuenta de referencia fuese un espacio de trabajo y M2 fallara, probar M1
requeriría un contrato nuevo. M3 queda fuera por las razones indicadas.
