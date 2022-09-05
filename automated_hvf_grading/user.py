# used to store patient data during extraction

import numpy as np
class User:
    def __init__(self):
        self.resetValues()
        
    attributeToHumanReadableDict = {
        "filename": "Filename",
        "name": "Name",
        "dob": "DOB",
        "id": "ID",
        "eye": "Eye",
        "test_date": "Test Date",
        "pattern_deviation_matrix": "Pattern Deviation Matrix",
        "strategy": "Strategy",
        "fovea": "Fovea",
        "layout_version": "Layout Version",
        "rx": "Rx",
        "vfi_24_2": "VFI 24-2",
        "vfi": "VFI",
        "ght": "GHT",
        "md_perc": "MD %",
        "md_db": "MD dB",
        "psd_perc": "PSD %",
        "psd_db": "PSD dB",
        "false_pos_perc": "False Pos %",
        "false_neg_perc": "False Neg %",
        "fixation_loss_perc": "Fixation Loss %",
        "reliable": "Reliable",
        "field_size": "Field Size",
        "criteria": "Criteria",
        "error": "Error",
        "is_abnormal": "Is Abnormal?",
    }

    def resetValues(self):
        self.filename = "N/A"
        self.name = "N/A"
        self.dob = "N/A"
        self.id = "N/A"
        self.eye = "N/A" # laterality
        self.test_date = "N/A"
        self.pattern_deviation_matrix = []

        self.strategy = "N/A"
        self.fovea = "N/A"
        self.layout_version = "N/A"
    
        self.rx = "N/A"

        self.vfi_24_2 = "N/A"
        self.vfi = "N/A"
        self.ght = "N/A"


        self.md_perc = "N/A"
        self.md_db = "N/A"

        self.psd_perc = "N/A"
        self.psd_db = "N/A"

        self.false_pos_perc = "N/A"
        self.false_neg_perc = "N/A"

        self.fixation_loss_perc = "N/A"
        self.reliable = "N/A" # determined by false_pos and fixation_loss values
        self.field_size = "N/A"
        self.criteria = "N/A" # category 2 or 3 as specified
        
        
        self.error = False # unreliable due to error in extracting values
        
        self.UL = False
        self.LL = False
        self.UM = False
        self.UC = False
        self.LC = False
        self.LM = False
        self.UR = False
        self.LR = False
        
        self.is_abnormal = "N/A"

    
    def getDict(self):
        """returns a dictionary of both attributse and values
        """
        # function currently showing other python internal object properties which we don't want
        return dict(self.__dict__.items())

    def getAttributes(self):
        return list(self.__dict__.keys())
    
    def getAttributesHuman(self):
        # return list(self.attributeToHumanReadableDict[header] for header in self.__dict__.keys())
        sort_idx = np.argsort(self.attributeToHumanReadableDict.keys())
        idx = np.searchsorted(self.attributeToHumanReadableDict.keys(),self.__dict__.keys(),sorter = sort_idx)
        return np.asarray(self.attributeToHumanReadableDict.values())[sort_idx][idx].tolist()

    def getValues(self):
        return list(self.__dict__.values())

    
        
        