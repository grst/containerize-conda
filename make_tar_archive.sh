cd PATH_TO_CONDA_ENV

# find $(readlink -f .) gets all files from the conda env as their absolute path (NOTE: it should be an absolute path, but not necessarily the realpath, but the absolute path used by conda)
# find -L . -exect readlink -f) gets all files and dereferences them (this includes all filese outside the conda env)
# using sort/uniq duplicate filese are removed
cat <(find $(readlink -f .)) <(find -L . -exec readlink -f "{}" ";") | sort | uniq > ~/Downloads/pircher_sc_integrate2_all_files2.txt

# create a tar archive from the file list above.
# DO NOT DEREFERNCE symbolic links
# dereferencing hard links is not necessary
# The tar file is a way to get symbolic links into the singularity container
tar cvf temp_conda_tar_archive.tar -T THE_FILE_WITH_ALL_FILENAMES_FROM_ABOVE

