#!/bin/bash
set -e
FULL_CURR_PATH=$(realpath ${0%/*})
FLD_NAME=${FULL_CURR_PATH##*/}
OUTPUT_DIR=$(realpath ${0%/*}/../Wiki)
RUN_SERVER=${1-0}

mkdir -p ${OUTPUT_DIR}

cd ${OUTPUT_DIR}

ln -s -f "${FULL_CURR_PATH}/mkdocs.yml" "${OUTPUT_DIR}"
if [ ! -d ${OUTPUT_DIR}/docs ]; then
    ln -s "${FULL_CURR_PATH}" "${OUTPUT_DIR}/docs"
fi

# Build mkdocs
# sudo apt install mkdocs mkdocs-material -y
mkdocs build

# Test local
echo "To Test Locally:"
echo  "python -m http.server -d ${OUTPUT_DIR}/site 8000"

if [ ${RUN_SERVER} -gt 0 ]; then
	python -m http.server -d ${OUTPUT_DIR}/site 8000
fi

