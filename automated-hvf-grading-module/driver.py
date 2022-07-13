# == runs functions ==
import pandas as pd


# == dependencies == 
from IPython.display import display # to display df for testing

from ParallelProcessing import ParallelProcess

# == build data frame == 
def buildDataframe():
    dataframe_column_names = [
        "FileName",
        "Name",
        "DOB",
        "ID",
        "Eye",
        "Size",
        "Date",
        "RX",
        "GHT",
        "VFI",
        "MD_db",
        "MD",
        "PSD",
        "PSD_db",
        "FalsePOS",
        "FixationLoss",
        "Reliable",
        "UL",
        "LL",
        "UM",
        "UC",
        "LC",
        "LM",
        "UR",
        "LR",
        "Criteria",
        "isAbnormal",
    ]

    ParallelProcess = ParallelProcess() # parallel processor object
    data = ParallelProcess.runParallel()
    return  pd.DataFrame(data, columns = dataframe_column_names)

df = buildDataframe()
pd.set_option(
    "display.max_rows", None, "display.max_columns", None
)  # shows full df

# display(df) # jupyter notebook 
print(df.head())

print("script complete")