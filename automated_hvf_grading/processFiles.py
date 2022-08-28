import math
import time
import importlib
import os

# == dependencies == 
from automated_hvf_grading.extractHVFData import ExtractHVFData
from automated_hvf_grading.processData import processData
from joblib import Parallel, delayed
from automated_hvf_grading.hvfAlgorithm import HVFAlgorithm

class ProcessFiles:
    def runFile(self, file_path, user):
        """driver to the program, runs a single sample and calls functions

        Args:
            file_path (path string)
            user (object): contains metadata grouped into one object

        Returns:
            user (object): updated
        """
        # updating data into user object
        user.file_path = file_path
        user.filename = os.path.basename(file_path)

        # update matrix and meta data
        user = ExtractHVFData.extractData(file_path, user)

        if user.pattern_deviation_matrix == "unknown":
            print("Error: cannot run algorithm as matrix is not extractable")
            user.error = True
            return user

        if user.eye == "Left":
            user.matrix = processData.mirrorYAxis(user.matrix)
        elif user.eye != "Right": 
            user.error = True
            print("Error: unable to distinguish if eye is left or right")

        user = processData.DetermineCriteria(user)
        
        try:
            Algorithm = HVFAlgorithm(user.pattern_deviation_matrix, user.eye, user.criteria)
            user.abnormal_regions = Algorithm.run()
        except Exception as e:
            print("Error: unable to run algorithm", str(e))
            user.error = True

        # check result of abnormal regions
        is_abnormal = False
        for region, abnormal in user.abnormal_regions.items()
            if abnormal:
                is_abnormal = True
                break
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
        
