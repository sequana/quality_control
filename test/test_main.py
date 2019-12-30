import easydev
import os
import tempfile
import subprocess
import sys
from sequana.pipelines_common import get_pipeline_location as getpath

sharedir = getpath('quality_control')

# The data set provided was using the index GTGAAA
# this is coming from a kit illumina:wq


def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_pipelines_quality_control --input-directory {}
          --working-directory --force""".format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.quality_control.main as m
    sys.argv = ["test", "--input-directory", sharedir, "--working-directory",
        directory.name, "--force"]
    m.main()

def test_full():

    with tempfile.TemporaryDirectory() as directory:
        print(directory)
        wk = directory

        cmd = "sequana_pipelines_quality_control --input-directory {} "
        cmd += "--working-directory {}  --force"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())

        stat = subprocess.call("sh quality_control.sh".split(), cwd=wk)

        assert os.path.exists(wk + "/multi_summary.html")

def test_version():
    cmd = "sequana_pipelines_quality_control --version"
    subprocess.call(cmd.split())

