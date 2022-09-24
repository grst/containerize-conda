#!/bin/bash

###################################
#
# Usage:
#   conda_to_singularity.sh <CONDA_ENV> <OUTPUT.sif>
#
###################################

CONDAENV=$1
CONTAINER=$(readlink -f $2)
DIR=${TMPDIR}/$(echo $CONDAENV | md5sum | awk '{print $1}')

mkdir -p $DIR

echo ENV=$CONDAENV
echo CONTAINER=$CONTAINER
echo DIR=$DIR

conda-pack -n $CONDAENV -o $DIR/packed_environment.tar.gz --ignore-missing-files --force && \
  cp Singularity $DIR && \
  cd $DIR && \
  singularity build --fakeroot --force $CONTAINER Singularity

