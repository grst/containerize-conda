#!/usr/bin/env python

import tempfile
from subprocess import call
from os.path import abspath, join as join_path, dirname, realpath
import argparse
from pathlib import Path
from time import sleep


def _generate_file_list(conda_env, filelist_path):
    """
    Generate list of all files in the conda env.

    We need to include all files as absolute paths, and also the symbolic links they are pointing to (which
    might be outside the environment). To this end, the first `find` lists all files in the conda env.
    The second find finds the files the links point to. Using sort/uniq removes the duplicates files.

    TODO: While this covered all the cases I encountered so far, I believe this would still fail if there were nested
    symbolic links outside the repository.
    """
    command = f"""\
        #!/bin/bash
        set -o pipefail

        cat <(find {conda_env}) <(find -L {conda_env} -exec readlink -f "{{}}" ";") | \\
            sort | \\
            uniq > {filelist_path}
        """
    call(command, shell=True, executable="/bin/bash")


def _build_tar_archive(filelist_path, archive_path):
    """Build a tar archive from the filelist"""
    call(["tar", "cf", archive_path, "-T", filelist_path])


def _build_container(tmpdir, singularity_file, output_path):
    """
    Actually builds the container.

    tmpdir is the temporary directory that already contains the tar archive.
    """
    call(
        [
            "singularity",
            "build",
            "--fakeroot",
            "--force",
            output_path,
            singularity_file,
        ],
        cwd=tmpdir,
    )


def conda2singularity(conda_env, output_path, template_path):
    output_path = abspath(output_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        print(f"Using temporary directory: {tmpdir}")
        singularity_file_path = tmpdir / "Singularity"
        filelist_path = tmpdir / "filelist.txt"
        tar_archive_path = tmpdir / "packed_env.tar"

        # Read Singularity template file
        with open(template_path) as f:
            template = "".join(f.readlines())
        template = template.format(conda_env=conda_env)

        # Write formatted template file
        with open(singularity_file_path, "w") as f:
            f.write(template)

        print("Building file list...")
        _generate_file_list(conda_env, filelist_path)

        # We are using a tar archive as tar is the only way of getting the symbolic links into the singularity
        # container as symbolic links.
        print("Building tar archive...")
        _build_tar_archive(filelist_path, tar_archive_path)

        print("Building singularity container...")
        _build_container(tmpdir, singularity_file_path, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a conda env to a singularity container."
    )
    parser.add_argument(
        "CONDA_ENV",
        help="Absolute path to the conda enviornment. Must be exactely the path as it shows up in `conda env list`, not a symbolic link to it, nor a realpath. ",
    )
    parser.add_argument(
        "OUTPUT_CONTAINER",
        help="Output path where the singularity container will be safed.",
    )
    parser.add_argument(
        "--template",
        help="Path to a Singularity template file. Must contain a `{conda_env}` placeholder. If not specified, uses the default template shipped with this script.",
        default=join_path(dirname(realpath(__file__)), "Singularity.template"),
    )
    args = parser.parse_args()
    conda2singularity(args.CONDA_ENV, args.OUTPUT_CONTAINER, args.template)
