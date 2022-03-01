#This script is used to generate Figure 2 in
#"Drivers of Future Physical Water Scarcity and its Economic Impacts in Latin America and the Caribbean"

#Running this code produces a list of parameter importance scores for all basins in the LAC region
#from running 500 bagged regression trees for the crop profit metric.

#load required libraries
library(dplyr)
library(randomForest)
library(magrittr)

#Set path (this should be changed for your local machine)
setwd("C:/Users/abirnb01/Documents/Research/NEXO-UA/LACwaterscarcity/data/query_results/")

#Load CSV of metrics data
#this has water price, crop profit, and physical water scarcity for the 40 LAC basins 
#from 2015 - 2100 (5 year increments)
metrics <- read.csv(file = 'scarcity_metrics.csv')

#initialize an empty dataframe to store the parameter importance scores
sum_importances = data.frame()

#specify year for regression analysis
yr <- 2100


#specify basin(s) for regression analysis
basin_list <- unique(metrics$basin)

#loop through basins
for (bs in basin_list) {
   
	#filter to single basin and year
	metrics %>% filter(basin==bs & year==yr) -> df_filt
		  
	#make sure that the parameters are categorical variables!
	df_filt$soc=as.factor(df_filt$soc)
	df_filt$ag=as.factor(df_filt$ag)
	df_filt$ssp=as.factor(df_filt$ssp)
	df_filt$gw=as.factor(df_filt$gw)
	df_filt$res=as.factor(df_filt$res)
	df_filt$esm=as.factor(df_filt$esm)
	df_filt$tax=as.factor(df_filt$tax)
		  
	#remove duplicates from dataset
	df_filt %>% distinct(soc,ag,gw,res,esm,tax,wta, .keep_all= TRUE) -> no_dups
	
	#filter data to just what's required for regression analysis (7 parameter assumptions,metric)
	#here the scarcity metric is % change in crop profit
	df_regr <- subset(no_dups, select = c("soc","ag","ssp","tax","gw","esm","res","profit_pchange"))
		  
	#regression using the randomforest package
	rf_regr <- randomForest(
	profit_pchange~.,
	data=df_regr,mtry=7,importance=TRUE,ntree=500) #to do bagging, set mtry = 7
		  
	#Put variable importance scores into dataframe
	importance_df <- as.data.frame(rf_regr %>% importance)
	importance_df$varnames <- rownames(importance_df)
	rownames(importance_df) <- NULL  
	importance_df$basin <- bs
	importance_df$year <- yr
	importance_df$metric <- 'crop_profit'
		
	#add to the sum_importances storage dataframe
	sum_importances <- rbind(sum_importances,importance_df)
}

#save sum_importances (variable importance scores for all basins) as csv
#make sure the save location is somewhere on your local machine
write.csv(sum_importances,
          paste0("C:/Users/abirnb01/Documents/Research/NEXO-UA/LACwaterscarcity/data/CART_results/rf_cropprofit.csv"))

