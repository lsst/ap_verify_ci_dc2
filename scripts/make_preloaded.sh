#!/usr/bin/bash
# Run this file to recreate preloaded into a fresh state.

set -e
set -x

# base butler repo and instrument
bash scripts/make_empty_preloaded_butler.sh

# get calibs from original repo
python scripts/import_calibs.py -c 2.2i/calib

# templates
python scripts/import_templates.py -t u/elhoward/DM-38451/templates -w "skymap='DC2' and tract=4431 and patch IN(9,10,16,17) and band='r'"

# refcats
python scripts/get_refcats.py

# pretrained NN models
python scripts/get_nn_models.py -m rbResnet50-DC2

bash scripts/generate_fake_injection_catalog.sh -b preloaded -o fake-injection-catalog

# collection chains
butler collection-chain preloaded LSSTCam-imSim/defaults templates/goodSeeing skymaps LSSTCam-imSim/calib \
    refcats models fake-injection-catalog

# make the export file for ap_verify to use
python scripts/make_preloaded_export.py --dataset ap_verify_ci_dc2
