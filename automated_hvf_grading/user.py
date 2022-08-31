# used to store patient data during extraction
class User:
    def __init__(self):
        self.resetValues()

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

        self.false_pos = "N/A"
        self.false_neg = "N/A"

        self.fixation_loss = "N/A"
        self.reliable = "N/A" # determined by false_pos and fixation_loss values
        self.field_size = "N/A"
        self.algorithm_criteria = "N/A" # category 2 or 3 as specified
        
        
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

    def getValues(self):
        return list(self.__dict__.values())

    
        
        