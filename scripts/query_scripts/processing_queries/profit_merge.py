#Abigail Birnbaum
#script to combine crop profit in scenarios and crop profit in corresponding unconstrained water scenarios
#requests for raw data to abigail.birnbaum@tufts.edu

#Import statements
import pandas as pd #for dataframe
import numpy as np

#for not printing warnings
import warnings; warnings.simplefilter('ignore')
import os
import glob

query = 'crop_profit_sum_unlimited'
unlim_profit = pd.read_pickle('/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/pickle_data/'+query)
query2 = 'crop_profit_sum'
scen_profit = pd.read_pickle('/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/pickle_data/'+query2)

#merge the two datasets
profit_merge = scen_profit.merge(unlim_profit,on=['year','basin','tax','ssp','ag','soc','Units_profit'],
                            suffixes=['_scenario','_unlimited'])

#remove ugly columns
profit_merge = profit_merge.drop(['scenario_scenario','scenario_unlimited'],axis=1)
profit_merge = profit_merge.rename(columns={'value_profit_scenario':'profit_scenario','value_profit_unlimited':'profit_unlimited',
                                           })

profit_merge['profit_pchange'] = 100*((profit_merge['profit_scenario'] - profit_merge['profit_unlimited'])/profit_merge['profit_unlimited'])

#save to pickle
profit_merge.to_pickle('/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/pickle_data/profit_lac')
