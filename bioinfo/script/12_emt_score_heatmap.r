#!/usr/bin/R
library('dplyr')
library('tibble')
#library('Rtsne')
library('rsq')
library('pheatmap')
setwd('/home/wukai/Desktop/bioinfo')

# load dataset
datatable = read.table('images_genomic_features_table.txt', header = TRUE, sep = '\t')
#features_table = datatable[,c(1,3,12,14,16:103)]
features_table = datatable[,1:103]
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
#features_table <- column_to_rownames(features_table, var = 'case_id')

anno <- features_table[,101:102]
normalized_features_table <- t(apply(features_table[,-c(101:102)],2,normalize))

EMT_label <- c()
EMT_label[which(anno$EMT_score > 0)] = 1
EMT_label[which(anno$EMT_score <= 0)] = 0
anno$EMT_label <- EMT_label
write.csv(rownames_to_column(cbind(t(normalized_features_table),anno), var = 'case_id') , 'features_table_for_emt_cls.csv', row.names = FALSE)

#write.csv(anno, 'feature_label_for_class.csv', row.names = FALSE)
# sort features
shap_table <- read.csv('shap_values_emt_score_cls.csv', header = TRUE, row.names = 1)

mean_abs <- function(values){
  return(mean(abs(values)))
}

shap_mean_table <- apply(shap_table, 2, mean_abs)
shap_mean_table <- as.data.frame(shap_mean_table)
colnames(shap_mean_table) <- 'shap_mean'
shap_mean_table <- rownames_to_column(shap_mean_table, var = 'features')
shap_mean_table <- shap_mean_table[order(shap_mean_table$shap_mean,decreasing = TRUE),]
filterd_table <- shap_mean_table[which(shap_mean_table$shap_mean > 0),]

normalized_features_table <- normalized_features_table[target_features,]


pdf('test.pdf',25,10)
pheatmap(normalized_features_table,
         #scale = 'row',
         annotation = anno,
         cluster_rows = TRUE,
         cluster_cols = TRUE)
dev.off()

# multi-var corrlation
normalized_features_table <- t(normalized_features_table)

normalized_features_table <- cbind(normalized_features_table, anno)
colnames(normalized_features_table)[90] <- 'EMT_score'




for(i in 2:(length(filterd_table$features))){
  #cluster_feature <- get(paste('cluster',i,sep =''))
  cluster_feature <- filterd_table$features[1:i]

  features = cluster_feature[1]
  for(j in 2:length(cluster_feature)){
    features <- paste(features, cluster_feature[j], sep = '+')
  }
  result = glm(as.formula(paste('EMT_label',features,sep = '~')), family = binomial(link = 'cauchit'), data = as.data.frame(normalized_features_table))
  print((rsq(result)))
}


corr <- function(value){
  return(as.numeric(as.character(value[1])))
}
corr_values <- apply(res, 2, corr)
max_index <- which.max(corr_values)
max_corr <- res[,max_index]
max_corr <- as.character(max_corr)
write.csv(as.data.frame(max_corr),'features_combin_purity_corrlation.csv',quote = FALSE,row.names = FALSE)


