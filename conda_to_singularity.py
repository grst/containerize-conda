#!/usr/bin/env python

"""
Usage:
  ./conda_to_singularity.py CONDA_ENV OUTPUT.sif

CONDA_ENV needs to be an absolute path to a conda environment.
"""

import sys
import tempfile
from subprocess import call
from os.path import abspath, join as join_path

conda_env, output_path = sys.argv[1:3]
output_path = abspath(output_path)

TEMPLATE = "./Singularity"

with open(TEMPLATE) as f:
  template = "".join(f.readlines())

template = template.format(path=conda_env)


with tempfile.TemporaryDirectory() as tmpdir:
  with open(join_path(tmpdir, "Singularity"), 'w') as f:
    f.write(template)
  print(tmpdir)
  call(["singularity", "build", "--fakeroot", "--force", output_path,  "Singularity"], cwd=tmpdir)



