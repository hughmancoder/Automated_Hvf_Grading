# == imports == 
import math
import time
import importlib
import os
from xml.etree.ElementInclude import LimitedRecursiveIncludeError
from joblib import Parallel, delayed
from multiprocessing import cpu_count # used to asses number of cpu cores

# == dependencies == 
from automated_hvf_grading.extractHVFData import ExtractHVFData
from automated_hvf_grading.processData import ProcessData
from automated_hvf_grading.hvfAlgorithm import HVFAlgorithm
from automated_hvf_grading.user import User
from automated_hvf_grading.dataFrame import DataFrame


class FileRunner:
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
            return list(FileRunner.absoluteFilePaths(absolute_directory_path)) # generator to list
    
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

    def runConcurrent(self, absolute_directory_path, sample_size = False):
        """runs jobs in path array one at a time 
            returns extracted dataFrame object with processed Files

        Args:
            absolute_directory_path (string): folder file path containing hvf samples
            sample_size (optional parameter)

        Returns:
            dataFrame object
        """
        # extract file paths 
        path_array = FileRunner.getPathArray(absolute_directory_path)

        # generate sample size
        if sample_size != False:
            path_array = FileRunner.getSamplesFromPathArray(path_array, sample_size)

        if len(path_array) <= 0:
            print("Info: no files to read")
            return None

        print("sampled array: ", path_array)

        # create objects 
        userObj = User()
        dataFrameObj = DataFrame(userObj)
        

        for file_path in path_array:
            userObj.resetValues() # reset object attributes rather than creating a new object
            userObj = self.runFile(file_path, userObj)
            dataFrameObj.addData(userObj)

        return dataFrameObj

    def runTwoJobsParallel(self, absolute_directory_path, sample_size = False):
        """runs two jobs in parallel

        Returns:
            DataFrame object
        """
        path_array = FileRunner.getPathArray(absolute_directory_path)

        if sample_size != False:
            path_array = FileRunner.getSamplesFromPathArray(path_array, sample_size)

        if len(path_array) <= 0:
            print("Info: no files to read")
            return None

        user_objects = [User() for i in range(len(path_array))]
        dataFrameObj = DataFrame(user_objects[0])

        print(f"Info: running jobs in parallel on 2 logical cores")

        user_objects = Parallel(n_jobs=-2)(delayed(self.runFile)(file_path, user_objects[i]) for i, file_path in enumerate(path_array))
    
        # update data frame
        for userObj in user_objects:
            dataFrameObj.addData(userObj)

        return dataFrameObj

    def runParallel(self, absolute_directory_path, sample_size = False):
        """runs as many jobs simultaneously as system will allow by counting the number of cpu cores
        Args:
            absolute_directory_path
            sample_size (bool, optional): generate sub array of sample_size

        Returns: DataFrame object
        """

        path_array = FileRunner.getPathArray(absolute_directory_path)

        if sample_size != False:
            path_array = FileRunner.getSamplesFromPathArray(path_array, sample_size)

        if len(path_array) <= 0:
            print("Info: no files to read")
            return None

        n_logical_cores = cpu_count() # get the number of logical cpu cores on computer
        print(f"Info: running jobs in parallel on {n_logical_cores} logical cores")

        user_objects = [User() for i in range(len(path_array))]
        dataFrameObj = DataFrame(user_objects[0])

        # passes by reference
        Parallel(n_jobs=-n_logical_cores)(delayed(self.runFile)(file_path, user_objects[i])for i, file_path in enumerate(path_array))

        for userObj in user_objects:
            dataFrameObj.addData(userObj)

        return dataFrameObj
        
