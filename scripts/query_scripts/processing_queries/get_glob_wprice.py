#Abigail Birnbaum
#Calculates global average water price (weighted by water withdrawals in basin to global water withdrawals)
#requests for raw data mentioned in this script should be made to abigail.birnbaum@tufts.edu

#Import statements
import pandas as pd #for dataframe
import numpy as np
#for plotting
import matplotlib.pyplot as plt
import seaborn as sns #for pretty plots/statistics
#for not printing warnings
import warnings; warnings.simplefilter('ignore')
import os
import glob
from functools import reduce


#set path to store result (change for your local machine)
newpath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/pickle_data/'

withdrawals = pd.read_pickle(newpath+'water_withdrawals_basin_flannery_combined') #load water withdrawals raw data

#load water price data (by basin)
wprice = pd.read_pickle(newpath+'water_prices_combined_renamed')

#Withdrawals - Get Global Water Withdrawals for Each Scenario

#sum up withdrawals across ALL basins
global_withdrawals_scenario = withdrawals.groupby(['Units','year','tax','ssp','ag','soc','gw','esm','res'])['value_scenario'].sum()
global_withdrawals_scenario = global_withdrawals_scenario.reset_index()

global_withdrawals_unlimited = withdrawals.groupby(['Units','year','tax','ssp','ag','soc','gw','esm','res'])['value_unlimited'].sum()
global_withdrawals_unlimited = global_withdrawals_unlimited.reset_index()

#merge the two global value datasets
global_withdrawals = global_withdrawals_scenario.merge(global_withdrawals_unlimited,on=['Units','year','tax','ssp','ag','soc','gw','esm','res'])

#merge global value with water_withdrawals in basin data
withdrawals = withdrawals.merge(global_withdrawals,on=['Units','year','tax','ssp','ag','soc','gw','esm','res'],
                               suffixes=['','_glob'])
withdrawals = withdrawals.rename(columns={'value_scenario':'ww_scenario',
                                         'value_unlimited':'ww_unlimited',
                                         'value_scenario_glob':'globww_scenario',
                                         'value_unlimited_glob':'globww_unlimited'})
withdrawals['ww_frac_scenario'] = withdrawals['ww_scenario']/withdrawals['globww_scenario']
withdrawals['ww_frac_unlimited'] = withdrawals['ww_unlimited']/withdrawals['globww_unlimited']
  
#merge price and withdrawals data
ww_price = withdrawals.merge(wprice,on=['basin','year','gw','res','esm','tax','ssp','ag','soc'],
                            suffixes=['_ww','_price'])

#get globally average water price for each scenario by summing price * fraction
ww_price['weighted_price_scenario'] = ww_price['ww_frac_scenario']*ww_price['price_scenario']
ww_price['weighted_price_unlimited'] = ww_price['ww_frac_unlimited']*ww_price['price_unlimited']

#now sum up across all basins
ww_price_sum_scenario = ww_price.groupby(['year','gw','res','esm','tax','soc','ag','ssp'])['weighted_price_scenario'].sum()
ww_price_sum_scenario = ww_price_sum_scenario.reset_index()

ww_price_sum_unlimited = ww_price.groupby(['year','gw','res','esm','tax','soc','ag','ssp'])['weighted_price_unlimited'].sum()
ww_price_sum_unlimited = ww_price_sum_unlimited.reset_index()

#MERGE THE TWO WEIGHTED GLOBAL SUMS TOGETHER
ww_price_sum = ww_price_sum_scenario.merge(ww_price_sum_unlimited,on=['year','gw','res','esm','tax','soc','ag','ssp'])

#save as pickle
ww_price_sum.to_pickle(newpath+'glob_wprice')

#also save all basin's water price in 2100
ww_price2 = ww_price.filter(['Units_price','basin','year','tax','ssp','ag','soc','gw','esm','res',
                           'price_scenario'])
ww_price2 = ww_price2[ww_price2.year==2100]
ww_price2.to_pickle('/cluster/tufts/lamontagnelab/abirnb01/Paper1/LACwaterscarcity/data/query_results/wprice_allbasins')

