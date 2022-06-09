from src.utils.all_utils import read_yaml, create_directory, save_local_df
import os
import argparse
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler


def feature_selection_split(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    # read preprocessing csv file from directory   
    artifact_dir = config['artifacts']['artifacts_dir']
    data_preprocessing_dir = config['artifacts']['data_preprocessing_dir']
    data_preprocessing_file = config['artifacts']['data_preprocessing_file']

    
    

    # open file from path
    data_path = os.path.join(artifact_dir, data_preprocessing_dir, data_preprocessing_file)
    # read csv file
    df = pd.read_csv(data_path)

    # --------------------FEATURE-SCALING---------------------------------
    
    x = df.drop('SalePrice', axis= 1)
    y = df['SalePrice']

    # scaling data using StandardScaler
    scaler = StandardScaler()
    x = scaler.fit_transform(x)

    # now we need to save scaled data into dataframe
    columns = df.drop('SalePrice', axis= 1)
    df_final = pd.DataFrame(x, columns=columns.columns)
    #print(df_final.head())

    # read params
    test_size = params['base']['test_size']
    ramdom_state = params['base']['random_state']
    model_selection_alpha = params['model_selection']['alpha']

    #------------------FEATURE-SELECTION-----------------------------------
    # first, I specify the Lasso Regression model, and I
    # select a suitable alpha (equivalent of penalty).
    # The bigger the alpha the less features that will be selected.

    # Then I use the selectFromModel object from sklearn, which
    # will select the features which coefficients are non-zero
    feature_model_sel = SelectFromModel(Lasso(alpha=model_selection_alpha, random_state=ramdom_state)) # remember to set the seed, the random state in this function
    feature_model_sel.fit(df_final, y)
    #print(feature_model_sel.get_support())

    # before feature scaling feature is: 73
    # after feature scaling feature is: 43
    selected_feature = df_final.columns[(feature_model_sel.get_support())]
    df = df_final[selected_feature]


    data_selection_dir = config['artifacts']['data_selection_dir']
    data_selection_file_dir = config['artifacts']['data_selection_file']

    create_directory([os.path.join(artifact_dir, data_selection_dir)])
    data_selection_file_path = os.path.join(artifact_dir, data_selection_dir, data_selection_file_dir)

    save_local_df(df, data_selection_file_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--config", '-c', default='config/config.yaml')
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    feature_selection_split(config_path=parsed_args.config,  params_path=parsed_args.params)