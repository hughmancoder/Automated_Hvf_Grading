import math
import time
import importlib
import os

# == dependencies == 
from automated_hvf_grading.extractHVFData import ExtractHVFData
from automated_hvf_grading.filterData import FilterData
from joblib import Parallel, delayed
from automated_hvf_grading.hvfAlgorithm import HVFAlgorithm
# from driver import RunFiles
# from filterData import filterData
# from AnalyseData import AnalyseProgression
# from algorithm import HVFAlgorithm

class ProcessFiles:

    def runFile(self, filepath): # Refactor
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
        error = False
        
        patient_list = ["Error"] * 23
        # varible to keep track of error in extraction (don't append to df if error is true)
        
        temp_dictionary["FILENAME"] = os.path.basename(filepath)

        mat = ExtractHVFData.readFile(filepath, temp_dictionary)

        if len(mat) == 0:
            patient_list[0] = os.path.basename(filepath)
            print("Error: matrix is empty data not extracted")
            return patient_list

        # formats percentage levels and flips matrix for L eye
        mat = FilterData.ProcessMatrix(mat, temp_dictionary["EYE"])
        psd = temp_dictionary["PSD_db"]
        if psd == "error":
            psd = 1e8  # pad with big number to exceed bounds

        eye = temp_dictionary["EYE"]
        rel = temp_dictionary["RELIABLE"]
        regSize = temp_dictionary["SIZE"]
        crit = FilterData.CheckCriteria(psd, temp_dictionary["GHT"])
        
        try:
            (region_list, result) = HVFAlgorithm.runAlgorithm(
                mat, regSize, rel, crit, eye)     
            importlib.reload(HVFAlgorithm.algorithm) # needed to sync cached variables with new inputs (may not be needed)
            patient_list = FilterData.formatList(region_list, crit, result, temp_dictionary)
        except Exception as e:
            print("Error: error running algorithm: " + e)

        return patient_list

    def runParallel(self, path_array):
        data = Parallel(n_jobs=-2)(delayed(self.runFile)(path) for path in path_array)
        return data

    # == for non-concurrent events == 

    def runFirstFile(self, path_array):
        print("running linear...")
        data = self.runFile(path_array[1])
        return data;
        
    def runLinear(self, path_array):
        """Run Linear

        Args:
            path_array (array): Array of File Paths

        Returns:
            array: Array of Data
        """
        print("running linear...")
        data = Parallel(n_jobs=-1)(delayed(self.runFile)(path) for path in path_array)
        return data # data in an array 
        
