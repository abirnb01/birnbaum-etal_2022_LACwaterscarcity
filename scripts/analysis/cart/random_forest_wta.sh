#!/bin/bash
#SBATCH --time=5-0:00:00
#SBATCH -p llab
#SBATCH --mem=8G

#SBATCH --cpus-per-task=1
#SBATCH --ntasks=1


module load use.own
module load R/4.0.0
module load java/1.8.0_60
module load gcc/7.3.0

Rscript /cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/new_query_analysis/RandomForest/rf_wta.R	
