#Abigail Birnbaum
#script to combine water withdrawals for all scenarios into single pickle
#raw data requests to abigail.birnbaum@tufts.edu

#which query do I want do import?
query = 'water_withdrawals_basin_flannery'

#Import statements
import os 
from pathlib import Path
import glob
import pandas as pd #for dataframe
import numpy as np
import warnings; warnings.simplefilter('ignore') #for not printing warnings
import time #for time debugging


#METHODS
def scen_columns(df):
# turn scenario into columns for different important dimensions

    df[['var1','var2','var3','gw','res','esm','tax']] = df['scenario'].str.split('_',n=6,expand=True)

    # #replacing scenario names with numberical conventions

    #groundwater
    df.loc[df.gw=='gwlo','gw']='1'
    df.loc[df.gw=='gwmed','gw']='2'
    df.loc[df.gw=='gwhi','gw']='3'

    #earth systems model
    df.loc[df.esm=='gfdl','esm']='1'
    df.loc[df.esm=='hadgem','esm']='2'
    df.loc[df.esm=='ipsl','esm']='3'
    df.loc[df.esm=='miroc','esm']='4'
    df.loc[df.esm=='noresm','esm']='5'

    #reservoir
    df.loc[df.res=='rs','res']='1'
    df.loc[df.res=='exp','res']='2'

    #tax
    df.loc[df.tax=='NDC_Tax_ffict','tax']='1'
    df.loc[df.tax=='NDC_Tax_uct','tax']='2'

    #now dealing with the first few variables...

    #add empty columns for ssp, ag, and soc
    df['ssp']=''
    df['ag']=''
    df['soc']=''

    #give var1 (ssp) value of 1 if var2 = socio and var3 = ag and value of 2 if var2 = ag and var3 = socio
    df.loc[df.var2.str[0]=='a','ssp']='2'
    df.loc[df.var2.str[0]=='s','ssp']='1'

    #assign numberic value to ag for which ag ssp it is - 
    df.loc[df.var2.str[0]=='a','ag']=df['var2'].str[-1]
    df.loc[df.var2.str[0]=='s','ag']=df['var3'].str[-1]

    #asign numberic value to soc for which soc ssp it is - 
    df.loc[df.var3.str[0]=='s','soc']=df['var3'].str[-1]
    df.loc[df.var3.str[0]=='a','soc']=df['var2'].str[-1]

    #get rid of var1, var2, var3 columns
    df = df.drop(['var1','var2','var3'],axis=1)

    #make the soc, ag, and ssp columns to be int not str
    df['ssp'] = df['ssp'].astype(int)
    df['soc'] = df['soc'].astype(int)
    df['ag'] = df['ag'].astype(int)
    df['esm'] = df['esm'].astype(int)
    df['tax'] = df['tax'].astype(int)
    df['res'] = df['res'].astype(int)
    df['gw'] = df['gw'].astype(int)
    
    return df

##
#####MAIN###
##
###path of query_results for specific query
path = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/'+query+'/'
os.chdir(path)
os.getcwd()
extension = 'csv'
#get all of the queries together in all_filenames
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
##
newpath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/'
##
#make new directory for new csv, if needed
isdir = os.path.isdir(newpath+query) 
if not isdir:
    os.mkdir(newpath+query)

###populate new folder with cleaned up csvs
for f in range(len(all_filenames[:])):
    query_df = scen_columns(pd.read_csv(all_filenames[f]))
    #query_df = query_df.drop(['scenario'],axis=1) #take out scenario column
    query_df = query_df[query_df.year>=2015] #set 2015 as base year, remove earlier values 

	#group by basin (agg across regions)
    query_df = query_df.groupby(['Units','scenario','basin','year','tax','ssp','ag','soc','gw','esm','res'])['value'].sum()
    query_df = query_df.reset_index()
    query_df = query_df.set_index('scenario')


    query_df.to_csv(newpath+query+'/'+query+str(f)+'.csv')

#get all of the csv (new ones) and combine
newpath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/'+query+'/'
os.chdir(newpath)
os.getcwd()

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames[:]])

#combined_csv = combined_csv.drop(['Unnamed: 0'],axis=1)
combined_csv.to_csv(newpath+query+'_combined.csv') #put in new csv
combined_csv.to_pickle('/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/pickle_data/'+query)
