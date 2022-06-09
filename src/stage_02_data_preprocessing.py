from src.utils.all_utils import read_yaml, create_directory, save_local_df
import os
import argparse
import pandas as pd
import numpy as np

def data_preprocessing(config_path):
    config = read_yaml(config_path)

    artifact_dir = config['artifacts']['artifacts_dir']
    raw_local_dir = config['artifacts']['raw_local_dir']
    raw_local_file = config['artifacts']['raw_local_file']

    raw_local_file_path = os.path.join(artifact_dir, raw_local_dir, raw_local_file)

    df = pd.read_csv(raw_local_file_path)
    
    
    #-----------DataPreprocessing-----------------------
    #drop ID column
    df.drop("Id", axis=1, inplace=True)
   
    # with list comprehension we drop columns that have more than 90% of null values
    [df.drop(feature,inplace=True, axis=1) for feature in df if df[feature].isnull().sum()/len(df[feature])*100 >= 80.0 ]
   
   # devide categorical null features and numerical null features
    categorical_nan = [feature for feature in df.columns if df[feature].dtypes=="O" and df[feature].isnull().sum()>=1]
    numerical_nan = [feature for feature in df.columns if df[feature].isnull().sum()>=1 and df[feature].dtypes!="O"]
    
    # temporary conver categorical null values with "missing"
    df[categorical_nan] = df[categorical_nan].fillna('missing')

    ### Replacing the numerical Missing Values
    for feature in numerical_nan:
        ## We will replace by using median since there are outliers
        median_value=df[feature].median()
        ## create a new feature to capture nan values
    #    dataset[feature+'nan']=np.where(dataset[feature].isnull(),1,0)
        df[feature].fillna(median_value,inplace=True)
    
    # here we do label encoding to transfer categorical values to numerical value
    categorical_features = [feature for feature in df.columns if df[feature].dtypes=='O']
    for feature in categorical_features:
        labels_ordered=df.groupby([feature])['SalePrice'].mean().sort_values().index
        labels_ordered={k:i for i,k in enumerate(labels_ordered,0)}
        df[feature]=df[feature].map(labels_ordered)
    
    # after preprocessing we need to save our csv file to atrifacts/data_preprocessing_dir/data_preprocessing.csv
    data_preprocessing_dir = config['artifacts']['data_preprocessing_dir']
    data_preprocessing_file_dir = config['artifacts']['data_preprocessing_file']

    create_directory([os.path.join(artifact_dir, data_preprocessing_dir)])
    data_preprocessing_file_path = os.path.join(artifact_dir, data_preprocessing_dir, data_preprocessing_file_dir)

    save_local_df(df, data_preprocessing_file_path)



if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")
    
    parsed_args = args.parse_args()

    data_preprocessing(config_path = parsed_args.config)

