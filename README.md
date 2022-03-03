[![DOI]()

# Drivers of Water Scarcity in Latin America and the Caribbean (Birnbaum et al. (2022), in revision)
This repository contains the code used to generate the figures in the paper Drivers of Water Scarcity in Latin America and the Caribbean by Birnbaum et al. (2022) currently under revision.

## Reproduce my results
To generate the GCAM databases used in this analysis, follow the instructions found here https://doi.org/10.5281/zenodo.4470017. Following these instructions will produce the GCAM databases for each scenario included in the analysis.

## Contents
The structure of this repository is as follows:

1. scripts: all of the scripts for generating the figures as well as analysis scripts are located in this directory
2. This README that explains the contents of the repository

Within the scripts directory are the following sub-directories:
1. main_figures: contains R scripts and Jupyter notebook used to generate the figures found in the main body of the paper
2. supplemental_figures: contains Jupyter notebook used to generate the figures found in the SI of the paper
3. query_scripts: contains scripts used to process raw data
4. LACwaterscarcity_env: yml file containing necessary dependencies to run the scripts in main_figures and supplemental_figures

The main_figures directory contains the following scripts:
1. main_figures_script.ipynb: Jupyter notebook used to generate Figures 1, 2, 3, and 5 in the paper. The Jupyter notebook can also be accessed at: 
2. CART_regression_physicalwaterscarcity.R: R script used to generate data for Figure 2 (regression trees with bagging on physical water scarcity metric)
3. CART_regression_waterprice.R: R script used to generate data for Figure 2 (regression trees with bagging on water price metric)
4. CART_regression_cropprofit.R: R script used to generate data for Figure 2 (regression trees with bagging on crop profit metric)
5. CART_classification_physicalwaterscarcity.R: R script used to generate classification trees in Figure 4 (physical water scarcity extremes)
6. CART_classification_waterprice.R: R script used to generate classification trees in Figure 6 (water price extremes)
7. CART_classification_cropprofit.R: R script used to generate classification trees in Figure 7 (crop profit extremes)
8. CART_classification_allmetricsextreme.R: R script used to generate classification trees in Figure 8 (extreme for all metrics)

The supplemental_figures directory contains the Jupyter notebook supplemental_figures.ipynb used to generate the figures in the supplement

The query_scripts directory contains the following sub-directories:
1. processing_queries: Python scripts used to process raw data
2. query_xml: xml files needed to produce raw data from GCAM databases

The processing_queries directory contains the following:
1. combine_scarcity_metrics: script that combines the physical water scarcity, water price, and crop profit scarcity metrics for all scenarios into a single file
2. get_glob_wprice: script to generate the global average water price (GAWP) for each scenario, weighted by basin water withdrawals/global water withdrawals
3. profit_import and profit_import_unlimited: scripts to calculate profit in scenarios and unconstrained water scenarios using profit rate and land allocation query results
4. query_import: script used to process raw query results (combined individual scenario results into a single file)
5. waterprice_cleanup: script used to process water price results 

The query_xml directory contains the .xml files used to produce the data used in this analysis.

Any additional questions regarding the scripts included in this repository should be directed to abigail.birnbaum@tufts.edu
