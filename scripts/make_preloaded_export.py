#!/usr/bin/env python
"""
Make the butler export yaml file to be used by ap_verify runs.
"""

import argparse
import logging
import os
import sys

import lsst.log
import lsst.skymap
import lsst.daf.butler as daf_butler
import lsst.ap.verify as ap_verify


def _make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True,
                        help="The name of the dataset as recognized by ap_verify.py.")
    return parser


def main():
    # Ensure logs from tasks are visible
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    lsst.log.configure_pylog_MDC("DEBUG", MDC_class=None)

    args = _make_parser().parse_args()
    dataset = ap_verify.dataset.Dataset(args.dataset)
    gen3_repo = os.path.join(dataset.datasetRoot, "preloaded")

    logging.info("Exporting registry to configure new repos...")
    _export_for_copy(dataset, gen3_repo)


def _export_for_copy(dataset, repo):
    """Export a butler repository so that a dataset can make copies later.

    Parameters
    ----------
    dataset : `lsst.ap.verify.dataset.Dataset`
        The dataset needing the ability to copy the repository.
    repo : `str`
        The location of the repository.
    """
    butler = daf_butler.Butler(repo)
    with butler.export(directory=dataset.configLocation, format="yaml") as contents:
        # Need all detectors, even those without data, for visit definition
        contents.saveDataIds(butler.registry.queryDataIds({"detector"}).expanded())
        contents.saveDatasets(butler.registry.queryDatasets(datasetType=..., collections=...))
        # Explicitly save the calibration and chained collections.
        # Do _not_ include the RUN collections here because that will export
        # an empty raws collection, which ap_verify assumes does not exist
        # before ingest.
        target_types = {daf_butler.CollectionType.CALIBRATION, daf_butler.CollectionType.CHAINED}
        for collection in butler.registry.queryCollections(..., collectionTypes=target_types):
            contents.saveCollection(collection)
        # Export skymap collection even if it is empty
        contents.saveCollection(lsst.skymap.BaseSkyMap.SKYMAP_RUN_COLLECTION_NAME)
        # Dataset export exports visits, but need matching visit definitions as
        # well (DefineVisitsTask won't add them back in).
        contents.saveDimensionData("exposure",
                                   butler.registry.queryDimensionRecords("exposure"))
        contents.saveDimensionData("visit_definition",
                                   butler.registry.queryDimensionRecords("visit_definition"))
        contents.saveDimensionData("visit_detector_region",
                                   butler.registry.queryDimensionRecords("visit_detector_region"))


if __name__ == "__main__":
    main()
