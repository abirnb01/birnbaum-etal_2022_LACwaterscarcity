#Abigail Birnbaum
#This script combines all three scarcity metrics (physical water scarcity,
#water price, and crop profit) into a single result file (saved as a pickle)
#requests for raw data mentioned in this script should be made to abigail.birnbaum@tufts.edu

#Import statements
import pandas as pd
import numpy as np
import warnings; warnings.simplefilter('ignore') #for not printing warnings
import os
import glob
from functools import reduce

##MAIN##

#Path to where data is located (change this for your local machine)
newpath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/pickle_data/'

#load water price data
wprice = pd.read_pickle(newpath+'water_prices_combined_lac')

#add in physical water scarcity column
scar_df = pd.read_csv('/cluster/tufts/lamontagnelab/shared/impact_scarcity_all.csv') #physical water scarcity from Dolan et al. (2021)
scar_df = scar_df.filter(['basin','year','scarcity','esm','ssp','soc','ag','tax','gw','res']) #limit to just WTA

#load crop profit data
profit = pd.read_pickle(newpath+'profit_lac')

#merge all of the data
dfs = [wprice,scar_df,profit]
mergedf = reduce(lambda  left,right: pd.merge(left,right,on=['basin','year','gw','res','tax','esm','ssp','ag','soc']), dfs)

mergedf = mergedf.filter(['basin','year','gw','res','esm','tax','ssp','ag','soc','price_scenario','price_unlimited',
                        'profit_scenario','profit_unlimited','profit_pchange','scarcity'])

mergedf.to_pickle(newpath+'price_profit_wta_data') #save results of all three scarcity metrics
