# == hvf library imports
from hvf_extraction_script.hvf_manager.hvf_export import Hvf_Export
from hvf_extraction_script.hvf_data.hvf_object import Hvf_Object
from hvf_extraction_script.utilities.file_utils import File_Utils

# import User
from automated_hvf_grading.processData import ProcessData
from pdf2image import convert_from_path
import os
import cv2
import pathlib  # pathy
import numpy as np

class ExtractHVFData:
    def __init__(self):
        pass

    @staticmethod
    def read_image_from_pdf(file_path):
        pdf = convert_from_path(file_path, single_file=True)
        cv_image = np.array(pdf[0]) 
        return cv_image[:, :, ::-1]
    
    @staticmethod
    def LevelToPercentage(value):
        if value == "5":
            return 5
        elif value == "2":
            return 2
        elif value == "1": 
            return 1
        elif value == "x":
            return 0.5
        else: # handles "."
            return "0"

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
                    hvf_img = self.read_image_from_pdf(file_path)
            else:
                hvf_img = File_Utils.read_image_from_file(file_path)

            # convert to json format 
            hvf_obj = Hvf_Object.get_hvf_object_from_image(hvf_img)
            serialized_string = hvf_obj.serialize_to_json();

        except Exception as e:
            print("Error: file not extractable", e)
            return user

        user = self.extractMetadata(user, hvf_obj)

        arr_obj = hvf_obj.pat_dev_percentile_array
        plot_object = arr_obj.plot_array
        rows, cols = plot_object.shape

        # shows matrix extraction as a string
        # print(hvf_obj.get_display_pat_perc_plot_string())

        # square irregular matrix by padding with zero
        matrix = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                # matrix[r, c] = self.LevelToPercentage(int(plot_object[r, c].get_enum()))
                # print(plot_object[r, c,].get_display_string())
                matrix[c,r] = self.LevelToPercentage(plot_object[r, c].get_display_string())

        user.matrix = matrix.tolist()
        return user
        
    def getSingleFieldPaths(self, size):
        """generates specified list of absolute paths from singleField samples
            may not work if not run outside of of module

        Args:
            sample size

        Returns:
            list of absolute file paths
        """
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

    def extractMetadata(self, user, hvf_obj):
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
            print("Error: unable to read client name or dob due to anonymized image", e)
        
        try:
            user.id =  hvf_obj.metadata[Hvf_Object.KEYLABEL_ID]
            user.field_size = hvf_obj.metadata[Hvf_Object.KEYLABEL_FIELD_SIZE]
            user.test_date = ProcessData.convDateFormat(hvf_obj.metadata[Hvf_Object.KEYLABEL_TEST_DATE])
            user.eye = hvf_obj.metadata[Hvf_Object.KEYLABEL_LATERALITY]
        except:
            print("Error: Invalid inputs")

        try:
            user.ght = hvf_obj.metadata[Hvf_Object.KEYLABEL_GHT].replace(" ", "") # remove whitespace
        except Exception as e:
            print("Error: ght unable to be extracted" + str(e))

        try:
            user.md_db = hvf_obj.metadata[Hvf_Object.KEYLABEL_MD]
            user.pdf_db = hvf_obj.metadata[Hvf_Object.KEYLABEL_PSD]
        except:
            print("Error: metadata db statistics not able to be extracted")

        try:
            user.rx = hvf_obj.metadata[Hvf_Object.KEYLABEL_RX]
            user.vfi = hvf_obj.metadata[Hvf_Object.KEYLABEL_VFI]
        except Exception as e:
            print("Error: rx and/or vfi no extractable")

        try:
            user.md_perc = hvf_obj.metadata[Hvf_Object.KEYLABEL_MDP]
            user.psd_perc = hvf_obj.metadata[Hvf_Object.KEYLABEL_PSDP]
        except Exception as e:
            print("Error: metadata % statistics not able to be extracted" + str(e))

        try:
            user.false_neg = int(hvf_obj.metadata[Hvf_Object.KEYLABEL_FALSE_NEG].rstrip("%"))
            user.false_pos = int(hvf_obj.metadata[Hvf_Object.KEYLABEL_FALSE_POS].rstrip("%"))
            numerator, denominator = hvf_obj.metadata[Hvf_Object.KEYLABEL_FIXATION_LOSS].split("/")
            user.fixation_loss = round((int(numerator) / int(denominator)) * 100, 2)  # convert to %
        except Exception as e:
            print("Error: metadata extraction" + str(e))

        # check if statistical values are reliable
        user.reliable = self.checkReliability(user.false_pos, user.fixation_loss, user.false_neg)
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

    
