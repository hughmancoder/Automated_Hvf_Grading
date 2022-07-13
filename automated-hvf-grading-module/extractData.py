# == hvf library imports
from hvf_extraction_script.hvf_manager.hvf_export import Hvf_Export
from hvf_extraction_script.hvf_data.hvf_object import Hvf_Object
from hvf_extraction_script.utilities.file_utils import File_Utils

# == other imports ==
from pdf2image import convert_from_path
from PIL import Image  # pillow
import datetime
import os
import pathlib  # pathy
import numpy as np

# == Note ==
# current class methods are static (for now) as we pass all funtion requisites as parameters

class extractHVFData:
    def __init__(self):
        print("extraction started")

    @staticmethod
    def convDateFormat(self, Date):  # change format to take in string
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
    def filterPDF(List):  # removes ensures that only pdf's are read
        for i in List:
            if ".png" in i:
                List.remove(i)
        return List

    @staticmethod
    def ExtractPDF(pdf_path, name):
        try:
            if os.path.exists(pdf_path):  # checking if path is valid
                # patient_dictionary["FILENAME"] = pdf_path
                pages = convert_from_path(pdf_path)
                cwd = pathlib.Path().resolve()  # resets path
                cwd = pathlib.Path().cwd()
                save_path = cwd + "/SingleField/ImageData"

                for img in pages:  # looping through in case it has 2 pages
                    name = name.replace("pdf", "png")
                    save_path = save_path + "/" + name
                    img.save(save_path)  # img.save(name)
                    return save_path
            else:
                print("Error: File path does not exist")
                return ""
        except:
            print("Error: df2image library can not read pdf, convert_from_path error")
            return ""

    def extractMatrix(self, image_path, temp_dictionary):
        # pdf extraction here
        if os.path.splitext(image_path)[-1].lower() == ".pdf":
            hvf_img = File_Utils.read_image_from_pdf(
                image_path
            )  # change to file if not working
        else:
            hvf_img = File_Utils.read_image_from_file(image_path)

        hvf_obj = Hvf_Object.get_hvf_object_from_image(hvf_img)
        hvf_obj.serialize_to_json()

        try:
            self.extractMetadata(
                hvf_obj, temp_dictionary
            )  # function to extract statistics form HVF file
        except Exception as e:
            print("Error: meta data unable to be extracted: " + e)
        # anonymiseData(image_path) #blanks out sensitive information
        devplot = hvf_obj.pat_dev_percentile_array
        devplotshape = devplot.plot_array.shape
        array = np.zeros(
            (10, 10)
        )  # pad with zeros for standard 10 * 10 formatList(result)
        for i in range(devplotshape[0]):
            for j in range(devplotshape[1]):
                array[j, i] = int(
                    devplot.plot_array[i, j].get_enum()
                )  # transpose array
        matrix = array.tolist()  # convert array into a 2D list as this is Algo format
        return matrix

    def checkReliability(self, FPOS, FixationLoss, GHT):  # fix criteria
        reliable = False
        if FixationLoss < 33 and FPOS < 33:
            reliable = True
        return reliable

    # feeding through file object to be used
    def extractMetadata(self, hvf_obj, patient_dictionary):
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
    def readFile( image_path, patient_dictionary):
        global error
        try:
            return extractHVFData.extractMatrix(image_path, patient_dictionary)
        except:
            error = True  # mark error so we pass over data frame
            print(
                "Error: Error occured in extracting matrix from VF file as file: "
                + image_path
                + " not in readable format"
            )
            return []
