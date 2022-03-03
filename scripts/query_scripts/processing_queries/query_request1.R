args = base::commandArgs(trailingOnly=TRUE) #include to run in parallel on cluster

#load required libraries
library(rgcam)
library(dplyr)

queryName<-'ag_production' #name of .xml file that I want to run

#Load in the GCAM databases (these paths will be different for your machine)
dbpath<-"/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/databases/ssp2ag5/"
dbs_unfiltered<-list.dirs(dbpath)
dbs1<-dbs_unfiltered[grepl("NDC",dbs_unfiltered)] %>% substr(.,62,nchar(.))

dbpath<-"/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/databases/ssp2ag4/"
dbs_unfiltered<-list.dirs(dbpath)
dbs2<-dbs_unfiltered[grepl("NDC",dbs_unfiltered)] %>% substr(.,62,nchar(.))

dbpath<-"/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/databases/ssp2ag3/"
dbs_unfiltered<-list.dirs(dbpath)
dbs3<-dbs_unfiltered[grepl("NDC",dbs_unfiltered)] %>% substr(.,62,nchar(.))

dbpath<-"/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/databases/ssp2ag2/"
dbs_unfiltered<-list.dirs(dbpath)
dbs4<-dbs_unfiltered[grepl("NDC",dbs_unfiltered)] %>% substr(.,62,nchar(.))

dbpath<-"/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/databases/ssp2ag1/"
dbs_unfiltered<-list.dirs(dbpath)
dbs5<-dbs_unfiltered[grepl("NDC",dbs_unfiltered)] %>% substr(.,62,nchar(.))

dbs<-c(dbs1,dbs2,dbs3,dbs4,dbs5)
dbpath<-"/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/databases/"

#function to produce query
make_query<-function(scenario){
dbLoc<-paste0(dbpath,scenario)
queryFile<-paste0('/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_files/',queryName,'.xml')
queryData=paste0('/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/temp_data_files/',queryName,"_",as.character(args[1]),'.dat')
queryResult<-rgcam::addScenario(dbLoc,queryData,queryFile=queryFile)
file.remove(queryData)
return(queryResult[[1]][[1]])
}

#save results of query, each in its own csv file
make_query(dbs[as.numeric(args[1])]) %>%
  readr::write_csv(paste0('/cluster/tufts/lamontagnelab/abirnb01/GCAM_queries/query_results/',queryName,'/r1_',queryName,"_",as.character(args[1]),".csv"))
