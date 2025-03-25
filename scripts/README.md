Dataset management scripts
==========================

This directory has  scripts for (re)creating the `ap_verify_ci_dc2` dataset.

*Any* change to the repo requires running `make_preloaded_export.py` to ensure the export file is up-to-date.
The data set will not run correctly without this step, but it also makes it easy to see and review each commit's changes.

Most scripts are designed to be modular, and can be called either all at once (through `make_preloaded.sh`), or individually.
However, `generate_fake_injection_catalog.sh` and `import_calibs.py` are not self-contained, and the user may need to manually edit chains before or after running them.
See each script's docstring for usage instructions; those scripts that take arguments also support `--help`.

Contents
--------
path                               | description
:----------------------------------|:-----------------------------
make_preloaded.sh                  | Rebuild everything from scratch.
generate_fake_injection_catalog.sh | Create source injection catalogs in tract 4431. Requires templates.
generate_self_preload.py           | Create preloaded APDB datasets by simulating a processing run with no pre-existing DIAObjects.
get_nn_models.py                   | Transfer a selected pretrained model from an external repo (such as `repo/main`) and register it in `preloaded/`.
get_refcats.py                     | Transfer refcats from an external repo (such as `repo/main`) and register them in `preloaded/`.
import_calibs.py                   | Transfer calibs from an external repo (such as `repo/main`) and register them in `preloaded/`.
import_templates.py                | Transfer templates from an external repo (such as `repo/main`) and register them in `preloaded/`.
make_empty_preloaded_butler.sh     | Replace `preloaded/` with a repo containing only dimension definitions and standard "curated" calibs.
make_preloaded_export.py           | Create an export file of `preloaded/` that's compatible with `butler import`.
