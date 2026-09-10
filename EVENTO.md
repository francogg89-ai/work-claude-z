# EVENTO — Intervención constitutiva del CONSTRUCTOR

Intervención previa a toda unidad, en la raíz del repositorio de trabajo. Explica la semántica
de la entrega; no repite lo que Git demuestra por sí mismo.

## Qué recibió

Un `next_prompt` de constitución inicial del primer CONSTRUCTOR, con `INCOMING_TURN_ID=1`
entero, emitido por el AUDITOR constituyente. Transportó identidad del trabajo y carril, método
gobernante, reglas de transporte, manifiesto, constitución, repositorios de trabajo, auditoría
y fuentes, raíz y rutas locales, entornos relevantes, capacidades delegadas, y la identidad
exacta del bootstrap del AUDITOR.

El prompt es transporte, no autoridad. Las identidades exactas que transportó se comprobaron
contra las fuentes antes de producir material.

## Qué hizo y por qué

1. Cargó `metodo/REVOLUTIONS.md` y `metodo/ROL-CONSTRUCTOR.md` en la identidad exacta del
   método gobernante, antes de cualquier acción sustantiva, conforme exige el propio método.
2. Localizó y leyó el bootstrap del AUDITOR constituyente en su identidad exacta.
3. Leyó la constitución inicial y el manifiesto aprobado en sus identidades exactas.
4. Comprobó el entorno local y las capacidades necesarias para esta intervención.
5. Creó `BOOTSTRAP.md`, preservando los hechos de origen y la identidad exacta del bootstrap
   del AUDITOR, porque las dos historias Git son independientes y ninguna puede inferir esa
   relación.
6. Creó `PLAN.md`.

No se aplicó el protocolo de derivación D1–D6: en la constitución inicial no existe todavía un
corte de work sobre el cual aplicarlo, y el método lo excluye expresamente para este caso.

No se ejecutó ninguna unidad material. El plan requiere auditoría y aprobación humana antes de
ejecutar sus unidades.

## Comprobación de capacidades

Ejecutado en el Windows local del CONSTRUCTOR, bajo `ROOT_LOCAL`.

| Comprobación | Resultado |
|---|---|
| `git -C <clon> rev-parse HEAD` en los cuatro clones fuente | `manifiestos-trabajo-ai` d369b2f21f35ec0ecaefdf579752a90c98b1c4dd; `metodo-manifiestos-ai` 452d8cce2dd36106e0efce0c957b951c713fdcc8; `rules-orchestrator-ai` e04e653fe6b9d3f394c18dee18274090ddb79ff9; `orchestra-revolutions-ai` 4d88fce3ed3c87bd231c45ec60dcb713538b2514 |
| `git cat-file -t` sobre las siete identidades exigidas por la constitución | las siete existen y son `commit`; rc=0 |
| `git -C audit-chatgpt-z fetch origin` y `ls-remote` | `origin/main` = b151dd8ebd2481283872e9437bb0f9cc8607811d; el clon local no tenía HEAD por haber sido clonado vacío |
| `git -C audit-chatgpt-z show b151dd8…:BOOTSTRAP.md` | bootstrap del AUDITOR leído en su identidad exacta |
| `git -C work-claude-z rev-list --count --all` y `ls-remote --heads origin` | 0 commits locales y 0 ramas remotas antes de esta intervención; rama `main` |
| `node --version`, `python --version`, `git --version` | v20.15.1; Python 3.12.4; git 2.54.0.windows.1 |
| `gh auth status` | sesión autenticada como `francogg89-ai`, con alcance `repo`; el valor del token no se registra ni se transporta |

Ningún blob de los repositorios fuente fue modificado y no se escribió fuera de
`work-claude-z`.

## Limitaciones de esta entrega

- La capacidad de publicar en `work-claude-z` no se comprobó por adelantado: su evidencia es la
  existencia del propio commit de esta intervención en el remoto, comprobable por el AUDITOR
  desde la fuente. Un `gh auth status` con alcance `repo` indica permiso declarado, no
  escritura ejercida.
- El `PLAN.md` no ejercita ninguna de sus verificaciones. Define casos, resultados esperados y
  condiciones de aceptación; los contratos previos discriminantes se propondrán en el
  `EVENTO.md` de cada unidad, antes de ejecutar, para que el AUDITOR los congele.
- No se comprobó ninguna integración externa. La viabilidad de operar desde la IA contratada
  del creador es exactamente la incertidumbre que la unidad 1 debe resolver, y este plan no la
  presume resuelta en ningún sentido.
- El directorio `.atl/` presente en el árbol de trabajo es material de herramientas del entorno
  local, ajeno a esta entrega; queda sin seguimiento y fuera del commit.

## Necesidad humana detectada

NECESIDAD DEL HUMANO — ejecutar las unidades de `PLAN.md` excede el perímetro delegado
vigente: la constitución del carril Z reserva al humano la aprobación del plan, y ninguna
unidad puede iniciarse sin ella. Esta intervención preserva el plan y se detiene antes de la
primera unidad.

Lo que se necesita es la aprobación humana de `PLAN.md` sobre su identidad exacta, y en
particular la decisión sobre la división en cuatro unidades y su secuencia.

El CONSTRUCTOR registra y rutea esta necesidad; no declara que sea real ni activa al humano.
Esa determinación corresponde al AUDITOR.
