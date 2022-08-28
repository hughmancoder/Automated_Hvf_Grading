import pandas as pd

# == checks for glaucoma progression == 
class BuildDataFrame:
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
    
    def AnalyseFiles(self, id, df):
        """[Analyses id in df and returns analysed sub-df]

        Args:
            id ([var]): [ID to be analysed]
            df ([df]): [dataframe to be analysed from]

        Returns:
            [df]: [df: dataframe with added data]
        """
        eyes = ["Left", "Right"]
        for eye in eyes:  # analyse left and right eye seperately
            df = self.sortByID(df, id)
            (progressive_regions, progression_index) = self.checkDefectProgression(df, eye)
            # returns subDf
            return self.addProgressionFromIndex(df, progression_index, progressive_regions, eye)

    # all python arguments are passed by reference / memory addresses (so large data is not an issue)
    @staticmethod
    def sortByID(df,ID):  # get subset via ID
        df = df[df['ID'] == ID]
        df = df.sort_values(by="Date")
        return df

    @staticmethod
    def sortByPath(path, df):  # get subset via path
        df = df[df["FileName"].str.contains(path)]
        df = df.sort_values(by="Date")
        return df

    @staticmethod
    def filterByEye(df, eye):
        return df[df["Eye"] == eye]

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
            for (
                region
            ) in (
                regions
            ):  # scoping thorugh all regions to search for region abnormalities
                l = df[region].values  # converts column to a list
                if (
                    (l[i] and l[i + 1])
                    or (l[i] and l[i + 2])
                    or (l[i + 1] and l[i + 2])
                ):  # progressor criteria
                    # update dictionary key to contain index
                    progressive_regions[region] = i

        # otherwise return -1 as index
        return (progressive_regions, progression_index)
