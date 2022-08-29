import pandas as pd

class DataFrame:

    def __init__(self, user):
        """creates a dataframe from user object

        Args:
            user (object)
        """
        # hard coded as we wan't to exclude some data to not clutter dataframe
        self.columns = []
        self.column_names = self.getObjectColumns(user)
        self.df = pd.DataFrame(columns = self.column_names)
    
    def getObjectColumns(self, user):
        return list(vars(user).keys())

    def getObjectValues(self, user):
        return list(vars(user).values())

    def addData(self, user): 
        temp = pd.DataFrame([vars(user)])
        self.df = pd.concat([self.df, temp], ignore_index=True)
    
        """
        # outdated way
        self.df = self.df.append(vars(user), ignore_index = True)
        """

    @staticmethod
    def sortByID(df, ID):  # get subset via ID
        sdf = df[df["ID"] == ID]
        sdf = sdf.sort_values(by="Date")
        return sdf

    @staticmethod
    def sortByPath(path, df):  # get subset via path
        df = df[df["FileName"].str.contains(path)]
        df = df.sort_values(by="Date")
        return df

    @staticmethod
    def filterByEye(df, eye):
        return df[df["Eye"] == eye]

    @staticmethod
    def locationLabels(region, eye):  
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

        if eye == "Left" or eye == "left":
            return leftConversion[region]
        return rightConversion[region]

    @staticmethod
    def checkDefectProgression(self, df, eye):  # checking progressor criteria
        df = self.filterByEye(df, eye)
        l = df["isAbnormal"].values
        length = len(l)
        # add variable for date
        progression_index = -1
        # progressive_regions = []
        progressive_regions = {
            "UL": -1,
            "LL": -1,
            "UM": -1,
            "UC": -1,
            "LC": -1,
            "LM": -1,
            "UR": -1,
            "LR": -1,
        }
        for i in range(length - 2):
            # check if at least 2 our of 3 consecutive progressions are abnormal (True) -> index: 1&2; 2&3
            if (l[i] and l[i + 1]) or (l[i + 1] and l[i + 2]):
                progression_index = i  # get return index of first progression

        if progression_index != -1:  # if we find a progression
            regions = ["UL", "LL", "UM", "UC", "LC", "LM", "UR", "LR"]
            for region in regions: 
                l = df[region].values  # converts column to a list
                 # progressor criteria: any 2 defective scans out of 3 consecutive chronological samples
                if (
                    (l[i] and l[i + 1])
                    or (l[i] and l[i + 2])
                    or (l[i + 1] and l[i + 2])
                ): 
                   
                    progressive_regions[region] = i
        return (progressive_regions, progression_index)

"""
class AnalyseData:
    def addProgressionFromIndex(
        self, df, index, progressive_regions, eye
    ):  # adds progression criteria to df
        df["Progression"] = False
        df["progressive_regions"] = ""  # intialise as empty
        df["Technical_progression"] = ""  # also intialise as empty
        if index <= 0:
            print("Info: No progression indicated")
            return df
        try:
            rows = len(df.index)
            pd.options.mode.chained_assignment = (
                None  # prevents pandas warning for chained assignment
            )
            df["Progression"].iloc[index:rows] = True
            for key, value in progressive_regions.items():
                if 0 <= value <= rows:
                    df["progressive_regions"].iloc[value:rows] += " " + \
                        str(key)
                    df["Technical_progression"].iloc[
                        value:rows
                    ] += " " + self.addMedicalTerm(str(key), eye)
            return df

        except Exception as e:
            print("Error: could not add progression criteria to df" + e)
            return df
    
    def analyseFiles(self, id, df):
        [Analyses id in df and returns analysed sub-df]

        Args:
            id ([var]): [ID to be analysed]
            df ([df]): [dataframe to be analysed from]

        Returns:
            [df]: [df: dataframe with added data]
        
        eyes = ["Left", "Right"]
        for eye in eyes:  # analyse left and right eye seperately
            df = self.sortByID(df, id)
            (progressive_regions, progression_index) = self.checkDefectProgression(df, eye)
            # returns subDf
            return self.addProgressionFromIndex(df, progression_index, progressive_regions, eye)
"""