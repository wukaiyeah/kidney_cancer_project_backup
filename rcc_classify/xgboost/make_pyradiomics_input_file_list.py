import os
import glob
import pandas as pd

if __name__ == '__main__':
    base_dir = '/share/Data01/wukai/rcc_classify/xgboost'
    image_source = '/share/service04/wukai/nnUNet_raw_data_base/nnUNet_raw_data/Task100_KidneyTumor/imagesTs'
    label_source = '/share/service04/wukai/nnUNet_raw_data_base/nnUNet_raw_data/Task100_KidneyTumor/labelsTsp'

    images_dir = glob.glob(os.path.join(image_source, '*nii.gz'))
    files_name = [file_dir.split('/')[-1] for file_dir in images_dir]
    print("Find total %d files need to be processed"%(len(files_name)))

    OUT = open(os.path.join(base_dir, 'file_dir_testset.csv'), 'w')
    OUT.write('Image'+','+'Mask'+'\n')
    for file_name in files_name:
        image_dir = os.path.join(image_source, file_name)
        label_dir = os.path.join(label_source, file_name.replace('_0000',''))
        assert os.path.exists(image_dir),'Can not find file in images dir %s'%(file_name)
        assert os.path.exists(label_dir),'Can not find file in labels dir %s'%(file_name)
        OUT.write(image_dir+','+label_dir+'\n')

    OUT.close()
