import os, csv
import shutil
##from os import listdir
##from os.path import isfile, join

LOGS_DIR = "logs"

def files_list(folder_path):
    ## input testing
    if not os.path.isdir(folder_path):
        raise Exception("specified folder path does not exist")
    if not len(os.listdir(folder_path)) > 0:
        raise Exception("specified folder path data dir does not contain any files")

    file_list = []

    for path, dirs, files in os.walk(folder_path):
        for filename in files:
            file_list.append(filename)  
    return file_list

def clean_ts_data_dir(clean=False):
    ts_data_dir = os.path.join(".","ts-data")
    if clean:
        print("cleaning ts_data folder...")
        shutil.rmtree(ts_data_dir)
    if not os.path.exists(ts_data_dir):
        os.mkdir(ts_data_dir)

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    if os.path.isfile(file_name):
        print ("File exist")
    else:
        print ("File not exist")
        return False
    
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False        
        
        
def update_train_log(tag, dates, rmse, runtime, model_version, model_note, test):
    if not os.path.isdir(LOGS_DIR):
        os.mkdir(LOGS_DIR)

    log_file = os.path.join(LOGS_DIR,"train.log") 
        
    entete = False
    
    if check_if_string_in_file(log_file, 'tag,dates,rmse,runtime,model_version,model_note,test'):
        print('Yes, string found in file')       
    else:
        print('String not found in file')
        entete = True
              
    with open(log_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        if entete == True:
             writer.writerow(["tag","dates","rmse","runtime","model_version","model_note","test"])
        
        writer.writerow([tag,dates,rmse,runtime,model_version,model_note,test])

def update_predict_log(country, y_pred, y_proba, target_date, runtime, model_version, test):
    if not os.path.isdir(LOGS_DIR):
        os.mkdir(LOGS_DIR)

    log_file = os.path.join(LOGS_DIR,"predict.log") 
        
    entete = False
    
    if check_if_string_in_file(log_file, 'country,y_pred,y_proba,target_date,runtime,model_version,test'):
        print('Yes, string found in file')       
    else:
        print('String not found in file')
        entete = True
              
    with open(log_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        if entete == True:
             writer.writerow(["country","y_pred","y_proba","target_date","runtime","model_version","test"])
        
        writer.writerow([country,y_pred,y_proba,target_date,runtime,model_version,test])
        #writer.writerow(["tag", tag])
        #writer.writerow(["dates", dates])
        #writer.writerow(["rmse", rmse])
        #writer.writerow(["runtime", runtime])
        #writer.writerow(["model_version", model_version])
        #writer.writerow(["model_note", model_note])
        #writer.writerow(["test", test])





