## In the Grading section
1. MD% and PSD% in the criteria for abnormal (criteria 3) - We noticed several fields that should be listed as 'abnormal' are not being labeled so. We think the problem may be arising with the coded definition for criteria 3 -  "a cluster of 3 contiguous points all depressed at p < 5% AND (GHT abnormal or PSD < 5%)". It seems that clusters depressed at p < 5% with a PSD < 5% are not being labeled as abnormal. The github repository lists the criteria 3 definition as PSD < 0.5% and so I wondered whether the code also lists it this way. It should be PSD < 5% (not 0.5%). 

2. Region defect not detected - I've attached a field in this email for your reference. You will note there is a cluster in the inferior Bjerum region that meets both criteria 2 and 3 - 3 points at p < 5% and 1 at p < 1% (criteria 2) and also the PSD < 5% (criteria 3). We've tried but can't seem to identify a reason why this region wasn't labelled as TRUE in the GUI. Could you please look into this?

3. Location labels - Some of the location labels are mixed up. What is labeled as temporal wedge is actually the nasal step and vice versa. This is the case for both superior and inferior hemifields, and also for both right and left eyes. 

4. Extraction failure label - Some patients have a very significant visual field defect (ie they are blind) and so Zeiss cannot calculate a Pattern Deviation plot for them (the plot that appears bottom right of the field PDF). The GUI spits this out as 'unable to extract' - would it be possible in this case to label it with something more descriptive/reflective of the issue eg 'too severe to analyse' ? 

5. VFI extraction - some of the Fields we will be importing into the app have the text 'VFI24-2" whereas some only have "VFI". These mean the same thing. Your code reads the former but not the latter and spits out 'extraction failure'. Would it be possible to alter the code to extract for "VFI" also? 

6. False negatives - this reliability index is not listed in the GUI output. Could you please add? (adjacent to false positives and fixation losses). You may also need to check that the 'reliability' column includes the false negative too in the definition (ie reliability should be defined as FNeg, FPos and FLoss individually all < 33%) 

In the Analysis (progression) section 
7. Progression column - what determines whether this column output is TRUE/FALSE ? 

8. Error message - sometimes the progression analysis works and other times it does not. We weren't able to work out any rhyme or reason to this, but on the occasions it did not work, it always gave the same error message which I've copied here: DevTools failed to load source map: Could not parse content for file:///C:/Users/Ayub/Downloads/hvfanalysis-win32-x64-0.0.3/resources/app/src/index.js.map: Unexpected end of JSON input. 

If possible, we also have a few small requests for the GUI output to make it more user friendly. 
Because the GUI table has many columns (and rows when examining multiple fields concurrently), it becomes quite cumbersome to scroll through and easy to lose your place in the table. 
- it would be great to be able to highlight/ 'select' a row of the table (ie an individual field) to make it easy to track when scrolling across
- would also be great if the column headings were locked so when scrolling down the rows these still stay at the top 
- would also be more intuitive to have a drop down filter for right and left eye if possible (appreciate you have already installed a text filter for this)
