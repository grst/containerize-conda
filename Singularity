Bootstrap: yum
OSVersion: 7
MirrorURL: http://mirror.centos.org/centos-%{{OSVERSION}}/%{{OSVERSION}}/os/$basearch/
Include: yum

%files
  {path}

%environment
  export NUMBA_CACHE_DIR=/tmp/numba_cache

%post
  yum install -y kernel-3.10.0-1160.11.1.el7
  curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > /install_conda.sh
  chmod +x /install_conda.sh
  /install_conda.sh -b -p /opt/conda
  rm /install_conda.sh
  echo "source /opt/conda/bin/activate {path}" >>$SINGULARITY_ENVIRONMENT

