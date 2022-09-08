import pandas as pd
from automated_hvf_grading.user import User

class DataFrame:

    def __init__(self, user):
        """creates a dataframe from user object
            soft coded from object attributes and values so that when we make changes to the object (such as adding new features), it automatically shows up on dataframe

        Args:
            user (object)
        """
        print("Info: creating new dataframe")
        self.column_names = user.getAttributes()
        self.df = pd.DataFrame(columns = self.column_names)

        """
        self.leftLabels = {
            "UL": "Superior temporal wedge",
            "LL": "Inferior temporal wedge",
            "UM": "Superior Bjerrum",
            "UC": "Superior paracentral",
            "LC": "Inferior paracentral",
            "LM": "Inferior Bjerrum",
            "UR": "Superior nasal step",
            "LR": "Inferior nasal step",
        }
        self.rightLabels = {
            "UL": "Superior nasal step",
            "LL": "Inferior nasal step",
            "UM": "Superior Bjerrum",
            "UC": "Superior paracentral",
            "LC": "Inferior paracentral",
            "LM": "Inferior Bjerrum",
            "UR": "Superior temporal wedge",
            "LR": "Inferior temporal wedge",
        }
        """
    
    def runDataFrame(self):
        pass
    
    def getHumanDf(self):
        # self.df.columns = self.df.columns.str.replace("_", " ")
        return self.df

    @staticmethod
    def listToDictionary(l1, l2):
        return dict(zip(l1, l2))

    def addData(self, userObj): 
        # temp = pd.DataFrame(userObj.getDict())
        temp = pd.DataFrame([vars(userObj)])
        self.df = pd.concat([self.df, temp], ignore_index=True)
    
        """
        # outdated way
        self.df = self.df.append(vars(user), ignore_index = True)
        """
    def remove_NA_Scans(self):
        self.df.dropna()
        self.df.drop(self.df[self.df["test_date"] == "N/A"].index, inplace=True)
        
    # patient filtering methods
    def sortByTestDate(self, df):
        self.remove_NA_Scans()
        return df.sort_values(by="test_date")

    def filterByID(self, id):
        tempObj = self
        tempObj.df[tempObj.df["id"] == id]
        return tempObj

    def filterByName(self, Name):
        return self.df[self.df["name"] == Name]
        
    def filterByFileFileName(self, filename): 
        return self.df[self.df["filename"].str.contains(filename)]

    def filterByEye(self, eye):
        """takes in df and generates subdf with left or right eye
            and sorts chronologically by date (needed for progression analysis)
            renames corresponding eye regions to medical terminologies for respective eye

        Args:
            df (dataframe): 
            eye (string): "Left" or "Right"

        Returns:
            sub dataframe
        """
        if eye != "Left" and eye != "Right":
            print("Error: only valid eye labels accepted Left and Right")
            return self.df

        """
        try:
            self.remove_NA_Scans()
        except Exception as e:
            print("Error removing faulty dates and scans " + str(e))
        """
        return self.sortByTestDate(self.df[self.df["eye"] == eye])

    @staticmethod
    def filterByEye_static(df, eye):
        if eye != "Left" and eye != "Right":
            print("Error: only valid eye labels accepted Left and Right")
            df
        try:
            df.dropna()
            df.drop(df[df["test_date"] == "N/A"].index, inplace=True)
        except Exception as e:
            print("Error removing faulty dates and scans " + str(e))

        return df[df["eye"] == eye].sort_values(by="test_date") 
    
    @staticmethod
    def filterByID_static(df, id):
        tempdf = df
        tempdf[tempdf["id"] == id]
        return tempdf
    """
    def renameHemifields(self, df, eye):
        rename = self.locationLabels(eye)
        return df.rename(columns = rename, inplace = False)
    
    def locationLabels(self, eye):  
        if eye == "Left":
            return self.leftLabels
        return self.rightLabels
    """

    @staticmethod
    def renameHemifields(df, eye):
        leftLabels = {
            "UL": "Superior temporal wedge",
            "LL": "Inferior temporal wedge",
            "UM": "Superior Bjerrum",
            "UC": "Superior paracentral",
            "LC": "Inferior paracentral",
            "LM": "Inferior Bjerrum",
            "UR": "Superior nasal step",
            "LR": "Inferior nasal step",
        }
        rightLabels = {
            "UL": "Superior nasal step",
            "LL": "Inferior nasal step",
            "UM": "Superior Bjerrum",
            "UC": "Superior paracentral",
            "LC": "Inferior paracentral",
            "LM": "Inferior Bjerrum",
            "UR": "Superior temporal wedge",
            "LR": "Inferior temporal wedge",
        }

        rename = rightLabels if eye == "Right" else leftLabels
        return df.rename(columns = rename, inplace = False)

    # progressor criteria
    def progressorCriteria(self, eye):
        """updates df with both progressor and confirmation field criteria

        Args (eye): "Left" or "Right"

        Returns updated df
        """
        
        df = self.filterByEye(eye)

        rows = df.shape[0]
        if rows <= 2:
            print(f"Info: {rows} samples is insufficient to evaluate progression criteria; issue could be wrong entry to filter patient")
            return self.renameHemifields(df, eye)

        df["progression"] = False
        p = df["is_abnormal"].values
        progression_index = -1
        for i in range(rows - 2):
            if (p[i] and p[i + 1]) or (p[i] and p[i + 2]) or (p[i + 1] and p[i + 2]):
                progression = True
                progression_index = i + 1
                break

        if progression_index > -1:
            df["progression"].iloc[progression_index:] = True
            df["progression_date"] = "-"
            df["progression_date"].iloc[progression_index:] = df["test_date"].iloc[progression_index]
            
        else:
            print("Info: no progression detected")
            return self.renameHemifields(df, eye)        
        
        # == confirmation field algorithm == 
        # save index of first progression
        region_progressions = {
            "UL": -1,
            "LL": -1,
            "UM": -1,
            "UC": -1,
            "LC": -1,
            "LM": -1,
            "UR": -1,
            "LR": -1
        }

        first_progression_date = "-"
        regions = df.loc[:, "UL" : "LR" :]
        v = regions.values.tolist()
        
        # checking for any 2 abnormal scans out of 3 chronological scans in same region
        for r in range(rows - 2):
            for c in range(8): 
                if (v[r][c] and v[r + 1][c]):
                    region = list(region_progressions.keys())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 1

                elif(v[r][c] and v[r + 2][c]):
                    region = list(region_progressions.keys())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 2

                elif(v[r + 1][c] and v[r + 2][c]):
                    region = list(region_progressions.keys())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 2

        progression_indexes = [i for i in region_progressions.values() if i != -1]
        if not len(progression_indexes):
            print("Info: No confirmation_fields found")
            return self.renameHemifields(df, eye)

        first_progression = min(progression_indexes)
        print(first_progression)
        df["confirmation_field"] = False
        df["confirmation_field_regions"] = ""

        if first_progression >= 0:
            try:
                df["confirmation_field"].iloc[first_progression:] = True
                for key, val in region_progressions.items():
                    if val >= 0:
                        df["confirmation_field_regions"].iloc[val:] += " " + str(key)
            except Exception as e:
                print("Error: ", e)
                return self.renameHemifields(df, eye)

        return self.renameHemifields(df, eye)

    @staticmethod             
    def progressorCriteria_df(df, eye, id):
        """updates df with both progressor and confirmation field criteria

        Args (eye): "Left" or "Right"

        Returns updated df
        """
        tempdf = df
        tempdf = DataFrame.filterByEye_static(tempdf, eye)
        tempdf = DataFrame.filterByID_static(tempdf, id)

        rows = tempdf.shape[0]
        if rows <= 2:
            print(f"Info: {rows} samples is insufficient to evaluate progression criteria; issue could be wrong entry to filter patient")
            return DataFrame.renameHemifields(tempdf, eye)

        tempdf["progression"] = False
        p = tempdf["is_abnormal"].values
        progression_index = -1
        for i in range(rows - 2):
            if (p[i] and p[i + 1]) or (p[i] and p[i + 2]) or (p[i + 1] and p[i + 2]):
                progression = True
                progression_index = i + 1
                break

        if progression_index > -1:
            tempdf["progression"].iloc[progression_index:] = True
            tempdf["progression_date"] = "-"
            tempdf["progression_date"].iloc[progression_index:] = tempdf["test_date"].iloc[progression_index]
            
        else:
            print("Info: no progression detected")
            return DataFrame.renameHemifields(tempdf, eye)        
        
        # == confirmation field algorithm == 
        # save index of first progression
        region_progressions = {
            "UL": -1,
            "LL": -1,
            "UM": -1,
            "UC": -1,
            "LC": -1,
            "LM": -1,
            "UR": -1,
            "LR": -1
        }

        first_progression_date = "-"
        regions = tempdf.loc[:, "UL" : "LR" :]
        v = regions.values.tolist()
        
        # checking for any 2 abnormal scans out of 3 chronological scans in same region
        for r in range(rows - 2):
            for c in range(8): 
                if (v[r][c] and v[r + 1][c]):
                    region = list(region_progressions.keys())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 1

                elif(v[r][c] and v[r + 2][c]):
                    region = list(region_progressions.keys())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 2

                elif(v[r + 1][c] and v[r + 2][c]):
                    region = list(region_progressions.keys())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 2

        progression_indexes = [i for i in region_progressions.values() if i != -1]
        if not len(progression_indexes):
            print("Info: No confirmation_fields found")
            return DataFrame.renameHemifields(tempdf, eye)

        first_progression = min(progression_indexes)
        print(first_progression)
        tempdf["confirmation_field"] = False
        tempdf["confirmation_field_regions"] = ""

        if first_progression >= 0:
            try:
                tempdf["confirmation_field"].iloc[first_progression:] = True
                for key, val in region_progressions.items():
                    if val >= 0:
                        tempdf["confirmation_field_regions"].iloc[val:] += " " + str(key)
            except Exception as e:
                print("Error: ", e)
                return DataFrame.renameHemifields(tempdf, eye)

        return DataFrame.renameHemifields(tempdf, eye)


