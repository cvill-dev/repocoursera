import unittest
import modelTool
import fileFolderManagementTool
import os
import requests
import json

class ModelTest(unittest.TestCase):

    def test_model_train(self):
        MODELS_DIR = "models"
        file_name = os.path.join(".",MODELS_DIR, "sl-united_kingdom-0_1.joblib")
        self.assertTrue(os.path.exists(file_name))

    def test_model_predict(self):
        country='all'
        year='2018'
        month='01'
        day='05'
        result = modelTool.model_predict(country,year,month,day)
        y_pred = result['y_pred']
        self.assertTrue(y_pred > 0)

            
class LoggerTest(unittest.TestCase):
        
    def test_train_log(self):
        """
        verify the train.log is created
        """

        log_file = os.path.join("logs", "train.log")
        if os.path.exists(log_file):
            os.remove(log_file)
        
        tag="Test country"
        dates=("2017-01-01", "2018-01-01")
        rmse = {'rmse': 0.7}
        runtime = "00:00:04"
        MODEL_VERSION = 0.1
        MODEL_VERSION_NOTE = "supervised learing model for time-series"
        
        fileFolderManagementTool.update_train_log(tag,dates,rmse,runtime, MODEL_VERSION, MODEL_VERSION_NOTE,test=True)
   
        self.assertTrue(os.path.exists(log_file))
             

    def test_predict_log(self):
        """
        verify the predict.log is created
        """        
        log_file = os.path.join("logs","predict.log")
        if os.path.exists(log_file):
            os.remove(log_file)
                      
        country = "test country"
        y_pred = [0]
        y_proba = [0.6, 0.4]
        target_date = '2019-01-01'
        runtime = "00:00:04"
        MODEL_VERSION = 0.1

        fileFolderManagementTool.update_predict_log(country,y_pred,y_proba,target_date,runtime, MODEL_VERSION, test=True)
        
        self.assertTrue(os.path.exists(log_file))


class ApiTest(unittest.TestCase):
        
    def test_predict_via_api(self):
        y_pred_expected = 183799.05
        #base_url = "http://127.0.0.1:7000/api_query_arguments"
        base_url = "http://0.0.0.0:7000/api_query_arguments"
        params = dict()
        params["country"] = "all"
        params["year"] = "2018"
        params["month"] = "01"
        params["day"] = "05"
        r = requests.get(base_url, params=params)
        rr = json.loads(r.content)
        print(rr)
        self.assertTrue(rr['y_pred'] == y_pred_expected)
        

if __name__ == '__main__':
    unittest.main()
