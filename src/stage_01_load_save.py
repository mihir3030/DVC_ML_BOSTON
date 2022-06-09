from src.utils.all_utils import read_yaml, create_directory
import os
import argparse
import pandas as pd
import shutil

def get_data(config_path):
    config = read_yaml(config_path)

    # save data to local directory
    artifacts_dir = config['artifacts']['artifacts_dir']
    raw_local_dir = config['artifacts']['raw_local_dir']

    raw_local_file = config['artifacts']['raw_local_file']

    # we got all informations. 
    # create path of directory
    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)

    create_directory(dirs = [raw_local_dir_path])

    raw_local_file_path = os.path.join(raw_local_dir_path, raw_local_file)
    
    
    original_data_path = "train.csv"
    
    shutil.copy(original_data_path, raw_local_file_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")

    parsed_args = args.parse_args()

    get_data(config_path = parsed_args.config)