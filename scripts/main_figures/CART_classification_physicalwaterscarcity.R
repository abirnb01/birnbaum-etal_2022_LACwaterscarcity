#This script is used to generate Figure 4 in
#"Drivers of Future Physical Water Scarcity and its Economic Impacts in Latin America and the Caribbean"

#Running this code produces a classification tree for the specified basin (variable "bs" - reurn the code with the basin 
#of your choice) 
#The binary classification threshold is whether a scenario is extreme for the physical water scarcity metric

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

yr<- 2100 #specify year of interest
bs<-'Rio Grande River' #specify basin of interest

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
df_filt %>% distinct(soc,ag,gw,res,esm,tax,wta, .keep_all= TRUE) -> no_dups

#create wta_binary which is threshold for most severe scenarios (physical water scarcity > 0.4)
no_dups$wta_binary <- no_dups$wta > 0.4

#filter to just parameter assumptions and binary threshold (wta_binary)
df_class <- subset(no_dups, select = c("soc","ag","ssp","tax","gw","esm","res","wta_binary"))

#run classification with max depth = 4
fit_class <- rpart(wta_binary ~ .,
                   method="class", data=df_class,control=c(maxdepth=4),cp=.000001)

#plot classification tree
rpart.plot(fit_class)
