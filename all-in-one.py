# Importing necessary libraries
import os
import sys
import re
import jsonTool
import dataframeTool
import visualizationTool
import displayTool
import fileFolderManagementTool
import modelTool

if __name__ == "__main__":

    data_dir = os.path.join(".","cs-train")
    print("data_dir: " + str(data_dir))
    print('\n') 
    displayTool.printmd("**I. PART 1 - CAPSTONE PROJECT**",  color="black")
    displayTool.printmd("**1. JSON FILES TO DATAFRAME:**",  color="black")
    displayTool.printmd("**Importing and Loading the json data into one data frame:**",  color="blue")
    fl = jsonTool.jsonFilesList(data_dir)   
    df = jsonTool.jsonFilesToOneDf(data_dir)
    
    print('\n')
    displayTool.printmd("**2. DATAFRAME TRANSORMATION:**",  color="black")
    df = dataframeTool.transform(df)
    print('\n')
    
    displayTool.printmd("**3. DATAFRAME INFO:**",  color="black")
    dataframeTool.display_df_info(df)
    print('\n')
    displayTool.printmd("**Display Pivot Tables:**",  color="blue")
    dataframeTool.displayPivotTables(df) 
    
    displayTool.printmd("**4. VISUALIZATIONS OF THE DATAFRAME:**",  color="black")
    print('\n')
    visualizationTool.plot_graphs_df(df)
    displayTool.printmd("**Plot correlation:**",  color="blue")
    visualizationTool.plot_corr(df)
    displayTool.printmd("**Plot Countries:**",  color="blue")
    visualizationTool.top_10_countries_years(df)
    visualizationTool.top_10_countries_months(df)
    visualizationTool.all_countries_year_months(df)
    visualizationTool.all_countries_days_of_week(df)
    
    displayTool.printmd("**5. TRANSFORMATION TO TIME-SERIES DATAFRAME:**",  color="black")
    df1 = dataframeTool.convert_to_ts(df)
    dataframeTool.display_ts_df_info(df1)
    
    displayTool.printmd("**6. VISUALIZATIONS OF TIME-SERIES DATAFRAME:**",  color="black")
    visualizationTool.plot_ts_df(df1)
    visualizationTool.plot_ts_df_3(df1) 
    displayTool.printmd("**Clean ts_data folder:**",  color="blue")
    fileFolderManagementTool.clean_ts_data_dir(clean=True)
    displayTool.printmd("**Generate csv files:**",  color="blue")
    dfs=dataframeTool.fetch_ts(df,df1)
    
    displayTool.printmd("**II. PART 2 - CAPSTONE PROJECT**",  color="black")
    displayTool.printmd("**Modeling ...**",  color="black")
    fileFolderManagementTool.clean_ts_data_dir(clean=True)   
    displayTool.printmd("**Training models**",  color="black")
    modelTool.model_train(df, df1,test=False)
    modelTool.model_train(df, df1,test=True)
    displayTool.printmd("**Loading models**",  color="black")
    all_data, all_models = modelTool.model_load()
    displayTool.printmd("**Model Loaded: **",  color="blue")
    print(all_models.keys())
    displayTool.printmd("**Test prediction**",  color="black")
    country='all'
    year='2018'
    month='01'
    day='05'
    result = modelTool.model_predict(country,year,month,day)
    print(result)