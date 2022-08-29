
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
pd.set_option("display.max_rows", None, "display.max_columns", None)



# testing data frame initialisation
user = user.User()
data_frame = dataFrame.DataFrame(user)
data_frame.addData(user)
display(data_frame.df)
# testing data frame addition


# testing data frame features
"""
c = [1,2,3]
dict = {1: 'b', 2:'c', 3:'d'}
dict1 = {1: 'd', 2:'a', 3:'d'}
output = pd.DataFrame(columns = c)
output = output.append(dict, ignore_index=True)
output = output.append(dict1, ignore_index=True)
print(output.head())
"""

# testing extraction
"""
extractor = extractHVFData.ExtractHVFData()
paths = extractor.getSingleFieldPaths(1)
FileProcesser = processFiles.ProcessFiles() # create processor object
for path in paths: 
    user = FileProcesser.runFile(path, user)
    data_frame.addData(user)

print(data_frame.getObjectValues(user))
display(data_frame.df)
"""

# testing user object
"""
user = user.User()
attributes = [a for a in dir(user) if not a.startswith('__')]
print(vars(user)) # unpacking object attributes
"""

# testing file path extraction
"""
extractor = extractHVFData.ExtractHVFData()
paths = extractor.getSingleFieldPaths(1)
print(paths[0])
"""

# testing errorSample from email
"""
pdf_path = '/Users/hughsignoriello/Desktop/Automated_Hvf_Grading/singleField/errorSample.pdf'
FileProcesser = processFiles.ProcessFiles() # create processor object
user = FileProcesser.runFile(pdf_path, user)
print(user.abnormal_regions)
print(user.criteria)
print(user.eye)
processData.ProcessData.PrintMatrix(user.pattern_deviation_matrix)
"""
              
# testing errorpdf extraction
"""
user = extractor.extractData(pdf_path, user)
attributes = [a for a in dir(user) if not a.startswith('__')]
print(vars(user))

processData.ProcessData.PrintMatrix(user.pattern_deviation_matrix)
"""

# testing bulk processing
"""
for path in paths:
    matrix = extractor.extractMatrix(path)

user = extractor.extractData(left_path, user)
mat = user.matrix
print(user.reliable)
print(user.eye)
processData.ProcessData.PrintMatrix(mat)
"""

# testing bounds
"""
region_map_20_left = {  
            "UL": (1, 2, 2, 4),
            "LL": (1, 5, 2, 7),
            "UM": (3, 2, 6, 3),  
            "UC": (3, 3, 6, 4),
            "LC": (3, 5, 6, 6),
            "LM": (3, 6, 6, 8),
            "UR": (7, 2, 9, 4),
            "LR": (7, 5, 9, 7)
}
region_map_20_right = {  
            "UL": (0, 2, 2, 4),  
            "LL": (0, 5, 2, 7),
            "UM": (3, 2, 6, 3),  
            "UC": (3, 3, 6, 4),
            "LC": (3, 5, 6, 6),
            "LM": (3, 6, 6, 8),
            "UR": (7, 2, 8, 4),
            "LR": (7, 5, 8, 7)
        }


m = np.zeros((10, 10)).tolist()

for region, coords in region_map_20_right.items():
    ux, uy, lx ,ly = coords
    for r in range(uy, ly + 1):
        for c in range(ux, lx + 1):
            m[r][c] = str(region) + ' '

processData.ProcessData.PrintMatrix(m)
"""
