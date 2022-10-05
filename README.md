ap_verify_ci_dc2
================

Data from the DC2 simulated dataset, to test basic functionality of alert production.

Relevant Files and Directories
------------------------------
path                  | description
:---------------------|:-----------------------------
`doc`                 | Contains Sphinx package documentation for the dataset. This documentation may be linked to from other packages, such as `ap_verify`.
`raw`                 | TBD
`config`              | Dataset-specific configs to help Stack code work with this dataset.
`pipelines`           | Dataset-specific pipelines to run on this dataset.
`preloaded`           | A Gen 3 Butler repository with contents TBD.
`dataIds.list`        | List of dataIds in this repo. For use in running Tasks. Currently set to run all Ids.
`scripts`             | Scripts and data for generating this dataset.

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
