import importlib
import pathlib
import os
import site


class filterData:
    def mirror(self, matrix):
        r = 0
        for subarray in matrix:
            matrix[r] = list(subarray[::-1])
            r += 1
        return matrix

    def PrintMatrix(mat):  # prints of matrix in easy to read format
        rows = len(mat[0])
        cols = len(mat)
        # the lines of code below are mostly ornamental
        for r in range(rows):
            if r == 5:
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

    def ProcessMatrix(self, matrix, eye):

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
                matrix = self.mirror(matrix)
            return matrix
        except:
            print("Error: empty matrix unable to be processed")
            return []

    def ExtractSingleFieldFilePath():
        importlib.reload(site)  # refreshes file path
        filepath = pathlib.Path().resolve()
        filepath = pathlib.Path().cwd()
        singlefieldpath = str(filepath) + "/SingleField"
        if os.path.exists(singlefieldpath):
            return singlefieldpath
        return filepath

    def FilePathToArray(filepath, size):
        try:
            Files = os.listdir(filepath)  # gets all files in that directory
            Sample = [str(filepath) + "/" + str(x) for x in Files[: int(size)]]
        except:
            print("Error: Invalid inputs")
            Sample = []
        return Sample

    def formatList(
        region_list, crit, result, patient_dictionary
    ):  # adds algorithm result to list
        l = list(patient_dictionary.values()) + [x[1] for x in region_list]
        l.append(crit)
        l.append(result)
        return l

    def filterPDF(List):  # removes pngs from list for later processing
        for i in List:
            if ".png" in i:
                List.remove(i)
        return List

    def addToDataFrame(List, data):  # adds list value to df
        data.append(List)
        return data

    def sortByID(df, ID):  # get subset via ID
        sdf = df[df["ID"] == ID]
        sdf = sdf.sort_values(by="Date")
        return sdf

    def addMedicalTerm(
        self, region, eye
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
