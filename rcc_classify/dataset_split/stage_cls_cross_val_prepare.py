# prepare 5 cross validation training list
import numpy as np
import os
import glob
import pickle
from sklearn.model_selection import StratifiedKFold
import sys
sys.path.append('/share/Data01/wukai/rcc_classify')
from config import config 

def creat_train_files(training_cases, clinical_dict, cf):
    print('Total training cases %d'%(len(training_cases)))
    files_dir = glob.glob(os.path.join(cf.enhanced_dir, '*.npz'))
    print('Total files %d'%(len(files_dir)))
    files_id = [dir.split('/')[-1].replace('.npz','') for dir in files_dir]
    training_files = []
    cases_label_0 = [case_id for case_id in training_cases if clinical_dict[case_id]['stage'] == 0]
    cases_label_1 = [case_id for case_id in training_cases if clinical_dict[case_id]['stage'] == 1]

    # have original files
    ori_files_dir = glob.glob(os.path.join(cf.cropped_dir, '*.npz'))
    ori_files_id = [dir.split('/')[-1].replace('.npz','') for dir in ori_files_dir]
    training_files = [file_id for file_id in ori_files_id if file_id.split('_')[0] in training_cases]

    # enhanced files
    files_dir = glob.glob(os.path.join(cf.enhanced_dir, '*.npz'))
    files_id = [dir.split('/')[-1].replace('.npz','') for dir in files_dir]


    files_label_0 = [file_id for file_id in files_id if file_id.split('_')[0] in cases_label_0 if file_id not in training_files]
    files_label_1 = [file_id for file_id in files_id if file_id.split('_')[0] in cases_label_1 if file_id not in training_files]
    balance_num = min(len(files_label_0), len(files_label_1)) # 平衡两个标签文件数量
    
    for files_id in files_label_0, files_label_1:
        training_files += np.random.choice(files_id, balance_num, replace=False).tolist()


    
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

    # 筛选透明细胞癌的cases
    rcc_cases_id = [case_id for case_id in training_cases if clinical_dict[case_id]['subtype'] == 1]
    # 提取样本肿瘤分期标签
    labels = [clinical_dict[case_id]['stage'] for case_id in rcc_cases_id]

    # five cross cases split
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    cases_split_result = []
    for train, test in kfold.split(rcc_cases_id, labels):
        training_cases = [rcc_cases_id[index] for index in train]
        training_labels = [labels[index] for index in train]
        testing_cases = [rcc_cases_id[index] for index in test]
        testing_labels = [labels[index] for index in test]

        training_files = creat_train_files(training_cases, clinical_dict, cf)
        testing_files = creat_test_files(testing_cases, cf)

        split_dict = {}
        split_dict = {'train_cases':training_cases,
                        'train_files':training_files,
                        'validate_cases':testing_cases,
                        'validate_files':testing_files}
        cases_split_result.append(split_dict)
    
    with open(os.path.join(cf.base_dir, 'stage_cls_cross_val_split.pkl'), 'wb') as OUT:
        pickle.dump(cases_split_result, OUT)

    


