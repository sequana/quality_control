import os
import subprocess
import sys
import tempfile

from click.testing import CliRunner

from sequana_pipelines.quality_control.main import main

from . import test_dir

sharedir = f"{test_dir}/data"

# The data set provided was using the index GTGAAA
# this is coming from a kit illumina:wq


def test_standalone_subprocess():
    with tempfile.TemporaryDirectory() as directory:
        cmd = f"sequana_quality_control --input-directory {sharedir} --working-directory {directory} --force"
        assert subprocess.call(cmd.split()) == 0


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    args = ["--input-directory", sharedir, "--working-directory", directory.name, "--force"]
    runner = CliRunner()
    results = runner.invoke(main, args)
    assert results.exit_code == 0


def test_full():

    with tempfile.TemporaryDirectory() as directory:
        print(directory)
        wk = directory

        cmd = "sequana_quality_control --input-directory {} "
        cmd += "--working-directory {}  --force "
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())

        stat = subprocess.call(["bash", "quality_control.sh"], cwd=wk)

        assert os.path.exists(wk + "/summary.html")


def test_version():
    cmd = "sequana_quality_control --version"
    subprocess.call(cmd.split())


def dryrun(*args):
    """Build the workflow with the given options and check that its DAG is valid"""
    with tempfile.TemporaryDirectory() as directory:
        cmd = ["sequana_quality_control", "--input-directory", sharedir, "--working-directory", directory, "--force"]
        assert subprocess.call(cmd + list(args)) == 0

        cmd = ["snakemake", "-s", "quality_control.rules", "--configfile", "config.yaml", "-n"]
        assert subprocess.call(cmd, cwd=directory) == 0


def test_skip_phix_removal():
    dryrun("--skip-phix-removal")


def test_disable_trimming():
    dryrun("--disable-trimming")


def test_skip_phix_removal_and_trimming():
    dryrun("--skip-phix-removal", "--disable-trimming")


def test_skip_fastqc():
    dryrun("--skip-fastqc-raw", "--skip-fastqc-cleaned")


def test_atropos():
    # atropos writes the report read by multiqc and by the HTML report
    dryrun("--software-choice", "atropos")
