#This script is used to generate Figure 8  in
#"Drivers of Future Physical Water Scarcity and its Economic Impacts in Latin America and the Caribbean"

#Running this code produces a classification tree for the specified basin (variable "bs" - reurn the code with the basin 
#of your choice) 
#The binary classification threshold is whether a scenario is extreme for all three scarcity metrics or not

#Load required libraries
library(rpart) #CART
library(rpart.plot) #plot CART
library(dplyr)
library(magrittr)

#Set path (this should be changed for your local machine)
setwd("C:/Users/abirnb01/Documents/Research/NEXO-UA/LACwaterscarcity/data/query_results/")


#Load CSV of metrics data
#this has water price, crop profit, and physical water scarcity for the 40 LAC basins 
#from 2015 - 2100 (5 year increments)
metrics <- read.csv(file = 'scarcity_metrics.csv')

yr <- 2100 #specify that we are looking at the year 2100
bs <- 'Peru-Pacific Coast' #specify the basin we are interested in (one of the 40 LAC basins)

#filter to just the basin and year that we want
metrics %>% filter(basin==bs & year==yr) -> df_filt

#make sure that the parameters are categorical variables!
df_filt$soc=as.factor(df_filt$soc)
df_filt$ag=as.factor(df_filt$ag)
df_filt$osf=as.factor(df_filt$osf)
df_filt$gw=as.factor(df_filt$gw)
df_filt$res=as.factor(df_filt$res)
df_filt$esm=as.factor(df_filt$esm)
df_filt$tax=as.factor(df_filt$tax)

#remove duplicates from dataset
df_filt %>% distinct(soc,ag,gw,res,esm,tax,pws, .keep_all= TRUE) -> no_dups

#create binary all_true to specify if all scarcity metrics are extreme or not
no_dups$all_true <- (no_dups$profit_pchange <= -5) & (no_dups$pws > 0.4) & (no_dups$price_scenario >= 1.1*no_dups$weighted_price_scenario)

sum(no_dups$all_true) #how many scenarios are extreme for all three metrics for this basin?

#get just the columns we need for CART (the seven parameters and the binary all_true column)
df_class <- subset(no_dups, select = c("soc","ag","osf","tax","gw","esm","res","all_true"))

#run classification with max depth = 4
fit_class <- rpart(all_true ~ .,
                   method="class", data=df_class,control=c(maxdepth=4),cp=.000001)

#plot classification results
rpart.plot(fit_class)

