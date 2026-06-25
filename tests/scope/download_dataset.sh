#!/bin/bash
# Download yaqiangsun/qubit_examples dataset from ModelScope to tmp directory

set -e

TMP_DIR="./tmp"
DATASET="yaqiangsun/qubit_examples"
TARGET_DIR="${TMP_DIR}/yaqiangsun/qubit_examples"

mkdir -p "${TMP_DIR}"

echo "Downloading dataset ${DATASET} to ${TARGET_DIR}..."
modelscope download --dataset "${DATASET}" --local_dir "${TARGET_DIR}"

echo "Download complete! Files saved to: ${TARGET_DIR}"
ls -la "${TARGET_DIR}"