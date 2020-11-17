# prepare 5 cross validation training list
import numpy as np
import os
import glob
import pickle
import json
from sklearn.model_selection import KFold
import sys
sys.path.append('/share/Data01/wukai/rcc_classify')
from config import config 

def creat_train_files(train_cases, cf):
    print('Total training cases %d'%(len(train_cases)))

    files_dir = glob.glob(os.path.join(cf.enhanced_dir, '*.npz'))
    files_id = [dir.split('/')[-1].replace('.npz','') for dir in files_dir]
    train_files = [file_id for file_id in files_id if file_id.split('_')[0] in train_cases]

    return train_files


def creat_test_files(test_cases, cf):
    print('Total testing cases %d'%(len(test_cases)))

    files_dir = glob.glob(os.path.join(cf.enhanced_dir, '*.npz'))
    files_id = [dir.split('/')[-1].replace('.npz','') for dir in files_dir]

    test_files = [file_id for file_id in files_id if file_id.split('_')[0] in test_cases]
    return test_files

if __name__ == '__main__':
    cf = config()
    assert os.path.exists(os.path.join(cf.base_dir, 'dataset_cases_split.pkl')), 'Need split cases first'
    with open(os.path.join(cf.base_dir, 'dataset_cases_split.pkl'), 'rb') as IN:
        dataset_split = pickle.load(IN)
    training_cases = dataset_split['training'] # training list
    testing_cases = dataset_split['testing'] # testing list

    with open(cf.immum_infiltration, 'r') as IN:
        immun_info = json.load(IN)

    # 获取training数据集中的cases_id
    cases_id = [case_id for case_id in training_cases if case_id in immun_info.keys()]

    # five cross cases split
    kfold = KFold(n_splits=5, shuffle=True, random_state=1234)
    cases_split_result = []
    for train, test in kfold.split(cases_id):
        train_cases = [cases_id[index] for index in train]
        val_cases = [cases_id[index] for index in test]

        train_files = creat_train_files(train_cases, cf)
        val_files = creat_test_files(val_cases, cf)

        split_dict = {}
        split_dict = {'train_cases':train_cases,
                        'train_files':train_files,
                        'validate_cases':val_cases,
                        'validate_files':val_files}
        cases_split_result.append(split_dict)
    
    with open(os.path.join(cf.base_dir, 'immun_infil_cross_val_split.pkl'), 'wb') as OUT:
        pickle.dump(cases_split_result, OUT)

    


