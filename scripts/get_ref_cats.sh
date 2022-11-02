#!/usr/bin/bash
# Identify refcats to use for this dataset, copy them into place, and
# ingest them into the butler.

# identify refcats that overlap our detectors
butler query-datasets /repo/dc2 --where "(instrument='LSSTCam-imSim' and visit=982985 and detector=164) \
    or (instrument='LSSTCam-imSim' and visit=943296 and detector=168)" cal_ref_cat_2_2

# NOTE: the below lines were created manually using the refcat shard ids printed from the above command.

# copy those refcats
mkdir -p refcats/cal_ref_cat_2_2/
cp /datasets/DC2/DR6/Run2.2i/v19.0.0-v1/ref_cats/cal_ref_cat/147160.fits refcats/cal_ref_cat_2_2/
cp /datasets/DC2/DR6/Run2.2i/v19.0.0-v1/ref_cats/cal_ref_cat/147092.fits refcats/cal_ref_cat_2_2/

# ingest them into the butler
butler register-dataset-type REPO cal_ref_cat_2_2 SimpleCatalog htm7
butler ingest-files -t direct REPO cal_ref_cat_2_2 refcats/DM-34845 cal_ref_cat_2_2.ecsv
butler collection-chain REPO --mode extend refcats refcats/DM-34845
