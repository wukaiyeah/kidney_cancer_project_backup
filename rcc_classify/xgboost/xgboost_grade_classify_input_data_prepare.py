import os
import json
import pandas as pd
import numpy as np
import glob
import pickle
from sklearn.model_selection import train_test_split
import sys
sys.path.append('/share/Data01/wukai/rcc_classify')
from config import config 

def prepare_files_id(cases_id, cf):
    files_dir = glob.glob(os.path.join(cf.cropped_dir,'*.npz'))
    files_id = [file_dir.split('/')[-1].replace('.npz','') for file_dir in files_dir]
    target_files_id = [file_id for file_id in files_id if file_id.split('_')[0] in cases_id] 
    return sorted(target_files_id)

def make_input_feature(files_id, features_dict):
    features_list = []
    for file_id in files_id:
        features_tumor = features_dict[file_id]['tumor']
        features_list.append(features_tumor)
    features_array = np.array(features_list)
    return features_array


def make_input_images_feature(files_id, features_dict):
    features_list = []
    for file_id in files_id:
        features_list.append(features_dict[file_id])
    features_array = np.vstack(features_list)
    return features_array


def make_target_labels(files_id, grade_dict):
    target_labels = []
    for file_id in files_id:
        case_id = file_id.split('_')[0]
        grade = grade_dict[case_id]

        target_labels.append(grade)
    return np.array(target_labels)

def constuct_dict(file_dir):
    assert os.path.exists(file_dir), 'Can not find file in %s'%file_dir
    grade_dict = {}
    with open(file_dir, 'r') as IN:
        info = IN.readlines()
        for line in info:
            if not line.startswith('case_id'):
                items = line.strip().split('\t')
                case_id = items[0]
                label = items[2]
                grade_dict[case_id] = int(label)
    return grade_dict



if __name__ == "__main__":
    cf = config()
    base_dir = '/share/Data01/wukai/rcc_classify/xgboost'
    clinical_dir = '/share/Data01/wukai/rcc_classify/clinical_all_rcc_dict.pkl'
    training_cases_info = '/share/Data01/wukai/rcc_classify/dataset_cases_split.pkl'
    tumor_cls_split_info = '/share/Data01/wukai/rcc_classify/tumor_cls_split.pkl'
    grade_info_dir = '/share/Data01/wukai/rcc_classify/xgboost/renal_cancer_grade_info.txt'
    pyradiomics_result_dir = '/share/Data01/wukai/rcc_classify/xgboost/pyradiomics_enhanced_result.json'
    pyradiomics_testset_dir = '/share/Data01/wukai/rcc_classify/xgboost/pyradiomics_testset_result.json'
    images_pca_features_dir = '/share/Data01/wukai/rcc_classify/xgboost/images_pca_tumor_features.pkl'
    images_svd_features_dir = '/share/Data01/wukai/rcc_classify/xgboost/images_svd_tumor_features.pkl'
    images_pca_testset_features_dir = '/share/Data01/wukai/rcc_classify/xgboost/images_pca_testset_tumor_features.pkl'
    images_svd_testset_features_dir = '/share/Data01/wukai/rcc_classify/xgboost/images_svd_testset_tumor_features.pkl'

    # load grade info 
    grade_dict = constuct_dict(grade_info_dir)



    # load training cases
    with open(training_cases_info, 'rb') as IN:
        training_cases_info = pickle.load(IN)
        training_cases = [case_id for case_id in training_cases_info['training'] if case_id in grade_dict.keys()]
        testing_cases = [case_id for case_id in training_cases_info['testing'] if case_id in grade_dict.keys()]


    # load pyradiomics result
    with open(pyradiomics_result_dir,'r') as IN:
        features_dict = json.load(IN)

    with open(pyradiomics_testset_dir,'r') as IN:
        features_testset_dict = json.load(IN)


    # load images pca features
    with open(images_pca_features_dir,'rb') as IN:
        images_pca_features_dict = pickle.load(IN)

    with open(images_pca_testset_features_dir,'rb') as IN:
        images_pca_testset_features_dict = pickle.load(IN)

    # load images pca features
    with open(images_svd_features_dir,'rb') as IN:
        images_svd_features_dict = pickle.load(IN)

    with open(images_svd_testset_features_dir,'rb') as IN:
        images_svd_testset_features_dict = pickle.load(IN)
    '''
    # load images isomap features
    with open(images_isomap_features_dir,'rb') as IN:
        images_isomap_features_dict = pickle.load(IN)

    # load dpn features
    with open(dpn_features_dir,'rb') as IN:
        dpn_features_dict = pickle.load(IN)

    # load images ics features
    with open(images_ica_features_dir,'rb') as IN:
        images_ica_features_dict = pickle.load(IN)

    # load images lle features
    with open(images_lle_features_dir,'rb') as IN:
        images_lle_features_dict = pickle.load(IN)

    # load images tsne features
    with open(images_tsne_features_dir,'rb') as IN:
        images_tsne_features_dict = pickle.load(IN)
    '''

    training_files_id = prepare_files_id(training_cases, cf)
    testing_files_id = prepare_files_id(testing_cases, cf)
    # prepare feature array
    training_features = make_input_feature(training_files_id, features_dict)
    testing_features = make_input_feature(testing_files_id, features_testset_dict)


    training_pca_features = make_input_images_feature(training_files_id, images_pca_features_dict)
    testing_pca_features = make_input_images_feature(testing_files_id, images_pca_testset_features_dict)

    training_svd_features = make_input_images_feature(training_files_id, images_svd_features_dict)
    testing_svd_features = make_input_images_feature(testing_files_id, images_svd_testset_features_dict)

    '''
    training_ica_features = make_input_images_feature(training_files_id, images_ica_features_dict)
    testing_ica_features = make_input_images_feature(testing_files_id, images_ica_features_dict)

    training_lle_features = make_input_images_feature(training_files_id, images_lle_features_dict)
    testing_lle_features = make_input_images_feature(testing_files_id, images_lle_features_dict)

    training_tsne_features = make_input_images_feature(training_files_id, images_tsne_features_dict)
    testing_tsne_features = make_input_images_feature(testing_files_id, images_tsne_features_dict)
    '''


    training_features = np.hstack((training_features, training_svd_features, training_pca_features))
    testing_features = np.hstack((testing_features,testing_svd_features, testing_pca_features))

    alias = list(pd.read_csv('/share/Data01/wukai/rcc_classify/xgboost/images_features_name_alias.txt',sep = '\t')['alias'])
    colnames = ['t_'+name for name in alias] + ['svd_%i'%i for i in range(24)] + ['pca_%i'%i for i in range(96)]
    
    training_features = pd.DataFrame(training_features)
    training_features.columns = colnames
    training_features.index = training_files_id
    training_features.to_csv('train_features_grade.csv', sep = ',',index=True)

    testing_features = pd.DataFrame(testing_features)
    testing_features.columns = colnames
    testing_features.index =testing_files_id
    testing_features.to_csv('test_features_grade.csv', sep = ',',index=True)



    np.savez_compressed(os.path.join(base_dir, 'train_features_grade_pyradiomics_images.npz'), data = training_features)
    np.savez_compressed(os.path.join(base_dir, 'testset_features_grade_pyradiomics_images.npz'), data = testing_features)
    # prepare target array
    training_labels = make_target_labels(training_files_id, grade_dict)
    testing_labels = make_target_labels(testing_files_id, grade_dict)
    np.savez_compressed(os.path.join(base_dir, 'train_grade_target.npz'), data = training_labels)
    np.savez_compressed(os.path.join(base_dir, 'test_grade_target.npz'), data = testing_labels)
