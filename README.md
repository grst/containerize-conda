# Containerize an existing conda environment

I use conda environments for working on data analysis projects.
Sometimes I need to revert to install using `pip` or `R`'s
`install.packages` if a package is not on bioconda or conda-forge.

This makes it very hard to reproduce the environment, and therefore,
the analysis, on another system. Even pure conda environments stored
as an `environment.yml` file tend to [break after a
while](https://github.com/conda/conda/issues/9257).

Using the instructions below allows to package an existing environment
into a Singularity container which should be more portable
and can also easily be integrated into a [fully reproducible
data analysis
workflow](https://grst.github.io/bioinformatics/2019/12/23/reportsrender.html)
based on e.g. [Nextflow](https://www.nextflow.io/).

## Usage

```
usage: conda_to_singularity.py [-h] [--template TEMPLATE] CONDA_ENV OUTPUT_CONTAINER

Convert a conda env to a singularity container.

positional arguments:
  CONDA_ENV            Absolute path to the conda enviornment. Must be exactely the path as it shows up in `conda env list`, not a symbolic link to it, nor a realpath.
  OUTPUT_CONTAINER     Output path where the singularity container will be safed.

optional arguments:
  -h, --help           show this help message and exit
  --template TEMPLATE  Path to a Singularity template file. Must contain a `{conda_env}` placeholder. If not specified, uses the default template shipped with this script.
```

For example

```
conda_to_singularity.py /home/sturm/.conda/envs/whatever whatever.sif
```

By default, the image will be based on CentOS 7. If you want a different base image,
you can modify `Singularity.template`, and specify it with the `--template` argument.


## How it works

Conda envs cannot simply be "moved" as some paths are hardcoded into the environment.
I previously applied `conda-pack` to solve this issue, which works fine in most cases
but breaks in some (especially for old environments that have a long history
of manually installing stuff through R or pip).

This is an other appraoch where the issue is solved by copying the conda environment
with its full absolute path to the container and append a line to the Singularity environment
file that activates the conda environment from that path once the container is started:

```
echo "source /opt/conda/bin/activate {conda_env}" >>$SINGULARITY_ENVIRONMENT
```

Naively, this could be solved with `%files /path/to/env`, however, this dereferences
all symbolic links, which breaks some environments. Instead, I build a tar archive
that keeps all symbolic links intact *within* the conda environment, but at the
same time include all files that are outside the conda env, but referenced
by a symbolic link.

I don't have a lot of experience yet if it is really more stable than conda-pack
or just happens to fail in different cases.

## Where's the conda-pack/Docker version?

This is an updated version of my scripts that works without `conda-pack` and turned out
to work even in cases where the conda-pack variant failed. It works only with Singularity at the moment. 
I don't see any major issues porting the new approach to Docker, but don't have need for that myself. 

If you are looking for the previous scripts based on `conda-pack`, because you need a Docker variant, or they just
work for you, they are in the [conda-pack](conda-pack) folder with a dedicated [README](conda-pack/README.md).




