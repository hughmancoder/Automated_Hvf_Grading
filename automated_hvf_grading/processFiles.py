import math
import time
import importlib
import os

# == dependencies == 
from automated_hvf_grading.extractHVFData import ExtractHVFData
from automated_hvf_grading.processData import ProcessData
from joblib import Parallel, delayed
from multiprocessing import cpu_count # used to asses number of cpu cores
from automated_hvf_grading.hvfAlgorithm import HVFAlgorithm


class ProcessFiles:
    def __init__(self):
        # instantiating objects
        self.extractor = ExtractHVFData()

    @staticmethod
    def absoluteFilePaths(directory):
        for dirpath,_,filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f)) # returns generator

    @staticmethod
    def getPathArray(absolute_directory_path):
        """takes in directory path and returns path array of all files paths in givendirectory

        Args:
            absolute_directory_path (string)

        Returns:
            list of file paths
        """
        if os.path.exists(absolute_directory_path):
            # files = os.listdir(absolute_folder_path) # show list of files
            return list(ProcessFiles.absoluteFilePaths(absolute_directory_path)) # generator to list
    
    @staticmethod
    def getSamplesFromPathArray(path_array, sample_size):
        if sample_size <= len(path_array):
            return path_array[:sample_size]
        return path_array        

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

        if user.pattern_deviation_matrix == "N/A":
            print("Error: cannot run algorithm as matrix is not extractable")
            user.error = True
            return user

        if user.eye == "Left":
            user.pattern_deviation_matrix = ProcessData.mirrorYAxis(user.pattern_deviation_matrix)
        elif user.eye != "Right": 
            user.error = True
            print("Error: unable to distinguish if eye is left or right")

        # print(vars(user))
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


    # def runConcurrent(self, path_array):
    #     """runs jobs in path array

    #         returns extracted dataFrame object with processed Files
    #     """
    #     # == extract file paths == 
    #     file_paths = self.extractor.getFieldPaths(folder_path, sample_size)

    #     # == create objects ==
    #     userObj = User()
    #     dataFrameObject = dataFrame.DataFrame(userObj)
    #     fileProcesser = processFiles.ProcessFiles() # create processor object

    #     for i, path in enumerate(file_paths): 
    #         userObj.resetValues() # reset object data rather than creating a new object
    #         userObj = fileProcesser.runFile(path, userObj)
    #         dataFrameObject.addData(userObj)

    #     return dataFrameObject

    def runTwoJobsParallel(self, path_array):
        return Parallel(n_jobs=-2)(delayed(self.runFile)(path) for path in path_array)

    def runParallel(self, path_array):
        """runs as many jobs simultaneously as system will allow by counting the number of cpu cores
        """
        # get the number of logical cpu cores on computer
        n_logical_cores = cpu_count()
        return Parallel(n_jobs=-n_logical_cores)(delayed(self.runFile)(path) for path in path_array)

        
        

        
    def runLinear(self, path_array):
        """Runs concurrently: runs one file at a time
        Args:
            path_array (array): Array of File Paths
        Returns:
            array: Array of Data
        """
        data = Parallel(n_jobs=-1)(delayed(self.runFile)(path) for path in path_array)
        return data 
        
