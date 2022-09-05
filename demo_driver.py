# imports
import pandas as pd
from IPython.display import display # displaying dataframe
import os

# dependencies
import automated_hvf_grading.driver as driver

# running driver.py script directly
if __name__ == "__main__":
    # == demo data == 
    # path ='./faultyFields'
    path = './singleField'
    sample_size = 1
    patient_id = "0034527.9"
    selected_eye = "Right"
    
    if os.path.exists(path):
        files = list(driver.FileRunner.absoluteFilePaths(path)) # generator to list

    dfObj  = driver.runParallel(files, sample_size)
  
    driver.printDf(dfObj.df)
    
    #selecting patient via filterByID or filterByName
    patientDfObj = driver.filterDFByID(dfObj, patient_id)

    analysis_df = driver.Analysis(dfObj, selected_eye)

    driver.printDf(analysis_df)

    
    

    
    
    
    