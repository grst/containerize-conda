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

## Prerequisites

 * [conda-pack](https://conda.github.io/conda-pack/)
 * either Docker, Podman or Singularity
 * source conda environment needs to be on a linux x64 machine. 

## Usage

1. Clone this repository (retrieve `Dockerfile`/`Singularity`)

```
git clone git@github.com:grst/containerize-conda.git
cd containerize-conda
```

2. Pack the environment

```
conda-pack -n <MY_ENV> -o packed_environment.tar.gz
```

3. Build the container

```
# With singularity
singularity build --fakeroot <OUTPUT_CONTAINER.sif> Singularity

# With Docker
docker build . -t <TAG>

# With Podman/Buildah
podman build . -t <TAG>
```

## How it works
Conda environment can't be just "moved" to another location, as some paths are
hardcoded into the environment. `conda-pack` takes care of replacing these paths
back to placeholders and creates a `.tar.gz` archive that contains the
environment. This environment can be unpacked to another machine (or, in our
case, a container). Running `conda-unpack` in the environment replaces the 
placeholders back to the actual paths matching the new location. 
