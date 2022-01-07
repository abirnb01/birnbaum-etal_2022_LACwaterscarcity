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

#for just one basin - test

yr <- 2100
bs <- 'Peru-Pacific Coast'

#LOOP

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
  
  #get 95th quantile (for ag profit --> 0.05 since lowest values are more severe)
  quantile(no_dups$profit_pchange, probs = 0.05, na.rm = FALSE,
           names = TRUE, type = 7) -> p
  
  #now set variable called profit_quantile (binary)
  no_dups$profit_quantile <- no_dups$profit_pchange <= p # if it's in the worst fifth percentile
  no_dups$all_true <- (no_dups$profit_pchange <= p) & (no_dups$scarcity > 0.4) & (no_dups$price_scenario >= 1.1*no_dups$weighted_price_scenario)
  #no_dups$profit_quantile <- 1*no_dups$profit_quantile #make sure that they're all integers
  sum(no_dups$all_true) #10 scenarios are extreme for all three
  
  df_class <- subset(no_dups, select = c("soc","ag","ssp","tax","gw","esm","res","all_true"))

  fit_class <- rpart(all_true ~ .,
                     method="class", data=df_class)
  rpart.plot(fit_class)

