Bootstrap: docker

From: continuumio/miniconda3

%files
	packed_environment.tar.gz /packed_environment.tar.gz

%post
	tar xvzf /packed_environment.tar.gz -C /opt/conda
	conda-unpack
	rm /packed_environment.tar.gz
