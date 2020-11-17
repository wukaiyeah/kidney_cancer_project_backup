#!/usr/bin/R
library('dplyr')
library('tibble')
#library('Rtsne')
library('rsq')
library('pheatmap')
library('parallel')
setwd('/home/wukai/Desktop/bioinfo')

# load dataset
datatable = read.table('images_genomic_features_table.txt', header = TRUE, sep = '\t')
#features_table = datatable[,c(1,3,12,14,16:103)]
features_table = datatable[,c(1:101)]
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
normalized_features_table <- apply(features_table,2,normalize)
normalized_features_table <- rownames_to_column(as.data.frame(normalized_features_table), var = 'case_id')
# load mutation table
muta_label <- read.table('kirc_case_mut_label.txt', header = TRUE, sep = '\t')
normalized_features_table <- inner_join(normalized_features_table, muta_label, by = 'case_id')
# for VHL mutation
write.csv(normalized_features_table,'features_table_for_mutation_class.csv', row.names = FALSE)

write.csv(normalized_features_table[,-c(102,103)], 'feature_table_for_class.csv', row.names = TRUE)
write.csv(normalized_features_table[,c(1,102:103)], 'feature_label_for_class.csv', row.names = FALSE)
