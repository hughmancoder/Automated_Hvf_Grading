import sys
import os
import numpy as np
import pandas as pd
# from automated_hvf_grading import extractHVFData

# from automated_hvf_grading import processData

# from automated_hvf_grading import dataFrame

# imports
from IPython.display import display # displaying dataframe
from multiprocessing import cpu_count

# dependencies
from automated_hvf_grading.fileRunner import FileRunner
from automated_hvf_grading.user import User
from automated_hvf_grading.dataFrame import DataFrame

# filter df by certain properties
def sortDataFrameByID(dfObject):
    return dfObject.sortByID(dfObject)

# def filterProperties(eye_to_filter):
#     # filter pdf properties
#     patient_id = "0034527.9"
#     # patient_data_frame = dataFrameObject.sortByID(patient_id)
#     patient_data_frame = dataFrameObject.df
#     patient_data_frame_right_eye = dataFrameObject.filterByEye(patient_data_frame, "Right")
#     display(patient_data_frame_right_eye)

#     progression_df = dataFrameObject.progressorCriteria(patient_data_frame_right_eye, "Right")
#     display(progression_df)
    
if __name__ == "__main__":
    # == demo == 
    absolute_folder_path = '/Users/hughsignoriello/Desktop/Automated_Hvf_Grading/singleField'
    sample_size = 10

    fileRunnerObj = FileRunner() 
    # fileRunnerObj.runConcurrent(absolute_folder_path, sample_size) # sample size is optional
    # dataFrameObj = fileRunnerObj.runParallel(absolute_folder_path, sample_size)
    
    # dataFrameObj = fileRunnerObj.runParallel(absolute_folder_path) # runs all jobs
    dataFrameObj = fileRunnerObj.runTwoJobsParallel(absolute_folder_path, sample_size)
    df = dataFrameObj.df
    pd.set_option("display.max_columns", len(df.columns)) # full width of res dataframe
    display(df)
    
    