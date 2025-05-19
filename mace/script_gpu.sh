#!/bin/bash

#SBATCH -p beagle3
#SBATCH --account=pi-gavoth
#SBATCH --gres=gpu:1
#SBATCH --job-name=matpes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

module load mpich/4.1.2+gcc-10.2.0 cuda/12.2 cmake/3.26 mkl gsl

conda activate /project2/gavoth/kuntalg/Softwares/MACE/mace_env

ntasks_per_node=$SLURM_NTASKS_PER_NODE
numnodes=$SLURM_JOB_NUM_NODES
n=$(( ntasks_per_node * numnodes ))

mpirun -np $n /project2/gavoth/kuntalg/Softwares/MACE/lammps/build/lmp -k on g 1 -sf kk -in water.in
