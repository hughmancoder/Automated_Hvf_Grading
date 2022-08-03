#abitrary intialisation
# mat = []
# region_size = "24-2"
#reliable = True
#criteria = 3;

def runAlgorithm(mat,region_size,reliable,criteria,eye):#eye added
    region_state =  [False for i in range(8)] #saving the states of regions in a boolean list
    region_map,regions = getRegionSize(region_size,eye)
    exploreRegions(mat,region_map,criteria,regions,region_state)     
    result = getResult(region_state)
    if(reliable==False):
        print("Info: visual field data unreliable, Defective marked as False by default")
        result = False
    
    region_list = list(zip(regions, region_state)) #print(region_list)
    # print("Algo result: ",region_list)

    return (region_list,result) 

def PrintMatrix(mat): #prints matrix in easy to read format
    rows = len(mat[0])
    cols = len(mat) 
    for r in range(rows):
        if(r==5):
            print("\n\n"+"-----------"+("---"*cols)+"\n") #ornamental formatting for matrix
        else: 
            print("\n")
        for c in range(cols):
            if(c==5):
                print("|   ",end = '')
            if(mat[r][c]== 0.5):
                print(str(mat[r][c])+" ", end = '')
            else:
                print(str(mat[r][c])+"   ", end = '')

def checkRegion_ii(mat,region,ux,uy,lx,ly): #A cluster of at least 3 contiguous points in the same region depressed at P < 5%, with at least one these < 1%

    for r in range(uy,ly): #checking horizontally contiguous region 
        for c in range(ux,lx-2):
            if(0 < mat[r][c] <=5 and 0 < mat[r][c+1] <=5 and 0 < mat[r][c+2] <=5):  #note we upper bounds are inclusive (<=) as we are concerned with only the value of the numbers and not the range
                if(0 < mat[r][c] <=1 or 0 < mat[r][c+1] <=1 or 0 < mat[r][c+2] <=1): #at least one is <=1
                    return True

    for r in range(uy,ly-2):
        for c in range(ux,lx): #checking vertically contiguous regions
            if((0 < mat[r][c] <=5) and (0 < mat[r+1][c] <=5) and (0 < mat[r+2][c] <=5)):
                if(0 < mat[r][c] <=1 or 0 < mat[r+1][c] <=1 or 0 < mat[r+2][c] <=1): 
                    return  True;
    for r in range(uy,ly-1): 
        for c in range(ux,lx-1):
            #checking pattern
            #|
            #|_  
            if(0 < mat[r][c] <5 and 0 < mat[r+1][c] <5 and 0 < mat[r+1][c+1] <5):
                if(0 < mat[r][c] <=1 or 0 < mat[r+1][c] <=1 or 0 < mat[r+1][c+1] <=1):
                    return True;
            #checking pattern
            #|-
            #|
            if(0 < mat[r][c+1] <=5 and 0 < mat[r][c] <=5 and 0 < mat[r+1][c] <=5):
                if(0 < mat[r][c+1] <=1 or 0 < mat[r][c] <=1 or 0 < mat[r+1][c] <=1):
                    region = True

    for r in range(uy,ly-1):
        for c in range(ux,lx-1):
            #checking pattern
            # -|
            #  |
            if(0 < mat[r][c] <=5 and 0 < mat[r][c+1] <=5 and 0 < mat[r+1][c+1] <=5):
                if(0 < mat[r][c] <=1 or 0 < mat[r][c+1] <=1 or 0 < mat[r+1][c+1] <=1):
                    return True
    
    for r in range(uy,ly-1):
        for c in range(ux+1,lx):  
            #checking pattern
            #  |
            # _|
            if(0 < mat[r][c] <=5 and 0 < mat[r+1][c] <=5 and 0 < mat[r+1][c-1] <=5):
                if(0 < mat[r][c] <=1 or 0 < mat[r+1][c] <=1 or 0 < mat[r+1][c-1] <=1):
                    return True
    return False;

def checkRegion_iii(mat,region,ux,uy,lx,ly): #(iii) A cluster of at least 3 contiguous points in the same region depressed at P < 5% AND (GHT = Outside Normal Limits OR PSD = P < 0.5%) 
    for r in range(uy,ly):
        for c in range(ux,lx-2):
            if(0 < mat[r][c] <=5 and 0 < mat[r][c+1] <=5 and 0 < mat[r][c+2] <=5):
                return True;
    #checking vertically contiguous regions
    # |
    # |
    # |
    for r in range(uy,ly-2):
        for c in range(ux,lx):
            if((0 < mat[r][c] <=5) and (0 < mat[r+1][c] <=5) and (0 < mat[r+2][c] <=5)):
               return True;

    for r in range(uy,ly-1):
        for c in range(ux,lx-1):
            #checking pattern
            #|
            #|_
            if(0 < mat[r][c] <=5 and 0 < mat[r+1][c] <=5 and 0 < mat[r+1][c+1] <=5):
                return True
            #checking pattern
            #|-
            #|
            if(0 < mat[r][c+1] <=5 and 0 < mat[r][c] <=5 and 0 < mat[r+1][c] <=5):
                return True
    
    for r in range(uy,ly-1):
        for c in range(ux,lx-1):
            #checking pattern
            # -|
            #  |
            if(0 < mat[r][c] <=5 and 0 < mat[r][c+1] <=5 and 0 < mat[r+1][c+1] <=5):
                return True
            

    for r in range(uy,ly-1):
        for c in range(ux+1,lx):  
            #checking pattern
            #  |
            # _|
            if(0 < mat[r][c] <=5 and 0 < mat[r+1][c] <=5 and 0 < mat[r+1][c-1] <=5):
                return True

    return False

