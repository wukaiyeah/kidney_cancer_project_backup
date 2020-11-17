#!/usr/bin/R
##---This script aims to conduct survival analysis
##--packages preparation
# install.packages('survival')
library('survival')
# BiocManager::install('survminer')
library('survminer') # for drawing
library('dplyr')
library('tibble')
##--environment setting
setwd("D:/AI_diagnosis/Renal_cancer_project/bioinfo")

##--load  data table
surv.table <- read.table('renal_tumor_images_features_surv_info.txt', header = TRUE, sep = '\t')

surv.table <-cbind(surv.table[,1:3], surv.table['tumor_original_glszm_SmallAreaHighGrayLevelEmphasis'])
colnames(surv.table)[4] <- 'feature'
surv.table <- surv.table[order(surv.table$feature, decreasing = FALSE),]

##--mark gene expressed high and low depend on fpkm,  use http://www.kmplot.com/analysis give the best cut off
surv.table <- surv.table[which(surv.table$months > 0),]
surv.table <- surv.table[which(surv.table$months < 100),]
# make level table
case.num <- length(surv.table$case_id)
level.table <- data.frame(level_1 = c(rep('low', 1), rep('high', case.num-1)))
for(i in 2:(case.num-1)){
  level.table <- cbind(level.table, c(rep('low', i), rep('high', case.num-i)))
}
colnames(level.table) <- paste('level', 1:(case.num-1), sep ='_')

# auto-find the perfect cutoff
time <- surv.table$months
event <- surv.table$status
surv.table <- cbind(surv.table, level.table)

log.rank.pval.list <- c() 
for (level in colnames(level.table)){
  sfit <- survfit(as.formula(paste('Surv(time = time, event = event) ~', level)), data = surv.table)
  p.value <- round(surv_pvalue(sfit)$pval, digits = 4)
  log.rank.pval.list <- append(log.rank.pval.list, p.value)
}
names(log.rank.pval.list) <- colnames(level.table)
level.sig <- log.rank.pval.list[which(log.rank.pval.list < 0.05)]
print(level.sig)
###############################

##--process survival analysis
time <- surv.table$months
event <- surv.table$status

# fitting survival curve
sfit <- survfit(Surv(time = time, event)~ level_269, data = surv.table)
summary(sfit)

# drawling plot
windowsFonts(Calibri = 'Calibri')
  
ggsurv <- ggsurvplot(sfit,
                     data = surv.table,
                     #conf.int=TRUE, 
                     # set line type
                     linetype = 1,
                     size = 3,                    
                     # set censor points
                     censor = TRUE,
                     censor.size = 8,
                     # set pvalue
                     pval = FALSE, # set later 
                     # set risk table 
                     risk.table = TRUE, 
                     risk.table.height = 0.27,
                     risk.table.fontsize = 14,
                     risk.table.pos = 'out',
                     risk.table.title = '',
                     # set title name
                     title = 'Survival Curve',
                     subtitle = 'tumor original glcm ClusterTendency',
                     xlab = 'Months',
                     ylab = 'Overall Survival',
                     legend.labs=c("high", "low"),
                     legend.title=c(""))
p.value <- data.frame(x = 10, y = 0.2, text = c('P = 0.042'))

ggsurv$plot <- ggsurv$plot + geom_text(data = p.value, aes(x = x, y = y, label = text), size = 10,  fontface = 'bold',show.legend = NA)

ggsurv$plot <- ggsurv$plot +theme(plot.title = element_text(size = 45,hjust = 0.5, face = 'bold',family = 'Calibri'),
                                  plot.subtitle = element_text(size = 30,hjust = 0.5, face = 'bold',family = 'Calibri'),
                                  axis.text.x = element_text(size =30, face = 'bold', color = 'black',family = 'Calibri'),
                                  axis.text.y = element_text(size =30, face = 'bold', color = 'black',family = 'Calibri'),
                                  axis.title.x = element_text(size = 45, face = 'bold',family = 'Calibri'),
                                  axis.title.y = element_text(size = 45, face = 'bold',family = 'Calibri'),
                                  legend.title = element_blank(),
                                  legend.text = element_text(size = 45, face = 'bold',family = 'Calibri'),
                                  legend.background = element_blank(),
                                  legend.key = element_rect(fill = NA, colour = NA, size=1),
                                  legend.position = c(0.8,0.8))

ggsurv$table <- ggsurv$table +theme(plot.title = element_text(size = 0.01),
                                    axis.text.x = element_text(size =45, face = 'bold', color = 'black',family = 'Calibri'),
                                    axis.text.y = element_text(size =45, face = 'bold', color = 'black',family = 'Calibri'),
                                    axis.title.x = element_text(size = 45, face = 'bold',family = 'Calibri'),
                                    axis.title.y = element_text(size = 45, face = 'bold',family = 'Calibri'),
                                    legend.title = element_blank(),
                                    legend.text = element_text(size = 45, face = 'bold',family = 'Calibri'),
                                    legend.background = element_blank(),
                                    legend.key = element_rect(fill = NA, colour = NA, size=1),
                                    legend.position = '')
ggsurv
ggsave("tumor_original_glcm_ClusterTendency_kmplot.jpg", plot = print(ggsurv), device = "jpeg", width = 12.5, height = 10, dpi = 300)


