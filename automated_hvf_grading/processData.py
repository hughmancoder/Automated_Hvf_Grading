import importlib
import pathlib
import datetime
import os
import site

class ProcessData:

    # as left eye is a mirror of right we mirror the matrix
    @staticmethod   
    def mirrorYAxis(matrix):
        r = 0 # row index
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
            print("\n")
            if(r == 5):
                for c in range(cols):
                    print(" --- " , end="") 
                print("\n")
            for c in range(cols):
                if c == 5:
                    print("|  ", end="")
                if str(mat[r][c]) == "0.0":
                    print(" . " + '  ', end="")
                else:
                    print(str(mat[r][c]) + '  ', end="")
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
    def DetermineCriteria(user): 
        """Determines algorithmic criteria
           Criteria 3: a cluster of 3 contiguous points all depressed at p < 5% 
           AND (GHT abnormal or PSD < 5%)
        Args:
            psd (_type_): string
            ght (_type_): string
        """
        ght = user.ght

        try:
            psd = float(user.psd)
            if ght == "OutsideNormalLimits" or psd < 5:
                user.criteria = 3
            else:
                user.criteria = 2
        except:
            print("Error: psd format corrupt")
        return user

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
            
        except:
            year = int(Date[-4:])
            month = Date[:3]
            day = int(Date[3:5])
        
        for index, item in enumerate(months):  # converting string to numerical value of month
                if item == month:
                    month = index + 1
        date = datetime.datetime(year, month, day)
        return date

    """
    def anonymiseData(image_path):
        img = Image.open(image_path).convert('RGB')
        img_arr = np.array(img)
        img_arr[100 : 250, 100 : 500] = (0, 0, 0)
        img = Image.fromarray(img_arr)
        img.save(image_path)
    """
