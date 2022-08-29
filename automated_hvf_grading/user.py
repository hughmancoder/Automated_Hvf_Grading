# used to store patient data during extraction
class User:
    def __init__(self):
        self.filename = "unknown"
        self.name = "unknown"
        self.dob = "unknown"
        self.id = "unknown"
        self.eye = "unknown"
        self.test_date = "unknown"
        self.pattern_deviation_matrix = []
        self.rx = "unknown"
    
        self.vfi = "unknown"
        self.ght = "unknown"

        self.md_perc = "unknown"
        self.md_db = "unknown"

        self.psd_perc = "unknown"
        self.psd_db = "unknown"

        self.false_pos = "unknown"
        self.false_neg = "unknown"

        self.fixation_loss = "unknown"
        self.reliable = "unknown" # determined by false_pos and fixation_loss values
        self.field_size = "unknown"
        self.algorithm_criteria = "unknown" # category 2 or 3 as specified
        
        
        self.error = False # unreliable due to error in extracting values
        
        self.UL = False
        self.LL = False
        self.UM = False
        self.UC = False
        self.LC = False
        self.LM = False
        self.UR = False
        self.LR = False
        
        self.is_abnormal = "unknown"

        
