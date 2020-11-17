import os
import glob
import json

def prepare_files_dir(json_dir):
    assert os.path.exists(json_dir), 'Can not find json file'
    with open(json_dir,'r') as IN:
        dataset = json.load(IN)
    training_set = dataset['training']

    images_dir = []
    masks_dir = []
    for file_dict in training_set:
        images_dir.append(file_dict['image'].replace('.nii.gz','_0000.nii.gz'))
        masks_dir.append(file_dict['label'])
    

    test_images_dir = [dir.replace('.nii.gz','_0000.nii.gz') for dir in dataset['test']]
    test_labels_dir = [dir.replace('imagesTs','labelsTs') for dir in dataset['test']]
    images_dir = images_dir + test_images_dir
    masks_dir = masks_dir + test_labels_dir

    for dir in masks_dir:
        assert os.path.exists(dir), 'Can not find file'
    for dir in images_dir:
        assert os.path.exists(dir), 'Can not find file'

    return images_dir, masks_dir

def write_input_csv(csv_dir, images_dir, masks_dir):
    with open(csv_dir,'w') as OUT:
        OUT.write('Image,Mask\n')
        for i in range(len(images_dir)):
            OUT.write(images_dir[i]+','+masks_dir[i]+'\n')

    
def run(csv_dir, para_dir, output_dir):
    cmd = 'pyradiomics %s --p %s --jobs %d -o %s -f csv' % ( csv_dir, para_dir, 30, output_dir)
    os.system(cmd)


# pyradiomics <path/to/input> -o results.csv -f csv


if __name__ == '__main__':
    base_dir = '/share/Data01/wukai/rcc_classify/xgboost'
    param1_dir = '/share/Data01/wukai/rcc_classify/xgboost/PyradiomicsSettings/Params.yaml'
    param2_dir = '/share/Data01/wukai/rcc_classify/xgboost/PyradiomicsSettings/Params_label2.yaml'
    source_dir = '/share/service04/wukai/nnUNet_raw_data_base/nnUNet_raw_data/Task100_KidneyTumor'
    #json_dir = os.path.join(source_dir, 'dataset.json')
    #images_dir, masks_dir = prepare_files_dir(json_dir)
    #print('Find %d files'%(len(images_dir)))

    csv_dir = os.path.join(base_dir, 'file_dir_testset.csv')
    #write_input_csv(csv_dir, images_dir, masks_dir)
    run(csv_dir, param1_dir, os.path.join(base_dir, 'kidney_tumor_testset_features_label_1.csv'))
    run(csv_dir, param2_dir, os.path.join(base_dir, 'kidney_tumor_testset_features_label_2.csv'))