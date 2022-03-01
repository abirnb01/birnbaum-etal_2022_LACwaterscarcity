[![DOI]()

# Scripts for Reproducing Figures in "Drivers of Water Scarcity in Latin America and the Caribbean" (Birnbaum et al. (2022), in revision)
Insert text here describing the paper

## Abstract

insert abstract here

## Contents

This repository contains the code used to generate the figures in the paper Drivers of Water Scarcity in Latin America and the Caribbean by Birnbaum et al. (2022) currently under revision. The structure of this repository is as follows:

1. scripts: all of the scripts for generating the figures as well as analysis scripts are located in this directory
2. This README that explains the contents of the repository

Within the scripts directory are the following sub-directories:
1. main_figures: contains R scripts and Jupyter notebook used to generate the figures found in the main body of the paper
2. supplemental_figures: contains Jupyter notebook used to generate the figures found in the SI of the paper

The main_figures directory contains the following scripts:
1. main_figures_script.ipynb: Jupyter notebook used to generate Figures 1, 2, 3, and 5 in the paper. The Jupyter notebook can also be accessed at: 
2. CART_regression_physicalwaterscarcity.R: R script used to generate data for Figure 2 (regression trees with bagging on physical water scarcity metric)
3. CART_regression_waterprice.R: R script used to generate data for Figure 2 (regression trees with bagging on water price metric)
4. CART_regression_cropprofit.R: R script used to generate data for Figure 2 (regression trees with bagging on crop profit metric)
5. CART_classification_physicalwaterscarcity.R: R script used to generate classification trees in Figure 4 (physical water scarcity extremes)
6. CART_classification_waterprice.R: R script used to generate classification trees in Figure 6 (water price extremes)
7. CART_classification_cropprofit.R: R script used to generate classification trees in Figure 7 (crop profit extremes)
8. CART_classification_allmetricsextreme.R: R script used to generate classification trees in Figure 8 (extreme for all metrics)

The supplemental_figures directory contains the Jupyter notebook supplemental_figures.ipynb used to generate Figures (XXX) in the supplement.
