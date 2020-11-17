import os
import glob
import pickle
import json
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from config import config
import matplotlib.pyplot as plt
def prepare_tumor_cls_dataset(cf):
    '''
    prepare experiment 
    return: a list contains every cases' dicts
    '''
    # training file
    with open(cf.tumor_cls_split, 'rb') as IN:
        files_info = pickle.load(IN)
    training_files_id = files_info['train_files']
    print('Find %d files for training' % len(training_files_id))

    # load clinical info
    with open(cf.clinical_file, 'rb') as IN:
        clinical_dict = pickle.load(IN)
    # 更改肿瘤分期标签
    for case_id in clinical_dict.keys():
        if clinical_dict[case_id]['stage'] < 2: # stage range from 0,1,2,3; I II III IV stage
            stage = 0
        elif clinical_dict[case_id]['stage'] >= 2:
            stage = 1
        clinical_dict[case_id]['stage'] = stage


    cases_info = []
    for file_id in training_files_id:
        case_id = file_id.split('_')[0]
        image_dir = os.path.join(cf.enhanced_dir, file_id+'.npz')
        assert os.path.exists(image_dir), 'Can not find file %s'%(file_id+'.npz')

        assert case_id in clinical_dict.keys(), 'Can not find case %s in clinical data'%(case_id)
        subtype = clinical_dict[case_id]['subtype']
        stage = clinical_dict[case_id]['stage']
        label = [int(subtype), int(stage)]

        cases_info.append({'case_id': case_id,
                            'file_id':file_id,
                            'file_dir':image_dir,
                            'label':label
                            })
    return cases_info




def prepare_cls_subtype_dataset(cf):
    '''
    prepare experiment 
    return: a list contains every cases' dicts
    '''
    # training file
    with open(cf.subtype_cross_val, 'rb') as IN:
        files_info = pickle.load(IN)
    training_files_id = files_info[cf.fold]['train_files']
    print('Find %d files for training' % len(training_files_id))

    # load clinical info
    with open(cf.clinical_file, 'rb') as IN:
        clinical_dict = pickle.load(IN)

    cases_info = []
    for file_id in training_files_id:
        case_id = file_id.split('_')[0]
        image_dir = os.path.join(cf.enhanced_dir, file_id+'.npz')
        assert os.path.exists(image_dir), 'Can not find file %s'%(file_id+'.npz')

        assert case_id in clinical_dict.keys(), 'Can not find case %s in clinical data'%(case_id)
        subtype = clinical_dict[case_id]['subtype']
        
        cases_info.append({'case_id': case_id,
                            'file_id':file_id,
                            'file_dir':image_dir,
                            'label':subtype
                            })
    return cases_info

def prepare_cls_stage_dataset(cf):
    '''
    prepare experiment 
    return: a list contains every cases' dicts
    '''
    # training file
    with open(cf.stage_cross_val, 'rb') as IN:
        files_info = pickle.load(IN)
    training_files_id = files_info[cf.fold]['train_files']
    print('Find %d files for training' % len(training_files_id))

    # load clinical info
    with open(cf.clinical_file, 'rb') as IN:
        clinical_dict = pickle.load(IN)
    # 更改肿瘤分期标签
    for case_id in clinical_dict.keys():
        if clinical_dict[case_id]['stage'] < 2: # stage range from 0,1,2,3; I II III IV stage
            stage = 0
        elif clinical_dict[case_id]['stage'] >= 2:
            stage = 1
        clinical_dict[case_id]['stage'] = stage

    cases_info = []
    for file_id in training_files_id:
        case_id = file_id.split('_')[0]
        image_dir = os.path.join(cf.enhanced_dir, file_id+'.npz')
        assert os.path.exists(image_dir), 'Can not find file %s'%(file_id+'.npz')

        assert case_id in clinical_dict.keys(), 'Can not find case %s in clinical data'%(case_id)
        stage = clinical_dict[case_id]['stage']
        
        cases_info.append({'case_id': case_id,
                            'file_id':file_id,
                            'file_dir':image_dir,
                            'label':stage
                            })
    return cases_info

def prepare_immun_infil_dataset(cf):
    '''
    prepare experiment 
    return: a list contains every cases' dicts
    '''
    # training file
    with open(cf.immum_cross_val, 'rb') as IN:
        files_info = pickle.load(IN)
    training_files_id = files_info[cf.fold]['train_files']
    print('Find %d files for training' % len(training_files_id))

    # load clinical info
    with open(cf.immum_infiltration, 'r') as IN:
        immun_dict = json.load(IN)

    cases_info = []
    for file_id in training_files_id:
        case_id = file_id.split('_')[0]
        image_dir = os.path.join(cf.enhanced_dir, file_id+'.npz')
        assert os.path.exists(image_dir), 'Can not find file %s'%(file_id+'.npz')

        assert case_id in immun_dict.keys(), 'Can not find case %s in immun data'%(case_id)
        immun_value = immun_dict[case_id][cf.algorithm]
        
        cases_info.append({'case_id': case_id,
                            'file_id':file_id,
                            'file_dir':image_dir,
                            'label':immun_value
                            })
    return cases_info



class BatchLoadar(Dataset):
    def __init__(self, cases_dict):
        self.cases_dict = cases_dict
        
    def __getitem__(self, index):
        # get the anchor index for current sample index
        # here we set the anchor index to the last one
        # sample in this group
        case_info = self.cases_dict[index]
        file_id = case_info['file_id']
        print('process '+file_id)
        all_data = np.load(case_info['file_dir'])['data'][None] # load data & add newaxis
        image = torch.from_numpy(all_data)
        label = torch.tensor(case_info['label'])
        '''
        for i,img in enumerate(image[0]):
            plt.imshow(img)
            plt.savefig('%d.png'%(i))
        '''
        return image,label

    def __len__(self):
        return len(self.cases_dict)



if __name__ == '__main__':
    # for debug
    cf = config()
    cf.algorithm = 'TIMER'
    cases_info_list = prepare_tumor_cls_dataset(cf)

    train_dataset = BatchLoadar(cases_info_list)
    dataloader = DataLoader(dataset= train_dataset, batch_size=4, shuffle=True, num_workers=0, drop_last =False)
    batch = iter(dataloader)
    image,label  = next(batch)
    print(label)
    print('ok')