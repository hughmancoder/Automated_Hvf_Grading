import pandas as pd

class DataFrame:

    def __init__(self, user):
        """creates a dataframe from user object

        Args:
            user (object)
        """
        # hard coded as we wan't to exclude some data to not clutter dataframe
        self.column_names = self.getObjectColumns(user)
        self.df = pd.DataFrame(columns = self.column_names)
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

    # patient filtering methods
    def sortByTestDate(self, df):
        return df.sort_values(by="test_date")

    def sortByID(self,id):
        return self.df[self.df["id"] == id]

    def sortByName(self, Name):
        return self.df[self.df["name"] == Name]
        
    def sortByFilePath(self, path): 
        return self.df[self.df["filename"].str.contains(path)]

    def filterByEye(self, df, eye):
        """takes in df and generates subdf with left or right eye
            sorts chronologically by date
            renames corresponding eye regions to medical terminologies for respective eye

        Args:
            df (dataframe): 
            eye (string): "Left" or "Right"

        Returns:
            sub dataframe
        """
        return self.sortByTestDate(df[df["eye"] == eye])

    def renameHemifields(self, df, eye):
        rename = self.locationLabels(eye)
        return df.rename(columns = rename, inplace = False)

    def locationLabels(self, eye):  
        if eye == "Left":
            return self.leftLabels
        return self.rightLabels

    # progressor criteria
    def progressorCriteria(self, df, eye):
        """takes in df and adds two new columns 
            a boolean to determine whether there is a progression detected,
            a date to determine the date of first progression onset
            and the total time the progrssion has been present in patient
        Args:
            df (dataframe): updated dataframe

        Returns updated df
        """
        p = df["is_abnormal"].values # progression 
        number_of_samples = len(p) 
        if number_of_samples <= 2:
            print(f"Info: {number_of_samples} is not enough samples to evaluate progression criteria")
            return df

        """
        # testing if there is a onset of defects in any of the regions
        for i in range(number_of_samples - 2):
             if (p[i] and p[i + 1]) or (p[i] and p[i + 2]) or (p[i + 1] and p[i + 2]):
                progression = True
                break
        """

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

        # checking for any 2 abnormal scans out of 3 chronological scans
        for r in range(len(v) - 2):
            for c in range(8): 
                if (v[r][c] and v[r + 1][c]):
                    region = list(region_progressions.values())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 1

                elif(v[r][c] and v[r + 2][c]):
                    region = list(region_progressions.values())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 2

                elif(v[r + 1][c] and v[r + 2][c]):
                    region = list(region_progressions.values())[c]
                    if(region_progressions[region] == -1): 
                        region_progressions[region] = r + 2
                    
            print(region_progressions)
            # adding progression data to df
            num_rows = len(df.index)
            df["progression"] = False
            df["progressive_regions"] = ""
            df["progression_date"] = ""

            first_progression = min(region_progressions.values()) # index of first progrssion

            if first_progression >= 0:
                try:
                    df["progression"].iloc[first_progression:] = True
                    df["progresson_date"].iloc[first_progression:] = df["test_date"].iloc[first_progression]
                    for key, val in region_progressions.items():
                        print(key, val)
                        if val != -1:
                            df["progressive_regions"].iloc[val:] = " " + str(key)
                except Exception as e:
                    print("Error: ", e)
                    df["progression"].iloc[first_progression:] = True
                    self.renameHemifields(df, eye)

            return self.renameHemifields(df, eye)
                        