#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import shutil
import sys
from pathlib import Path

import click_completion
import rich_click as click
from sequana_pipetools import SequanaManager
from sequana_pipetools.options import *

import sequana_pipelines.quality_control.data

click_completion.init()

NAME = "quality_control"


help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--skip-phix-removal",
            "--skip-fastqc-raw",
            "--skip-fastqc-cleaned",
        ],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions)
@include_options_from(ClickGeneralOptions)
@include_options_from(ClickTrimmingOptions, software=["cutadapt", "atropos"])
@click.option("--skip-phix-removal", is_flag=True, help="Do no remove the Phix")
@click.option("--skip-fastqc-raw", is_flag=True, help="Do not perform fastqc on raw data")
@click.option("--skip-fastqc-cleaned", is_flag=True, help="Do not perform fastqc on cleaned data")
def main(**options):

    manager = SequanaManager(options, NAME)
    manager.setup()

    options = manager.options

    cfg = manager.config.config

    # fill the config file with input parameters

    # --------------------------------------------------- input  section
    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.input_pattern = options.input_pattern
    cfg.input_readtag = options.input_readtag

    # --------------------------------------------------------- trimming
    cfg.trimming.software_choice = options.trimming_software_choice
    cfg.trimming.do = not options.disable_trimming
    qual = options.trimming_quality

    if options.trimming_software_choice in ["cutadapt", "atropos"]:
        cfg.cutadapt.tool_choice = options.trimming_software_choice
        cfg.cutadapt.fwd = options.trimming_adapter_read1
        cfg.cutadapt.rev = options.trimming_adapter_read2
        cfg.cutadapt.m = options.trimming_minimum_length
        cfg.cutadapt.mode = options.trimming_cutadapt_mode
        cfg.cutadapt.options = options.trimming_cutadapt_options  # trim Ns -O 6
        cfg.cutadapt.quality = 30 if qual == -1 else qual

    # -------------------------------------------------- bwa section
    cfg.bwa_mem_phix.do = not options.skip_phix_removal

    # copy required file (possibly)
    p = Path(sequana_pipelines.quality_control.data.__path__[0])
    phix = str(p / "phiX174.fa")
    shutil.copy(phix, manager.workdir)

    if options.skip_fastqc_cleaned:
        cfg.fastqc.do_after_adapter_removal = False

    if options.skip_fastqc_raw:
        cfg.fastqc.do_raw = False

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
