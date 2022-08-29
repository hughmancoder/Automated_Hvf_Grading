import sys
import os
import numpy as np
import pandas as pd
from automated_hvf_grading import extractHVFData
from automated_hvf_grading import user
from automated_hvf_grading import processData
from automated_hvf_grading import processFiles
from automated_hvf_grading import dataFrame
from IPython.display import display # displaying dataframe

# create data_frame
user = user.User()
dataFrameObject = dataFrame.DataFrame(user)

# extract files
extractor = extractHVFData.ExtractHVFData()
paths = extractor.getSingleFieldPaths(4)
fileProcesser = processFiles.ProcessFiles() # create processor object
for path in paths: 
    user = fileProcesser.runFile(path, user)
    dataFrameObject.addData(user)

display(dataFrameObject.df)

# filter pdf properties
patient_id = "0034527.9"
# patient_data_frame = dataFrameObject.sortByID(patient_id)
patient_data_frame = dataFrameObject.df
patient_data_frame_right_eye = dataFrameObject.filterByEye(patient_data_frame, "Right")
display(patient_data_frame_right_eye)

progression_df = dataFrameObject.progressorCriteria(patient_data_frame_right_eye, "Right")
display(progression_df)