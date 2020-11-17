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


# load TCGAbiolinks subtype info table
subtype <- read.table('tcgabiolinks_rcc_subtype_info.txt', header = TRUE, sep = '\t')
subtype <- subtype[which(subtype$cancer.type == 'KIRC'),]
subtype <- subtype[,c(1,3,6)]
colnames(subtype) <- c('case_id','subtype_mRNA','subtype_miRNA')
#--for subtype mRNA
mRNA <- na.omit(subtype[,c(1,2)])
subtype_mRNA <- c()
subtype_mRNA[mRNA$subtype_mRNA == 3] = 1
subtype_mRNA[mRNA$subtype_mRNA == 2] = 1
subtype_mRNA[mRNA$subtype_mRNA == 1] = 0
subtype_mRNA[mRNA$subtype_mRNA == 4] = 0
mRNA$subtype_mRNA = subtype_mRNA
filtered_features_table <- inner_join(normalized_features_table, mRNA, by = 'case_id')
write.csv(filtered_features_table, 'features_table_for_sutype_mRNA_cls.csv', row.names = FALSE, quote = FALSE)

write.csv(filtered_features_table[,-102], 'feature_table_for_class.csv', row.names = TRUE)
write.csv(filtered_features_table[,c(1,102)], 'feature_label_for_class.csv', row.names = FALSE)


#--for subtype miRNA
miRNA <- na.omit(subtype[,c(1,3)])
subtype_miRNA<- c()
subtype_miRNA[miRNA$subtype_miRNA== 3] = 0
subtype_miRNA[miRNA$subtype_miRNA== 2] = 1
subtype_miRNA[miRNA$subtype_miRNA== 1] = 0
subtype_miRNA[miRNA$subtype_miRNA== 4] = 0
miRNA$subtype_miRNA= subtype_miRNA
filtered_features_table <- inner_join(normalized_features_table, miRNA, by = 'case_id')
write.csv(filtered_features_table, 'features_table_for_sutype_miRNA_cls.csv', row.names = FALSE, quote = FALSE)

write.csv(filtered_features_table[,-102], 'feature_table_for_class.csv', row.names = TRUE)
write.csv(filtered_features_table[,c(1,102)], 'feature_label_for_class.csv', row.names = FALSE)
          
