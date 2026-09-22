# AUTORIZACION MATERIAL — C-U2-8 / GATE-INTENTO-1

ATTEMPT_NUMBER=1
PARENT_WORK_SHA=8767b85c18206d903fcc5cc798937e59dfeda25a
CONTRACT_BLOB_SHA=454287de6c25b3a6dd5a6f983c3fe0b9b11d3c12
CHECKPOINT_BLOB_SHA=c031bade9667977bef0869ab120f23fe240a2ad8
AUDIT_SHA=cd998b6789e815ffbc5e7f6b695f6d64cbe4ecdf

H2=ACTIVADA
AUTORIZACION_HUMANA=SI

ALCANCE=Crear exclusivamente este registro material de autorización append-only para gate-intento-1.

PROHIBICIONES=Esta autorización no habilita ejecutar el gate ambiental, P0, C0, P1-P11, R0-R6 ni RZ; no habilita instalar dependencias, modificar el entorno, abrir túnel, usar ChatGPT real ni crear evidencia de ejecución.

REGLA_DE_DETENCION=Después de materializar este archivo, detenerse y devolver WORK_SHA_AUTORIZACION y AUTH_BLOB_SHA al AUDITOR. No ejecutar ningún comando del gate hasta recibir un nuevo sobre EJECUCION_GATE que referencie exactamente ATTEMPT_NUMBER=1, WORK_SHA_AUTORIZACION y AUTH_BLOB_SHA.

ORIGEN=Autorización humana explícita recibida para C-U2-8, limitada exclusivamente a la materialización de este archivo.