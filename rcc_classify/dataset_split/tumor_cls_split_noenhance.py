# prepare 5 cross validation training list
import numpy as np
import os
import glob
import pickle
from sklearn.model_selection import StratifiedKFold, KFold
import sys
sys.path.append('/share/Data01/wukai/rcc_classify')
from config import config 


def creat_train_files(training_cases, clinical_dict, cf):
    print('Total training cases %d'%(len(training_cases)))
    # have original files
    ori_files_dir = glob.glob(os.path.join(cf.cropped_dir, '*.npz'))
    ori_files_id = [dir.split('/')[-1].replace('.npz','') for dir in ori_files_dir]
    training_files = [file_id for file_id in ori_files_id if file_id.split('_')[0] in training_cases]


    stage = [clinical_dict[file_id.split('_')[0]]['stage'] for file_id in training_files]
    subtype = [clinical_dict[file_id.split('_')[0]]['subtype'] for file_id in training_files]
    print(sum(stage)/len(stage))
    print(sum(subtype)/len(subtype))

    return training_files

def creat_test_files(testing_cases, cf):
    print('Total testing cases %d'%(len(testing_cases)))

    files_dir = glob.glob(os.path.join(cf.enhanced_dir, '*.npz'))
    print('Total files %d'%(len(files_dir)))
    files_id = [dir.split('/')[-1].replace('.npz','') for dir in files_dir]

    testing_files = [file_id for file_id in files_id if file_id.split('_')[0] in testing_cases]

    return testing_files

if __name__ == '__main__':
    cf = config()
    assert os.path.exists(os.path.join(cf.base_dir, 'dataset_cases_split.pkl')), 'Need split cases first'
    with open(os.path.join(cf.base_dir, 'dataset_cases_split.pkl'), 'rb') as IN:
        dataset_split = pickle.load(IN)
    training_cases = dataset_split['training'] # training list

    with open(cf.clinical_file, 'rb') as IN:
        clinical_dict = pickle.load(IN)
    # 更改肿瘤分期标签
    for case_id in training_cases:
        if clinical_dict[case_id]['stage'] < 2: # stage range from 0,1,2,3; I II III IV stage
            stage = 0
        elif clinical_dict[case_id]['stage'] >= 2:
            stage = 1
        clinical_dict[case_id]['stage'] = stage

    subtype = [clinical_dict[case_id]['subtype'] for case_id in training_cases]
    stage = [clinical_dict[case_id]['stage'] for case_id in training_cases]


    train_files = creat_train_files(training_cases, clinical_dict, cf)


    split_dict = {}
    split_dict = {'train_cases':training_cases,
                    'train_files':train_files,
                    'validate_cases':dataset_split['testing']}

    with open(os.path.join(cf.base_dir, 'tumor_cls_split_noEnhance.pkl'), 'wb') as OUT:
        pickle.dump(split_dict, OUT)


    # five cross val
    '''
    kfold = KFold(n_splits=5, shuffle=True, random_state=1234)
    cross_val_split = []

    for train, val in kfold.split(training_cases):
        train_cases = [training_cases[index] for index in train]
        validate_cases = [training_cases[index] for index in val]
        
        train_files = creat_train_files(train_cases, clinical_dict, cf)
        validate_files = creat_test_files(validate_cases, cf)

        split_dict = {}
        split_dict = {'train_cases':train_cases,
                        'train_files':train_files,
                        'validate_cases':validate_cases,
                        'validate_files':validate_files}
        cross_val_split.append(split_dict)

    with open(os.path.join(cf.base_dir, 'tumor_cls_cross_val_split.pkl'), 'wb') as OUT:
        pickle.dump(cross_val_split, OUT)
    '''

