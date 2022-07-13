import math
import time
import importlib
import os

# == dependencies == 
from extractData import extractHVFData
from joblib import Parallel, delayed
from driver import RunFiles
from extractData import extractHVFData
from filterData import filterData
from AnalyseData import AnalyseProgression
from algorithm import HVFAlgorithm

class ParallelProcess:
    """
    def __init__(self, dispatch_timestamp, batch_size, parallel):
        self.dispatch_timestamp = dispatch_timestamp
        self.batch_size = batch_size
        self.parallel = parallel
        self.total_n_jobs = 0 # default value

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
        print( "ETA: {}s".format(time_remaining / 60))
        # Added code - end
        if self.parallel._original_iterator is not None:
            self.parallel.dispatch_next()
    """

    # == pulls all files together == 
    @staticmethod
    def RunFiles(filepath): 
        print("Info: Analysing " + filepath)
        temp_dictionary = {
            "FILENAME": "",
            "NAME": "",
            "DOB": "",
            "ID": "",
            "EYE": "",
            "SIZE": "",
            "DATE": "",
            "RX": "",
            "GHT": "",
            "VFI": "",
            "MD_%": "",
            "MD_db": "",
            "PSD_%": "",
            "PSD_db": "",
            "FALSE_POS": "",
            "FIXATION_LOSS": "",
            "RELIABLE": False,
        }
        patient_list = ["Error"] * 23
        # varible to keep track of error in extraction (don't append to df if error is true)
        error = False
        temp_dictionary["FILENAME"] = os.path.basename(filepath)

        mat = extractHVFData.readFile(filepath, temp_dictionary)

        if len(mat) == 0:
            patient_list[0] = os.path.basename(filepath)
            print("Error: matrix is empty data not extracted")
            return patient_list

        # formats percentage levels and flips matrix for L eye
        mat = filterData.ProcessMatrix(mat, temp_dictionary["EYE"])
        psd = temp_dictionary["PSD_db"]
        if psd == "error":
            psd = 1e8  # pad with big number to exceed bounds

        eye = temp_dictionary["EYE"]
        rel = temp_dictionary["RELIABLE"]
        regSize = temp_dictionary["SIZE"]
        crit = filterData.CheckCriteria(psd, temp_dictionary["GHT"])
        
        try:
            (region_list, result) = HVFAlgorithm.runAlgorithm(
                mat, regSize, rel, crit, eye)     
            importlib.reload(HVFAlgorithm.algorithm) # needed to sync cached variables with new inputs (may not be needed)
            patient_list = filterData.formatList(region_list, crit, result, temp_dictionary)
        except Exception as e:
            print("Error: error running algorithm: " + e)

        return patient_list

    def runParallel(self):
        # joblib.parallel.ParallelProcessing = ParallelProcessing
        path = extractHVFData.ExtractSingleFieldFilePath()
        path_array = filterData.FilePathToArray(path)  

        # == get sample == 
        #path_array_sample = filterData.FilePathSampleToArray(path, 12)  

        self.total_n_jobs = len(path_array)
        
        # runs two at a time (SPEED IMPROVEMENT: increase number from 2)
        data = Parallel(n_jobs=-2)(delayed(RunFiles)(path) for path in path_array)
        return data

    # == for non-concurrent events == 

    def runFirstFile(self):
        files_path = filterData.ExtractSingleFieldFilePath()
        path_array = filterData.FilePathToArray(files_path)
        firstPath = path_array[0] # get first item
        return RunFiles(firstPath) 
        
    def runLinear(self):
        print("running files...")
        files_path = filterData.ExtractSingleFieldFilePath()
        path_array = filterData.FilePathToArray(files_path)
        return [RunFiles(path) for path in path_array] # data in an array 
        