def getRegionSize(region_size,eye):
    # region_map_30_right = {#region coordinates for 30-2 matrix
    #     "UL": (0,1,2,5), #Format: (ux,uy,lx,ly)
    #     "LL": (0,5,2,8), #index (0,9)
    #     "UM": (3,1,6,4), #region bound asymetric so uy = 1 instead of 0
    #     "UC": (3,3,6,4), #upper and lower central
    #     "LC": (3,5,6,6),
    #     "LM": (3,6,6,9),
    #     "UR": (7,1,9,4),
    #     "LR": (7,5,9,8)
    # }

    region_map_20_right = { #coordinates for 24-2 matrix
        "UL": (0,2,2,4), #Format: (ux,uy,lx,ly)
        "LL": (0,5,2,7),
        "UM": (3,2,6,3), #asymmetric upper middle uy = 2 instead of 1
        "UC": (3,3,6,4),
        "LC": (3,5,6,6),
        "LM": (3,6,6,8), 
        "UR": (7,2,8,4),
        "LR": (7,5,8,7)
    }


    # region_map_30_left = {#region coordinates for 30-2 matrix
    #     "UL": (0,1,2,5), #Format: (ux,uy,lx,ly)
    #     "LL": (0,5,2,8), #index (0,9)
    #     "UM": (3,1,6,4), #region bound asymetric so uy = 1 instead of 0
    #     "UC": (3,3,6,4), #upper and lower central
    #     "LC": (3,5,6,6),
    #     "LM": (3,6,6,9),
    #     "UR": (7,1,9,4),
    #     "LR": (7,5,9,8)
    # }

    region_map_20_left = { #coordinates for 24-2 matrix
        "UL": (0,2,1,4), 
        "LL": (0,5,1,7),
        "UM": (2,2,5,3), #asymmetric upper middle uy = 2 instead of 1
        "UC": (2,3,5,4),
        "LC": (2,5,5,6),
        "LM": (2,6,5,8), 
        "UR": (6,2,8,4),
        "LR": (6,5,8,7)
    }

    # if(region_size == "30-2"):
    #     print("\n30-2 matrix detected")
    #     region_map = region_map_30
    #     regions = [*region_map_30]
    #     print(regions)

    if(eye == "Left"):
        #print("\n24-2 matrix detected")
        region_map = region_map_20_left
        regions = [*region_map_20_left] #dictionary to list
    else:
        region_map = region_map_20_right
        regions = [*region_map_20_right]

    return region_map, regions   

def exploreRegions(mat,region_map,criteria,regions,region_state): #runs function on all regions
    for i in range(len(regions)): #now checking each region
        region = regions[i]
        (ux,uy,lx,ly) = region_map[region]  
        if(criteria == 3): # iii) A cluster of at least 3 contiguous points in the same region depressed at P < 5% AND (GHT = Outside Normal Limits OR PSD = P < 0.5%) 
            # print("criteria iii applied")
            if(checkRegion_iii(mat,region,ux,uy,lx+1,ly+1)==True): #we add one as range(lower,upper) does not include last element
                region_state = UpdateState(region_state,True,region,regions)
        else: #ii) 3 contiguous points are less than P = 5% with at least 1 less than 1%
            #print("criteria ii applied")
            if(checkRegion_ii(mat,region,ux,uy,lx+1,ly+1)==True):
                region_state = UpdateState(region_state,True,region,regions)
    return region_state            

def getResult(region_state): #check if at least one if false
            for i in region_state:
                if(i == True):
                    return True
            return False
 
def UpdateState(region_state,outcome,region,regions): #modifies the boolean list  
    index = regions.index(region)
    if(0<=index<=8):
        region_state[index] = outcome
    return region_state


# ==testing file==

#row refers to which spreadsheet row correlates to which file
# mat_row2 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0], [0.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0.0], [0.0, 0, 5, 0, 0, 0, 0, 0, 0, 0.0], [0, 0, 5, 0, 0, 0, 0, 0.0, 0, 0.0], [0, 0, 0, 0, 0, 5, 0, 0.0, 5, 0.0], [0.0, 0, 5, 1, 5, 5, 0, 0, 0, 0.0], [0.0, 0.0, 0, 0, 5, 5, 0, 0, 0.0, 0.0], [0.0, 0.0, 0.0, 0, 0, 2, 5, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
# mat_row3 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0], [0.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0.0], [0.0, 0, 0, 1, 0, 5, 0, 0, 0, 0.0], [0, 0, 0, 0.5, 5, 5, 5, 0.0, 0, 0.0], [0, 0, 0, 0, 0, 5, 0, 0.0, 0, 0.0], [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0], [0.0, 0.0, 2, 5, 0, 0, 0, 0, 0.0, 0.0], [0.0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]] #col 30

#==uncomment below to test==
# mat_row4 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0, 0, 0, 5, 0.0, 0.0, 0.0], [0.0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0.0], [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0], [0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0.0], [0, 0, 0, 0, 0, 0, 0, 0.0, 5, 0.0], [0.0, 0.5, 0, 0, 0.5, 0, 0, 5, 2, 0.0], [0.0, 0.0, 2, 2, 0.5, 0, 0, 0, 0.0, 0.0], [0.0, 0.0, 0.0, 1, 0, 0, 0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
# mat = mat_row4

# region_size = "24-2"
# criteria = 3
# reliable = True

# print(runAlgorithm(mat,region_size,True,criteria)) #runAlgorithm(mat,region_size,reliable,criteria)
# PrintMatrix(mat)