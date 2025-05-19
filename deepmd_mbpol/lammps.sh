#!/bin/bash

#SBATCH --job-name=wat_AANN
#SBATCH --output=us-%j.out
#SBATCH --account=pi-gavoth
#SBATCH --partition=gavoth
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48

module load python
module load intelmpi
ulimit -l unlimited
conda deactivate
conda activate /project2/gavoth/kuntalg/Softwares/DeePMD/deepmd_plumed

PLUMED_KERNEL=/project2/gavoth/kuntalg/Softwares/PLUMED/plumed-2.4.0/opt/lib/libplumedKernel.so

cores=48

mpirun -np ${cores} lmp_mpi -in in.water -var SEED ${RANDOM}
