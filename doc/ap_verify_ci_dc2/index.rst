.. _ap_verify_ci_dc2-package:

################
ap_verify_ci_dc2
################

The ``ap_verify_ci_dc2`` package is a minimal collection of images from the simulated DC2 dataset, formatted for use with :doc:`/modules/lsst.ap.verify/index`.
It is intended as a basic functionality test for the Alert Production pipeline.

.. _ap_verify_ci_dc2-using:

Using ap_verify_ci_dc2
======================

This dataset is designed for "quick and dirty" integration testing of the existing alert production verification tooling.
The input data were chosen arbitrarily, so they are not even suitable for testing of difference imaging analysis.

.. _ap_verify_ci_dc2-contents:

Dataset contents
================

The ``preloaded/`` butler repo contains two overlapping exposures of ``LSSTCam-imSim`` from DC2 ``tract=4431``, with ``patches=(9,10,16,17)``, ``goodSeeingCoadd`` datasets for those patches to make templates from, DC2 refcats covering that region, and skymaps, calibrations, and pretrained ML models necessary to process the data.

* visit=982985, detector=164
* visit=943296, detector=168

.. _ap_verify_ci_dc2-contributing:

Contributing
============

``ap_verify_ci_dc2`` is developed at https://github.com/lsst/ap_verify_ci_dc2.
You can find Jira issues for this module under the `ap_verify <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20ap_verify%20AND%20text~"DC2">`_ component.

.. If there are topics related to developing this module (rather than using it), link to this from a toctree placed here.

.. .. toctree::
..    :maxdepth: 1
