class HVFAlgorithm:
    def __init__(self, matrix, eye, criteria):
        self.abnormal_regions = {
            "UL": False,
            "LL": False,
            "UM": False,
            "UC": False,
            "LC": False,
            "LM": False,
            "UR": False,
            "LR": False
        }
        self.matrix = matrix
        self.eye = eye
        self.criteria = criteria


    def run(self):
        """runs algorithm with given criteria
        Returns:
            abnormal_regions: dictionary with abnormally graded regions as true
        """
        coord_map = self.getRegionCoords()
        for region, coord in coord_map.items():
            self.runRegion(coord, region)
        return self.abnormal_regions

    def runRegion(self, coord, region):  
        """runs algorithmic criteria on specified region
        """
        ux, uy, lx, ly = coord # unpack coordinates
        if self.criteria == 3 and self.checkRegion_iii(self.matrix, ux, uy, lx + 1, ly + 1): # + 1 as python range generator doesn't include upper bounds
            self.abnormal_regions[region] = True
        elif self.criteria == 2 and self.checkRegion_iii(self.matrix, ux, uy, lx + 1, ly + 1): 
            self.abnormal_regions[region] = True
        
    def getRegionCoords(self):
        """coordinates for 24-2 matrix
           tuple format: (ux,uy,lx,ly)
           index range: (0,9) 
        """
        region_map_20_left = {  
            "UL": (1, 2, 2, 4),
            "LL": (1, 5, 2, 7),
            "UM": (3, 2, 6, 3),  
            "UC": (3, 3, 6, 4),
            "LC": (3, 5, 6, 6),
            "LM": (3, 6, 6, 8),
            "UR": (7, 2, 9, 4),
            "LR": (7, 5, 9, 7)
        }
        region_map_20_right = {  
            "UL": (0, 2, 2, 4),  
            "LL": (0, 5, 2, 7),
            "UM": (3, 2, 6, 3),  
            "UC": (3, 3, 6, 4),
            "LC": (3, 5, 6, 6),
            "LM": (3, 6, 6, 8),
            "UR": (7, 2, 8, 4),
            "LR": (7, 5, 8, 7)
        }
        if self.eye == "Left":
            return region_map_20_left
        return region_map_20_right
        
    def checkRegion_ii(self, mat, ux, uy, lx, ly):
        """ evaluates criteria 2: 
        A cluster of at least 3 contiguous points in the same region 
        depressed at P < 5% with at least one these < 1%

        Args:
            mat (list): hvf matrix
            region (matrix sub region): one of ul, ll, um, uc, lc, lm, ur, lr

        Returns: boolean indicating if region is abnormal
        """
        for r in range(uy, ly):  # checking horizontally contiguous region
            for c in range(ux, lx - 2):
                if (
                    0 < mat[r][c] <= 5 and 0 < mat[r][c + 1] <= 5 and 0 < mat[r][c + 2] <= 5
                ):  # note we upper bounds are inclusive (<=) as we are concerned with only the value of the numbers and not the range
                    if (
                        0 < mat[r][c] <= 1
                        or 0 < mat[r][c + 1] <= 1
                        or 0 < mat[r][c + 2] <= 1
                    ):  # at least one is <=1
                        return True

        for r in range(uy, ly - 2):
            for c in range(ux, lx):  # checking vertically contiguous regions
                if (
                    (0 < mat[r][c] <= 5)
                    and (0 < mat[r + 1][c] <= 5)
                    and (0 < mat[r + 2][c] <= 5)
                ):
                    if (
                        0 < mat[r][c] <= 1
                        or 0 < mat[r + 1][c] <= 1
                        or 0 < mat[r + 2][c] <= 1
                    ):
                        return True

        for r in range(uy, ly - 1):
            for c in range(ux, lx - 1):
                # checking pattern
                # |
                # |_
                if (
                    0 < mat[r][c] <= 5
                    and 0 < mat[r + 1][c] <= 5
                    and 0 < mat[r + 1][c + 1] <= 5
                ):
                    if (
                        0 < mat[r][c] <= 1
                        or 0 < mat[r + 1][c] <= 1
                        or 0 < mat[r + 1][c + 1] <= 1
                    ):
                        return True
                # checking pattern
                # |-
                # |
                if 0 < mat[r][c + 1] <= 5 and 0 < mat[r][c] <= 5 and 0 < mat[r + 1][c] <= 5:
                    if (
                        0 < mat[r][c + 1] <= 1
                        or 0 < mat[r][c] <= 1
                        or 0 < mat[r + 1][c] <= 1
                    ):
                        region = True

        for r in range(uy, ly - 1):
            for c in range(ux, lx - 1):
                # checking pattern
                # -|
                #  |
                if (
                    0 < mat[r][c] <= 5
                    and 0 < mat[r][c + 1] <= 5
                    and 0 < mat[r + 1][c + 1] <= 5
                ):
                    if (
                        0 < mat[r][c] <= 1
                        or 0 < mat[r][c + 1] <= 1
                        or 0 < mat[r + 1][c + 1] <= 1
                    ):
                        return True

        for r in range(uy, ly - 1):
            for c in range(ux + 1, lx):
                # checking pattern
                #  |
                # _|
                if (
                    0 < mat[r][c] <= 5
                    and 0 < mat[r + 1][c] <= 5
                    and 0 < mat[r + 1][c - 1] <= 5
                ):
                    if (
                        0 < mat[r][c] <= 1
                        or 0 < mat[r + 1][c] <= 1
                        or 0 < mat[r + 1][c - 1] <= 1
                    ):
                        return True
        return False

    def checkRegion_iii(self, mat, ux, uy, lx, ly):  # (iii) A cluster of at least 3 contiguous points in the same region depressed at P < 5%
        for r in range(uy, ly):
            for c in range(ux, lx - 2):
                if 0 < mat[r][c] <= 5 and 0 < mat[r][c + 1] <= 5 and 0 < mat[r][c + 2] <= 5:
                    return True
        # checking vertically contiguous regions
        # |
        # |
        # |
        for r in range(uy, ly - 2):
            for c in range(ux, lx):
                if (
                    (0 < mat[r][c] <= 5)
                    and (0 < mat[r + 1][c] <= 5)
                    and (0 < mat[r + 2][c] <= 5)
                ):
                    return True

        for r in range(uy, ly - 1):
            for c in range(ux, lx - 1):
                # checking pattern
                # |
                # |_
                if (
                    0 < mat[r][c] <= 5
                    and 0 < mat[r + 1][c] <= 5
                    and 0 < mat[r + 1][c + 1] <= 5
                ):
                    return True
                # checking pattern
                # |-
                # |
                if 0 < mat[r][c + 1] <= 5 and 0 < mat[r][c] <= 5 and 0 < mat[r + 1][c] <= 5:
                    return True

        for r in range(uy, ly - 1):
            for c in range(ux, lx - 1):
                # checking pattern
                # -|
                #  |
                if (
                    0 < mat[r][c] <= 5
                    and 0 < mat[r][c + 1] <= 5
                    and 0 < mat[r + 1][c + 1] <= 5
                ):
                    return True

        for r in range(uy, ly - 1):
            for c in range(ux + 1, lx):
                # checking pattern
                #  |
                # _|
                if (
                    0 < mat[r][c] <= 5
                    and 0 < mat[r + 1][c] <= 5
                    and 0 < mat[r + 1][c - 1] <= 5
                ):
                    return True

        return False

"""
    APPENDIX: coordinate map for 30-2 matricies (future proofed)
    region_map_30_right = {
        "UL": (0,1,2,5), 
        "LL": (0,5,2,8), 
        "UM": (3,1,6,4), 
        "UC": (3,3,6,4), 
        "LC": (3,5,6,6),
        "LM": (3,6,6,9),
        "UR": (7,1,9,4),
        "LR": (7,5,9,8)
    }
    region_map_30_left = {
        "UL": (0,1,2,5), 
        "LL": (0,5,2,8), 
        "UM": (3,1,6,4), 
        "UC": (3,3,6,4), 
        "LC": (3,5,6,6),
        "LM": (3,6,6,9),
        "UR": (7,1,9,4),
        "LR": (7,5,9,8)
    }

    if(region_size == "30-2"):
        print("\n30-2 matrix detected")
        region_map = region_map_30
        regions = [*region_map_30]
"""