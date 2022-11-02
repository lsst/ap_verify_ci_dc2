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

"""Find the refcats that cover the desired dataIds, copy them to a temporary
location, and ingest them into the preloaded butler.
"""

import os.path
import shutil
import tempfile

import astropy.table

from lsst.daf.butler import Butler, CollectionType, DatasetType
from lsst.daf.butler.script import ingest_files


REPO = "/repo/dc2"
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
REPO_LOCAL = os.path.join(SCRIPT_DIR, "..", "preloaded")
DATA_IDS = [dict(detector=164, visit=982985, instrument="LSSTCam-imSim"),
            dict(detector=168, visit=943296, instrument="LSSTCam-imSim")]
REFCAT_NAME = "cal_ref_cat_2_2"

butler = Butler(REPO)

query = "(instrument='{instrument}' and detector={detector} and visit={visit})"
where = " or ".join(query.format(**id) for id in DATA_IDS)
refcats = set(butler.registry.queryDatasets(REFCAT_NAME, where=where, collections="refcats"))

table = astropy.table.Table(names=("filename", "htm7"), dtype=("str", "int"))

with tempfile.TemporaryDirectory() as tmp:
    for refcat in refcats:
        uri = butler.getURI(refcat, collections="refcats")
        file = os.path.join(tmp, uri.split()[-1])
        shutil.copy(uri.path, file)
        table.add_row((file, refcat.dataId["htm7"]))

    with tempfile.NamedTemporaryFile(suffix=".ecsv") as ingest_file:
        table.write(ingest_file.name, overwrite=True)

        local_butler = Butler(REPO_LOCAL, writeable=True)
        dataset_type = DatasetType(REFCAT_NAME,
                                   ["htm7"],
                                   "SimpleCatalog",
                                   universe=local_butler.registry.dimensions,
                                   isCalibration=False)
        local_butler.registry.registerDatasetType(dataset_type)
        ingest_files(REPO_LOCAL, REFCAT_NAME, f"refcats/{REFCAT_NAME}", ingest_file.name, transfer="copy")
        local_butler.registry.registerCollection("refcats", CollectionType.CHAINED)
        local_butler.registry.refresh()
        local_butler.registry.setCollectionChain("refcats", [f"refcats/{REFCAT_NAME}"])
