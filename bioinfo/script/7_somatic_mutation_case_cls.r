#!/usr/bin/R
library('dplyr')
library('tibble')
setwd('/home/wukai/Desktop/bioinfo')
# load mutation data
datatable <- read.table('./kirc_tcga/data_mutations_mskcc.txt', header = TRUE, sep = '\t',quote = '')
# load image feature table
features_table <- read.table('./images_features_table.txt', header = TRUE, sep = '\t')
case_id <- gsub('_.*','',features_table$sample_id)

# filter datatable
datatable <- datatable[which(substr(datatable$Tumor_Sample_Barcode,1,12) %in% case_id),]

# for VHL 
target_datatable <- datatable[which(datatable$Hugo_Symbol %in% c('VHL')),]
target_cases <- target_datatable$Tumor_Sample_Barcode
target_cases <- unique(substr(as.character(target_cases),1,12))

total_cases <- unique(substr(datatable$Tumor_Sample_Barcode,1,12))

cases_label = c()
for(case_id in total_cases){
    if(case_id %in% target_cases){
        cases_label <- append(cases_label, 1)
    }else{
        cases_label <- append(cases_label, 0)
    }
}

VHL_result <- data.frame(case_id = total_cases, VHL_label = cases_label)

#--for 'PBRM1'
target_datatable <- datatable[which(datatable$Hugo_Symbol %in% c('PBRM1')),]
target_cases <- target_datatable$Tumor_Sample_Barcode
target_cases <- unique(substr(as.character(target_cases),1,12))

total_cases <- unique(substr(datatable$Tumor_Sample_Barcode,1,12))

cases_label = c()
for(case_id in total_cases){
    if(case_id %in% target_cases){
        cases_label <- append(cases_label, 1)
    }else{
        cases_label <- append(cases_label, 0)
    }
}

PBRM1_result <- data.frame(case_id = total_cases, PBRM1_label = cases_label)

#--result
result <- inner_join(VHL_result,PBRM1_result, by = 'case_id')


write.table(result, 'kirc_case_mut_label.txt', sep = '\t', quote = FALSE, row.names = FALSE)



