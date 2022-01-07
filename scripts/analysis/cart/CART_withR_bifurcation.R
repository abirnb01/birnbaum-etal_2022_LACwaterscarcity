#EXAMINE THE BIFURCATION

#LOAD NECESSARY LIBRARIES
library(rpart)
library(rpart.plot)
library(dplyr)
library(magrittr)

library(ggplot2)
library(ggfortify)

#LOAD DATA (price_profit_wta_data.csv) - this has water price, ag profit, and physical water scarcity for the 40 LAC basins from 2015 - 2100 (5 year increments)
metrics <- read.csv(file = '/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/final_results/csv_files/price_profit_wta_data.csv')
#head(metrics)

yr <- 2100
bs <- 'Peru-Pacific Coast'

#filter to just the basin and year that we want
metrics %>% filter(basin==bs & year==yr) -> df_filt

#K-means clustering!

#look just at data with scarcity > 0.5
#df_filt %>% filter(scarcity>0.5) -> df_split

#filter to just the wta and water price
df_kmeans <- subset(df_filt, select = c("price_scenario","scarcity"))

#kmeans
kmean <- kmeans(df_kmeans, centers=3,nstart=35)
#kmean = kmeans(df_kmeans, centers=matrix(c(0,0,4,0.5),ncol=2))

#plotting
#autoplot(kmean, df_kmeans, frame = TRUE)
plot(df_kmeans,col=kmean$cluster,frame= TRUE)

#add to dataframe df_filt
df_filt$cluster = kmean$cluster

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


# Now run CART - binary classification ---> do this with rpart (have metrics dataset there)
# limit to scenarios with scarcity > 0.5
#no_dups %>% filter(scarcity>0.25) -> df_split

# yes if price_scenario > 0.5 too, no if price_scenario < 0.5
#df_split$split_var <- df_split$price_scenario > 0.3

#CLASSIFICATION ON SPLIT_VAR
df_class <- subset(no_dups, select = c("soc","ag","ssp","tax","gw","esm","res","cluster"))


#now try classification
fit_class <- rpart(cluster ~ .,
                   method="class", data=df_class,control=c(maxdepth=4),cp=.000001)
rpart.plot(fit_class)

