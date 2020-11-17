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
features_table = datatable[,c(1:101,104,105)]
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

purity_label <- c()
purity_label[which(anno$purity > 0.6)] = 1
purity_label[which(anno$purity <= 0.6)] = 0
anno$purity_label <- purity_label

write.csv(rownames_to_column(cbind(t(normalized_features_table),anno), var = 'case_id') , 'features_table_for_purity_cls.csv', row.names = FALSE)
#write.csv(anno, 'feature_label_for_class.csv', row.names = FALSE)

# sort features
shap_table <- read.csv('shap_values_purity_cls.csv', header = TRUE, row.names = 1)

mean_abs <- function(values){
    return(mean(abs(values)))
}

shap_mean_table <- apply(shap_table, 2, mean_abs)
shap_mean_table <- as.data.frame(shap_mean_table)
colnames(shap_mean_table) <- 'shap_mean'
shap_mean_table <- rownames_to_column(shap_mean_table, var = 'features')
shap_mean_table <- shap_mean_table[order(shap_mean_table$shap_mean,decreasing = TRUE),]
filterd_table <- shap_mean_table[which(shap_mean_table$shap_mean > 0),][1:50,]

#normalized_features_table <- normalized_features_table[filterd_table$features,]


# pdf('test.pdf',25,10)
# pheatmap(normalized_features_table,
#          #scale = 'row',
#          annotation = anno,
#          cluster_rows = TRUE,
#          cluster_cols = TRUE)
# dev.off()

# multi-var corrlation
normalized_features_table <- t(normalized_features_table)

normalized_features_table <- cbind(normalized_features_table, anno)



# for(i in 2:(length(filterd_table$features))){
#     #cluster_feature <- get(paste('cluster',i,sep =''))
#     cluster_feature <- filterd_table$features[1:i]
#     
#     features = cluster_feature[1]
#     for(j in 2:length(cluster_feature)){
#         features <- paste(features, cluster_feature[j], sep = '+')
#     }
#     result = glm(as.formula(paste('EMT_label',features,sep = '~')), family = binomial(link = 'cauchit'), data = as.data.frame(normalized_features_table))
#     print((rsq(result)))
# }
# multi-thread


initial_selected_features <- 2
end_selected_features <- 30
all_features <- as.character(filterd_table$features)
all_combination <- combn(all_features,initial_selected_features)
all_correlation <- rep(0,ncol(all_combination))


#combination_matrix <- matrix(data = "0",nrow=end_selected_features,ncol = ncol(all_combination))
# for (i in 1:ncol(all_combination)) {
#     max <- -1
#     features <- paste(all_combination[,i][1],all_combination[,i][2],sep = '+')
#     result <- glm(as.formula(paste('purity_label', features,sep = '~')), family = binomial(link = "cauchit"), data = as.data.frame(normalized_features_table))
#     
#     if(rsq(result)>max){
#         max<-rsq(result)
#         max_combine <- all_combination[,i]
#     }
# }

feature_ascend <- function(x) {
    #max_combine <- all_combination[,i]
    max_combine <- x
    max <- -1
    left_all_features <- setdiff(all_features, max_combine)
    max_input <- paste(max_combine, collapse = "+")
    all_combination <- combn(left_all_features,5)
    for (j in 1:ncol(all_combination)) {
        left_features <- paste(as.character(all_combination[,j]),collapse = "+")
        input_features <- paste(max_input, left_features, sep = "+")
        result2 <- glm(as.formula(paste('purity_label', input_features,sep = '~')),family = binomial(link = "cauchit"), data = as.data.frame(normalized_features_table))
        current_cor <- rsq(result2)
        if(current_cor>max){
            max<-current_cor
            max_current_feature <- input_features
        }
    }
    #max_combine <- union(max_combine,max_current_feature)

    #all_correlation[i] <- max
    #combination_matrix[,i] <- max_combine
    out <- c(max,max_combine)
    return(out)
}
clnum<-detectCores()
cl <- makeCluster(getOption("cl.cores", clnum))
clusterExport(cl,c("end_selected_features","all_features","normalized_features_table","rsq"),envir = environment())

input_combination <- list()
for (k in 1:ncol(all_combination)) {
    input_combination[[k]] <- as.character(all_combination[,k])
}

#res <- parLapply(cl, input_combination,feature_ascend)
#stopCluster(cl)


res <- list()
for(i in 57:length(input_combination)){
    print(i)
    res[[i]] <- feature_ascend(input_combination[[i]])
}

max_cor<-0
max_index <- 1
for (l in 1:length(res)) {
    if(as.numeric(res[[l]][1]>max_cor)){
        max_cor<- as.numeric(res[[l]][1])
        max_index <- l
    }
}
write.csv(as.data.frame(res[[max_index]]), 'features_30_combin_purity_corrlation.csv',quote = FALSE, row.names = FALSE)





