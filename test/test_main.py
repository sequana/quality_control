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
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_quality_control --input-directory {}
          --working-directory --force""".format(
        sharedir, directory.name
    )
    subprocess.call(cmd.split())


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

        stat = subprocess.call("sh quality_control.sh".split(), cwd=wk)

        assert os.path.exists(wk + "/summary.html")


def test_version():
    cmd = "sequana_quality_control --version"
    subprocess.call(cmd.split())
