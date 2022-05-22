#This script is used to generate Figure 7 in
#"Drivers of Future Physical Water Scarcity and its Economic Impacts in Latin America and the Caribbean"

#Running this code produces a classification tree for the specified basin (variable "bs" - reurn the code with the basin 
#of your choice) 
#The binary classification threshold is whether a scenario is severe for the crop profit change metric

#Load required libraries
library(rpart) #CART
library(rpart.plot) #plot CART
library(dplyr)
library(magrittr)

#Set path (this should be changed for your local machine)
#setwd("C:/Users/abirnb01/Documents/Research/NEXO-UA/LACwaterscarcity/data/query_results/")
setwd("C:/Users/birnb/Documents/Tufts Research/NEXO-UA/LACwaterscarcity/data/query_results/")

#Load CSV of metrics data
#this has water price, crop profit, and physical water scarcity for the 40 LAC basins 
#from 2015 - 2100 (5 year increments)
metrics <- read.csv(file = 'scarcity_metrics.csv')

yr<- 2100 #specify year of interest
bs<-'Mexico-Interior' #specify basin of interest
#bs<-'East Brazil-South Atlantic Coast'

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

#set binary threshold caled profit_binary of profit_pchange -5%
no_dups$profit_binary <- no_dups$profit_pchange <= -5 # if it's in the worst fifth percentile

#filter just to columns of interest (7 parameters plus binary threshold)
df_class <- subset(no_dups, select = c("soc","ag","osf","tax","gw","esm","res","profit_binary"))

#run classification with max depth = 4
fit_class <- rpart(profit_binary ~ .,
                   method="class", data=df_class,control=c(maxdepth=4),cp=.000001)

#plot classification tree
rpart.plot(fit_class)

