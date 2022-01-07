#CART AND RANDOM FOREST ON BASIN,YEAR
#helpful resources: https://towardsdatascience.com/random-forest-in-r-f66adf80ec9
#and code bagged_CART.R from Flannery Dolan

#LOAD NECESSARY LIBRARIES
library(dplyr)
library(randomForest)
library(magrittr)

#LOAD DATA (price_profit_wta_data.csv) - this has water price, ag profit, and physical water scarcity for the 40 LAC basins from 2015 - 2100 (5 year increments)
metrics <- read.csv(file = '/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/csv_files/price_profit_wta_data.csv')
#head(metrics)

#empty dataframe
sum_importances = data.frame()

#specify year
yr <- 2100

#SPECIFY BASINS
basin_list <- unique(metrics$basin)
#basin_list <- list('Rio Verde','Rio Lerma')


#LOOP
for (bs in basin_list) {
  
  print(bs)
      
	#filter to just the basin and year that we want
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
	df_filt %>% distinct(soc,ag,gw,res,esm,tax,scarcity, .keep_all= TRUE) -> no_dups
		  
	df_regr <- subset(no_dups, select = c("soc","ag","ssp","tax","gw","esm","res","profit_pchange"))
		  
	#random forest (regression)
	rf_regr <- randomForest(
	profit_pchange~.,
	data=df_regr,mtry=7,importance=TRUE,ntree=500) #bagging (mtry = 7)
		  
	#Put variable importances into dataframe
	importance_df <- as.data.frame(rf_regr %>% importance)
	importance_df$varnames <- rownames(importance_df)
	rownames(importance_df) <- NULL  
	importance_df$basin <- bs
	importance_df$year <- yr
	importance_df$metric <- "ag_profit"
		
	#add to sum_importances storage dataframe
	sum_importances <- rbind(sum_importances,importance_df)
}

#save as csv
write.csv(sum_importances,
          paste0("/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/csv_files/rf_agprofit.csv"))

