import json
import os


def read_json_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path,"r") as Json_file:
                data = json.load(Json_file)
            return data
        except Exception as error:
            raise Exception(error)
    else:
        raise Exception("File does not exist")
        
        
def write_json_file(file_path, data):
    if os.path.exists(os.path.dirname(file_path)):
        try:
            with open(file_path, "w") as Json_file:
                json.dump(data, Json_file)
        except Exception as error:
            raise Exception(error)
    else:
        raise Exception("Directory does not exist")


def write_text_file(file_path, data):
    with open(file_path, "w") as file1:
        for line in data:
            file1.write(line+"\n")


def read_text_file(file_path):
    with open(file_path, "r") as file1:
        data = file1.readlines()
        data = [eachLine.strip() for eachLine in data]
    return data
