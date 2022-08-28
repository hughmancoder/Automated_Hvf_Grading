import importlib
import pathlib
import datetime
import os
import site

class ProcessData:
    @staticmethod
    def mirror(matrix):
        r = 0
        for subarray in matrix:
            matrix[r] = list(subarray[::-1])
            r += 1
        return matrix

    @staticmethod
    def PrintMatrix(mat):  
        """prints of matrix in easy to read format_summary_

        Args:
            mat (list)
        """
        rows = len(mat[0])
        cols = len(mat)
        
        for r in range(rows):
            if r == 5:
                # ornaments for formatting spacing
                print("\n\n" + "-----------" + ("---" * cols) + "\n")
            else:
                print("\n")
            for c in range(cols):
                if c == 5:
                    print("|   ", end="")
                if mat[r][c] == 0.5:
                    print(str(mat[r][c]) + " ", end="")
                else:
                    print(str(mat[r][c]) + "   ", end="")

    @staticmethod
    def ProcessMatrix(matrix, eye):

        level_map = {  # converts levels to VFI percentages for grading
            "1.0": 0,
            "2.0": 5,
            "3.0": 2,
            "4.0": 1,
            "5.0": 0.5,
            "1": 0,  # as format sometimes differs
            "2": 5,
            "3": 2,
            "4": 1,
            "5": 0.5,
        }
        try:
            (rows, cols) = (len(matrix[0]), len(matrix))
            for r in range(rows):
                for c in range(cols):
                    if str(matrix[r][c]) in level_map:
                        matrix[r][c] = level_map[str(matrix[r][c])]

            if eye == "Left":
                matrix = FilterData.mirror(matrix)
            return matrix
        except:
            print("Error: empty matrix unable to be processed")
            return []

    @staticmethod
    def ExtractSingleFieldFilePath():
        importlib.reload(site)  # refreshes file path
        filepath = pathlib.Path().resolve()
        filepath = pathlib.Path().cwd()
        singlefieldpath = str(filepath) + "/SingleField"
        if os.path.exists(singlefieldpath):
            return singlefieldpath
        return filepath

    @staticmethod
    def FilePathSampleToArray(filepath, sample_size):
        try:
            Files = os.listdir(filepath)  # gets all files in that directory
            Sample = [str(filepath) + "/" + str(x) for x in Files[: int(sample_size)]]
        except:
            print("Error: Invalid inputs")
            Sample = []
        return Sample

    def FilePathToArray(filepath):
        try:
            Files = os.listdir(filepath)  # gets all files in that directory
            Sample = [str(filepath) + "/" + str(fileName) for fileName in Files]
        except:
            print("Error: Invalid inputs")
            Sample = []
        return Sample

    @staticmethod
    def formatList(
        region_list, crit, result, patient_dictionary
    ):  # adds algorithm result to list
        l = list(patient_dictionary.values()) + [x[1] for x in region_list]
        l.append(crit)
        l.append(result)
        return l

    @staticmethod
    def filterPDF(List):  # removes pngs from list for later processing
        for i in List:
            if ".png" in i:
                List.remove(i)
        return List

    @staticmethod
    def addToDataFrame(List, data):  # adds list value to df
        data.append(List)
        return data

    @staticmethod
    def sortByID(df, ID):  # get subset via ID
        sdf = df[df["ID"] == ID]
        sdf = sdf.sort_values(by="Date")
        return sdf

    @staticmethod
    def addMedicalTerm(
        region, eye
    ):  # function converts regions to technical medical Terms
        leftConversion = {
            "UL": "Superior temporal wedge",
            "LL": "Inferior temporal wedge",
            "UM": "Superior Bjerrum",
            "UC": "Superior paracentral",
            "LC": "Inferior paracentral",
            "LM": "Inferior Bjerrum",
            "UR": "Superior nasal step",
            "LR": "Inferior nasal step",
        }
        rightConversion = {
            "UL": "Superior nasal step",
            "LL": "Inferior nasal step",
            "UM": "Superior Bjerrum",
            "UC": "Superior paracentral",
            "LC": "Inferior paracentral",
            "LM": "Inferior Bjerrum",
            "UR": "Superior temporal wedge",
            "LR": "Inferior temporal wedge",
        }
        try:
            if eye == "Left":
                return leftConversion[region]

            return rightConversion[region]
            # otherwise it's the right eye
        except:
            return "error"

    # @static method
    def checkReliability(FPOS, FixationLoss, GHT): 
        """
        check if user
        """
        reliable = False
        if FixationLoss < 33 and FPOS < 33:
            reliable = True
        return reliable

    def CheckCriteria(psd, ght):  # checks which criteria to run on matrix
        # print("Info: ght, psd: ", ght,psd)
        # print(type(int(psd)))
        try:
            psd = float(psd)
        except:
            psd = 1e10  # otherwise pad with big number to exceed criteria bounds of 0.5
        if ght == "OutsideNormalLimits":
            ght_outside_normal_limits = True
        else:
            ght_outside_normal_limits = False
        try:
            if ght_outside_normal_limits or psd < 0.5:
                return 3  # criteria 3 running
        except:
            if ght_outside_normal_limits:
                return 3

        return 2  # criteria 2 default

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

    @staticmethod
    def convDateFormat(Date):  
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
