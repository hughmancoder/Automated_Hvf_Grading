import math
import time
import importlib
import os

# == dependencies == 
from automated_hvf_grading.extractHVFData import ExtractHVFData
from automated_hvf_grading.processData import ProcessData
from joblib import Parallel, delayed
from automated_hvf_grading.hvfAlgorithm import HVFAlgorithm


class ProcessFiles:
    def __init__(self):
        # instantiating objects
        self.extractor = ExtractHVFData()

    def runFile(self, file_path, user):
        """driver to the program, runs a single sample and calls functions

        Args:
            file_path (path string)
            user (object): contains metadata grouped into one object

        Returns:
            user (object): updated
        """
        # check valid path first
        if os.path.exists(file_path) == False:
            print("Error: invalid file path")
            user.error = True
            return user
        
        user.filename = os.path.basename(file_path)
        user = self.extractor.extractData(file_path, user) # update matrix and meta data

        if user.pattern_deviation_matrix == "unknown":
            print("Error: cannot run algorithm as matrix is not extractable")
            user.error = True
            return user

        if user.eye == "Left":
            user.pattern_deviation_matrix = ProcessData.mirrorYAxis(user.pattern_deviation_matrix)
        elif user.eye != "Right": 
            user.error = True
            print("Error: unable to distinguish if eye is left or right")

        user = ProcessData.DetermineCriteria(user)
        
        try:
            Algorithm = HVFAlgorithm(user.pattern_deviation_matrix, user.eye, user.criteria)
            abnormal_regions = Algorithm.run()
        except Exception as e:
            print("Error: unable to run algorithm", str(e))
            user.error = True
            return user

        # check result of abnormal regions and update user dictionary
        is_abnormal = False
        for region, abnormal in abnormal_regions.items():
            setattr(user, region, abnormal)
            if abnormal:
                is_abnormal = True
        user.is_abnormal = is_abnormal

        return user

    def runParallel(self, path_array):
        data = Parallel(n_jobs=-2)(delayed(self.runFile)(path) for path in path_array)
        return data
        
    def runLinear(self, path_array):
        """Runs concurrently: runs one file at a time
        Args:
            path_array (array): Array of File Paths
        Returns:
            array: Array of Data
        """
        data = Parallel(n_jobs=-1)(delayed(self.runFile)(path) for path in path_array)
        return data 
        
