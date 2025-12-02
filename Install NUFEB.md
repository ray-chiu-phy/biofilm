# Install NUFEB
We want to compile NUFEB able to produce VTK and HDF5 output files. That said, there were troubles while building the VTK and HDF5 codes under the `thirdparty` folder in `NUFEB-2`, so instead we simply download both libraries on our own.
## Install VTK
To install VTK via Conda, first activate our conda environment and run the following command: 
``` 
conda install conda-forge::vtk
```
By default, this will also pull in the standard `
hdf5` package, which does not include MPI support. Since NUFEB needs an MPI-enabled HDF5 library, we should remove the default one before proceeding:
```
conda remove --force hdf5
```
## Install HDF5
We first download the HDF5 source code from the [official website](https://www.hdfgroup.org/download-hdf5/source-code/), and extract the downloaded tar file `hdf5-1.14.6.tar.gz`:
```
tar xvzf hdf5-1.14.6.tar.gz
```
Then we install some packages needed for compilation in our environment:
```
conda install gcc_linux-64 gxx_linux-64 gfortran_linux-64
```
Now change into the directory `hdf5-1.14.6` , a folder extracted from the tar file. And set the compiler and enable MPI support:
```
export CC=mpicc
export HDF5_MPI="ON"
```
Next, Configure the build:
```
./configure --enable-shared --enable-parallel --prefix=/home/user/lib/hdf5
```
We can also set the directory for hdf5:
```
export HDF5_DIR="/home/user/lib/hdf5"
```
Finally, we compile and install hdf5 by:
```
make
```
```
make install
```
## Compile NUFEB
We first install the following packages by:
```
sudo apt update
sudo apt-get install cmake git-core g++ openmpi-bin openmpi-common libopenmpi-dev libpng-dev ffmpeg
```
(or install them via `conda` )
Secondly, get the NUFEB files from github by running:
```
git clone https://github.com/nufeb/NUFEB-2.git
```
This will create a directory `NUFEB-2`. Inside it, you’ll find a `lib` folder, which contains three subdirectories: `hdf5`, `nufeb`, and `vtk`. 

Next, we need to edit the Makefile in each of those subdirectories to point to the right include and library locations. In `Makefile.lammps` in `hdf5/Makefile.lammps`:
```
# Settings that the LAMMPS build will import when this package library is used

hdf5_SYSINC = -I/home/user/lib/hdf5/include
hdf5_SYSLIB = -lhdf5
hdf5_SYSPATH = -L/home/user/lib/hdf5/lib
```
In `vtk/Makefile.lammps`:
```
# Settings that the LAMMPS build will import when this package library is used

vtk_SYSINC  = -I$(CONDA_PREFIX)/include -I$(CONDA_PREFIX)/include/vtk-9.4
vtk_SYSLIB = -lvtksys-9.4 -lvtkCommonCore-9.4 -lvtkCommonExecutionModel-9.4 -lvtkCommonMisc-9.4 -lvtkCommonMath-9.4 -lvtkCommonSystem-9.4 -lvtkCommonTransforms-9.4 -lvtkIOCore-9.4 -lvtkIOXML-9.4 -lvtkIOXMLParser-9.4 -lvtkIOLegacy-9.4 -lvtkIOParallelXML-9.4 -lvtkCommonDataModel-9.4 -lvtkParallelCore-9.4
vtk_SYSPATH = -L$(CONDA_PREFIX)/lib
```
 In `nufeb/Makefile.lammps_hdf5_vtk8.0`:
```
# Settings that the LAMMPS build will import when this package library is used

nufeb_SYSINC = -DENABLE_DUMP_BIO_HDF5 -I/home/user/lib/hdf5/include -DENABLE_DUMP_GRID -I$(CONDA_PREFIX)/include/vtk-9.4
nufeb_SYSPATH = -L/home/user/lib/hdf5/lib -L$(CONDA_PREFIX)/lib
nufeb_SYSLIB = -lhdf5 -lhdf5_hl -lvtksys-9.4 -lvtkCommonCore-9.4 -lvtkCommonExecutionModel-9.4 -lvtkCommonMisc-9.4 -lvtkCommonMath-9.4 -lvtkCommonSystem-9.4 -lvtkCommonTransforms-9.4 -lvtkIOCore-9.4 -lvtkIOXML-9.4 -lvtkIOXMLParser-9.4 -lvtkIOLegacy-9.4 -lvtkIOParallelXML-9.4 -lvtkCommonDataModel-9.4 -lvtkParallelCore-9.4
```
Finally, add the following line to your `~/.bashrc`:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/user/lib/hdf5/lib
```
Then run:
```
source ~/.bashrc
```
to apply the change.

Now we are able to compile NUFEB. Change the working directory back to `NUFEB-2` and run:
```
./install.sh --enable-vtk --enable-hdf5
```
Voilà! We’ve successfully compiled NUFEB with VTK visualization support!🥳