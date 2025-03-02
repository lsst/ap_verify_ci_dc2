#!/usr/bin/bash
# Run this file to recreate preloaded into a fresh state.

# Abort script on any error
set -e
# Echo all commands
set -x

SCRIPT_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"
DATASET_REPO="${SCRIPT_DIR}/../preloaded/"


# base butler repo and instrument
bash "${SCRIPT_DIR}/make_empty_preloaded_butler.sh"

# get calibs from original repo
python "${SCRIPT_DIR}/import_calibs.py -c 2.2i/calib"

# templates
python "${SCRIPT_DIR}/import_templates.py" -t u/elhoward/DM-38451/templates -w "skymap='DC2' and tract=4431 and patch IN(9,10,16,17) and band='r'"

# refcats
python "${SCRIPT_DIR}/get_refcats.py"

# pretrained NN models
python "${SCRIPT_DIR}/get_nn_models.py" -m rbResnet50-DC2

# Precomputed fake sources
bash "${SCRIPT_DIR}/generate_fake_injection_catalog.sh" -b preloaded -o fake-injection-catalog

# Preloaded APDB catalogs
python "${SCRIPT_DIR}/generate_self_preload.py"

# collection chains
butler collection-chain "${DATASET_REPO}" LSSTCam-imSim/defaults templates/goodSeeing skymaps LSSTCam-imSim/calib \
    refcats dia_catalogs models fake-injection-catalog

# make the export file for ap_verify to use
python "${SCRIPT_DIR}/make_preloaded_export.py"
