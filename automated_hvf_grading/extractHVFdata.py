# == hvf library imports
from hvf_extraction_script.hvf_manager.hvf_export import Hvf_Export
from hvf_extraction_script.hvf_data.hvf_object import Hvf_Object
from hvf_extraction_script.utilities.file_utils import File_Utils

# == other imports ==
from pdf2image import convert_from_path
from PIL import Image  # pillow
import datetime
import os
import cv2
import pathlib  # pathy
import numpy as np

# == Note ==
# current class methods are static (for now) as we pass all function requisites as parameters


class ExtractHVFData:
    def __init__(self):
        print("extraction started")

    @staticmethod
    def read_image_from_pdf(file_path):
        pdf = convert_from_path(file_path, single_file=True)
        #pdf = convert_from_path(file_path, single_file=True, poppler_path="./src/poppler-0.68.0/bin")
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

    def extractMatrix(self, file_path):
        """takes in a png image path or pdf path and returns extracted hvf pattern deviation matrix 
            we can also extract all user data from hvf_obj json and any other needed user arrays
        
        Args:
            file_path (string)
            userData (object)

        Returns:
            matrix (list of lists)
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
            return []

        arr_obj = hvf_obj.pat_dev_percentile_array
        plot_object = arr_obj.plot_array
        rows, cols = plot_object.shape

        #shows matrix extraction as a string
        print(hvf_obj.get_display_pat_perc_plot_string())

        # square irregular matrix by padding with zero
        matrix = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                # matrix[r, c] = self.LevelToPercentage(int(plot_object[r, c].get_enum()))
                # print(plot_object[r, c,].get_display_string())
                matrix[c,r] = self.LevelToPercentage(plot_object[r, c].get_display_string())
        return matrix.tolist()
        
    # delete this
    def extractMatrixOld(self, file_path, temp_dictionary):
        """takes in a png image path or pdf path and returns extracted hvf matrix 

        Args:
            file_path (string)
            userData (object)

        Returns:
            matrix (list of lists)
        """

        
        # if os.path.splitext(file_path)[-1].lower() == ".pdf":
        try:
            if file_path.endswith(".pdf"):
                hvf_img = File_Utils.read_image_from_file(file_path)  # change to file if not working
                print(hvf_img)
            else:
                hvf_img = File_Utils.read_image_from_file(file_path)

            hvf_obj = Hvf_Object.get_hvf_object_from_image(hvf_img)
            hvf_obj.serialize_to_json()

        except Exception as e:
            print("Error: ", e)
            hvf_obj = None

        try:
            self.extractMetadata(
                hvf_obj, temp_dictionary
            )  # function to extract statistics form HVF file
        except Exception as e:
            print("Error: meta-data unable to be extracted: " + e)

        # anonymiseData(image_path)

        devplot = hvf_obj.pat_dev_percentile_array
        devplotshape = devplot.plot_array.shape
        # pad with zeros for standard 10 * 10 formatList(result)
        array = np.zeros((10, 10))
        for i in range(devplotshape[0]):
            for j in range(devplotshape[1]):
                array[j, i] = int(
                    devplot.plot_array[i, j].get_enum()
                )  # transpose array

        hvf_obj.get_display_raw_val_plot_string()
        matrix = array.tolist()  # convert array into a 2D list as this is Algo format
        return matrix

    def getSingleFieldPaths(self, size):
        """generates specified list of absolute paths from singleField samples

        Args:
            sample size

        Returns:
            list of absolute file paths
        """
        # may only work in development environment
        file_batches = os.walk('../singleField')
        absolute_path = os.path.abspath("..") + "/singleField"
        try:
            files = list(file_batches)[0][2]
            if size < len(files):
                return [absolute_path + "/" + f for f in files][:size]
            else:
                print("Error: sample size larger than number of files")
        except:
            return []

    @staticmethod
    def convDateFormat(self, Date):  
    # change  date format to take in string
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]  # enumerate list of months
        try:
            year = int(Date[-4:])
            month = Date[:3]
            day = int(Date[3:6])
            for index, item in enumerate(
                months
            ):  # converting string to numerical value of month
                if item == month:
                    month = index + 1
            date = datetime.datetime(year, month, day)
            return date
        except:
            year = int(Date[-4:])
            month = Date[:3]
            day = int(Date[3:5])
            for index, item in enumerate(
                months
            ):  # converting string to numerical value of month
                if item == month:
                    month = index + 1
            date = datetime.datetime(year, month, day)
            return date

        else:
            print("Error: Format error, unable to convert date to datetime object")
            return Date

    """
    def anonymiseData(image_path):
        img = Image.open(image_path).convert('RGB')
        img_arr = np.array(img)
        img_arr[100 : 250, 100 : 500] = (0, 0, 0)
        img = Image.fromarray(img_arr)
        img.save(image_path)
    """
    @staticmethod
    def filterPDF(List):
        """ensures only pdfs are read

        Args:
            List (_type_): _description_

        Returns:
            list: only .pdf files
        """
        for f in List:
            if f.endswith(".png"):
                List.remove(f)
        return List
    
    def checkReliability(self, FPOS, FixationLoss, GHT):  # fix criteria
        reliable = False
        if FixationLoss < 33 and FPOS < 33:
            reliable = True
        return reliable

    # feeding through file object to be used
    def extractMetadataOld(self, hvf_obj, patient_dictionary):
        try:
            patient_dictionary["NAME"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_NAME]
            patient_dictionary["DOB"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_DOB]
            patient_dictionary["ID"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_ID]
            patient_dictionary["SIZE"] = hvf_obj.metadata[
                Hvf_Object.KEYLABEL_FIELD_SIZE
            ]
            patient_dictionary["DATE"] = self.convDateFormat(
                hvf_obj.metadata[Hvf_Object.KEYLABEL_TEST_DATE]
            )  # converts to datetime object
            patient_dictionary["EYE"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_LATERALITY]

            if hvf_obj.metadata[Hvf_Object.KEYLABEL_NAME] == "Extraction Failure":
                print("Error: Unable to read client details due to anonymised image")

        except:
            print("Error: Unable to extract client details")

        # checking to see if VF matrix is considered reliable based on the following function arguments:
        try:

            patient_dictionary["GHT"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_GHT]
            patient_dictionary["MD_db"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_MD]
            patient_dictionary["MD_%"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_MDP]
            patient_dictionary["RX"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_RX]
            patient_dictionary["VFI"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_VFI]
            FalsePos = hvf_obj.metadata[Hvf_Object.KEYLABEL_FALSE_POS]
            patient_dictionary["FALSE_POS"] = int(FalsePos.rstrip("%"))

            FixationLoss = hvf_obj.metadata[Hvf_Object.KEYLABEL_FIXATION_LOSS]
            FixationList = FixationLoss.split("/")
            patient_dictionary["FIXATION_LOSS"] = round(
                (int(FixationList[0]) / int(FixationList[1])) * 100, 2
            )  # converting fixation loss fraction to percentage

        except Exception as e:  # displays command line error message
            print("Error : Unable to read error margins " + e)

        try:
            patient_dictionary["PSD_%"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_PSDP]
            patient_dictionary["PSD_db"] = hvf_obj.metadata[Hvf_Object.KEYLABEL_PSD]
        except:
            print("Error: PSD Extraction Failed: " + e)
            patient_dictionary["PSD_db"] = "error"

        print(patient_dictionary)
        try:
            patient_dictionary["RELIABLE"] = self.checkReliability(
                patient_dictionary["FALSE_POS"],
                patient_dictionary["FIXATION_LOSS"],
                hvf_obj.metadata[Hvf_Object.KEYLABEL_GHT],
            )
        except Exception as e:
            print("Error: Reliability Check failed: " + e)
        return patient_dictionary

    # this function runs all the functions above
    @staticmethod
    def readFile(image_path, patient_dictionary):
    
        try:
            return ExtractHVFData.extractMatrix(image_path, patient_dictionary)
        except:
            # error = True  # mark error so we pass over data frame
            print(
                "Error: Error in extractHVFdata occured in extracting matrix from VF file as file: "
                + image_path
                + " not in readable format"
            )
            return []
