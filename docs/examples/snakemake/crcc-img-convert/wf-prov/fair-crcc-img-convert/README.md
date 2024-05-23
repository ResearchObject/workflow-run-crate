# Snakemake workflow: `FAIR CRCC - image conversion`

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.3.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/crs4/fair-crcc-img-convert/workflows/Tests/badge.svg?branch=main)](https://github.com/crs4/fair-crcc-img-convert/actions?query=branch%3Amain+workflow%3ATests)


A Snakemake workflow for converting whole-slide images (WSI) from the [CRC
Cohort](https://www.bbmri-eric.eu/scientific-collaboration/colorectal-cancer-cohort/)
from vendor-specific image formats to open image formats (at the moment,
OME-TIFF).  The workflow also encrypts the new image files with
[Crypt4GH](https://doi.org/10.1093/bioinformatics/btab087).


## What's the CRC Cohort?

The CRC Cohort is a collection of clinical data and digital high-resolution
digital pathology images pertaining to tumor cases.  The collection has been
assembled from a number of participating biobanks and other partners through the
[ADOPT BBMRI-ERIC](https://www.bbmri-eric.eu/scientific-collaboration/adopt-bbmri-eric/) project.

Researchers interested in using the data for science can [apply for
access](https://www.bbmri-eric.eu/services/access-policies/).


## Usage

The usage of this workflow is described in the [Snakemake Workflow Catalog](https://snakemake.github.io/snakemake-workflow-catalog/?usage=crs4%2Ffair-crcc-img-convert).

If you use this workflow in a paper, don't forget to give credits to the authors by citing the URL of this repository and its DOI (see above).
