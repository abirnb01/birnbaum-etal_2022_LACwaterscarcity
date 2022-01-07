#CART AND RANDOM FOREST ON BASIN,YEAR
#helpful resources: https://towardsdatascience.com/random-forest-in-r-f66adf80ec9
#and code bagged_CART.R from Flannery Dolan

#LOAD NECESSARY LIBRARIES
library(rpart)
library(rpart.plot)
library(dplyr)
library(randomForest)
library(magrittr)

#LOAD DATA (price_profit_wta_data.csv) - this has water price, ag profit, and physical water scarcity for the 40 LAC basins from 2015 - 2100 (5 year increments)
metrics <- read.csv(file = '/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/csv_files/price_profit_wta_data.csv')
#head(metrics)

#FOR LOOP
#loop through basins and years of interest
#start with year = 2100
#basins = Mexico-Northwest Coast, Rio Grande, Rio Verde, Peru-Pacific Coast, North Chile-Pacific Coast
yr <- 2100
basin_list <- list('Mexico-Northwest Coast','Rio Grande River','Rio Verde','Peru-Pacific Coast',
              'North Chile-Pacific Coast')
#LOOP
for (bs in basin_list) {
bs
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

df_regr <- subset(no_dups, select = c("soc","ag","ssp","tax","gw","esm","res","price_scenario"))
df_class <- subset(no_dups, select = c("soc","ag","ssp","tax","gw","esm","res","wprice_binary"))

#cart using rpart --> regression
fit_regr <- rpart(price_scenario ~ .,
             method="anova", data=df_regr,control=c(maxdepth=4),cp=.000001)
png(file=paste0("/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/CART_trees/water_price",bs,"_",yr,"_regr.png"))
rpart.plot(fit_regr)
dev.off()

#now try classification
#if price_scenario>glob_avg
fit_class <- rpart(wprice_binary ~ .,
             method="class", data=df_class,control=c(maxdepth=4),cp=.000001)
png(file=paste0("/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/CART_trees/water_price",bs,"_",yr,"_class.png"))
rpart.plot(fit_class)
dev.off()
}







#random forest
#rf <- randomForest(
#  price_scenario~.,
#  data=df_filt,importances=TRUE,method='anova',control=c(maxdepth=4),cp=.000001)

