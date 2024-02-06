#!/usr/bin/bash
# Run this file to recreate preloaded into a fresh state.

set -e
set -x

# base butler repo and instrument
bash scripts/make_empty_preloaded_butler.sh

# get calibs from original repo
python scripts/import_calibs.py -c 2.2i/calib

# skymaps, as produced by export_skymaps.py
butler import -t copy --export-file etc/skymaps.yaml preloaded/ /sdf/group/rubin/repo/dc2

# templates
butler register-dataset-type preloaded/ goodSeeingCoadd ExposureF band skymap tract patch
butler ingest-files -t copy preloaded/ goodSeeingCoadd templates/goodSeeing etc/templates.ecsv

# refcats
python scripts/get_refcats.py

# pretrained NN models
python scripts/get_nn_models.py -m rbResnet50-DC2

# collection chains
butler collection-chain preloaded LSSTCam-imSim/defaults templates/goodSeeing skymaps LSSTCam-imSim/calib \
    refcats models


# make the export file for ap_verify to use
python scripts/make_preloaded_export.py --dataset ap_verify_ci_dc2
