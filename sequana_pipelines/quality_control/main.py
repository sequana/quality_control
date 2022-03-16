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
import sys
import os
import argparse
import subprocess

from sequana_pipetools.options import *
from sequana_pipetools.options import before_pipeline
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog
from sequana_pipetools import SequanaManager

col = Colors()

NAME = "quality_control"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(
            usage=usage,
            prog=prog,
            description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline")
        pipeline_group.add_argument("--skip-phix-removal", action="store_true", help="Do no remove the Phix")
        pipeline_group.add_argument("--skip-fastqc-raw", action="store_true", help="Do not perform fastqc on raw data")
        pipeline_group.add_argument(
            "--skip-fastqc-cleaned", action="store_true", help="Do not perform fastqc on cleaned data"
        )

        so = TrimmingOptions(software=["cutadapt", "atropos"])
        so.software_default = "cutadapt"
        so.add_options(self)

        so = KrakenOptions()
        so.add_options(self)

        # others
        self.add_argument("--run", default=False, action="store_true", help="execute the pipeline directly")


def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    if options.from_project is None:
        cfg = manager.config.config

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

        # ------------------------------------- kraken
        if options.skip_kraken is True:
            cfg.kraken.do = False
        else:
            cfg.kraken.do = True

        if options.kraken_databases:
            cfg.kraken.databases = [os.path.abspath(x) for x in options.kraken_databases]
        for this in options.kraken_databases:
            manager.exists(this)

        if options.skip_fastqc_cleaned:
            cfg.fastqc.do_after_adapter_removal = False

        if options.skip_fastqc_raw:
            cfg.fastqc.do_raw = False

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()

    if options.run:
        subprocess.Popen(["sh", "{}.sh".format(NAME)], cwd=options.workdir)


if __name__ == "__main__":
    main()
