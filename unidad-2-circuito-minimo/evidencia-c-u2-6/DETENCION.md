# Detención de C-U2-6 en P0

CANDIDATE_WORK_SHA=00191fced16826fe4e67bcdc2dd9b147115dafb0
CONTRACT_BLOB_SHA=fa2ef53e760f849af0772af7181f342f3310f805
CHECKPOINT_BLOB_SHA=5d38c62b8ef97ea99430846d0cff7d20fe23a130

## Comando literal ejecutado

```text
python -m pytest -q tests/test_comandos_literales.py
```

## Resultado

La ejecución terminó con resultado no cero porque el intérprete informó:

```text
C:\Python312\python.exe: No module named pytest
```

La salida completa real queda preservada en `p0-comandos.txt`.

## Regla aplicada

El checkpoint exige que P0 termine con código 0 y, si no, ordena detenerse sin comenzar P1. No se ejecutaron C0, P1-P11, R0, R1-R6 ni RZ. No se abrió túnel, no se usó ChatGPT real y no se compartieron secretos. No hubo reintento ni instalación posterior.
