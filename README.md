ap_verify_ci_dc2
================

Simulated LSST data from `/repo/dc2`, for testing alert production in the LSST Science Pipelines.

This and other ap_verify "datasets" are based on  [ap_verify_dataset_template](https://github.com/lsst-dm/ap_verify_dataset_template).

Contains two overlapping exposures of `LSSTCam-imSim` from DC2 `tract=4431`, with `patches=(9,10,16,17)`:

* visit=982985, detector=164
* visit=943296, detector=168

Relevant Files and Directories
------------------------------
path                  | description
:---------------------|:-----------------------------
`doc`                 | Contains Sphinx package documentation for the dataset. This documentation may be linked to from other packages, such as `ap_verify`.
`etc`                 | Files necessary for reconstructing the repo (e.g. refcat yaml ingest files).
`raw`                 | Raw ImSim exposures.
`config`              | Dataset-specific configs to help the Science Pipelines work with this dataset, including the butler `export.yaml` file used by `ap_verify.py`
`pipelines`           | To be populated with dataset-specific pipelines. Currently contains three example files specialized for ImSim data.
`preloaded`           | Starter Butler repo containing a skymap, calibs, coadds to use as difference imaging templates, ImSim refcats covering the relevant sky region, mock APDB outputs based on the raw images, and a pretrained machine learning model for real/bogus classification.
`scripts`             | Scripts for regenerating this dataset.

Butler Collections
------------------

The butler repository in `preloaded/` contains the following collections; these may be chained collections containing arbitrarily-named runs.

collection              | description
:-----------------------|:-----------------------------
`<instrument>/calib`    | Master calibration files for the data in the `raw` directory.
`refcats`               | Level 7 HTM shards from relevant reference catalogs.
`skymaps`               | Skymaps for the template coadds.
`templates/<type>`      | Coadd images produced by a compatible version of the LSST pipelines. For example, `deepCoadd` images go in a `templates/deep` collection.
`dia_catalogs`          | Catalogs representing the contents of the APDB at the start of each visit.
`models`                | Pretrained machine learning models.
`<instrument>/defaults` | A chained collection linking all of the above.

Git LFS
-------

To clone and use this repository, you'll need Git Large File Storage (LFS).

Our [Developer Guide](http://developer.lsst.io/en/latest/tools/git_lfs.html) explains how to setup Git LFS for LSST development.

Usage
-----

`ap_verify_ci_dc2` is designed to be run using [`ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/), which is distributed as part of the `lsst_distrib` package of the [LSST Science Pipelines](https://pipelines.lsst.io/).

This dataset is not included in `lsst_distrib` and is not available through `newinstall.sh`.
However, it can be installed explicitly with the [LSST Software Build Tool](https://developer.lsst.io/stack/lsstsw.html) or by cloning directly:

    git clone https://github.com/lsst/ap_verify_ci_dc2/
    setup -r ap_verify_ci_dc2

See the Science Pipelines documentation for more detailed instructions on [installing datasets](https://pipelines.lsst.io/modules/lsst.ap.verify/datasets-install.html) and [running `ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/running.html).
