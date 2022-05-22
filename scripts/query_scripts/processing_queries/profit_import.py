#Abigail Birnbaum
#Calculate profit for each basin using raw land allocation and profit rate query results ($1975)
#requests for raw data mentioned in this script should be sent to abigail.birnbaum@tufts.edu

#Import statements
import pandas as pd #for dataframe
import numpy as np
#for not printing warnings
import warnings; warnings.simplefilter('ignore')
import os
import glob

#METHODS

#update scenario names for df2 (create columns for tax, ssp, ag, soc, esm, gw, rs)
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

lac_basins_short = ['Patagonia','RioLaPlata','LaPuna','MarChiq','NegroR',
              'ArgCstN','ChileCstN','Pampas','Salinas','ArgColoR',
              'ArgCstS','ChileCstS','AmazonR','BrzCstE','BrzCstN',
              'SAmerCstNE','OrinocoR','ParnaibaR','SaoFrancR',
              'TocantinsR','BrzCstS','MexBaja','California',
              'GrijUsuR','Tehuantpc','UsaColoRS','MexInt',
              'MexCstNW','MexGulf','MexCstW','Papaloapan',
              'RioBalsas','RioGrande','RioLerma','RioVerde',
              'CntAmer','YucatanP','SAmerCstN','MagdalenaR',
              'ColEcuaCst','PeruCst','Caribbean']

              
lac_basins_long = ['Central Patagonia Highlands', 'La Plata', 'La Puna Region',
       'Mar Chiquita', 'Negro', 'North Argentina-South Atlantic Coast',
       'North Chile-Pacific Coast', 'Pampas Region', 'Salinas Grandes',
       'South America-Colorado', 'South Argentina-South Atlantic Coast',
       'South Chile-Pacific Coast', 'Amazon',
       'East Brazil-South Atlantic Coast',
       'North Brazil-South Atlantic Coast',
       'Northeast South America-South Atlantic Coast', 'Orinoco',
       'Parnaiba', 'Sao Francisco', 'Tocantins',
       'Uruguay-Brazil-South Atlantic Coast', 'Baja California',
       'California River', 'Grijalva-Usumacinta',
       'Isthmus of Tehuantepec', 'Lower Colorado River',
       'Mexico-Interior', 'Mexico-Northwest Coast', 'North Gulf',
       'Pacific Central Coast', 'Papaloapan', 'Rio Balsas',
       'Rio Grande River', 'Rio Lerma', 'Rio Verde',
       'Southern Central America', 'Yucatan Peninsula', 'Caribbean Coast',
       'Magdalena', 'Colombia-Ecuador-Pacific Coast',
       'Peru-Pacific Coast','Caribbean']

#mapping
#make dictionary between lac_basins_short and lac_basins_long
short_to_long = dict(zip(lac_basins_short,lac_basins_long))

#LOAD DATA
newpath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/'
pr_query = 'profit_rate_lac'
lac_query = 'land_alloc_lac'

#get all database names

#THIS CODE HELPS US GET THE DB NAMES
lac_path = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/'+lac_query+'/'
os.chdir(lac_path)
os.getcwd()
extension = 'csv'
#get all of the queries together in all_filenames
all_filenames2 = [i for i in glob.glob('*.{}'.format(extension))]
dbnames = [] #empty list for all the db names
for fname in all_filenames2:
    dbnames.append(fname.replace("_land_alloc_lac.csv",""))
    
lac_path = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/'+lac_query+'/'
pr_path = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/' +pr_query+'/'

###################MAIN#############################

for db in dbnames[:]: #for each database in dbnames

    #now for each db name, get the corresponding profit rate and land allocation
    querypr = pd.read_csv(pr_path+db+'_profit_rate_lac.csv')
    querylac = pd.read_csv(lac_path+db+'_land_alloc_lac.csv')
    
    #merge the two dataframes
    df_profit = querypr.merge(querylac,on=['scenario','region','landleaf','year'],suffixes=['_pr','_lac'])
    df_profit['value_profit'] = df_profit['value_pr']*df_profit['value_lac']
    df_profit['Units_profit'] = '$1975'
    
    #clean up merged dataframe
    df_filt = df_profit[df_profit.year>=2015]     #limit to year >= 2015
    
    df_filt = df_filt.filter(['scenario','region','landleaf','year','value_profit','Units_profit'])
    
    #split up landleaf into crop, basin, irrigation or rainfed
    df_filt[['crop','basin','ww_type','hi_lo']] = df_filt.landleaf.str.rsplit('_',3,expand=True)
    
    #limit to just basins in LAC
    df_filt = df_filt[(df_filt.basin.isin(lac_basins_short)) & (~(df_filt.basin.isin(['California','UsaColoRS'])))]
    #rename water basins appropriately
    df_filt.basin = df_filt.basin.map(short_to_long)

    #limit land type to just crops
    crop_list = ['Corn','FiberCrop','FodderGrass','FodderHerb','MiscCrop','OilCrop',
       'OtherGrain','Rice','Root_Tuber','SugarCrop','Wheat','PalmFruit']
    df_filt = df_filt[df_filt.crop.isin(crop_list)]
    
    #filter scenario name out into parameters
    df_filt = scen_columns(df_filt)
        
    #save profit data (by crop) - may need this later
    savepath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/crop_profit'
    isdir = os.path.isdir(savepath) 
    if not isdir:
        os.mkdir(savepath)
    
    df_filt.to_csv(savepath+'/'+db+'_profit.csv')
    
    #now sum up across crops to get basin net profit
    
    #save profit sum data
    savepath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/crop_profit_sum'
    isdir = os.path.isdir(savepath) 
    if not isdir:
        os.mkdir(savepath)
    
    #sum across region, landleaf, crop, ww_type, hi_lo (get total crop profit for basin)
    df_sum = df_filt.groupby(['scenario','year','basin','tax','ssp','ag','soc','esm','res','gw'])['value_profit'].sum()
    df_sum = df_sum.reset_index()
    df_sum['Units_profit'] = '$1975'
    df_sum = df_sum.set_index('scenario')
    
    #save as csv
    df_sum.to_csv(savepath+'/'+db+'_profit_sum.csv')
    
#Now sum up crop profit sums across databases to get single pickle file that contains it for all of the databases
query = 'crop_profit_sum'
newpath = '/cluster/tufts/lamontagnelab/abirnb01/Paper1/GCAM_queries/query_results/final_results/'
os.chdir(newpath+query)
os.getcwd()

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames[:]])

combined_csv.to_pickle('/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/pickle_data/'+query)
