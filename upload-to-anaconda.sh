#!/bin/sh

# conda config --set anaconda_upload no
# conda config --add channels conda-forge
# conda-build . --python 3.6
conda-build . --python 3.7
conda-build . --python 3.8
conda-build . --python 3.9
# anaconda login
# anaconda upload --user mpcabd /opt/conda/conda-bld/noarch/arabic-reshaper-*-py36_0.tar.bz2
anaconda upload --user mpcabd /opt/conda/conda-bld/noarch/arabic-reshaper-*-py37_0.tar.bz2
anaconda upload --user mpcabd /opt/conda/conda-bld/noarch/arabic-reshaper-*-py38_0.tar.bz2
anaconda upload --user mpcabd /opt/conda/conda-bld/noarch/arabic-reshaper-*-py39_0.tar.bz2
