## Prerequisites

 * [conda-pack](https://conda.github.io/conda-pack/)
 * either Docker, Podman or Singularity
 * source conda environment needs to be on a linux x64 machine.

## Usage

1. Clone this repository (retrieve `Dockerfile`/`Singularity`)

```
git clone git@github.com:grst/containerize-conda.git
cd containerize-conda/conda-pack
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
