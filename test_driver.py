
import sys
import os
from automated_hvf_grading import extractHVFData
from automated_hvf_grading import user
from automated_hvf_grading import processData

# testing user object
user = user.User()

# testing extractMatrix
extractor = extractHVFData.ExtractHVFData()
paths = extractor.getSingleFieldPaths(1)
print(paths[0])
right_path = "0/Users/hughsignoriello/Desktop/automated_hvf_grading/automated_hvf_grading/../singleField/a.pdf"
left_path = "/Users/hughsignoriello/Desktop/automated_hvf_grading/automated_hvf_grading/../singleField/2.pdf"
# """
# for path in paths:
#     matrix = extractor.extractMatrix(path)
# """
# user = extractor.extractData(left_path, user)
# mat = user.matrix
# print(user.reliable)
# print(user.eye)
# processData.ProcessData.PrintMatrix(mat)

# == test bounds == 

region_map_20_left = {  
            "UL": (1, 2, 2, 4),
            "LL": (1, 5, 2, 7),
            "UM": (2, 2, 5, 3),  # asymmetric UM region
            "UC": (3, 3, 6, 4),
            "LC": (3, 5, 6, 6),
            "LM": (2, 6, 5, 8),
            "UR": (7, 2, 9, 4),
            "LR": (7, 5, 9, 7)
}

region_map_20_right = {  
            "UL": (0, 2, 2, 4),  
            "LL": (0, 5, 2, 7),
            "UM": (3, 2, 6, 3),  # asymmetric UM region as uy is 2 instead of 1
            "UC": (3, 3, 6, 4),
            "LC": (3, 5, 6, 6),
            "LM": (3, 6, 6, 8),
            "UR": (7, 2, 8, 4),
            "LR": (7, 5, 8, 7)
        }

import numpy as np
m = np.zeros((10, 10)).tolist()

for region, coords in region_map_20_right.items():
    ux, uy, lx ,ly = coords
    for r in range(uy, ly + 1):
        for c in range(ux, lx + 1):
            m[r][c] = str(region) + ' '

processData.ProcessData.PrintMatrix(m)