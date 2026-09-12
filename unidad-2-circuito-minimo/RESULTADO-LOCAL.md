# RESULTADO LOCAL — Unidad 2: lo que el bloque local dejó demostrado

Integra durablemente el resultado de los contratos locales de U2, para que no dependa de leer el
`EVENTO.md` de una entrega que después se reemplaza. Es material de trabajo, no un veredicto:
quién interpretó cada corrida y con qué resultado está en las auditorías citadas.

**Qué no hace este documento.** No declara U2 cerrada. No sustituye a los contratos ni a sus
interpretaciones. No extiende ninguna observación a un candidato distinto del que corrió.

## Identidad de lo que sostiene este resultado

| Qué | Identidad exacta |
|---|---|
| Contrato `C-U2-1` | `unidad-2-circuito-minimo/EVENTO.md`, blob `aa20b7cc648a2e159478f13f1f9e3a68d641f685`, sobre `work-claude-z @ bddc126ab0e7f15f386220015088cd27dd64a459` |
| Congelamiento de `C-U2-1` | `audit-chatgpt-z @ 625b0bbabc181a68d4f5eb43ad803d777eeef0ec` |
| Resultado de `C-U2-1` | **FALLO** en C2.3; interpretado en `audit-chatgpt-z @ 8aea847d731ac65bacb9d4089041f1bf7adacb80` |
| Evidencia de `C-U2-1` | `unidad-2-circuito-minimo/evidencia/`, diecinueve artefactos |
| Contrato `C-U2-2` | `unidad-2-circuito-minimo/EVENTO.md`, blob `e3d439b57ff5555354cbfa4e4e92a91f630ca1f0`, sobre `work-claude-z @ 320a643b3880b2e6522b9dfb35a708c5fb898713` |
| Congelamiento de `C-U2-2` | `audit-chatgpt-z @ 5ab5a6457f9b39966277ad38c92c154de8dbc968` |
| Resultado de `C-U2-2` | **ÉXITO**; interpretado en `audit-chatgpt-z @ 4d41104700ba4aa1b99c0169b711874df59bd2da` |
| Evidencia de `C-U2-2` | `unidad-2-circuito-minimo/evidencia-c-u2-2/`, diecinueve artefactos |

Los dos paquetes se conservan. El de `C-U2-1` documenta un fallo y un defecto —el contacto que
volvía en la página de rechazo y el testigo que quedaba en claro— y por eso no se reescribe.

## Qué quedó demostrado, y sobre qué candidato

Sobre `320a643b3880b2e6522b9dfb35a708c5fb898713`, con datos sintéticos, sin red y sin ningún
modelo:

| Caso de `PLAN.md` | Qué quedó demostrado |
|---|---|
| C2.1 | El ciclo cierra: una misma propuesta, `P-001`, recorre recepción, ronda, evaluación, invitación, ampliación, segunda evaluación, publicación autorizada y voto, y cada paso quedó trazado en la evidencia |
| C2.2 | El original conserva su huella `5b97906e` después de la ampliación; la ampliación es un registro nuevo con su propia autoría y su tipo; la segunda evaluación la cita |
| C2.3 | Ningún dato de contacto aparece en ninguna superficie pública, en ninguna respuesta del conector ni en la evidencia, incluidas las páginas de rechazo del formulario |
| C2.4 | Publicar sin la autorización del creador se rechaza y no publica nada |
| C2.5 | Repetir el identificador de operación no crea una segunda invitación ni una segunda entrada publicada |
| C2.9 | La guía pública contiene objetivo, criterios, condiciones, plazos y forma de participar, y un envío compuesto solo con eso es aceptado |
| C2.12 | Cada propuesta pertenece a un solo canal y cada ronda fija su conjunto; lo recibido después de un corte cae en el siguiente |
| C2.13 | Un envío a la convocatoria ya cortada se rechaza nombrando el canal permanente, sin reasignar nada |
| C2.14 | Los campos anunciados antes de enviar son exactamente los que exponen el portal y la vista de vivo, sin sobrantes ni faltantes |
| C2.15 | Toda superficie que muestra la fecha la presenta como recepción en el sistema y ninguna afirma autoría |

Además quedó demostrada la propiedad que `PLAN.md` exige antes de abrir una convocatoria: no hubo
recepción ni corte antes de que el creador aprobara la interpretación de sus criterios, y la
discrepancia que devolvió quedó registrada.

## Qué **no** demuestra

- Nada sobre la operación real desde la IA contratada: C2.6, C2.7, C2.8, C2.10 y C2.11 siguen
  pendientes y necesitan su propio contrato.
- Nada sobre interoperabilidad de la autenticación del extremo: el flujo de autorización está
  implementado y ejercitado localmente, pero que un anfitrión real lo complete solo lo muestra la
  corrida real.
- Nada sobre datos reales, volumen, concurrencia ni comprensión de una persona real. La evaluación
  la produjo un ejecutor determinista, no un modelo.
- El control de votación marca el navegador; no comprueba identidad de personas.

## Qué condiciona en lo que sigue

1. El circuito local es el que se opera en la corrida real: lo que allí se ejercita es la
   operación conversacional sobre este mismo material, no otro.
2. Publicar e invitar seguirán exigiendo la autorización del creador en el panel, también cuando
   el conector esté autorizado: tener token no alcanza.
3. El original se muestra por la vista del conector, no por la prosa del modelo, porque U1 midió
   que esa prosa no es literal.
4. La exposición pública alcanzable sigue siendo una necesidad material del humano (H-2) y no se
   resuelve con nada de lo demostrado acá.
