import os
import json
import jsonschema
from jsonschema import validate
import pandas as pd
import fileFolderManagementTool
import dataframeTool

def jsonFilesList(folder_path):
    #print("Folder: " + folder_path)
    fl = fileFolderManagementTool.files_list(folder_path)
    j = 0
    for f in fl:
        print(f)    
        l = jsonFileMetrics(folder_path, f)
        j = j + l
    print("\tNumber of items in all JSON files: " + str(j))
    return fl

def jsonFilesToOneDf(folder_path):
    print("\tFolder: " + folder_path)
    fl = fileFolderManagementTool.files_list(folder_path)
    frames = []
    for f in fl:
        datafr = pd.read_json(os.path.join(folder_path, f))
        df1 = dataframeTool.renameColumn(datafr)
        frames.append(df1)
    df = pd.concat(frames, sort=True)
    #df.reset_index(drop=True, inplace=True) 
    #df.to_json("MergeJson.json") 
    return df    
    
def jsonFileMetrics(folder, file):
    with open(os.path.join(folder, file)) as f: 
        data = json.load(f)   
    items_num = len(data)
    print("\tNumber of items in the file: " + str(items_num))
    #print("\tFirst item in the file: " + str(data[0]))    
    return items_num