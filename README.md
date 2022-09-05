# automated-hvf-grading
humphrey visual field matrix reading, grading and analysis automated via python script for research at Flinders University

### supporting library:
__hvf_extraction_script__
https://github.com/msaifee786/hvf_extraction_script

### Regions 
![image info](images/regions.png)

### changes
***
- rewrote entire repository from ground up!
- improved error messages and error checking
- all user bug fixes resolved (7/8 tested)
- more reliable extraction
- more extraction features
- many more features
- improved parallel processing takes full advantage of cpu: program can now process large file batches very quickly on multi-core cpu's

### features
***
- algorithm to automate reading hvf % pattern deviation field scans
- data filtering such as sorting eye by left and right, patient name, chronological order
- automating progression of glaucoma: we can chronologically map past outcomes and apply  progressor criteria (see below) to detect an onset
- parallel processing: runParallel function allows us to run jobs simulatenously on multi-core computer saving time for huge file batches by using full cpu processing capabilities


### Run backend
1. create conda environment (see developer notes below)
2. run from driver.ipynb


### Algorithmic Criteria
***
  An eye was deemed to have progressed if there was a new cluster of visual field defects that were reproduced in a consecutive field (but not necessarily the same visual field locations). A cluster of visual field defects was defined as 3 contiguous points abnormal in the pattern deviation probability plot at P < 5%, at least one of which is P< 1%. If the GHT was “Outside Normal Limits” or the global PSD was P < 5% on the two consecutive HVFs, then the individual points only needed to be abnormal on the pattern deviation probability plot at P < 5%. 

  In other words:

  category 2) A cluster of at least 3 contiguous points in the same region depressed at P < 5%, with at least one these < 1%

  category 3) A cluster of at least 3 contiguous points in the same region depressed at P < 5% AND (GHT = Outside Normal Limits OR PSD = P < 5%)


### Terminology
    abnormal: there is a defect in eye as given algorithmic criteria is satisfied

    reliable: data is reliable if and only if false pos and fixation loss are both less than 33%

    error: this is a flag to mark that there may be an error present in result due to not being able to extract every feature consequently leading to unreliable dependencies

    confirmation field: "2/3 consecutive chronological defects in the same region" 

    Progrssion in eye was deemed to have progressed if there was a new cluster of visual field defects that were reproduced in a consecutive field (but not necessarily the same visual field locations). A cluster of visual field defects was defined as 3 contiguous points abnormal in the pattern deviation probability plot at P < 5%, at least one of which is P< 1%. If the GHT was “Outside Normal Limits” or the global PSD was P < 5% on the two consecutive HVFs, then the individual points only needed to be abnormal on the pattern deviation probability plot at P < 5%. 

    progressor criteria: any 2 defective scans out of 3 consecutive chronological samples

    Progression column: output is determined as true if the progression criteria listed above is satisfied

    Progression onset: date of the first recorded progression


### short hand terminology
***
  matrix sub-regions: ul, ll, um, uc, lc, lm, ur, lr
  upper left, lower left, upper middle, upper central, lower central, lower middle, upper right, lower right
  final output listed as equivalent medical terms


### location labels
  __left eye__
  "UL": "Superior temporal wedge",
  "LL": "Inferior temporal wedge",
  "UM": "Superior Bjerrum",
  "UC": "Superior paracentral",
  "LC": "Inferior paracentral",
  "LM": "Inferior Bjerrum",
  "UR": "Superior nasal step",
  "LR": "Inferior nasal step",
        
  __right eye__
  "UL": "Superior nasal step",
  "LL": "Inferior nasal step",
  "UM": "Superior Bjerrum",
  "UC": "Superior paracentral",
  "LC": "Inferior paracentral",
  "LM": "Inferior Bjerrum",
  "UR": "Superior temporal wedge",
  "LR": "Inferior temporal wedge",
  

  ### left eye
 ![image info](images/lefteyeregions.png)
 
 ### right eye
 ![image info](images/righteyeregions.png)

### To-do
- [x] refactor code using OOP
- [x] refactor into a modules

- [x] get driver.py to run
- [x] fix criteria in algorithm (< 5 % not 0.5 %) 
- [x] get extraction to work
- [x] refactor: remove temp_dictionary and use patientData class
- [x] refactor: make dataFrame class and have dataFrame methods 
- [x] refactor analyseData, build dataFrame into DataFrame class

- [x] create subdf for specific patient
- [x] work on creating sub_dfs for left and right eye
- [x] add medical terms to sub_df title
- [x] sort chronologically just before applying progrssor criteria on subdf for given patient
- [x] fix progression analysis function
- [x] add date of first progression to column
- [x] fix two differnt vfi labels through pattern matching

