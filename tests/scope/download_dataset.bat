@echo off
REM Download yaqiangsun/qubit_examples dataset from ModelScope to tmp directory

setlocal enabledelayedexpansion

set "TMP_DIR=.\tmp"
set "DATASET=yaqiangsun/qubit_examples"
set "TARGET_DIR=%TMP_DIR%\yaqiangsun\qubit_examples"

if not exist "%TMP_DIR%" mkdir "%TMP_DIR%"

echo Downloading dataset %DATASET% to %TARGET_DIR%...
modelscope download --dataset %DATASET% --local_dir "%TARGET_DIR%"

echo Download complete! Files saved to: %TARGET_DIR%
dir "%TARGET_DIR%"

endlocal