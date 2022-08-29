# automated-hvf-grading
humphrey visual field matrix reading, grading and analysis automated via python script for research at Flinders University

### supporting library:
https://github.com/msaifee786/hvf_extraction_script

### Regions 
![image info](images/regions.png)


### features
- algorithm to automate reading hvf % pattern deviation field scans
- data filtering such as sorting eye by left and right, patient name, chronological order
- automating progression of glaucoma: we can chronologically map past outcomes and apply  progressor criteria (see below) to detect an onset

### Algorithmic Criteria

  category 2) A cluster of at least 3 contiguous points in the same region depressed at P < 5%, with at least one these < 1%

  category 3) A cluster of at least 3 contiguous points in the same region depressed at P < 5% AND (GHT = Outside Normal Limits OR PSD = P < 5%)

### Terminology
    abnormal: there is a defect in eye as given algorithmic criteria is satisfied

    reliable: data is reliable if and only if false pos and fixation loss are both less than 33%

    error: this is a flag to mark that there may be an error present in result due to not being able to extract every feature consequently leading to unreliable dependencies

    progression: a chronological progression of abnormal eye scans (True indicates progrgression)

    progressor criteria: any 2 defective scans out of 3 consecutive chronological samples

    Progression column: output is determined as true if the progression criteria listed above is satisfied

    Progression onset: date of the first recorded progression

### short hand terminology
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

 ### questions
 - what do we do if we cannot extract psd percentage? Reliability is determined if psd < 33% or ght outside limits so if we can't determine this criteria should we use 2 or 3 as deafult or just skip this scan and move on to the next one?

 - A progression is marked as 2/3 consecutive chronological defects right?

- is Terminology listed above correct?

### To-do
- [x] refactor code using OOP
- [x] refactor into a module
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
- [ ] fix progression analysis function
- [ ] fix two differnt vfi lavbels through pattern matching
- [ ] create driver functions for both concurrent and parallel jobs


### intial bug fixes based on user requirements
- [x] MD% and PSD% in the criteria for abnormal (criteria 3) [Fix psd < 5%]
- [x] region defect not detected upon criteria 2 and 3 (see file error2.pdf)
- [x] location labels mixed up (nasal step labeled as temporal wedge) 
- [x] more specific and reliable error messages
- [x] extraction failure labels (unable to extract -> more specific label: 'too severe to analyse')
- [ ] VFI extraction (VFI24-2 and VFI are varying formats)
- [x] reliability = FNeg, FPos, FLoss all < 33 %
- [x] Progression column: comment on what determined whether output if true or false
- [ ] Progression analysis inconsistent (errors sometimes occur)


### GUI / Sonel
__Note__: driver.ipynb shows the full integration of how I am running objects
- [x] parseDataFrame run data is not defined
- [x] False negatives (list reliability index on GUI)
- [x] highlight/ 'select' a row of the table (ie an individual field) to make it easy to track when scrolling across
- [x] column headings should be locked so when scrolling down the rows these still stay at the top
- [x] implement a more intuitive drop down filter for right and left eye
- [ ] absolutely all user object variables displayed on GUI output

Fix the following library aspects:
Error: ght unable to be extractedtype object 'Hvf_Object' has no attribute 'KEYLABEL_GHT'
Error: rx and/or vfi not extractable
Error: metadata md % not able to be extractedtype object 'Hvf_Object' has no attribute 'KEYLABEL_MDP'
Error: metadata psd % not able to be extractedtype object 'Hvf_Object' has no attribute 'KEYLABEL_PSDP'

### notes / issues
__sample field attached to email___
- [ ] the issue with errorSample is that the psd % cannot be properly read or ght.Therefore we cannot determine if criteria 3 is valid so I coded the algorithm to  default to criteria 2

- [ ] __run time__: takes about 36 seconds to completely extract, analyse and asses 20 samples: 1.8 per sample on average (parallel dispatching speeds this up though)

- [ ] __mixed up hemifields__
as left and right eyes have differnt hemifields and the extraction is a mixed samples of both left and right eyes then in order to process it we need to divide data frame into left and right eyes seperately before we apply progressor criteria or labelling

To solve this problem, hemifield labels are converted with a map and will not be labelled until data is split into sub-data frames by eye

- [ ] we are extracting only pattern deviation matricies however this package is capable of extracting, processing and analysing other matricies

- [ ] Some PDF are corrupt and will always fail to be processed (tesseract)

- [ ] ght is commonly unable to be extracted, the extraction mechanism/code should be looked into in more detail


### developer notes
to run library environment: 
```
conda create --name automated-hvf-grading
conda activate automated-hvf-grading
conda install pip
conda install -c conda-forge tesseract
pip install hvf-extraction-script
```
### GUI demo
![image info](images/GUIGrading.png)
**select python interpreter: automated-hvf-grading**