- [x] processed files changed to file runner
- [x] work on creating a new object for each user object file run as objects previous values get carried across
https://stackoverflow.com/questions/21598872/how-to-create-multiple-class-objects-with-a-loop-in-python
- [x] create driver functions for both concurrent and parallel jobs (8 cores) in driver.py
- [x] parallel environment working
- [x] progression functionality seperated

- [x] filter out N/A on dfs
- [x] add filtering to progressor criteria

- [x] change progressor criteria to take in object
- [x] all functions return progObject

- [x] recheck criteria according to email in processData

- [ ] grade trial folder and send results to Nia

### Extensions
- [ ] get working for 32-2 pdfs

### intial bug fixes based on user requirements
- [x] MD% and PSD% in the criteria for abnormal (criteria 3) [Fix psd < 5%]
- [x] region defect not detected upon criteria 2 and 3 (see file error2.pdf)
- [x] location labels mixed up (nasal step labeled as temporal wedge) 
- [x] more specific and reliable error messages
- [x] extraction failure labels (unable to extract -> more specific label: 'too severe to analyse')
- [x] VFI extraction (VFI24-2 and VFI are varying formats)
- [x] reliability = FNeg, FPos, FLoss all < 33 %
- [x] Progression column: comment on what determined whether output if true or false
- [x] Progression analysis inconsistent (errors sometimes occur)

- [x] Error: ght unable to be extracted type object 'Hvf_Object' has no attribute 'KEYLABEL_GHT'
- [x] Error: metadata md % not able to be extracted type object 'Hvf_Object' has no attribute 'KEYLABEL_MDP'
- [ ] Error: metadata psd % not able to be extracted type object 'Hvf_Object' has no attribute 'KEYLABEL_PSDP'


### GUI / Sonel
__Note__: driver.ipynb shows the full integration of how I am running objects
- [x] parseDataFrame run data is not defined
- [x] False negatives (list reliability index on GUI)
- [x] highlight/ 'select' a row of the table (ie an individual field) to make it easy to track when scrolling across
- [x] column headings should be locked so when scrolling down the rows these still stay at the top
- [x] implement a more intuitive drop down filter for right and left eye
- [ ] absolutely all user object variables displayed on GUI output
- [ ] integrate parallel joblib up to 7 jobs for parallel processor for 8 core cpu
- [ ] filter by eye left and right integration

- [ ] psd % readings extremely inconsistent -- improve readings

Fix the following library aspects:
Error: ght unable to be extractedtype object 'Hvf_Object' has no attribute 'KEYLABEL_GHT'
Error: rx and/or vfi not extractable
Error: metadata md % not able to be extractedtype object 'Hvf_Object' has no attribute 'KEYLABEL_MDP'
Error: metadata psd % not able to be extractedtype object 'Hvf_Object' has no attribute 'KEYLABEL_PSDP'

### notes / issues
***
__sample field attached to email___
- [ ] the issue with errorSample is that the psd % cannot be properly read or ght.Therefore we cannot determine if criteria 3 is valid so I coded the algorithm to  default to criteria 2

- [ ] progressor criteria not testing on a large sample size -- could still need work

- [ ] __run time__: takes about 36 seconds to completely extract, analyse and asses 20 samples: 1.8 per sample on average (parallel dispatching speeds this up though)

- [x] __mixed up hemifields__
as left and right eyes have differnt hemifields and the extraction is a mixed samples of both left and right eyes then in order to process it we need to divide data frame into left and right eyes seperately before we apply progressor criteria or labelling

To solve this problem, hemifield labels are converted with a map and will not be labelled until data is split into sub-data frames by eye

- [ ] we are extracting only pattern deviation matricies however this package is capable of extracting, processing and analysing other matricies

- [x] Some PDF are corrupt and will always fail to be processed (tesseract)

- [x] ght is commonly unable to be extracted, the extraction mechanism/code should be looked into in more detail


### developer notes
***
to run library environment: 
Install either Conda or Miniconda and run the following commands
```bash
conda create --name ENV_NAME regex pillow fuzzywuzzy pandas python-levenshtein numpy joblib IPython pdf2image
conda activate ENV_NAME
conda install -c conda-forge tesserocr poppler
pip install -r requirements.txt
```
To install the modified hvf_extraction_library:
```bash
# navigate to /hvf_extraction_script (modified)
pip install . (OR python setup.py install / develop)
```

Packing env for use in front end:
```bash
conda pack -n ENV_NAME -o env.zip
```
### Hugh's development environment for modified library
```
conda create --name ENV_NAME
conda activate ENV_NAME

conda install pip
conda install -c conda-forge tesseract tesserocr poppler
```
cd to hvf_extraction script and run:
```
python setup.py develop
```
install other libraries:
```
pip install -r requirements.txt
```


### GUI demo
![image info](images/GUIGrading.png)
**select python interpreter: automated-hvf-grading**
