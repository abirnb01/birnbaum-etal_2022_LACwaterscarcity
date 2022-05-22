#Abigail Birnbaum
#script to combine query results from scenarios and unconstrained scenarios into single result
#for water withdrawals and water price
#requests for raw data to abigail.birnbaum@tufts.edu

#import statements
import pandas as pd
import numpy as np
import os
import glob

#newpath = '/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/pickle_data/'
#query1 = 'water_withdrawals_basin_flannery'
#df1 = pd.read_pickle(newpath+query1)
#df2 = pd.read_pickle(newpath+query1+'_unlimited')

#comb_df = df1.merge(df2,on=['Units','basin','year','tax','ssp','ag','soc'],suffixes=['_scenario','_unlimited'])

#comb_df = comb_df.drop(['scenario_scenario','scenario_unlimited'],axis=1)

#comb_df.to_pickle(newpath+query1+'_combined')


newpath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/pickle_data/'
query1 = 'water_prices'
df1 = pd.read_pickle(newpath+query1)
df2 = pd.read_pickle(newpath+query1+'_unlimited')

comb_df = df1.merge(df2,on=['Units','market','year','tax','ssp','ag','soc'],suffixes=['_scenario','_unlimited'])

comb_df = comb_df.drop(['scenario_scenario','scenario_unlimited'],axis=1)

comb_df.to_pickle(newpath+query1+'_combined')
