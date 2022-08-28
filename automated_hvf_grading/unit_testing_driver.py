
import sys
import os
from extractHVFData import ExtractHVFData

# == testing matrix extraction ==
extractor = ExtractHVFData()
paths = extractor.getSingleFieldPaths(1)

print(paths[0])
path = "/Users/hughsignoriello/Desktop/automated-hvf-grading/singleField/a.pdf"

"""
for path in paths:
    matrix = extractor.extractMatrix(path)
"""
matrix = extractor.extractMatrix(path)
print(matrix)
