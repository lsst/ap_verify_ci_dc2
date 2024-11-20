#!/usr/bin/env python
# This file is part of ap_verify_ci_dc2.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Script for copying templates appropriate for these fields.

The datasets can be from any source.

Example:
$ python import_dia_preload.py -t "u/me/DM-123456-template"
imports DIA preload sources from u/me/DM-123456-template in /repo/dc2 to
dia_catalogs/apdb in this dataset's preloaded repo. See
import_dia_preload.sh -h for more options.
"""

import argparse
import logging
import os
import sys
import tempfile

import lsst.log
import lsst.skymap
from lsst.daf.butler import Butler, CollectionType


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
lsst.log.configure_pylog_MDC("DEBUG", MDC_class=None)


########################################
# Command-line options

def _make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="source_repo", default="/repo/dc2",
                        help="Repo to import from, defaults to '/repo/dc2'.")
    parser.add_argument("-t", dest="source_collection", required=True,
                        help="Collection to import from.")
    parser.add_argument("-w", dest="where",
                        help="Query datasets dimension expression to restrict the datasets "
                             "that will be imported from the source collection.")
    return parser


args = _make_parser().parse_args()


########################################
# Export/Import

PRELOAD_TYPES = ["preloaded_diaSources", "preloaded_diaObjects", "preloaded_diaForcedSources"]
TEMPLATE_COLLECT = "preloade/apdb"
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_REPO = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "preloaded"))


def _export(butler, export_file, where):
    """Export the files to be copied.

    Parameters
    ----------
    butler : `lsst.daf.butler.Butler`
        A Butler pointing to the repository and collection(s) to be
        exported from.
    export_file : `str`
        A path pointing to a file to contain the export results.
    where : `str`
        Query datasets dimension expression.

    Returns
    -------
    runs : iterable [`str`]
        The names of the runs containing exported templates.
    """
    with butler.export(filename=export_file, transfer=None) as contents:
        datasets = []
        for name in PRELOAD_TYPES:
            temp = butler.registry.queryDatasets(name, findFirst=True, where=where)
            logging.info(f"Found {len(list((temp)))} of {name}.")
            contents.saveDatasets(temp)
            datasets.extend(temp)
        # Do not save butler.collections -- if they are RUN collections, it's
        # redundant; if they are CHAINED, they likely contain content that
        # isn't being transferred.
        return {t.run for t in datasets}


def _import(butler, export_file, base_dir):
    """Import the exported files.

    Parameters
    ----------
    butler : `lsst.daf.butler.Butler`
        A Butler pointing to the dataset repository.
    export_file : `str`
        A path pointing to a file containing the export results.
    base_dir : `str`
        The base directory for the file locations in ``export_file``.
    """
    butler.import_(directory=base_dir, filename=export_file, transfer="copy")


with tempfile.NamedTemporaryFile(suffix=".yaml") as export_file:
    source_butler = Butler(args.source_repo, collections=args.source_collection, writeable=False)
    runs = _export(source_butler, export_file.name, args.where)
    dest_butler = Butler(DATASET_REPO, writeable=True)
    import os; print(os.getpid()); import ipdb; ipdb.set_trace();
    _import(dest_butler, export_file.name, args.source_repo)
    dest_butler.registry.registerCollection(TEMPLATE_COLLECT, CollectionType.CHAINED)
    dest_butler.registry.setCollectionChain(TEMPLATE_COLLECT, runs)

logging.info(f"DIA preload datasets stored in {DATASET_REPO}:{TEMPLATE_COLLECT}.")
