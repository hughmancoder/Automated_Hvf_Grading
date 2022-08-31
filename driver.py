# imports
import numpy as np
import pandas as pd
from IPython.display import display # displaying dataframe
from multiprocessing import cpu_count

# dependencies
from automated_hvf_grading.fileRunner import FileRunner
from automated_hvf_grading.user import User
from automated_hvf_grading.dataFrame import DataFrame

# == helper functions (not strictly needed) == 

def filterDFByID(dfObject, id):
    return dfObject.filterByID(id)

def filterByName(dfObject, patient_name):
    return dfObject.filterByName(patient_name)

def Analysis(dfObject, eye):
    """Important: filter dfObject by id or name
    of individual patient as the whole idea of 
    analysis is to run only on an individual 
    patient scans

    Args:
        dfObject 
        eye 

    Returns:
        analysis data frame
    """
    if eye != "Left" and eye != "Right":
        print("Error: progression analysis not applicable, eye must be 'Left' or 'Right' only")
        return dfObject.df
    return dfObject.progressorCriteria(eye)

def printDf(df):
    pd.set_option("display.max_columns", len(df.columns)) # full width of res dataframe
    display(df)

# ==  different ways of running tasks: functions listed fastest to slowest ==
def runParallel(absolute_directory_path, sample_size):
    """runs files and outputs dataFrame object
    """
    fileRunnerObj = FileRunner() 
    return fileRunnerObj.runParallel(absolute_directory_path, sample_size)

def runTwoJobsParallel(absolute_directory_path, sample_size):
    fileRunnerObj = FileRunner() 
    return fileRunnerObj.runTwoJobsParallel(absolute_directory_path, sample_size)

def runConcurrent(absolute_directory_path, sample_size):
    fileRunnerObj = FileRunner() 
    return fileRunnerObj.runConcurrent(absolute_directory_path, sample_size) 

def runAllJobs(absolute_directory_path):
    fileRunnerObj = FileRunner() 
    return fileRunnerObj.runParallel(absolute_directory_path)

def saveDf(df):
    # saves to current repository
    df.to_csv('save.csv')

# running driver.py script directly
if __name__ == "__main__":
    # == demo data == 
    # path ='/Users/hughsignoriello/Desktop/Automated_Hvf_Grading/faultyFields'
    path = '/Users/hughsignoriello/Desktop/Automated_Hvf_Grading/singleField'
    sample_size = 10
    patient_id = "0034527.9"
    selected_eye = "Right"

    dfObj  = runParallel(path, sample_size)
  
    printDf(dfObj.df)
    
    #selecting patient via filterByID or filterByName
    patientDfObj = filterDFByID(dfObj, patient_id)

    analysis_df = Analysis(dfObj, selected_eye)

    printDf(analysis_df)

    
    

    
    
    
    