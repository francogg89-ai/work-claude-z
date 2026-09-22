# AUTORIZACION MATERIAL — C-U2-9 / GATE-INTENTO-1

ATTEMPT_NUMBER=1
PARENT_WORK_SHA=a8f054c4c52ea547bc89464216ab999fef5cb405
CONTRACT_BLOB_SHA=3c416d9d790624020bd422f273d8b6f487fce939
CHECKPOINT_BLOB_SHA=05edc4e08eedfd4ff52e4f2eb82b42eea9ceca8a
AUDIT_SHA=a6ba2c5ade4b11175f80d4bc0bb74e6fbe246d54

H2=ACTIVADA
AUTORIZACION_HUMANA=SI

ALCANCE=Crear exclusivamente este registro material de autorización append-only para gate-intento-1.

PROHIBICIONES=Esta autorización no habilita ejecutar el gate ambiental, P0, C0, P1-P11, R0-R6 ni RZ; no habilita instalar dependencias, modificar el entorno, abrir túnel, usar ChatGPT real ni crear gate-intento-1, comandos.txt, DETENCION.md o p0-comandos.txt.

REGLA_DE_DETENCION=Después de materializar este archivo, detenerse y devolver WORK_SHA_AUTORIZACION y AUTH_BLOB_SHA al AUDITOR. No ejecutar ningún comando del gate hasta recibir un nuevo sobre EJECUCION_GATE que referencie exactamente ATTEMPT_NUMBER=1, WORK_SHA_AUTORIZACION y AUTH_BLOB_SHA.

ORIGEN=Sobre MATERIALIZAR del AUDITOR a6ba2c5ade4b11175f80d4bc0bb74e6fbe246d54, posterior a la autorización humana para iniciar el handshake.