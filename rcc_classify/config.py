import os
import numpy as np

class config():
    def __init__(self):
        self.base_dir = '/share/Data01/wukai/rcc_classify'
        self.image_dir0 = '/share/Data01/wukai/Task001_KITS19/imagesTr'
        self.mask_dir0 = '/share/Data01/wukai/Task001_KITS19/labelsTr'
        self.image_dir1 = '/share/service04/wukai/CT_image/CPTAC-CCRCC/images'
        self.mask_dir1 = '/share/service04/wukai/CT_image/CPTAC-CCRCC/labels_refined'
        self.image_dir2 = '/share/service04/wukai/CT_image/TCGA-KICH/images'
        self.mask_dir2 = '/share/service04/wukai/CT_image/TCGA-KICH/labels_refined'
        self.image_dir3 = '/share/service04/wukai/CT_image/TCGA-KIRC/images'
        self.mask_dir3 = '/share/service04/wukai/CT_image/TCGA-KIRC/labels_refined'
        self.image_dir4 = '/share/service04/wukai/CT_image/TCGA-KIRP/images'
        self.mask_dir4 = '/share/service04/wukai/CT_image/TCGA-KIRP/labels_refined'
        
        self.testset_image_dir = '/share/service04/wukai/nnUNet_raw_data_base/nnUNet_raw_data/Task100_KidneyTumor/imagesTs'
        self.testset_mask_dir = '/share/service04/wukai/nnUNet_raw_data_base/nnUNet_raw_data/Task100_KidneyTumor/labelsTsp'
        self.testset_resample_dir = '/share/service04/wukai/CT_image/testset/images_resampled'
        self.testset_normalized_dir = '/share/service04/wukai/CT_image/testset/images_normalized'
        self.testset_cropped_dir = '/share/service04/wukai/CT_image/testset/images_cropped'

        self.resample_dir = '/share/service04/wukai/CT_image/images_resampled'
        self.normalized_dir = '/share/service04/wukai/CT_image/images_normalized'
        self.cropped_dir = '/share/service04/wukai/CT_image/images_cropped'
        self.enhanced_dir = '/share/service04/wukai/CT_image/images_enhanced'

        self.clinical_file = '/share/Data01/wukai/rcc_classify/clinical_all_rcc_dict.pkl'

        self.process_num = 30
        self.target_spacing = [2.5,2.5,2.5] # [H,Y,X]
        self.tumor_size_threshold = 48*24*24
        self.crop_size = [64,64,64]
        self.flip_H = True # flip horizontal
        self.flip_V = True
        self.flip_Z = True
        self.rotate_list = [i for i in range(0, 360, 30)][1:] # 每30度旋转一次，共11次变换
        self.gaussian_sigma_list = [0.2,0.4,0.6]

        self.subtype_cross_val = '/share/Data01/wukai/rcc_classify/subtype_cls_cross_val_split.pkl'
        self.stage_cross_val= '/share/Data01/wukai/rcc_classify/stage_cls_cross_val_split.pkl'
        self.tumor_cls_cross_val = '/share/Data01/wukai/rcc_classify/tumor_cls_cross_val_split.pkl'
        self.tumor_cls_split = '/share/Data01/wukai/rcc_classify/tumor_cls_split.pkl'
        self.tumor_cls_split_noEnhance = '/share/Data01/wukai/rcc_classify/tumor_cls_split_noEnhance.pkl'

        self.immum_infiltration = '/share/Data01/wukai/rcc_classify/immum_infiltration.json'
        self.immum_cross_val = '/share/Data01/wukai/rcc_classify/immun_infil_cross_val_split.pkl'
        self.fold = 0 # 0,1,2,3,4

