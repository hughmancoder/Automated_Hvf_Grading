import argparse
import pandas as pd
from automated_hvf_grading import driver

parser = argparse.ArgumentParser(description='HVF Progression')
parser.add_argument("--group", "-g", type=int, help="Group Method; 0 = By Patient ID, 1 = Seperate Folders", default=0, choices=[0, 1])
parser.add_argument("--eye", "-e", type=str, help="Eye to use in Analysis: 'left' or 'right'", default='Left', choices=['Left', 'Right'])
parser.add_argument("--progression", "-p", help='Progression analysis method to use; 0 = Default', type=int, choices=[0])
parser.add_argument("--csvpath", "-c", help='Path to CSV', type=str)
parser.add_argument("--json", "-j", help='JSON String', type=str)
parser.add_argument("--files", "-f", nargs='+', type=str, help='Path to each file as a different argument')
args = parser.parse_args()
if args.files:
    df = driver.runParallel(args.files).df
    pd.set_option("display.max_rows", None, "display.max_columns", None) #setting to show full df
    htmloutput = df.to_html(border=0, table_id="grading-table", classes=["table"], index=False, justify="left").replace('\n', ' ').replace('\r', '')
    jsonoutput = df.to_json(index=False, orient="table")
    print(htmloutput)
    print(jsonoutput)

elif args.progression is not None:
    if args.csvpath:
        df = pd.read_csv(args.csvpath)
    elif args.json:
        df = pd.read_json(args.json, orient="table")
    if args.progression == 0:
        ids = []
        if args.group == 0:
            ids = df.id.unique()
            # print(ids)
        elif args.group == 1:
            print("Error: Group method not implemented")

        outdf = driver.runParallelAnalysis(df, ids, args.eye)
        htmloutput = outdf.to_html(border=0, table_id="analysis-table", classes=["table"], index=False, justify="left").replace('\n', ' ').replace('\r', '')
        jsonoutput = outdf.to_json(index=False, orient="table")
        print(htmloutput)
        print(jsonoutput)