# == runs functions == 
import joblib.parallel
from . import BatchCompletionCallBack 

def RunFiles(filepath):
    print("Info: Analysing "+filepath)
    temp_dictionary = {
        "FILENAME": "",
        "NAME": "",
        "DOB": "",
        "ID": "",
        "EYE": "",
        "SIZE": "",
        "DATE": "",
        "RX": "",
        "GHT": "",
        "VFI": "",
        "MD_%": "",
        "MD_db": "",
        "PSD_%": "",
        "PSD_db": "",
        "FALSE_POS": "",
        "FIXATION_LOSS": "",
        "RELIABLE": False
    }
    patient_list = ["Error"]*23
    # varaible to keep track of error in extraction (don't append to df if error is true)
    error = False
    temp_dictionary["FILENAME"] = os.path.basename(filepath)

    mat = readFile(filepath, temp_dictionary)
    # if(error == True): continue #skip this iteration of for loop if error is found
    if(len(mat) == 0):
        patient_list[0] = os.path.basename(filepath)
        print("Error: matrix is empty data not extracted")
        return patient_list

    # formats percentage levels and flips matrix for L eye
    mat = ProcessMatrix(mat, temp_dictionary["EYE"])
    psd = temp_dictionary["PSD_db"]
    if(psd == "error"):
        psd = 1E+8  # pad with big number to exceed bounds
    eye = temp_dictionary["EYE"]
    rel = temp_dictionary["RELIABLE"]  
    regSize = temp_dictionary["SIZE"]
    crit = CheckCriteria(psd, temp_dictionary["GHT"])
    # temp_dictionary["ID"] = "customID"; #temporary test
    try:
        # signature: runAlgorithm(mat,region_size,reliable,criteria)
        (region_list, result) = algorithm.runAlgorithm(mat, regSize, rel, crit,eye)
        # algorithm.PrintMatrix(mat)
        # needed to sync cached variables with new inputs #MAY NOT BE NEEDED
        importlib.reload(algorithm)
        patient_list = formatList(region_list, crit, result, temp_dictionary)
    except Exception as e:
        print("Error: error running algorithm: " + e)

    return patient_list

def AnalyseFiles(id, df):
    """[Analyses id in df and returns analysed sub-df]

    Args:
        id ([var]): [ID to be analysed]
        df ([df]): [dataframe to be analysed from]

    Returns:
        [df]: [df: dataframe with added data]
    """
    eyes = ["Left","Right"]
    for eye in eyes: #analyse left and right eye seperately
        df = sortByID(df,id)
        (progressive_regions, progression_index) = checkDefectProgression(df,eye)
        return addProgressionFromIndex(df,progression_index,progressive_regions,eye) #returns subDf

joblib.parallel.BatchCompletionCallBack = BatchCompletionCallBack

path = ExtractSingleFieldFilePath()
array = FilePathToArray(path,12) #ExtractFiles(path, NumFiles)

total_n_jobs = len(array);
data = Parallel(n_jobs=-2)(delayed(RunFiles)(i) for i in array)
title = ["FileName", "Name", "DOB", "ID", "Eye", "Size", "Date","RX","GHT","VFI","MD_db", "MD", "PSD","PSD_db","FalsePOS",
         "FixationLoss", "Reliable", "UL", "LL", "UM", "UC", "LC", "LM", "UR", "LR", "Criteria","isAbnormal"]; 

df = pd.DataFrame(data, columns=title)
pd.set_option("display.max_rows", None, "display.max_columns", None) #setting to show full df

display(df) # print(df.head())

