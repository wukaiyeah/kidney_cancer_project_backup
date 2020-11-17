# prepare 5 cross validation training list
import numpy as np
import os
import glob
import pickle
from sklearn.model_selection import train_test_split
import sys
sys.path.append('/share/Data01/wukai/rcc_classify')
from config import config 

if __name__ == '__main__':
    cf = config()
    with open(cf.clinical_file, 'rb') as IN:
        clinical_dict = pickle.load(IN)

    files_dir = glob.glob(os.path.join(cf.enhanced_dir,'*.npz'))
    files_id = [dir.split('/')[-1].replace('.npz','') for dir in files_dir]
    cases_id = [id.split('_')[0] for id in files_id]
    cases_id = list(set(cases_id)) # unique
    for case_id in cases_id: #判断所得到的case_id是否都有临床资料
        assert case_id in clinical_dict.keys(), '%s not in clinical info dict'%(case_id)
    subtype = [clinical_dict[case_id]['subtype'] for case_id in cases_id]

    # train & test split
    training_cases, testing_cases, training_subtype, testing_subtype = train_test_split(cases_id, subtype, test_size=0.2, shuffle= True, stratify=subtype, random_state=1234)

    dataset_split = {'training':training_cases,
                    'testing':testing_cases}
    with open(os.path.join(cf.base_dir, 'dataset_cases_split.pkl'), 'wb') as OUT:
        pickle.dump(dataset_split, OUT)

    


