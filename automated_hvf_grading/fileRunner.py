# == imports == 
from asyncio import constants
from ctypes import Array
import os
from joblib import Parallel, delayed
import joblib.parallel
import math
import time
import pandas as pd

# == dependencies == 
from automated_hvf_grading.extractHVFdata import ExtractHVFData
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
        """driver to the program, runs a single file and calls functions

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
    
    def runCustomParallel(self, path_array: Array, n_jobs: int, sample_size = False):
        """Runs files in path array using provided n_jobs

        Args:
            path_array (_type_): array of file paths
            n_jobs (_type_): Joblib n_jobs parameter
            sample_size (bool, optional): Sample of files to process. Defaults to False.

        Returns:
            _type_: dataFrame object
        """

        # check valid sample size        
        if sample_size > len(path_array):
            sample_size = len(path_array)

        if sample_size != False:
            path_array = FileRunner.getSamplesFromPathArray(path_array, sample_size)
        
        if len(path_array) <= 0:
            print("Info: no files to read")
            return None
        
        total_n_jobs = len(path_array)
        
        class BatchCompletionCallBack(object):
            def __init__(self, dispatch_timestamp, batch_size, parallel):
                self.dispatch_timestamp = dispatch_timestamp
                self.batch_size = batch_size
                self.parallel = parallel

            def __call__(self, out):
                self.parallel.n_completed_tasks += self.batch_size
                this_batch_duration = time.time() - self.dispatch_timestamp

                self.parallel._backend.batch_completed(self.batch_size,
                                                this_batch_duration)
                self.parallel.print_progress()
                # Added code - start
                progress = math.trunc((self.parallel.n_completed_tasks / total_n_jobs) * 100)
                print("Progress: {}".format(progress))

                time_remaining = math.trunc((this_batch_duration / self.batch_size) * (total_n_jobs - self.parallel.n_completed_tasks))
                print( "ETA: {}s".format(time_remaining/60))
                # Added code - end
                if self.parallel._original_iterator is not None:
                    self.parallel.dispatch_next()
                    
        joblib.parallel.BatchCompletionCallBack = BatchCompletionCallBack

        user_objects = [User() for i in range(len(path_array))]
        dataFrameObj = DataFrame(user_objects[0])

        print(f"Info: Processing {total_n_jobs} files")

        user_objects = Parallel(n_jobs = n_jobs)(delayed(self.runFile)(file_path, user_objects[i]) for i, file_path in enumerate(path_array))
    
        # update data frame
        for userObj in user_objects:
            dataFrameObj.addData(userObj)

        return dataFrameObj
    
    def runCustomParallelAnalysis(self, n_jobs, df, ids, eye):
        """Runs 

        Args:
            n_jobs (_type_): Joblib n_jobs parameter

        Returns:
            _type_: dataFrame object
        """
        
        total_n_jobs = len(ids)
        
        class BatchCompletionCallBack(object):
            def __init__(self, dispatch_timestamp, batch_size, parallel):
                self.dispatch_timestamp = dispatch_timestamp
                self.batch_size = batch_size
                self.parallel = parallel

            def __call__(self, out):
                self.parallel.n_completed_tasks += self.batch_size
                this_batch_duration = time.time() - self.dispatch_timestamp

                self.parallel._backend.batch_completed(self.batch_size,
                                                this_batch_duration)
                self.parallel.print_progress()
                # Added code - start
                progress = math.trunc((self.parallel.n_completed_tasks / total_n_jobs) * 100)
                print("Progress: {}".format(progress))

                time_remaining = math.trunc((this_batch_duration / self.batch_size) * (total_n_jobs - self.parallel.n_completed_tasks))
                print( "ETA: {}s".format(time_remaining/60))
                # Added code - end
                if self.parallel._original_iterator is not None:
                    self.parallel.dispatch_next()
                    
        joblib.parallel.BatchCompletionCallBack = BatchCompletionCallBack
        
        sliced_dfs = Parallel(n_jobs=n_jobs, prefer="threads")(delayed(DataFrame.progressorCriteria_df)(df, eye, i) for i in ids)
        # update data frame
        

        return pd.concat(sliced_dfs, ignore_index=True)