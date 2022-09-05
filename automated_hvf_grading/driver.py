# imports
import pandas as pd
from IPython.display import display # displaying dataframe

# dependencies
from automated_hvf_grading.fileRunner import FileRunner

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
def runParallel(file_paths, sample_size = False):
    """runs files and outputs dataFrame object
    """
    fileRunnerObj = FileRunner() 
    return fileRunnerObj.runCustomParallel(file_paths, -2, sample_size)

def runTwoJobsParallel(file_paths, sample_size = False):
    fileRunnerObj = FileRunner() 
    return fileRunnerObj.runCustomParallel(file_paths, 2, sample_size)

def runConcurrent(file_paths, sample_size = False):
    fileRunnerObj = FileRunner() 
    return fileRunnerObj.runCustomParallel(file_paths, 1, sample_size) 

def saveDf(df):
    # saves to current repository
    df.to_csv('save.csv')

    
    

    
    
    
    