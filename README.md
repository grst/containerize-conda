# Containerize an existing conda environment

I use conda environments for working on data analysis projects.
Sometimes I need to revert to install using `pip` or `R`'s
`install.packages` if a package is not on bioconda or conda-forge.

This makes it very hard to reproduce the environment, and therefore,
the analysis, on another system. Even pure conda environments stored
as an `environment.yml` file tend to [break after a
while](https://github.com/conda/conda/issues/9257).

Using the instructions below allows to package an existing environment
into a Docker or Singularity container which should be more portable
and can also easily be integrated into a [fully reproducible
data analysis
workflow](https://grst.github.io/bioinformatics/2019/12/23/reportsrender.html)
based on e.g. [Nextflow](https://www.nextflow.io/).

## Variant without conda-pack (singularity only)

Conda envs cannot simply be "moved" as some paths are hardcoded into the environment.
I previously applied `conda-pack` to solve this issue, which works fine in most cases
but breaks in some (especially for old environments that have a long history
of manually installing stuff through R or pip)

This is an other appraoch where the issue is solved by copying the conda environment
with its full absolute path to the container and append a line to the Singularity environment
file that activates the conda environment from that path once the container is started.

Naively, this could be solved with `%files /path/to/env`, however, this dereferences
all symbolic links, which breaks some environments. Instead, I involve some bash/tar
magic to keep all symbolic links intact *within* the conda environment, but at the
same time include all files that are outside the conda env, but referenced
by a symbolic link.

I don't have a lot of experience yet if it is really more stable than conda-pack
or just happens to fail in different cases.


