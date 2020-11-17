#!/usr/bin/python
import os
import random
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score,roc_auc_score
from xgboost import XGBClassifier
from xgboost import plot_importance
import shap
def test(bst, test_X, test_Y):
    # get prediction
    xg_test = xgb.DMatrix(test_X, label=test_Y)
    pred = bst.predict(xg_test)
    accuracy = np.sum(pred == test_Y) / test_Y.shape[0]
    print('Test Accuracy = {}'.format(accuracy))



if __name__ == '__main__':
    base_dir = '/home/wukai/Desktop/xgboost'
    train_label_dir = os.path.join(base_dir,'train_grade_target.npz')
    train_feature_dir = os.path.join(base_dir,'train_features_grade_pyradiomics_images.npz')
    test_label_dir = os.path.join(base_dir, 'test_grade_target.npz')
    test_feature_dir = os.path.join(base_dir, 'testset_features_grade_pyradiomics_images.npz')

    train_feature = np.load(train_feature_dir)['data']
    train_label = np.load(train_label_dir)['data']

    test_feature = np.load(test_feature_dir)['data']
    test_label = np.load(test_label_dir)['data']

    '''
    #x_train,x_test,y_train,y_test = train_test_split(feature, label, test_size = 0.1)  
    dtrain = xgb.DMatrix(train_feature, train_label)
    dtest  = xgb.DMatrix(test_feature, train_label)

    param = {'objective':'multi:softmax',
            'learning_rate':0.001,
            "eval_metric":"mlogloss",
            'eta':0.1,
            'max_depth':3,
            'nthread':2,
            'num_class':3,
            'seed':1234}
    # use softmax multi-class classification
    cv_res= xgb.cv(param, dtrain, early_stopping_rounds=100,nfold=5,show_stdv=True)
    print('Best number of trees = {}'.format(cv_res.shape[0]))
    print(cv_res)
    '''


    # for tumor subtype cls
    model = XGBClassifier(learning_rate = 0.08, 
                            scale_pos_weight = 0.86,
                            n_estimators=300,
                            max_depth = 8,
                            subsample = 0.74,
                            reg_lambda = 1.1,
                            num_boost_round = 100,
                            min_child_weight = 1,
                            colsample_bytree=1)
    '''
    model = XGBClassifier(learning_rate = 0.08, 
                            scale_pos_weight = 0.86,
                            n_estimators=300,
                            max_depth = 8,
                            subsample = 0.74,
                            reg_lambda = 1.1,
                            num_boost_round = 100,
                            min_child_weight = 1,
                            colsample_bytree=1)
    '''
    eval_set = [(test_feature, test_label)]
    model.fit(train_feature, train_label, early_stopping_rounds=100, eval_metric=['auc'], eval_set=eval_set, verbose=True)

    y_pred = model.predict_proba(test_feature)
    y_pred_proba = y_pred[:,1] 
    y_pred_class = [0 if proba < 0.5 else 1 for proba in y_pred_proba ]

    accuracy = accuracy_score(test_label, y_pred_class)
    print("Subtype class accuracy: %.2f%%" % (accuracy * 100.0))
    Precision = precision_score(test_label, y_pred_class, average='binary')
    print("Subtype class precision: %.2f%%" % (Precision * 100.0))
    F1_score = f1_score(test_label, y_pred_class, average='binary') 
    print('Subtype F1 score:%.2f%%' %(F1_score*100.0))
    Recall_score = recall_score(test_label, y_pred_class, average='binary')
    print('Subtype Recall score label:%.2f%%' %(Recall_score*100.0))
    Auc_score = roc_auc_score(test_label, y_pred_proba)
    print('Subtype auc score label:%.2f%%' %(Auc_score*100.0))


    # write output
    result = pd.DataFrame()
    result['grade_label'] = test_label
    result['grade_proba'] = y_pred_proba

    # write output file
    result.to_csv('/home/wukai/Desktop/xgboost/testset_grade_pred_proba.csv',index=False,sep=',')

    # model explain
    # make train features table into pandas DataFrame
    train_feature_table = pd.DataFrame(train_feature)
    # input colnames
    alias = list(pd.read_csv('/home/wukai/Desktop/xgboost/images_features_name_alias.txt',sep = '\t')['alias'])
    colnames = ['t_'+name for name in alias] + ['svd_%i'%i for i in range(24)] + ['pca_%i'%i for i in range(96)]

    train_feature_table.columns = colnames

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(train_feature_table)
    pd.DataFrame(shap_values).to_csv('/home/wukai/Desktop/xgboost/xgboost_grade_shap_values.csv', sep = ',', index= False)
    shap.summary_plot(shap_values, train_feature_table, show = False, max_display = 20,plot_size = (16.,12.),title='XGBoost Subtype')
    plt.savefig('./grade_cls_shap_beeswarm.pdf', bbox_inches='tight')
    plt.close()
    #pd.DataFrame(train_feature).to_csv('/share/Data01/wukai/rcc_classify/xgboost/xgboost_train_features.csv', sep = ',', index= False)

    print('OK')

