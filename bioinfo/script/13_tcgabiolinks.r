#!/usr/bin/R
library('dplyr')
library('tibble')
library('pheatmap')
#library('TCGAbiolinks')
setwd('/home/wukai/Desktop/bioinfo')


# subtypes <- PanCancerAtlas_subtypes()
# 
# # load images feature table
# features_table <- read.table('images_features_table.txt', header=TRUE, sep = '\t')
# cases_id <- features_table$sample_id
# case_id = gsub('_.*', '',as.character(cases_id))
# # filter tcgabiolinks subtype
# subtypes_info <- subtypes[which(substr(subtypes$pan.samplesID,1,12) %in% case_id),]
# subtypes_info$pan.samplesID <- substr(subtypes_info$pan.samplesID,1,12)
# #write.table(as.data.frame(subtypes_info), 'tcgabiolinks_rcc_subtype_info.txt',row.names = FALSE, quote = FALSE, sep = '\t',)

subtypes_info <- read.table('tcgabiolinks_rcc_subtype_info.txt', header = TRUE, sep = '\t')
    
subtypes_info <- subtypes_info[grep('KIRC',subtypes_info$Subtype_Selected),]
subtypes_info <- subtypes_info[which(subtypes_info$cancer.type == 'KIRC'),]

subtypes_info <- as.data.frame(subtypes_info)[,c(1,3,6)]
colnames(subtypes_info)[1] <- c('case_id')

mRNA_anno <- data.frame(anno$Subtype_mRNA, row.names = rownames(anno))
colnames(mRNA_anno) <- 'Subtype_mRNA'
mRNA_anno <- na.omit(mRNA_anno)
mRNA_label <- c()
mRNA_label[which(mRNA_anno$Subtype_mRNA == 2)] = 'low'
mRNA_label[which(mRNA_anno$Subtype_mRNA == 3)] = 'low'
mRNA_label[which(mRNA_anno$Subtype_mRNA == 1)] = 'high'
mRNA_label[which(mRNA_anno$Subtype_mRNA == 4)] = 'high'
mRNA_anno<- cbind(mRNA_anno, mRNA_label)

miRNA_anno <- data.frame(anno$Subtype_miRNA, row.names = rownames(anno))
colnames(miRNA_anno) <- 'Subtype_miRNA'
miRNA_anno <- na.omit(miRNA_anno)
miRNA_label <- c()
miRNA_label[which(miRNA_anno$Subtype_miRNA == 2)] = 'low'
miRNA_label[which(miRNA_anno$Subtype_miRNA == 3)] = 'mid'
miRNA_label[which(miRNA_anno$Subtype_miRNA == 4)] = 'mid'
miRNA_label[which(miRNA_anno$Subtype_miRNA == 1)] = 'high'
miRNA_anno<- cbind(miRNA_anno, miRNA_label)


# load features
features_table <-  read.table('images_features_table.txt', header = TRUE, sep = '\t')
cases_id <- gsub('_.*','',features_table$sample_id)
features_table <- cbind(cases_id, features_table)
features_table <- features_table[,c(1,3:102)]
feature_names <- read.table('images_features_name_alias.txt', header = TRUE, sep = '\t')
colnames(features_table)[2:101] <- as.character(feature_names$alias)
# rm duplicate
features_table <- features_table[!duplicated(features_table$cases_id),]


# filter sample
rownames(features_table) <- NULL
features_table <- column_to_rownames(features_table, var= 'cases_id')
features_table <- features_table[rownames(mRNA_anno),]
features_table <- t(features_table)

normalize <- function(values){
  min_value <- min(values)
  max_value <- max(values)
  return((values - min_value)/(max_value - min_value))
}
features_table <- features_table[,-106]

normalized_features_table <- t(apply(features_table,1,normalize))

pdf('tcgabiolinks_mRNA_subtype_heatmap.pdf',15,10)
pheatmap(normalized_features_table, 
         annotation = mRNA_anno,
         #scale = 'row',
         cluster_rows = TRUE,
         cluster_cols = TRUE,)
dev.off()

# filter sample for miRNA
# load features
features_table <-  read.table('images_features_table.txt', header = TRUE, sep = '\t')
cases_id <- gsub('_.*','',features_table$sample_id)
features_table <- cbind(cases_id, features_table)
features_table <- features_table[,c(1,3:102)]
feature_names <- read.table('images_features_name_alias.txt', header = TRUE, sep = '\t')
colnames(features_table)[2:101] <- as.character(feature_names$alias)
# rm duplicate
features_table <- features_table[!duplicated(features_table$cases_id),]
rownames(features_table) <- NULL
features_table <- column_to_rownames(features_table, var= 'cases_id')
features_table <- features_table[rownames(miRNA_anno),]
features_table <- t(features_table)

normalize <- function(values){
    min_value <- min(values)
    max_value <- max(values)
    return((values - min_value)/(max_value - min_value))
}
features_table <- features_table[,-98]

normalized_features_table <- t(apply(features_table,1,normalize))

pdf('tcgabiolinks_miRNA_subtype_heatmap.pdf',15,10)
pheatmap(normalized_features_table, 
         annotation = miRNA_anno,
         #scale = 'row',
         cluster_rows = TRUE,
         cluster_cols = TRUE,)
dev.off()
