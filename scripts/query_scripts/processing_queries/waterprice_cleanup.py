#Rename water price basin names appropriately

#import statements
import pandas as pd

newpath = '/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/pickle_data/' #path - set for your local machine

query1 = 'water_withdrawals_basin_flannery' #load in water withdrawals data
ww_df = pd.read_pickle(newpath+query1+'_combined')

query2 = 'water_prices' #load in price data
price_df = pd.read_pickle(newpath+query2+'_combined')

price_df = price_df.rename(columns={'market':'basin','value_scenario':'price_scenario','value_unlimited':'price_unlimited'})
price_df.basin = price_df.basin.replace(' ','',regex=True) #take out spaces in market names (to make sure alphabetizing is correct)

#change basin names in price_df to match ww_df
markets = price_df.basin.unique()[:]
basins = ww_df.basin.unique()[:]
markets.sort()
basins.sort()
markets_to_basins = dict(zip(markets,basins))

#rename water basins appropriately
price_df.basin = price_df.basin.map(markets_to_basins)

#save price result as csv with new names
price_df.to_pickle('/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/pickle_data/water_prices_combined_renamed')
