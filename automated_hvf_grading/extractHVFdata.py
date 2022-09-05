# == hvf library imports
from hvf_extraction_script.hvf_data.hvf_object import Hvf_Object
from hvf_extraction_script.utilities.file_utils import File_Utils

# import User
from automated_hvf_grading.processData import ProcessData
import numpy as np

from automated_hvf_grading.user import User

class ExtractHVFData:
    def __init__(self):
        pass
    
    @staticmethod
    def levelToPercentage(value):
        if value == "5":
            return 5
        elif value == "2":
            return 2
        elif value == "1": 
            return 1
        elif value == "x":
            return 0.5
        else: # handles "."
            return 0

    def extractData(self, file_path, user):
        """takes in a png image path or pdf path and returns extracted hvf 
            pattern deviation matrix and medatadata which is updated in user object
            
        
        Args:
            file_path (string)
            user (object containing patient data)

        Returns:
            user object
        """
        try:
            if file_path.endswith(".pdf"):
                print(file_path)
                hvf_img = File_Utils.read_image_from_pdf(file_path)
            else:
                hvf_img = File_Utils.read_image_from_file(file_path)

            # convert to json format 
            hvf_obj = Hvf_Object.get_hvf_object_from_image(hvf_img)
            
        except Exception as e:
            print("Error: file not extractable:", e)
            return user

        user = self.extractMetadata(user, hvf_obj)

        arr_obj = hvf_obj.pat_dev_percentile_array
        plot_object = arr_obj.plot_array
        rows, cols = plot_object.shape
        
        """
        # show extractable figures as json (Hack)
        print(hvf_obj.serialize_to_json());
        # shows matrix extraction as a string
        serialized_string = hvf_obj.serialize_to_json();
        print(hvf_obj.get_display_pat_perc_plot_string())
        """

        try:
            # square irregular matrix by padding with zero
            matrix = np.zeros((rows, cols))
            for r in range(rows):
                for c in range(cols):
                    matrix[c,r] = self.levelToPercentage(plot_object[r, c].get_display_string())

            user.pattern_deviation_matrix = matrix.tolist()
        except Exception as e:
            print("Error: matrix cannot be extracted due to errors in hvf_extraction_script (supporting library: https://github.com/msaifee786/hvf_extraction_script)")
        
        return user
        
    def extractMetadata(self, user: User, hvf_obj):
        """updates user meta data in user object from hvf object

        Args:
            user (object)

        Returns:
            updated user object
        """
        try:
            user.name = hvf_obj.metadata[Hvf_Object.KEYLABEL_NAME]
            user.dob = hvf_obj.metadata[Hvf_Object.KEYLABEL_DOB]
        except Exception as e:
            print("Error: unable to read client name or dob due to anonymized image ", e)
        
        try:
            user.eye = hvf_obj.metadata[Hvf_Object.KEYLABEL_LATERALITY]
        except Exception as e:
            user.error = True
            print("Error: cannot determine eye" + str(e))

        try:
            user.strategy = hvf_obj.metadata[Hvf_Object.KEYLABEL_STRATEGY]
            user.fovea = hvf_obj.metadata[Hvf_Object.KEYLABEL_FOVEA]
            user.layout_version = hvf_obj.metadata[Hvf_Object.KEYLABEL_LAYOUT]    
        except Exception as e:
            print("Error: " + str(e))

        try:
            user.id =  hvf_obj.metadata[Hvf_Object.KEYLABEL_ID]
        except Exception as e:
            print("Error: invalid ID " + str(e))

        try:
            user.test_date = ProcessData.convDateFormat(hvf_obj.metadata[Hvf_Object.KEYLABEL_TEST_DATE])
        except Exception as e:
            print("Error: date unable to be determined " + str(e))

        try:
            user.field_size = hvf_obj.metadata[Hvf_Object.KEYLABEL_FIELD_SIZE]
        except Exception as e:
            print("Error: field size unable to be determined " + str(e))

        try:
            user.ght = hvf_obj.metadata[Hvf_Object.KEYLABEL_GHT].replace(" ", "") # remove whitespace
        except Exception as e:
            print("Error: ght unable to be extracted " + str(e))

        try:
            user.md_db = hvf_obj.metadata[Hvf_Object.KEYLABEL_MD]
            user.psd_db = hvf_obj.metadata[Hvf_Object.KEYLABEL_PSD].replace(":", "")
        except:
            print("Error: metadata db statistics not able to be extracted")

        try:
            user.rx = hvf_obj.metadata[Hvf_Object.KEYLABEL_RX]

            vfi = hvf_obj.metadata[Hvf_Object.KEYLABEL_VFI]
            if len(vfi) >= 4 and vfi[:4] == "24-2":
                user.vfi_24_2 = vfi[5:]
                # user.vfi = "N/A"
            else:
                user.vfi = vfi.replace(":","")
                # user.vfi_24_2 = "N/A"

        except Exception as e:
            print("Error: rx and/or vfi not extractable " + str(e))

        try:
            user.md_perc = hvf_obj.metadata[Hvf_Object.KEYLABEL_MDP]
        except Exception as e:
            print("Error: metadata md % not able to be extracted " + str(e))

        try:
            user.psd_perc = hvf_obj.metadata[Hvf_Object.KEYLABEL_PSDP]
        except Exception as e:
            print("Error: metadata psd % not able to be extracted " + str(e))

        try:
            user.false_neg_perc = int(hvf_obj.metadata[Hvf_Object.KEYLABEL_FALSE_NEG].rstrip("%"))
            user.false_pos_perc = int(hvf_obj.metadata[Hvf_Object.KEYLABEL_FALSE_POS].rstrip("%"))
            numerator, denominator = hvf_obj.metadata[Hvf_Object.KEYLABEL_FIXATION_LOSS].split("/")
            user.fixation_loss = round((int(numerator) / int(denominator)) * 100, 2)  # convert to %
        except Exception as e:
            print("Error: metadata extraction " + str(e))

        # other extractable data
        """
        KEYLABEL_STRATEGY
        KEYLABEL_TEST_DURATION
        KEYLABEL_PUPIL_DIAMETER
        KEYLABEL_LATERALITY
        KEYLABEL_FOVEA
        """

        # check if statistical values are reliable
        user.reliable = self.checkReliability(user.false_pos_perc, user.fixation_loss, user.false_neg_perc)
        return user

    @staticmethod
    def checkReliability(fpos, fixation_loss, fneg): 
        reliable = False # unreliable unless otherwise proven true
        try:
            if float(fixation_loss) < 33 and float(fpos) < 33 and float(fneg) < 33:
                reliable = True
        except:
            print("Error: insufficient fixation loss and fpos extraction to determine reliablility")

        return reliable

"""
def getSingleFieldPaths(self, size):
    # may only work in development environment
    if __name__ == '__main__':
        print("Environment error: this function only works when run same path as module")
        absolute_path = os.path.abspath("..") + "/singleField"            
        file_batches = os.walk('../singleField')
    else:
        absolute_path = os.path.dirname(os.path.abspath(__file__)) + "/../singleField"
        # absolute_path = os.path.abspath() 
        file_batches = os.walk('/singleField')
        if not os.path.exists(absolute_path):
            print(f"Error: {absolute_path} does not existpath does not exist")
            return []
    try:
        files = os.listdir(absolute_path)
        if size < len(files):
            return [absolute_path + "/" + f for f in files][:size]
        else:
            print("Error: sample size larger than number of files")
    except Exception as e:
        print("Error:", e)
        return []
"""