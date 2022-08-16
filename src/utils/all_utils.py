from fsutil import exists
import yaml
import os


def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return content


def create_directory(dirs=list):
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        print(f"directory created at {dir_path}")

def create_directory2(dirs=list):
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        print(f"directory created at {dir_path}")

def save_local_df(data, data_path, index_status=False):
    data.to_csv(data_path, index=index_status)
    print(f"file save at {data_path}")