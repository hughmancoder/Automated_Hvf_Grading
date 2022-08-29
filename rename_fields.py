import os
import pathlib

# single_field_path = str(pathlib.Path().resolve()) + '/single_field'
def main(): 
    """Renames file in singleField folder to numerical names so it is easier to track files
    """
    folder = "singleField"
    for count, filename in enumerate(os.listdir(folder)):
        print(filename)
        dst = f"sf_{str(count)}.pdf"
        src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        dst =f"{folder}/{dst}"
        if filename.endswith(".pdf"):
            # rename() function will
            os.rename(src, dst)

# Driver Code
if __name__ == '__main__':
    main()