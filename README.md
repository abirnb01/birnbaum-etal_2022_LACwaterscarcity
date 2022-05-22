# Drivers of Water Scarcity in Latin America and the Caribbean (Birnbaum et al. (2022), in revision)
This repository contains the code used to generate the figures in the paper Drivers of Water Scarcity in Latin America and the Caribbean by Birnbaum et al. (2022) currently under revision.

## Reproduce my results
To generate the GCAM databases used in this analysis, follow the instructions from Dolan et al. (2021) found here https://doi.org/10.5281/zenodo.4470017. Following these instructions will produce the GCAM databases for each scenario included in the analysis and their corresponding unconstrained water scenarios.

To replicate the results from this analysis, generate the raw query results using the scripts found in the query_scripts directory (see query_request1.R for an example of how to run a query) and then run the R scripts and Jupyter notebooks found in main_figures and supplemental_figures directories. 

## Contents
The structure of this repository is as follows:

1. scripts: all of the scripts for generating the figures as well as analysis scripts are located in this directory
2. This README that explains the contents of the repository

Within the scripts directory are the following sub-directories:
1. main_figures: contains R scripts and Jupyter notebook used to generate the figures found in the main body of the paper
2. supplemental_figures: contains Jupyter notebook used to generate the figures found in the SI of the paper
3. query_scripts: contains scripts used to process raw data
4. LACwaterscarcity_env: yml file containing necessary dependencies to run the scripts in main_figures_script.ipynb and supplemental_figures_script.ipynb

The main_figures directory contains the following scripts:
1. main_figures_script.ipynb: Jupyter notebook used to generate Figures 1, 2, 3, and 5 in the paper.
2. CART_regression_physicalwaterscarcity.R: R script used to generate data for Figure 2 (regression trees with bagging on physical water scarcity metric)
3. CART_regression_waterprice.R: R script used to generate data for Figure 2 (regression trees with bagging on water price metric)
4. CART_regression_cropprofit.R: R script used to generate data for Figure 2 (regression trees with bagging on crop profit change metric)
5. CART_classification_physicalwaterscarcity.R: R script used to generate classification trees in Figure 4 (severe physical water scarcity outcomes)
6. CART_classification_waterprice.R: R script used to generate classification trees in Figure 6 (severe water price outcomes)
7. CART_classification_cropprofit.R: R script used to generate classification trees in Figure 7 (severe crop profit change outcomes)
8. CART_classification_allmetrics_severe.R: R script used to generate classification trees in Figure 8 (severe outcomes for all three metrics)

The supplemental_figures directory contains the Jupyter notebook supplemental_figures.ipynb used to generate the figures in the supplement

The query_scripts directory contains the following sub-directories:
1. processing_queries: Python scripts used to process raw data
2. query_xml: xml files needed to produce raw data from GCAM databases

The processing_queries directory contains the following:
1. combine_scarcity_metrics.py: script that combines the physical water scarcity, water price, and crop profit change scarcity metrics for all scenarios into a single file
2. get_glob_wprice.py: script to generate the global weighted average water price for each scenario, weighted by basin water withdrawals/global water withdrawals
3. profit_import.py and profit_import_unlimited.py: scripts to calculate profit in scenarios and unconstrained water scenarios using profit rate and land allocation query results
4. profit_merge.py: script used to combine profit in scenarios with profit in corresponding unconstrained water scenarios
5. query_combine.py: script used to combine query results in scenarios with query results in corresponding unconstrained water scenarios (for water withdrawals and water price)
6. query_import.py and query_import_unlimited.py: scripts used to process raw query results (combined individual scenario results into a single file)
7. query_request1.R: example of script used to generate raw query results
8. water_withdrawals_import.py and water_withdrawals_import_unlimited.py: scripts used to process raw water withdrawals data
9. waterprice_cleanup.py: script used to process water price results 


The query_xml directory contains the .xml files used to produce the raw data used in this analysis:
1. ag_production.xml: ag production in a region for each crop
2. ag_production_basin.xml: ag production in a specified basin for each crop
3. ag_tech_yield_basin.xml: ag tech yield in a specified basin for each land use type
4. demand_balance_crop_commodity_region.xml: consumption of goods (crops, meat, etc..)
5. land_alloc_basin.xml: land allocation in a specified basin (thous km^2)
6. land_alloc_lac.xml: land allocation for all of the basins in Latin America and the Caribbean (thous km^2)
7. land_crop.xml: land allocation by region (thous km^2)
8. profit_rate_basin.xml: profit rate in a specified basin ($1975/thous km^2)
9. profit_rate_lac.xml: profit rate in all basins in Latin America and the Caribbean ($1975/thous km^2)
10. runoff_basin.xml: maximum available runoff in all basins (km^3)
11. water_prices.xml: water prices for all basins ($/m^3)
12. water_withdrawals_basin.xml: water withdrawals (km^3) for all basins

Any questions regarding the scripts included in this repository should be directed to abigail.birnbaum@tufts.edu

## References
Dolan, F. C. (2021). Evaluating the Economic Impact Of Water Scarcity In a Changing World. Zenodo. https://doi.org/10.5281/zenodo.4470017
