#!/usr/bin/R
library('dplyr')
library('tibble')
library('Rtsne')
library('pheatmap')
setwd('D:/AI_diagnosis/Renal_cancer_project/bioinfo')

# load dataset
datatable = read.table('images_genomic_features_table.txt', header = TRUE, sep = '\t')
features_table = datatable[,c(1,3,12,14,16:101)]
#features_table = datatable[,1:101]
rownames(features_table) <- NULL
features_table <- column_to_rownames(features_table, var = 'case_id')

remove_case1 <- c('TCGA-CZ-4865','TCGA-B0-4713','TCGA-DV-5565','TCGA-CJ-4920','TCGA-BP-5192','TCGA-B0-5697','TCGA-KM-8441','TCGA-BP-4965')
remove_case2 <- c('TCGA-B0-5697','TCGA-BP-5192','TCGA-CJ-4907','TCGA-B0-5085','TCGA-DW-5560','TCGA-BP-4965','TCGA-KN-8430')
remove_case3 <- c('TCGA-CZ-5462','TCGA-KM-8438')
remove_case4 <- c('TCGA-G7-A8LB','TCGA-B8-5162')
features_table <- features_table[-c(143,1,150,127,91,8,165.69),]
features_table <- features_table[-c(8,98,122,5,147,67,165),]
features_table <- features_table[-c(137,151),]
features_table <- features_table[-c(146,20),]

normalize <- function(values){
  min_value <- min(values)
  max_value <- max(values)
  return((values - min_value)/(max_value - min_value))
}

