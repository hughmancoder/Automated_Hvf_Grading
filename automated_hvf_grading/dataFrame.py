class DataFrame:
    def __init__(self):
        pass
    
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
        try:
            if eye == "Left":
                return leftConversion[region]
            # right eye
            return rightConversion[region]
        except:
            return "error"
